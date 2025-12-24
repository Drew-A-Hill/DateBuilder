import datetime

from bintrees import RBTree

class FindDate:
    """
    Internal helper for checking whether a given date exists in an RBTree.
    """
    @staticmethod
    def find_date_exist(tree: RBTree, date: datetime.date) -> bool:
        """
        Check whether the given date exists in the tree.
        :param tree: The tree to be searched. Keys are expected to be datetime.date.
        :param date: The date being searched for.
        :return: True if the date exists in the tree, False otherwise.
        """
        return date in tree.keys()
