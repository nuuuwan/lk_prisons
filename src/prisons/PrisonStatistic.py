import json
import logging
import os
import re
from dataclasses import asdict, dataclass
from html import unescape

import requests

log = logging.getLogger(__name__)

URL_STATISTICS = "http://prisons.gov.lk/web/en/statistics-information-en/"
REQUEST_TIMEOUT = 30
DIR_DATA = "data"


@dataclass
class PrisonStatistic:
    """Statistical snapshot of Sri Lankan prisons.

    Data is scraped from the daily snapshot published by the Department of
    Prisons at http://prisons.gov.lk/web/en/statistics-information-en/, which
    is embedded on the page as a published Google Slides presentation.
    """

    date_str: str

    convicted_male: int
    convicted_female: int
    convicted_total: int

    unconvicted_male: int
    unconvicted_female: int
    unconvicted_total: int

    total_male: int
    total_female: int
    total_total: int

    convicted_release_male: int
    convicted_release_female: int
    convicted_release_total: int

    unconvicted_release_on_bail_male: int
    unconvicted_release_on_bail_female: int
    unconvicted_release_on_bail_total: int

    @staticmethod
    def _decode(text: str) -> str:
        """Decode the ``\\xNN`` and HTML entity escaping used in the embed."""
        text = re.sub(
            r"\\x([0-9a-fA-F]{2})",
            lambda m: chr(int(m.group(1), 16)),
            text,
        )
        text = text.replace("\\/", "/")
        return unescape(text)

    @staticmethod
    def _get_slides_embed_url(statistics_html: str) -> str:
        match = re.search(
            r'src="(https://docs\.google\.com/presentation/[^"]+/embed[^"]*)"',
            statistics_html,
        )
        if not match:
            raise ValueError("Could not find Google Slides embed URL.")
        return unescape(match.group(1))

    @staticmethod
    def _get_label_blocks(embed_html: str) -> list[list[str]]:
        """Return each slide element's ``aria-label`` as a list of lines."""
        blocks = []
        for raw_label in re.findall(
            r"aria-label\\x3d\\x22(.*?)\\x22", embed_html
        ):
            decoded = PrisonStatistic._decode(raw_label)
            lines = [line.strip() for line in decoded.split("\n")]
            lines = [line for line in lines if line]
            if lines:
                blocks.append(lines)
        return blocks

    @staticmethod
    def _extract_numbers(lines: list[str]) -> list[int]:
        return [int(line) for line in lines if re.fullmatch(r"\d+", line)]

    @classmethod
    def from_html(
        cls, statistics_html: str, embed_html: str
    ) -> "PrisonStatistic":
        del statistics_html  # embed_html carries all the snapshot data
        blocks = cls._get_label_blocks(embed_html)

        date_str = None
        totals = None
        convicted_release = None
        unconvicted_release = None

        for lines in blocks:
            text = " ".join(lines)
            if "Last Updated On" in text:
                match = re.search(r"(\d{4}/\d{2}/\d{2})", text)
                if match:
                    date_str = match.group(1)
            elif "Total of all Convicted and Unconvicted" in text:
                totals = cls._extract_numbers(lines)
            elif "Unconvicted Prisoners Release on bail" in text:
                unconvicted_release = cls._extract_numbers(lines)
            elif "Convicted Prisoners Release" in text:
                convicted_release = cls._extract_numbers(lines)

        if date_str is None:
            raise ValueError("Could not parse 'Last Updated On' date.")
        if not totals or len(totals) != 9:
            raise ValueError(
                "Could not parse convicted/unconvicted totals table."
            )
        if not convicted_release or len(convicted_release) != 3:
            raise ValueError("Could not parse convicted prisoners release.")
        if not unconvicted_release or len(unconvicted_release) != 3:
            raise ValueError(
                "Could not parse unconvicted prisoners release on bail."
            )

        prison_statistic = cls(
            date_str=date_str,
            convicted_male=totals[0],
            convicted_female=totals[1],
            convicted_total=totals[2],
            unconvicted_male=totals[3],
            unconvicted_female=totals[4],
            unconvicted_total=totals[5],
            total_male=totals[6],
            total_female=totals[7],
            total_total=totals[8],
            convicted_release_male=convicted_release[0],
            convicted_release_female=convicted_release[1],
            convicted_release_total=convicted_release[2],
            unconvicted_release_on_bail_male=unconvicted_release[0],
            unconvicted_release_on_bail_female=unconvicted_release[1],
            unconvicted_release_on_bail_total=unconvicted_release[2],
        )
        prison_statistic.validate()
        return prison_statistic

    def validate(self) -> None:
        """Check the snapshot is internally consistent.

        Raises ``ValueError`` when any row/column total does not match the
        sum of its parts.
        """
        checks = [
            # Male + Female == Total (rows).
            ("convicted M+F", self.convicted_male, self.convicted_female,
             self.convicted_total),
            ("unconvicted M+F", self.unconvicted_male, self.unconvicted_female,
             self.unconvicted_total),
            ("total M+F", self.total_male, self.total_female,
             self.total_total),
            # Convicted + Unconvicted == Total (columns).
            ("male C+U", self.convicted_male, self.unconvicted_male,
             self.total_male),
            ("female C+U", self.convicted_female, self.unconvicted_female,
             self.total_female),
            ("total C+U", self.convicted_total, self.unconvicted_total,
             self.total_total),
            # Release tables: Male + Female == Total.
            ("convicted release M+F", self.convicted_release_male,
             self.convicted_release_female, self.convicted_release_total),
            ("unconvicted release M+F",
             self.unconvicted_release_on_bail_male,
             self.unconvicted_release_on_bail_female,
             self.unconvicted_release_on_bail_total),
        ]
        for name, part_a, part_b, total in checks:
            if part_a + part_b != total:
                raise ValueError(
                    f"Validation failed for {name}: "
                    f"{part_a} + {part_b} != {total}"
                )

        for name, value in asdict(self).items():
            if name == "date_str":
                continue
            if value < 0:
                raise ValueError(
                    f"Validation failed: {name} is negative ({value})"
                )

    @property
    def dir_data(self) -> str:
        """Directory ``data/<yyyy-mm-dd>`` for this snapshot's date."""
        date_dir = self.date_str.replace("/", "-")
        return os.path.join(DIR_DATA, date_dir)

    def save(self, statistics_html: str = "", embed_html: str = "") -> None:
        """Save the parsed data (and any source HTML) to ``data/<yyyy-mm-dd>``."""
        os.makedirs(self.dir_data, exist_ok=True)

        path_data = os.path.join(self.dir_data, "data.json")
        with open(path_data, "w", encoding="utf-8") as fout:
            json.dump(asdict(self), fout, indent=2)
        log.info(f"Wrote {path_data}")

        for file_name, content in [
            ("statistics.html", statistics_html),
            ("slides_embed.html", embed_html),
        ]:
            if not content:
                continue
            path = os.path.join(self.dir_data, file_name)
            with open(path, "w", encoding="utf-8") as fout:
                fout.write(content)
            log.info(f"Wrote {path}")

    @classmethod
    def from_web(cls) -> "PrisonStatistic":
        log.info(f"Fetching {URL_STATISTICS}")
        statistics_html = requests.get(
            URL_STATISTICS, timeout=REQUEST_TIMEOUT
        ).text
        embed_url = cls._get_slides_embed_url(statistics_html)
        log.info(f"Fetching {embed_url}")
        embed_html = requests.get(embed_url, timeout=REQUEST_TIMEOUT).text
        prison_statistic = cls.from_html(statistics_html, embed_html)
        prison_statistic.save(statistics_html, embed_html)
        return prison_statistic
