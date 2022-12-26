import csv
import datetime as dt

from .constants import BASE_DIR, DATETIME_FORMAT


class PepParsePipeline:
    def open_spider(self, spider):
        self.result = {}
        self.total_pep_count = 0

    def process_item(self, item, spider):
        self.result[item["status"]] = self.result.get(item["status"], 0) + 1
        self.total_pep_count += 1
        return item

    def close_spider(self, spider):
        self.results = (
            [("Статус", "Количество")]
            + list(self.result.items())
            + [("Total", self.total_pep_count)]
        )
        results_dir = BASE_DIR / "results"
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f"status_summary_{now_formatted}.csv"
        file_path = results_dir / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f, dialect="unix")
            writer.writerows(self.results)
