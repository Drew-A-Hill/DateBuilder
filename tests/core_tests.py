import datetime
import datetime as dt
from typing import Any, Dict

import pytest
from bintrees import RBTree

import date_tree_builder.date_builder as datebuilder
from date_tree_builder.date_builder import DateBuilder


# --------------- Creates a dummy date object for the test ------------------
class DummyObject:
    """
    Creates dummy object to be used as the date object
    """
    def __init__(self):
        self.date = None

# --------------- Tests getting the count of elements added ----------------

def test_get_count():
    """
    Tests how getting the count of the number of dates in the tree
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 1)
    last: datetime.date = datetime.date(2025, 1, 5)

    # Add 5 dates to tree
    db.add_dates(first, last)

    assert db.get_count == 5

def test_get_count_empty():
    """
    Tests how getting the count of the number of dates when there are no elements added to the tree
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    assert db.get_count == 0

def test_count_after_remove():
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 1)
    last: datetime.date = datetime.date(2025, 1, 5)

    # Add 5 dates to tree
    db.add_dates(first, last)

    assert db.get_count == 5

    # Remove 01/01/2025
    db.delete_date(first)

    assert db.get_count == 4

# ------------------------------ Tests adding dates ------------------------------

def test_add_date_range():
    """
    Tests successful adding of date range
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 1)
    last: datetime.date = datetime.date(2025, 1, 5)

    # Add 5 dates to tree
    result: RBTree = db.add_dates(first, last)

    current = first

    # Checks if dates are in tree
    for key in result.keys():
        assert key == current
        current = current + datetime.timedelta(1)

def test_add_single_date():
    """
        Tests successful adding of a single date
        """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 1)
    last: datetime.date = datetime.date(2025, 1, 1)

    # Add date to tree
    date_tree: RBTree = db.add_dates(first, last)
    result: datetime.date = date_tree.min_key()

    # Checks if dates are in tree
    count_results: int = len(date_tree)

    assert count_results == 1
    assert result == first

def test_lower_bound_date_greater():
    """
    Tests that a ValueError exception is correctly raised when the lower bound date is greater than upper bound date
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 2)
    last: datetime.date = datetime.date(2025, 1, 1)

    with pytest.raises(ValueError):
        db.add_dates(first, last)

# ------------------------------ Tests deleting dates ------------------------------

# ------------------------------ Tests filtering dates -----------------------------

# ------------------------------ Tests finding dates -------------------------------

# ------------------ Tests the include_days_of_week functionality ------------------

def test_include_all_days_of_week():
    """
    Tests to see if all the days of week have been added successfully
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Includes all dates
    db.include_days_of_week(include_all=True)

    # Retrieves the list of added days of week
    results: list[int] = db.days_of_week.get_included()

    # Checks that all days of week have been added
    for i in range(len(results)):
        assert results[i] == i

    # Checks for 0 dow elements in list
    assert len(results) == 7

def test_exclude_all_days_of_week():
    """
    Tests to see if all the days of week have been added excluded
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Includes all dates
    db.include_days_of_week(exclude_all=True)

    # Retrieves the list of added days of week
    results: list[int] = db.days_of_week.get_included()

    # Checks for 0 dow elements in list
    assert len(results) == 0

def test_days_of_week_both_include_exclude_true():
    """
    Tests to see if a ValueError exception is correctly raised when both include_all and exclude_all are marked True
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Includes all dates
    with pytest.raises(ValueError):
        db.include_days_of_week(include_all=True, exclude_all=True)

def test_days_of_week_both_include_all_and_day_true():
    """
    Tests to see if a ValueError exception is correctly raised when both include_all and a day of week are marked True
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Includes all dates
    with pytest.raises(ValueError):
        db.include_days_of_week(include_all=True, monday=True)

def test_days_of_week_both_exclude_all_and_day_true():
    """
    Tests to see if a ValueError exception is correctly raised when both exclude_all and a day of week are marked True
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Includes all dates
    with pytest.raises(ValueError):
        db.include_days_of_week(exclude_all=True, monday=True)

def test_add_remove_dow():
    """
    Tests including single days of the week
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    def remove_and_test():
        """
        Removes and tests that dows have been removed
        """
        db.include_days_of_week(exclude_all=True)
        result: int = len(db.days_of_week.get_included())

        # Checks for no days included
        assert result == 0

    # Includes days and checks it has been included then removes days and checks it has been removed
    # Include Monday (0)
    db.include_days_of_week(monday=True)
    result: int = db.days_of_week.get_included()[0]

    assert result == 0

    # Remove Monday
    remove_and_test()

    # Include Tuesday (1)
    db.include_days_of_week(tuesday=True)
    result: int = db.days_of_week.get_included()[0]

    assert result == 1

    # Remove Tuesday
    remove_and_test()

    # Include Wednesday (2)
    db.include_days_of_week(wednesday=True)
    result: int = db.days_of_week.get_included()[0]

    assert result == 2

    # Remove Wednesday
    remove_and_test()

    # Include Thursday (3)
    db.include_days_of_week(thursday=True)
    result: int = db.days_of_week.get_included()[0]

    assert result == 3

    # Remove Thursday
    remove_and_test()

    # Include Friday (4)
    db.include_days_of_week(friday=True)
    result: int = db.days_of_week.get_included()[0]

    assert result == 4

    # Remove Friday
    remove_and_test()

    # Include Saturday (5)
    db.include_days_of_week(saturday=True)
    result: int = db.days_of_week.get_included()[0]

    assert result == 5

    # Remove Saturday
    remove_and_test()

    # Include Sunday (6)
    db.include_days_of_week(sunday=True)
    result: int = db.days_of_week.get_included()[0]

    assert result == 6

    # Remove Sunday
    remove_and_test()

def test_add_remove_multi_dow():
    """
    Tests including multiple days of the week and excluding them
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    def remove_and_test():
        """
        Removes and tests that dows have been removed
        """
        db.include_days_of_week(exclude_all=True)
        result: int = len(db.days_of_week.get_included())

        # Checks for no days included
        assert result == 0

    # Include Monday (0) and Tuesday (1)
    db.include_days_of_week(monday=True)
    db.include_days_of_week(tuesday=True)

    result_mon: int = db.days_of_week.get_included()[0]
    assert result_mon == 0

    result_tue: int = db.days_of_week.get_included()[1]
    assert result_tue == 1

    result_count: int = len(db.days_of_week.get_included())
    assert  result_count == 2

    remove_and_test()

def test_reset_after_add():
    """
    Tests that day of week tracker is reset after each add instance
    """
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Includes 3 days
    db.include_days_of_week(monday=True, wednesday=True, friday=True)

    # Determines date range
    first: datetime.date = datetime.date(2025, 1, 1)
    last: datetime.date = datetime.date(2025, 1, 31)

    # Checks that there are 3 days of week
    result = len(db.days_of_week.get_included())
    assert result == 3

    # Adds dates in range based on day of week
    db.add_dates(first, last)

    # Checks for reset
    result = len(db.days_of_week.get_included())
    assert result == 0

# --------------- Below tests the display_dates functionality ---------------

def test_display_dates_non_empty_tree():
    """
    Tests display date for a non-empty tree. This is a manual test where the dates 2025/01/01, 2025/01/02,
    2025/01/03, 2025/01/04, 2025/01/05 should appear in the terminal
    """
    # Sets up tree with added dates so display dates can be tested
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Sets first and last date in datetime
    first_date: datetime.date = dt.date(2025, 1, 1)
    last_date: datetime.date = dt.date(2025, 1, 5)

    # Includes days of week
    db.include_days_of_week(include_all=True)

    # Adds dates to tree
    db.add_dates(first_date, last_date)

    # Displays the tree in the terminal
    db.display_dates(tree)

def test_display_dates_empty_tree():
    """
    Tests display date for an empty tree. This should raise a KeyError Exception.
    """
    # Sets up tree with added dates so display dates can be tested
    # Sets up the date builder with a tree and date object
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    db: DateBuilder = DateBuilder(tree, date_obj)

    # Tries to display dates of an empty tree
    with pytest.raises(KeyError):
        db.display_dates(tree)

# --------------- Below tests the str_to_date functionality ---------------
def test_str_to_date_pass(monkeypatch: pytest.MonkeyPatch):
    """
    Tests to see if str_to_date returns the correct date time
    """
    called: Dict[str, Any] = {}

    class FakeHelperMethods:
        @staticmethod
        def str_to_date(date_str: str) -> dt.date:
            called["arg"] = date_str
            # Sentinel value so we know this was used
            return dt.date(2025, 12, 31)

    monkeypatch.setattr(datebuilder, "HelperMethods", FakeHelperMethods)

    result = DateBuilder.str_to_date("01/01/2025")

    assert result == dt.date(2025, 12, 31)
    assert called["arg"] == "01/01/2025"

def test_str_to_date_failed_match():
    """
    Tests for that dates don't match when providing differing dates
    """
    result = DateBuilder.str_to_date("01/01/2025")

    assert not result == dt.date(2021, 12, 31)

def test_str_to_date_correct_raise_invalid_y_m_d():
    """
    Tests that a ValueError exception is correctly raised when providing a date in an invalid format yyyy/mm/dd rather
    than dd/mm/yyyy
    """
    with pytest.raises(ValueError):
        DateBuilder.str_to_date("2025/01/01")

def test_str_to_date_correct_raise_invalid_year_len():
    """
    Tests that a ValueError exception is correctly raised when providing a date in an invalid format dd/mm/yyyyy rather
    than dd/mm/yyyy
    """
    with pytest.raises(ValueError):
        DateBuilder.str_to_date("01/01/20205")

def test_str_to_date_correct_raise_invalid_seperator():
    """
    Tests that a ValueError exception is correctly raised when providing a date in an invalid format dd-mm-yyyy rather
    than dd/mm/yyyy
    """
    with pytest.raises(ValueError):
        DateBuilder.str_to_date("01-01-2025")

def test_str_to_date_correct_raise_invalid_type():
    """
    Tests that a TypeError exception is correctly raised when providing a date as a datetime rather than str
    """
    date: datetime.date = datetime.date(2025, 1, 1)

    with pytest.raises(TypeError):
        DateBuilder.str_to_date(date)