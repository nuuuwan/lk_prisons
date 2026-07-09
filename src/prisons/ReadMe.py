import json
import logging
import os
from dataclasses import asdict, fields

from prisons.PrisonStatistic import DIR_DATA, URL_STATISTICS, PrisonStatistic

log = logging.getLogger(__name__)

PATH_README = "README.md"


class ReadMe:
    """Generates ``README.md`` from all saved prison-statistic snapshots."""

    @staticmethod
    def _load_all() -> list[PrisonStatistic]:
        prison_statistics = []
        if os.path.isdir(DIR_DATA):
            for date_dir in sorted(os.listdir(DIR_DATA)):
                path = os.path.join(DIR_DATA, date_dir, "data.json")
                if not os.path.exists(path):
                    continue
                with open(path, encoding="utf-8") as fin:
                    prison_statistics.append(PrisonStatistic(**json.load(fin)))
        return prison_statistics

    @staticmethod
    def _humanize(field_name: str) -> str:
        return field_name.replace("_", " ").title()

    @classmethod
    def _build_table(cls, prison_statistics: list[PrisonStatistic]) -> str:
        value_fields = [
            f.name for f in fields(PrisonStatistic) if f.name != "date_str"
        ]

        header = ["Date"] + [cls._humanize(name) for name in value_fields]
        lines = [
            "| " + " | ".join(header) + " |",
            "| " + " | ".join(["---"] * len(header)) + " |",
        ]

        for prison_statistic in sorted(
            prison_statistics, key=lambda ps: ps.date_str, reverse=True
        ):
            data = asdict(prison_statistic)
            date_str = prison_statistic.date_str
            date_link = f"[{date_str}]({DIR_DATA}/{date_str})"
            row = [date_link] + [
                f"{data[name]:,}" for name in value_fields
            ]
            lines.append("| " + " | ".join(row) + " |")

        return "\n".join(lines)

    @classmethod
    def build(cls) -> str:
        prison_statistics = cls._load_all()

        parts = [
            "# lk_prisons",
            "",
            "Daily statistical snapshots of Sri Lankan prisons.",
            "",
            "## Source",
            "",
            "Data is scraped from the daily snapshot published by the "
            "Sri Lanka Department of Prisons at "
            f"[{URL_STATISTICS}]({URL_STATISTICS}). The snapshot is "
            "embedded on that page as a published Google Slides "
            "presentation.",
            "",
            "## Data",
            "",
        ]

        if prison_statistics:
            parts.append(
                f"Snapshots collected: **{len(prison_statistics)}**. "
                f"Raw data per date is under [{DIR_DATA}/]({DIR_DATA})."
            )
            parts.append("")
            parts.append(cls._build_table(prison_statistics))
        else:
            parts.append("_No data collected yet._")

        parts.append("")
        return "\n".join(parts)

    @classmethod
    def update(cls) -> None:
        readme = cls.build()
        with open(PATH_README, "w", encoding="utf-8") as fout:
            fout.write(readme)
        log.info(f"Wrote {PATH_README}")
