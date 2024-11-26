import time
import datetime
import json


class CommonUtil:

    @staticmethod
    def today() -> str:
        return datetime.today().strftime("%Y%m%d")

    @staticmethod
    def date_to_api(date: datetime) -> str:
        return date.strftime("%Y%m%d")

    @staticmethod
    def api_date_to_datetime(date: str) -> datetime:
        return datetime.datetime.strptime(date, "%Y%m%d").date()

    @staticmethod
    def calendar_date_to_datetime(date: str) -> datetime:
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()

    @staticmethod
    def excel_datetime() -> str:
        """Returns the current datetime in a formatted string

        Returns:
            str: 2024-01-01_14-00
        """
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    @staticmethod
    def get_days_from_week(date: datetime) -> list:
        """Returns all days of the week that contain the selected day.

        Args:
            date (datetime): selected day

        Returns:
            list: list of dates
        """
        year = date.isocalendar()[0]
        week = date.isocalendar()[1]
        startdate = time.asctime(time.strptime(
            '%d %d 1' % (year, week), '%Y %W %w'))
        startdate = datetime.datetime.strptime(
            startdate, '%a %b %d %H:%M:%S %Y')
        dates = [startdate.strftime("%Y-%m-%d")]
        for i in range(1, 7):
            day = startdate + datetime.timedelta(days=i)
            dates.append(day.strftime("%Y-%m-%d"))

        return dates

    @staticmethod
    def pretty_print(data: any) -> None:
        print(json.dumps(data, indent=4, sort_keys=True))
