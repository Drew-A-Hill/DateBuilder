import datetime

from bintrees import RBTree

from ._days_of_week import DaysOfWeek

class FilteredDates:
    def __init__(self, tree: RBTree, days_of_week: DaysOfWeek):
        self.tree = tree
        self.days_of_week = days_of_week

    def get_filtered_date_range(self, days: list[int] = None, months: list[int] = None,
                                years: list[int] = None) -> RBTree:
        """

        :param days:
        :param months:
        :param years:
        :return:
        """
        filtered_range: RBTree = RBTree()

        for key in self.tree.keys():

            # Checks if current_key is in the desired year
            if years is not None and key.year not in years:
                continue

            # Checks if current_key is in the desired month
            if months is not None and key.month not in months:
                continue

            # Checks if current_key is the desired day of the month
            if days is not None and key.day not in days:
                continue

            # Checks for day of week
            if len(self.days_of_week.get_included()) > 0:
                if key.weekday() not in self.days_of_week.get_included():
                    continue

            # If the date meets the parameters adds it to the filtered tree
            value: object = self.tree.get_value(key)
            filtered_range.insert(key, value)

        return filtered_range


    def get_filtered_dates(self, day: int = None, month: int = None, year: int = None) -> RBTree:
        """
        Retrieve dates filtered by optional month, day, day of week, and/or year.

        :param day:
        :param month:
        :param year: Year to be filtered by

        Recommended usage:
            Parameter usage:
                get_dates(month=1, year=2020)
                get_dates(year=2020, month=1)
                get_dates(year=2020), etc

            General usage information:
                - Filtering by 3 parameters (day, month, year) will provide a tree of a specified date.
                - Filtering by 4 parameters (day, day of week, month, year) may provide and empty tree.
                - Filtering by day of week can be combined with month and year will provide all instances of that day
                  of the week.
                    -- TO FILTER BY DAY OF WEEK: User must add the days of the week by using the DaysOfWeek class which
                       can be accessed by calling the days_of_week field. See DaysOfWeek class for documentation.
                - Filtering by day and year for example get_dates(day=1, year=2020) will provide a tree containing the
                  1st of the month for every month in the year
                - Filtering by month and year for example get_dates(month=1, year=2020) will add all dates in january
                  2020 to a tree

        :return: A new tree containing filtered dates
        """
        years: list[int] = []
        months: list[int] = []
        days: list[int] = []

        # Checks if year is not None so it can be used in call to filter logic
        if year is not None:
            years.append(year)

        # Checks if month is not None so it can be used in call to filter logic
        if month is not None:
            months.append(month)

        # Checks if day is not None so it can be used in call to filter logic
        if day is not None:
            days.append(day)

        return self.get_filtered_date_range(years=years, months=months, days=days)