import datetime

from bintrees import RBTree

class FindDate:

    @staticmethod
    def find_date_exist(tree: RBTree, date: datetime.date) -> bool:
        """
        Finds if a date exists in the tree and returns True if the date exists and False if the date does not exist.
        :param tree: The tree to be searched
        :param date: The date being searched for
        :return: Bool response if the date has been found
        """
        for key in tree.keys():
            if key == date:
                return  True

        return False
