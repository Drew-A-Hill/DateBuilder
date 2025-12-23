
class DaysOfWeek:
    def __init__(self):
        """
        Instantiates the object such that each day of the week is false
        """
        self.included_days_list: list[int] = []

    def get_included(self) -> list[int]:
        """
        Adds int form of the days that are included dates to a list.
        :return: A list of included dates
        """
        return self.included_days_list

    @staticmethod
    def _include_exclude_check(days_list: list[bool], action: str) -> None:
        """

        :param days_list:
        :param action:
        :return:
        """
        for each in days_list:
            if each is True:
                raise ValueError(f"Marking both {action} all and a specific day as True is invalid, if the intent is "
                                 f"to {action} all only mark {action}_all as True")

    def include_all(self, days_list: list[bool]):
        """

        :param days_list:
        :return:
        """
        self._include_exclude_check(days_list, "include")
        for i in range(0, 6):
            self.included_days_list.append(i)

    def exclude_all(self, days_list: list[bool]):
        """

        :param days_list:
        :return:
        """
        self._include_exclude_check(days_list, "exclude")
        self.included_days_list.clear()

    def included_days(self, monday=False, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=False,
                     sunday=None, include_all=False, exclude_all=False) -> None:
        """

        :param monday:
        :param tuesday:
        :param wednesday:
        :param thursday:
        :param friday:
        :param saturday:
        :param sunday:
        :param include_all:
        :param exclude_all:
        :return:
        """
        days: list[bool] = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

        if include_all is True and exclude_all is True:
            raise ValueError("Can not mark both include_all and exclude_all as True")

        if include_all is True:
            self.include_all(days)

        elif exclude_all is True:
            self.exclude_all(days)

        else:
            for i in range(len(days)):
                if days[i] is True:
                    self.included_days_list.append(i)





