from datetime import datetime

from bintrees import RBTree

class ShowDates:

    def show_dates(self, tree: RBTree) -> None:
        """
        Displays the dates in the tree to the terminal to provide user with a visual representation of the dates added
        :return: None
        """
        current: datetime.date = tree.min_key()
        next_key: datetime.date = tree.succ_key(current)

        while next_key is not None:
            print(current)
            current = next_key

    def show_date_count(self, tree: RBTree) -> None:
        """
        Displays number of dates in tree
        :return: None
        """
        current: datetime.date = tree.min_key()
        next_key: datetime.date = tree.succ_key(current)
        count: int = 0

        while next_key is not None:

            if current is not None:
                count = count + 1

            current = next_key

        print(count)