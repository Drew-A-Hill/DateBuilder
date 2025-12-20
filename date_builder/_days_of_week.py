
class DaysOfWeek:
    def __init__(self):
        """
        Instantiates the object such that each day of the week is false
        """
        self.mon: bool = False
        self.tue: bool = False
        self.wed: bool = False
        self.thu: bool = False
        self.fri: bool = False
        self.sat: bool = False
        self.sun: bool = False

    def monday(self, include: bool = False) -> None:
        """
        Sets the date bool for mon to True if to be included and False if to be excluded
        :param include: Input for determining inclusion
        :return: None
        """
        self.mon = include

    def tuesday(self, include: bool = False) -> None:
        """
        Sets the date bool for tue to True if to be included and False if to be excluded
        :param include: Input for determining inclusion
        :return: None
        """
        self.tue = include

    def wednesday(self, include: bool = False) -> None:
        """
        Sets the date bool for wed to True if to be included and False if to be excluded
        :param include: Input for determining inclusion
        :return: None
        """
        self.wed = include

    def thursday(self, include: bool = False) -> None:
        """
        Sets the date bool for thu to True if to be included and False if to be excluded
        :param include: Input for determining inclusion
        :return: None
        """
        self.thu = include

    def friday(self, include: bool = False) -> None:
        """
        Sets the date bool for fri to True if to be included and False if to be excluded
        :param include: Input for determining inclusion
        :return: None
        """
        self.fri = include

    def saturday(self, include: bool = False) -> None:
        """
        Sets the date bool for sat to True if to be included and False if to be excluded
        :param include: Input for determining inclusion
        :return: None
        """
        self.sat = include

    def sunday(self, include: bool = False) -> None:
        """
        Sets the date bool for sun to True if to be included and False if to be excluded
        :param include: Input for determining inclusion
        :return: None
        """
        self.sun = include

    def include_exclude_all(self, status: bool) -> None:
        """
        Updates all days of the week with either True or False
        :param status: True or False
        :return: None
        """
        self.monday(status)
        self.tuesday(status)
        self.wednesday(status)
        self.thursday(status)
        self.friday(status)
        self.saturday(status)
        self.sunday(status)

    def include_all(self) -> None:
        """
        Includes all days by calling include_exclude_all and passing true as the signal to include
        :return: None
        """
        self.include_exclude_all(True)

    def exclude_all(self) -> None:
        """
        Excludes all days by calling include_exclude_all and passing false as the signal to exclude
        :return: None
        """
        self.include_exclude_all(False)

    def get_included(self) -> list[int]:
        """
        Adds int form of the days that are included dates to a list
        :return: A list of included dates
        """
        included_dow: list[int] = []
        if self.mon is True:
            included_dow.append(0)

        if self.tue is True:
            included_dow.append(1)

        if self.wed is True:
            included_dow.append(2)

        if self.thu is True:
            included_dow.append(3)

        if self.fri is True:
            included_dow.append(4)

        if self.sat is True:
            included_dow.append(5)

        if self.sun is True:
            included_dow.append(6)

        return included_dow