import datetime

from bintrees import RBTree

from _days_of_week import DaysOfWeek


class AddDates:
    def __init__(self, date_obj: object, tree: RBTree):
        """
        Instantiates the object with the correct arguments to add dates as a key and object as a value to the tree
        :param date_obj: The object to be used as the default for the value
        :param tree: The tree that stores the dates and object as a key value pair
        """
        self.date_obj = date_obj
        self.tree = tree
        self.days_of_week: DaysOfWeek = DaysOfWeek()

    def _copy_obj(self) -> object:
        """
        Makes a copy of the object passed by the user. Assumes this is a non-unique object that will have fields updated
        at a later time
        :return: The object
        """
        copy: object = self.date_obj
        return copy

    def new_date_tree(self) -> RBTree:
        """
        Creates a new empty tree
        :return: None
        """
        return RBTree()

    def add_date_tree(self, first_date: datetime.date, last_date: datetime.date = None,
                      unique_obj: object = None) -> RBTree:
        """
        Adds dates to the tree between two dates (inclusive). If there is no last date therefore only the first date
        will be added. The dates will become the key, and the generic object passed at installation or unique object
        passed when this method is called is the object.
        :param first_date: The first date to add to the tree
        :param last_date: The last date to add to the tree
        :param unique_obj: The unique object to use as the value if needed otherwise None is the default
        :return: The tree with the added dates
        """
        # Checks for single date entry occurring by lack of last date
        if last_date is None:
            last_date = first_date

        if last_date < first_date:
            raise ValueError()

        if len(self.days_of_week.get_included()) == 0:
            raise ValueError("No days of weeks were included")

        current_date: datetime.date = first_date
        while current_date <= last_date:
            if current_date.weekday() in self.days_of_week.get_included():

                # Checks if user has passed a unique object for each date.
                if unique_obj is not None:
                    self.tree.insert(current_date, unique_obj)

                else:
                    self.tree.insert(current_date, self._copy_obj())
                current_date = current_date + datetime.timedelta(1)

        return self.tree


