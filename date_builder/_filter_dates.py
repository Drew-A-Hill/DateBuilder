import datetime

from bintrees import RBTree

from _days_of_week import DaysOfWeek

class FilteredDates:
    def __init__(self, tree: RBTree, days_of_week: DaysOfWeek):
        self.tree = tree
        self.days_of_week = days_of_week

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
        filtered: RBTree = RBTree()
        current_key: datetime.date = self.tree.min_key()
        next_key: datetime.date = self.tree.succ_key(current_key)
        current_value: object = self.tree.get_value(current_key)

        flag = False
        while next_key is not None:
            # Checks if current is in the desired year
            if year == current_key.year:
                flag = True

            # Checks if current is in the desired month
            if month == current_key.month:
                flag = True
            elif month is None:
                pass
            else:
                flag = False

            # Checks if current is the desired day of the month
            if day == current_key.day:
                flag = True
            elif day is None:
                pass
            else:
                flag = False

            # Checks for day of week
            if len(self.days_of_week.get_included()) > 0:
                if current_key.weekday() in self.days_of_week.get_included():
                    flag = True

                else:
                    flag = False


            # If the date meets the parameters adds it to the filtered tree
            if flag is True:
                filtered.insert(current_key, current_value)

            # Resets the flag for next iteration
            flag = False

            current_key = next_key

        return filtered

    def get_filtered_date_range(self, days: list[int] = None, months: list[int] = None,
                                years: list[int] = None) -> RBTree:
        pass


