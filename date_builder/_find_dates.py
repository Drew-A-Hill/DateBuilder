import datetime

from bintrees import RBTree

from ._helper_methods import HelperMethods

class FindDate:
    def __init__(self, tree: RBTree):
        """
        Instantiates the object with the tree.
        :param tree: The tree that stores the dates and object as a key value pair
        """
        self.tree = tree

    def find_date(self, date: str) -> bool:
        """
        Finds if a date exists in the tree and returns True if the date exists and False if the date does not exist.
        :param date: The date being searched for
        :return: Bool response if the date has been found
        """
        date: datetime.date =  HelperMethods.str_to_date(date)
        x: datetime.date = self.tree.min_key()

        while self.tree.succ_key(x) is not None:
            if x == date:
                return True

            x = self.tree.succ_key(x)

        return False

