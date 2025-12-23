from datetime import datetime

from bintrees import RBTree

class ShowDates:

    @staticmethod
    def show_dates(tree: RBTree) -> None:
        """
        Displays the dates in the tree to the terminal to provide user with a visual representation of the dates added
        :return: None
        """
        current: datetime.date = tree.min_key()

        while current is not None:
            print(current)

            try:
                current = tree.succ_key(current)

            except KeyError:
                current = None