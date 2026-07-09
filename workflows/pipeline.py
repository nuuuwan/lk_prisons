import logging
import sys

sys.path.insert(0, "src")

from prisons import PrisonStatistic  # noqa: E402

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    prison_statistic = PrisonStatistic.from_web()
    log.info(prison_statistic)


if __name__ == "__main__":
    main()
