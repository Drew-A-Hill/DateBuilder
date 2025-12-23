from datetime import datetime

from bintrees import RBTree

from ._filter_dates import FilteredDates
from ._days_of_week import DaysOfWeek
from ._delete_dates import DeleteDates
from ._find_dates import FindDate
from ._add_dates import AddDates
from ._helper_methods import HelperMethods
from ._show_dates import ShowDates

class DateBuilder:
    def __init__(self, tree: RBTree, date_obj: object, days_of_week: DaysOfWeek):
        """
        Instantiates the object that encapsulates the operations on the tree holding dates with the object to be used
        as the generic value.
        DateBuilder methods for a tree are:
        - new_date_tree(self) -> None
        - add_date_tree(self, first_date: datetime.date, last_date: datetime.date = None, unique_obj: object = None)
        - date_finder_tree(self, date: datetime.date) -> bool
        - delete_dates_tree(self, date : datetime.date) -> RBTree
        - def show_dates_tree(self) -> None
        :param date_obj: The object to be used as the generic value given there is not a unique object given directly
        """
        self.date_obj = date_obj
        self.tree = tree
        self.days_of_week: DaysOfWeek = days_of_week
        self.find = FindDate()

    @property
    def get_count(self) -> int:
        """

        :return:
        """
        return len(self.tree)

    def add_date_tree(self, first_date: datetime.date, last_date: datetime.date = None,
                      unique_obj: object = None) -> RBTree:
        """
        Adds dates to the tree between two dates (inclusive). If there is no last date therefore only the first date
        will be added. The dates will become the key, and the generic object passed at installation or unique object
        passed when this method is called is the object.
        :param first_date: The first date to add to the tree
        :param last_date: The last date to add to the tree
        :param unique_obj: The unique object to use as the value if needed otherwise None is the default
        :return: The tree with the added dates
        """
        return AddDates(self.date_obj, self.tree, self.days_of_week).add_date(first_date, last_date, unique_obj)

    def find_date(self, date: datetime.date) -> bool:
        """
        Finds if a date exists in the tree and returns True if the date exists and False if the date does not exist.
        :param date: The date being searched for
        :return: Bool response if the date has been found
        """
        return self.find.find_date_exist(self.tree, date)

    def delete_date(self, date: datetime.date) -> RBTree:
        """
        Deletes a single date from the tree if the date exists within the tree. If the date does not exist then a
        value error is raised
        :param date: The date to be removed
        :return: The tree with the date removed
        """
        return DeleteDates(self.tree, self.days_of_week).delete_date(date)

    def delete_date_range(self, lower_date: datetime.date=None, upper_date: datetime.date=None):
        """

        :param lower_date:
        :param upper_date:
        :return:
        """
        return DeleteDates(self.tree, self.days_of_week).delete_date_range(upper_date, lower_date)


    def filter_dates(self, day: int = None, month: int = None, year: int = None) -> RBTree:
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
        return FilteredDates(self.tree, self.days_of_week).get_filtered_dates(day, month, year)

    def filtered_date_range(self, days: list[int] = None, months: list[int] = None,
                                years: list[int] = None) -> RBTree:
        """

        :param days:
        :param months:
        :param years:
        :return:
        """
        return FilteredDates(self.tree, self.days_of_week).get_filtered_date_range(days, months, years)

    @staticmethod
    def show_dates(tree: RBTree) -> None:
        """
        Prints the dates in the tree to the terminal to provide user with a visual representation of the dates added
        :return: None
        """
        ShowDates.show_dates(tree)

    @staticmethod
    def str_to_date(date_str: str) -> datetime.date:
        """

        :param date_str:
        :return:
        """
        return HelperMethods.str_to_date(date_str)

