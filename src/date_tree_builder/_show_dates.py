from datetime import datetime

from bintrees import RBTree

class ShowDates:

    @staticmethod
    def show_dates(tree: RBTree) -> None:
        """
        Displays the dates in the tree to the terminal to provide user with a visual representation of the dates added
        :return: None
        """
        if tree.is_empty():
            raise KeyError("Tree is empty")

        for key in tree.keys():
            print(key)
