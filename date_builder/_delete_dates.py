import datetime

from bintrees import RBTree

import _find_dates
from _days_of_week import DaysOfWeek
from _helper_methods import HelperMethods

class DeleteDates:
    def __init__(self, find: FindDates.FindDate, tree: RBTree):
        """
        Instantiates the delete date object with the necessary arguments
        :param find: The find date object used to find if a date is in tree
        :param tree: The tree that stores the dates and object as a key value pair
        """
        self.tree = tree
        self.days_of_week: DaysOfWeek = DaysOfWeek()
        self.find = find

    def delete_date_tree(self, date_str: str) -> RBTree:
        """
        Deletes a single date from the tree if the date exists within the tree. If the date does not exist then a
        value error is raised
        :param date_str: The date to be removed in str form
        :return: The tree with the date removed
        """
        if self.find.find_date(date_str) is False:
            raise ValueError("Date is not found")

        date: datetime.datetime = HelperMethods.str_to_date(date_str)
        self.tree.remove(date)

        return self.tree

    def delete_before(self, before_date: str, by_day: bool = False) -> RBTree:
        """
        Deletes all dates before a specified date. If the by date is selected as True then days_of_week.day of week in
        range to be deleted must be called. For example if the argument by_day is True and the desired action is to
        remove all mondays before the specified date then day_of_week.monday(True) must be called.
        :param before_date: The upper limit of dates to be deleted
        :param by_day: Signal that only the designated days of week will be deleted
        :return: The tree with the date removed
        """
        if self.find.find_date(before_date) is False:
            raise ValueError("Date is not found")

        current: datetime.date = self.tree.min_key()
        stop_date: datetime.date = HelperMethods.str_to_date(before_date)
        while current < stop_date:
            next_date: datetime.date = self.tree.succ_key(current)

            try:
                if by_day is True and current.weekday() in self.days_of_week.get_included():
                    self.tree.remove(current)

                elif by_day is False:
                    self.tree.remove(current)

            except KeyError:
                pass

            current = next_date

        return self.tree

    def delete_after(self, after_date: str, by_day: bool = False) -> RBTree:
        """
        Deletes all dates after a specified date. If the by date is selected as True then days_of_week.day of week in
        range to be deleted must be called. For example if the argument by_day is True and the desired action is to
        remove all mondays before the specified date then day_of_week.monday(True) must be called.
        :param after_date: The lower limit of dates to be deleted
        :param by_day: Signal that only the designated days of week will be deleted
        :return: The tree with the date removed
        """
        if self.find.find_date(after_date) is False:
            raise ValueError("Date is not found")

        current: datetime.date = self.tree.succ_key(HelperMethods.str_to_date(after_date))

        while self.tree.succ_key(current) is not None:
            next_date: datetime.date = self.tree.succ_key(current)

            try:
                if by_day is True and current.weekday() in self.days_of_week.get_included():
                    self.tree.remove(current)

                elif by_day is False:
                    self.tree.remove(current)

            except KeyError:
                pass

            current = next_date

        return self.tree

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
        if self.find.find_date(first_date) is False:
            raise ValueError("Date is not found")

        current: datetime.date = self.tree.succ_key(HelperMethods.str_to_date(first_date))
        last = datetime.date = HelperMethods.str_to_date(last_date)

        while current < last:
            next_date: datetime.date = self.tree.succ_key(current)

            try:
                if by_day is True and current.weekday() in self.days_of_week.get_included():
                    self.tree.remove(current)

                elif by_day is False:
                    self.tree.remove(current)

            except KeyError:
                pass

            current = next_date

        return self.tree









