import json
import logging
import os
from dataclasses import asdict
from datetime import date

from prisons.PrisonStatistic import DIR_DATA, URL_STATISTICS, PrisonStatistic

log = logging.getLogger(__name__)

PATH_README = "README.md"

COLOR_MALE = "#2196F3"  # Blue
COLOR_FEMALE = "#EC407A"  # Pink
COLOR_CONVICTED = "#E53935"  # Red
COLOR_UNCONVICTED = "#FFB300"  # Amber
COLOR_BAIL = "#FFB74D"  # Light Orange
COLOR_RELEASED = "#43A047"  # Green


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

    @staticmethod
    def _get_lines_for_charts(latest: PrisonStatistic) -> list[str]:
        def pie(title, explanation, slices):
            # slices: list of (label, value, color); pieN colors Nth slice
            theme_vars = ", ".join(
                f"'pie{i + 1}': '{color}'"
                for i, (_, _, color) in enumerate(slices)
            )
            lines = [
                f"### {title}",
                "",
                explanation,
                "",
                "```mermaid",
                "%%{init: {'themeVariables': {" + theme_vars + "}}}%%",
                f"pie showData title {title}",
            ]
            for label, value, _ in slices:
                lines.append(f'    "{label}" : {value}')
            lines += ["```", ""]
            return lines

        return (
            [
                "## Charts",
                "",
                f"All charts below describe the prison population and "
                f"releases recorded on **{latest.date_str}**.",
                "",
            ]
            + pie(
                "Population: Convicted vs Unconvicted",
                "How the total prison population splits between people "
                "already **convicted** of a crime and those **unconvicted** "
                "(remand prisoners awaiting trial or sentencing).",
                [
                    ("Convicted", latest.convicted_total, COLOR_CONVICTED),
                    ("Unconvicted", latest.unconvicted_total,
                     COLOR_UNCONVICTED),
                ],
            )
            + pie(
                "Population: Male vs Female",
                "The gender split across the entire prison population "
                "(convicted and unconvicted combined).",
                [
                    ("Male", latest.total_male, COLOR_MALE),
                    ("Female", latest.total_female, COLOR_FEMALE),
                ],
            )
            + pie(
                "Convicted Population by Gender",
                "The gender split among **convicted** prisoners only.",
                [
                    ("Male", latest.convicted_male, COLOR_MALE),
                    ("Female", latest.convicted_female, COLOR_FEMALE),
                ],
            )
            + pie(
                "Unconvicted Population by Gender",
                "The gender split among **unconvicted** (remand) prisoners "
                "only.",
                [
                    ("Male", latest.unconvicted_male, COLOR_MALE),
                    ("Female", latest.unconvicted_female, COLOR_FEMALE),
                ],
            )
            + pie(
                "Releases: Released vs Bail",
                "Of the prisoners leaving custody on this day, how many were "
                "**released** after serving as convicted prisoners versus "
                "**released on bail** while still unconvicted.",
                [
                    ("Released (Convicted)",
                     latest.convicted_release_total, COLOR_RELEASED),
                    ("Released on Bail (Unconvicted)",
                     latest.unconvicted_release_on_bail_total, COLOR_BAIL),
                ],
            )
            + pie(
                "Convicted Releases by Gender",
                "The gender split among convicted prisoners **released** on "
                "this day.",
                [
                    ("Male", latest.convicted_release_male, COLOR_MALE),
                    ("Female", latest.convicted_release_female, COLOR_FEMALE),
                ],
            )
            + pie(
                "Bail Releases by Gender",
                "The gender split among unconvicted prisoners **released on "
                "bail** on this day.",
                [
                    ("Male", latest.unconvicted_release_on_bail_male,
                     COLOR_MALE),
                    ("Female", latest.unconvicted_release_on_bail_female,
                     COLOR_FEMALE),
                ],
            )
        )

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
            ]
            lines += cls._get_lines_for_charts(latest)
            lines += [
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
