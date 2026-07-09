import json
import logging
import os
from dataclasses import asdict
from datetime import date

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
    def _get_lines_for_header(latest_date_str: str) -> list[str]:
        latest_badge = latest_date_str.replace("-", "--").replace(" ", "_")
        update_badge = date.today().isoformat()
        update_badge = update_badge.replace("-", "--").replace(" ", "_")
        return [
            "![Latest Data](https://img.shields.io/badge/"
            + f"latest_data-{latest_badge}-green)",
            "![Last Checked](https://img.shields.io/badge/"
            + f"last_checked-{update_badge}-purple)",
            "",
        ]

    @staticmethod
    def _get_lines_for_footer() -> list[str]:
        return [
            "![Maintainer]"
            + "(https://img.shields.io/badge/maintainer-nuuuwan-red)",
            "![MadeWith](https://img.shields.io/badge/made_with-python-blue)",
            "[![License: MIT]"
            + "(https://img.shields.io/badge/License-MIT-yellow.svg)]"
            + "(https://opensource.org/licenses/MIT)",
        ]

    @classmethod
    def build(cls) -> str:
        prison_statistics = cls._load_all()
        prison_statistics.sort(key=lambda ps: ps.date_str, reverse=True)

        lines = ["# lk_prisons", ""]

        if prison_statistics:
            lines += cls._get_lines_for_header(prison_statistics[0].date_str)

        lines += [
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
        ]

        if prison_statistics:
            latest = prison_statistics[0]
            lines += [
                f"## Latest Data ({latest.date_str})",
                "",
                "```json",
                json.dumps(asdict(latest), indent=2),
                "```",
                "",
                "## History",
                "",
            ]
            for prison_statistic in prison_statistics:
                date_str = prison_statistic.date_str
                lines.append(f"- [{date_str}]({DIR_DATA}/{date_str})")
            lines.append("")
        else:
            lines += ["## Data", "", "_No data collected yet._", ""]

        lines += cls._get_lines_for_footer()
        lines.append("")
        return "\n".join(lines)

    @classmethod
    def update(cls) -> None:
        readme = cls.build()
        with open(PATH_README, "w", encoding="utf-8") as fout:
            fout.write(readme)
        log.info(f"Wrote {PATH_README}")
