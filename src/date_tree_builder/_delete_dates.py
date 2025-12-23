import datetime

from bintrees import RBTree

from ._find_dates import FindDate
from ._days_of_week import DaysOfWeek
from ._helper_methods import HelperMethods

class DeleteDates:
    def __init__(self, tree: RBTree, days_of_week: DaysOfWeek):
        """
        Instantiates the delete date object with the necessary arguments
        :param tree: The tree that stores the dates and object as a key value pair
        """
        self.tree = tree
        self.days_of_week: DaysOfWeek = days_of_week
        self.find = FindDate

    def delete_date(self, date: datetime.date) -> RBTree:
        """
        Deletes a single date from the tree if the date exists within the tree. If the date does not exist then a
        value error is raised
        :param date: The date to be removed
        :return: The tree with the date removed
        """
        if self.find.find_date_exist(self.tree, date) is False:
            raise ValueError("Date is not found")

        self.tree.remove(date)

        return self.tree

    def delete_date_range(self, lower_date: datetime.date=None, upper_date: datetime.date=None) -> RBTree:
        """

        :param lower_date:
        :param upper_date:
        :return:
        """
        for key in self.tree.keys():
            if lower_date is None and upper_date is None:
                raise ValueError("Both lower date and upper date can not be None")

            if lower_date is not None and key < lower_date:
                continue

            else:
                self.tree.remove(key)

            if upper_date is not None and key > upper_date:
                break

        return self.tree










