from datetime import datetime

class HelperMethods:

    @staticmethod
    def str_to_date(date: str) -> datetime.date:
        """
        Converts the date as a string into the date as a datetime.date object
        :param date: The date as a string
        :return: The date as a datetime.date object
        """
        try:
            return datetime.strptime(date, "%m/%d/%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use dd/mm/yyyy format!")