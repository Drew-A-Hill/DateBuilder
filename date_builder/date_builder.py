from datetime import datetime

from bintrees import RBTree

from ._days_of_week import DaysOfWeek
from ._delete_dates import DeleteDates
from ._find_dates import FindDate
from ._add_dates import AddDates
from ._show_dates import ShowDates

class DateBuilder:
    def __init__(self, tree: RBTree, date_obj: object):
        """
        Instantiates the object that encapsulates the operations on the tree holding dates with the object to be used
        as the generic value.
        DateBuilder methods for a tree are:
        - new_date_tree(self) -> None
        - add_date_tree(self, first_date: datetime.date, last_date: datetime.date = None, unique_obj: object = None)
        - date_finder_tree(self, date: str) -> bool
        - delete_dates_tree(self, date : str) -> RBTree
        - def show_dates_tree(self) -> None
        :param date_obj: The object to be used as the generic value given there is not a unique object given directly
        """
        self.date_obj = date_obj
        self.tree = tree
        self.days_of_week = DaysOfWeek()

    def new_date_tree(self) -> None:
        """
        Creates a new empty tree
        :return: None
        """
        self.tree = AddDates(self.date_obj, self.tree).new_date_tree()

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
        return AddDates(self.date_obj, self.tree).add_date_tree(first_date, last_date, unique_obj)

    def date_finder_tree(self, date: str) -> bool:
        """
        Finds if a date exists in the tree and returns True if the date exists and False if the date does not exist.
        :param date: The date being searched for
        :return: Bool response if the date has been found
        """
        return FindDate(self.tree).find_date(date)

    def delete_dates_tree(self, date_str : str) -> RBTree:
        """
        Deletes a single date from the tree if the date exists within the tree. If the date does not exist then a
        value error is raised
        :param date_str: The date to be removed in str form
        :return: The tree with the date removed
        """
        return DeleteDates(FindDate(self.tree), self.tree).delete_date_tree(date_str)

    def delete_before(self, before_date: str, by_day: bool = False) -> RBTree:
        """
        Deletes all dates before a specified date. If the by date is selected as True then days_of_week.day of week in
        range to be deleted must be called. For example if the argument by_day is True and the desired action is to
        remove all mondays before the specified date then day_of_week.monday(True) must be called.
        :param before_date: The upper limit of dates to be deleted
        :param by_day: Signal that only the designated days of week will be deleted
        :return: The tree with the date removed
        """
        return DeleteDates(FindDate(self.tree), self.tree).delete_before(before_date, by_day)

    def delete_after(self, after_date: str, by_day: bool = False) -> RBTree:
        """
        Deletes all dates after a specified date. If the by date is selected as True then days_of_week.day of week in
        range to be deleted must be called. For example if the argument by_day is True and the desired action is to
        remove all mondays before the specified date then day_of_week.monday(True) must be called.
        :param after_date: The lower limit of dates to be deleted
        :param by_day: Signal that only the designated days of week will be deleted
        :return: The tree with the date removed
        """
        return DeleteDates(FindDate(self.tree), self.tree).delete_after(after_date, by_day)

    def delete_between(self, first_date: str, last_date: str, by_day: bool = False) -> RBTree:
        """
        Deletes all dates between specified dates. If the by date is selected as True then days_of_week.day of week in
        range to be deleted must be called. For example if the argument by_day is True and the desired action is to
        remove all mondays before the specified date then day_of_week.monday(True) must be called.
        :param first_date: The lower limit of dates to be deleted
        :param last_date: The upper limit of dates to be deleted
        :param by_day: Signal that only the designated days of week will be deleted
        :return: The tree with the date removed
        """
        return DeleteDates(FindDate(self.tree), self.tree).delete_between(first_date, last_date, by_day)

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
        return Filter.FilteredDates(self.tree, self.days_of_week).get_filtered_dates(day, month, year)

    def filtered_date_range(self, days: list[int] = None, months: list[int] = None,
                                years: list[int] = None) -> RBTree:
        """

        :param day_of_week:
        :param days:
        :param months:
        :param years:
        :return:
        """
        return Filter.FilteredDates(self.tree, self.days_of_week).get_filtered_date_range(days, months, years)

    def show_dates_tree(self, tree: RBTree) -> None:
        """
        Prints the dates in the tree to the terminal to provide user with a visual representation of the dates added
        :return: None
        """
        ShowDates().show_dates(tree)

