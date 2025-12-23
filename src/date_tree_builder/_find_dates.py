import datetime

from bintrees import RBTree

from ._helper_methods import HelperMethods

class FindDate:

    @staticmethod
    def find_date_exist(tree: RBTree, date: datetime.date) -> bool:
        """
        Finds if a date exists in the tree and returns True if the date exists and False if the date does not exist.
        :param tree: The tree to be searched
        :param date: The date being searched for
        :return: Bool response if the date has been found
        """
        current: datetime.date = tree.min_key()

        while current is not None:
            if current == date:
                return True

            current = tree.succ_key(current)

        return False

    def find_date(self, tree:RBTree , date: datetime.date):
        """
        Finds if a date exists in the tree and returns True if the date exists and False if the date does not exist.
        :param tree: The tree to be searched
        :param date: The date being searched for
        :return: Bool response if the date has been found
        """
        current: datetime.date = tree.min_key()

        while current is not None:
            if current == date:
                return True

            current = tree.succ_key(current)

        return False