import datetime

from bintrees import RBTree

from ._helper_methods import HelperMethods

class FindDate:

    @staticmethod
    def find_date(tree: RBTree, date: str) -> bool:
        """
        Finds if a date exists in the tree and returns True if the date exists and False if the date does not exist.
        :param tree: The tree to be searched
        :param date: The date being searched for
        :return: Bool response if the date has been found
        """
        date: datetime.date =  HelperMethods.str_to_date(date)
        x: datetime.date = tree.min_key()

        while tree.succ_key(x) is not None:
            if x == date:
                return True

            x = tree.succ_key(x)

        return False

