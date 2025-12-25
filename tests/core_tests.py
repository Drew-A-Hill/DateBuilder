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

# ----------------- Creates a date builder for the test --------------------
def builder() -> DateBuilder:
    """
    Creates the instance of the DateBuilder to be used for testing
    :return: The DateBuilder instance
    """
    tree: RBTree = RBTree()
    date_obj: object = DummyObject()
    return DateBuilder(tree, date_obj)

# --------------- Tests getting the count of elements added ----------------

def test_get_count():
    """
    Tests how getting the count of the number of dates in the tree
    """
    # Sets up the date builder with a tree and date object
    db = builder()

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 1)
    last: datetime.date = datetime.date(2025, 1, 5)

    # Add 5 dates to tree
    db.add_dates(first, last)

    assert db.count == 5

def test_get_count_empty():
    """
    Tests how getting the count of the number of dates when there are no elements added to the tree
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    assert db.count == 0

def test_count_after_remove():
    db: DateBuilder = builder()

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 1)
    last: datetime.date = datetime.date(2025, 1, 5)

    # Add 5 dates to tree
    db.add_dates(first, last)

    assert db.count == 5

    # Remove 01/01/2025
    db.delete_date(first)

    assert db.count == 4

# ------------------------------ Tests adding dates ------------------------------

def test_add_date_range():
    """
    Tests successful adding of date range
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()
    tree: RBTree = db.tree

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

    # Checks that the tree returned is the same as the tree ref
    assert len(tree) == len(result)

def test_add_single_date():
    """
        Tests successful adding of a single date
        """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()
    tree: RBTree = db.tree

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 1)

    # Add date to tree
    date_tree: RBTree = db.add_dates(first)
    result: datetime.date = date_tree.min_key()

    # Checks if dates are in tree
    count_results: int = len(date_tree)

    # Checks that the tree returned is the same as the tree ref
    assert len(tree) == len(date_tree)

    assert count_results == 1
    assert result == first

def test_lower_bound_date_greater():
    """
    Tests that a ValueError exception is correctly raised when the lower bound date is greater than upper bound date
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, 2)
    last: datetime.date = datetime.date(2025, 1, 1)

    with pytest.raises(ValueError):
        db.add_dates(first, last)

# ------------------------------ Tests deleting dates ------------------------------
def add_date_helper(db: DateBuilder, first: int, last: int = None) -> RBTree:
    """
    Provides a tree of dates to delete from.
    """
    # Include all days of week
    db.include_days_of_week(include_all=True)

    # Determines range of dates to add
    first: datetime.date = datetime.date(2025, 1, first)

    if last is not None:
        last: datetime.date = datetime.date(2025, 1, last)

        # Adds dates to date tree
        db.add_dates(first, last)

    else:
        # Adds dates to date tree
        db.add_dates(first)

    return db.tree

def test_delete_single_date_element():
    """
    Tests deleting a date from the tree
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    tree: RBTree = add_date_helper(db, 1, 30)

    assert tree.is_empty() is False
    assert len(tree) == 30

    # Deletes Date
    db.delete_date(datetime.date(2025, 1, 1))

    assert len(tree) == 29

def test_delete_single_date_element_multi():
    """
    Tests deleting a date from the tree multiple times
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Tree with added dates
    add_date_helper(db, 1, 30)

    # Checks that there have been dates added to the tree
    assert db.is_empty is False
    assert len(db.tree) == 30

    # Dates to delete
    date1: datetime = datetime.date(2025, 1, 1)
    date2: datetime = datetime.date(2025, 1, 2)

    # Checks for dates before deletion
    assert db.find_date(db.tree, date1)
    assert db.find_date(db.tree, date2)

    # Deletes Date
    db.delete_date(date1)

    assert len(db.tree) == 29
    # Checks for date after deletion
    assert db.find_date(db.tree, date1) is False

    # Deletes Date
    db.delete_date(datetime.date(2025, 1, 2))

    assert len(db.tree) == 28
    # Checks for date after deletion
    assert db.find_date(db.tree, date2) is False

def test_delete_from_empty():
    """
    Tests deleting from empty tree correctly raises ValueError
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Checks that tree is empty
    assert db.is_empty

    with pytest.raises(ValueError):
        db.delete_date(datetime.date(2025, 1, 2))

def test_delete_single_not_found():
    """
    Tests deleting from tree that doesn't have the date correctly raises ValueError
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds Dates
    add_date_helper(db, 2, 10)

    with pytest.raises(ValueError):
        db.delete_date(datetime.date(2025, 1, 1))

def test_delete_to_empty():
    """
    Tests deleting from tree that doesn't have the date correctly raises ValueError
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds Dates
    add_date_helper(db, 1, 1)

    # Deletes only date
    db.delete_date(datetime.date(2025, 1, 1))

    # Checks its empty
    assert db.is_empty

def test_delete_date_between_range():
    """
    Tests deleting a range of dates from the tree between the uber and lower bound inclusive
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds dates
    add_date_helper(db, 1, 10)

    # Checks dates were added
    assert db.is_empty is False
    assert len(db.tree) == 10

    # Lower bound of dates to remove
    lower_date: datetime.date = datetime.date(2025, 1, 1)
    upper_date: datetime.date = datetime.date(2025, 1, 5)

    # Deletes Date
    db.delete_date_range(lower_date, upper_date)

    assert len(db.tree) == 5

def test_delete_dates_from_lower():
    """
    Tests deleting all dates from the lower bound date to the max date
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds dates
    add_date_helper(db, 1, 10)

    #Checks dates were added
    assert db.is_empty is False
    assert len(db.tree) == 10

    # Lower bound of dates to remove
    lower_date: datetime.date = datetime.date(2025, 1, 6)

    # Deletes Date
    db.delete_date_range(lower_date=lower_date)

    assert len(db.tree) == 5

    # Checks for a date that should be in tree
    assert db.find_date(db.tree, datetime.date(2025, 1, 5))

    # Checks for a date that should not be in the tree
    assert db.find_date(db.tree, datetime.date(2025, 1, 6)) is False

def test_delete_dates_from_upper():
    """
    Tests deleting all dates from the upper bound date to the min date
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds dates
    add_date_helper(db, 1, 10)

    #Checks dates were added
    assert db.is_empty is False
    assert len(db.tree) == 10

    # Upper bound of dates to remove
    upper: datetime.date = datetime.date(2025, 1, 5)

    # Deletes Date
    db.delete_date_range(upper_date=upper)

    assert len(db.tree) == 5

    # Checks for a date that should be in tree
    assert db.find_date(db.tree, datetime.date(2025, 1, 6))

    # Checks for a date that should not be in the tree
    assert db.find_date(db.tree, datetime.date(2025, 1, 5)) is False

def test_remove_from_range_date_doesnt_exist():
    """
    Tests deleting dates from a range when a date doesn't exist in the range
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds dates
    add_date_helper(db, 1, 10)

    # Checks dates were added
    assert db.is_empty is False
    assert len(db.tree) == 10

    # Deletes a single date
    date: datetime.date = datetime.date(2025, 1, 3)
    db.delete_date(date)

    # Checks dates been removed
    assert db.find_date(db.tree, date) is False

    # Date range
    lower_date: datetime.date = datetime.date(2025, 1, 1)
    upper_date: datetime.date = datetime.date(2025, 1, 5)

    # Deletes Date
    db.delete_date_range(lower_date, upper_date)

    assert len(db.tree) == 5

    # Checks for a date that should be in tree
    assert db.find_date(db.tree, datetime.date(2025, 1, 6))

    # Checks for a date that should not be in the tree
    assert db.find_date(db.tree, datetime.date(2025, 1, 5)) is False
    assert db.find_date(db.tree, datetime.date(2025, 1, 3)) is False

def tests_delete_from_empty():
    """
    Tests that if there is an attempt to remove from an empty tree that a ValueError is raised
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Checks dates were added
    assert db.is_empty

    # Date range
    lower_date: datetime.date = datetime.date(2025, 1, 1)
    upper_date: datetime.date = datetime.date(2025, 1, 5)

    with pytest.raises(ValueError):
        db.delete_date_range(lower_date, upper_date)

# ------------------------------ Tests filtering dates -----------------------------
def test_filter_by_year():
    """
    Tests filtering dates by year only
    """
    # Sets up the date builder with a tree and date object
    db = builder()

    # Range of dates to be added
    first = datetime.date(2024, 12, 1)
    last  = datetime.date(2025, 1, 1)

    # Includes days of week
    db.include_days_of_week(include_all=True)

    # Adds date range
    db.add_dates(first, last)

    # Includes days of week for filter
    db.include_days_of_week(include_all=True)

    # Filters for 2025
    filtered_2025 = db.filter_dates(year=2025)

    assert len(filtered_2025) == 1
    assert db.find_date(filtered_2025, last)
    assert db.find_date(filtered_2025, first) is False

    # Includes days of the week for 2024 filtering
    db.include_days_of_week(include_all=True)

    # Adds date range
    filtered_2024 = db.filter_dates(year=2024)

    assert len(filtered_2024) == 31
    assert db.find_date(filtered_2024, first)
    assert db.find_date(filtered_2024, last) is False

def test_filter_by_month():
    """
    Tests filtering dates by month only
    """
    # Sets up the date builder with a tree and date object
    db = builder()

    # Range of dates to be added
    first = datetime.date(2023, 12, 1)
    last = datetime.date(2025, 12, 1)

    # Includes days of week
    db.include_days_of_week(include_all=True)

    # Adds date range
    db.add_dates(first, last)

    # Includes days of week for filter
    db.include_days_of_week(include_all=True)

    # Filters dates by month january
    filtered_jan: RBTree = db.filter_dates(month=1)

    # Dates to be checked against filtered tree
    filter1_true1: datetime.date = datetime.date(2024,1,5)
    filter1_true2: datetime.date = datetime.date(2025, 1, 5)
    filter1_false1: datetime.date = datetime.date(2025, 12, 31)
    filter1_false2: datetime.date = datetime.date(2023, 11, 1)

    assert len(filtered_jan) == 62
    assert db.find_date(filtered_jan, filter1_true1)
    assert db.find_date(filtered_jan, filter1_true2)
    assert db.find_date(filtered_jan, filter1_false1) is False
    assert db.find_date(filtered_jan, filter1_false2) is False

    # Filters dates by month december
    db.include_days_of_week(include_all=True)
    filtered_dec: RBTree = db.filter_dates(month=12)

    # Dates to be checked against filtered tree
    filter2_true1: datetime.date = datetime.date(2024, 12, 5)
    filter2_true2: datetime.date = datetime.date(2025, 12, 1)
    filter2_false1: datetime.date = datetime.date(2024, 5, 5)
    filter2_false2: datetime.date = datetime.date(2025, 4, 5)
    filter2_false3: datetime.date = datetime.date(2022, 4, 5)

    assert len(filtered_dec) == 63
    assert db.find_date(filtered_dec, filter2_true1)
    assert db.find_date(filtered_dec, filter2_true2)
    assert db.find_date(filtered_dec, filter2_false1) is False
    assert db.find_date(filtered_dec, filter2_false2) is False
    assert db.find_date(filtered_dec, filter2_false3) is False

def test_filter_by_year_month():
    """
    Tests filtering dates by year and month
    :return:
    """
    # Sets up the date builder with a tree and date object
    db = builder()

    # Range of dates to be added
    first = datetime.date(2023, 12, 1)
    last = datetime.date(2025, 12, 1)

    # Includes days of week
    db.include_days_of_week(include_all=True)

    # Adds date range
    db.add_dates(first, last)

    # Includes days of week for filter
    db.include_days_of_week(include_all=True)

    # Filters dates by month january 2024
    filtered_jan: RBTree = db.filter_dates(year=2024, month=1)

    # Dates to be checked against filtered tree
    filter1_true1: datetime.date = datetime.date(2024, 1, 5)
    filter1_true2: datetime.date = datetime.date(2024, 1, 31)
    filter1_false1: datetime.date = datetime.date(2025, 12, 31)
    filter1_false2: datetime.date = datetime.date(2023, 11, 1)
    filter1_false3: datetime.date = datetime.date(2025, 1, 1)

    assert len(filtered_jan) == 31
    assert db.find_date(filtered_jan, filter1_true1)
    assert db.find_date(filtered_jan, filter1_true2)
    assert db.find_date(filtered_jan, filter1_false1) is False
    assert db.find_date(filtered_jan, filter1_false2) is False
    assert db.find_date(filtered_jan, filter1_false3) is False

    # Filters dates by month december
    db.include_days_of_week(include_all=True)
    filtered_dec: RBTree = db.filter_dates(year=2025, month=11)

    # Dates to be checked against filtered tree
    filter2_true1: datetime.date = datetime.date(2025, 11, 5)
    filter2_true2: datetime.date = datetime.date(2025, 11, 1)
    filter2_false1: datetime.date = datetime.date(2024, 5, 5)
    filter2_false2: datetime.date = datetime.date(2025, 4, 5)
    filter2_false3: datetime.date = datetime.date(2022, 11, 5)

    assert len(filtered_dec) == 30
    assert db.find_date(filtered_dec, filter2_true1)
    assert db.find_date(filtered_dec, filter2_true2)
    assert db.find_date(filtered_dec, filter2_false1) is False
    assert db.find_date(filtered_dec, filter2_false2) is False
    assert db.find_date(filtered_dec, filter2_false3) is False

def test_filter_by_year_day():
    """
    Tests filtering dates by year and day
    """
    # Sets up the date builder with a tree and date object
    db = builder()

    # Range of dates to be added
    first = datetime.date(2023, 12, 1)
    last = datetime.date(2026, 12, 1)

    # Includes days of week
    db.include_days_of_week(include_all=True)

    # Adds date range
    db.add_dates(first, last)

    # Includes days of week for filter
    db.include_days_of_week(include_all=True)

    # Filters dates by month first of 2024
    filtered_first_2024: RBTree = db.filter_dates(year=2024, day=1)

    # Dates to be checked against filtered tree
    filter1_true1: datetime.date = datetime.date(2024, 1, 1)
    filter1_true2: datetime.date = datetime.date(2024, 12, 1)
    filter1_false1: datetime.date = datetime.date(2025, 12, 1)
    filter1_false2: datetime.date = datetime.date(2023, 11, 1)
    filter1_false3: datetime.date = datetime.date(2024, 1, 5)

    assert len(filtered_first_2024) == 12
    assert db.find_date(filtered_first_2024, filter1_true1)
    assert db.find_date(filtered_first_2024, filter1_true2)
    assert db.find_date(filtered_first_2024, filter1_false1) is False
    assert db.find_date(filtered_first_2024, filter1_false2) is False
    assert db.find_date(filtered_first_2024, filter1_false3) is False

    # Filters dates by 31st 2025
    db.include_days_of_week(include_all=True)
    filtered_31st_2025: RBTree = db.filter_dates(year=2025, day=31)

    # Dates to be checked against filtered tree
    filter2_true1: datetime.date = datetime.date(2025, 12, 31)
    filter2_true2: datetime.date = datetime.date(2025, 1, 31)
    filter2_false1: datetime.date = datetime.date(2024, 5, 31)
    filter2_false2: datetime.date = datetime.date(2025, 4, 5)
    filter2_false3: datetime.date = datetime.date(2025, 11, 5)

    assert len(filtered_31st_2025) == 7
    assert db.find_date(filtered_31st_2025, filter2_true1)
    assert db.find_date(filtered_31st_2025, filter2_true2)
    assert db.find_date(filtered_31st_2025, filter2_false1) is False
    assert db.find_date(filtered_31st_2025, filter2_false2) is False
    assert db.find_date(filtered_31st_2025, filter2_false3) is False

def test_filter_by_month_day():
    """
    Tests filtering dates by month and day
    """
    # Sets up the date builder with a tree and date object
    db = builder()

    # Range of dates to be added
    first = datetime.date(2023, 12, 1)
    last = datetime.date(2026, 12, 1)

    # Includes days of week
    db.include_days_of_week(include_all=True)

    # Adds date range
    db.add_dates(first, last)

    # Includes days of week for filter
    db.include_days_of_week(include_all=True)

    # Filters dates by month first of december
    filtered_dec_1st: RBTree = db.filter_dates(month=12, day=1)

    # Dates to be checked against filtered tree
    filter1_true1: datetime.date = datetime.date(2024, 12, 1)
    filter1_true2: datetime.date = datetime.date(2025, 12, 1)
    filter1_false1: datetime.date = datetime.date(2025, 12, 5)
    filter1_false2: datetime.date = datetime.date(2023, 11, 1)
    filter1_false3: datetime.date = datetime.date(2024, 1, 5)

    assert len(filtered_dec_1st) == 4
    assert db.find_date(filtered_dec_1st, filter1_true1)
    assert db.find_date(filtered_dec_1st, filter1_true2)
    assert db.find_date(filtered_dec_1st, filter1_false1) is False
    assert db.find_date(filtered_dec_1st, filter1_false2) is False
    assert db.find_date(filtered_dec_1st, filter1_false3) is False

def test_filter_by_year_month_day():
    """
    Tests filtering dates by year, month,  and day
    """
    # Sets up the date builder with a tree and date object
    db = builder()

    # Range of dates to be added
    first = datetime.date(2023, 12, 1)
    last = datetime.date(2026, 12, 1)

    # Includes days of week
    db.include_days_of_week(include_all=True)

    # Adds date range
    db.add_dates(first, last)

    # Includes days of week for filter
    db.include_days_of_week(include_all=True)

    # Filters dates for 12/1/2025
    filtered_dec_1st_2025: RBTree = db.filter_dates(year=2025, month=12, day=1)

    # Dates to be checked against filtered tree
    filter1_true1: datetime.date = datetime.date(2025, 12, 1)
    filter1_false1: datetime.date = datetime.date(2025, 12, 5)
    filter1_false2: datetime.date = datetime.date(2023, 12, 1)
    filter1_false3: datetime.date = datetime.date(2025, 1, 1)

    assert len(filtered_dec_1st_2025) == 1
    assert db.find_date(filtered_dec_1st_2025, filter1_true1)
    assert db.find_date(filtered_dec_1st_2025, filter1_false1) is False
    assert db.find_date(filtered_dec_1st_2025, filter1_false2) is False
    assert db.find_date(filtered_dec_1st_2025, filter1_false3) is False

# ------------------------------ Tests finding dates -------------------------------
def test_find_true():
    """
    Tests that find_date correctly returns True
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds dates
    add_date_helper(db, 1)

    assert db.find_date(db.tree, datetime.date(2025, 1, 1))

def test_find_false():
    """
    Tests that find_date correctly returns False
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds dates
    add_date_helper(db, 1)

    assert db.find_date(db.tree, datetime.date(2025, 1, 2)) is False

def test_invalid_date_type():
    """
    Tests that find_date correctly raises ValueError when passed an invalid date type
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds dates
    add_date_helper(db, 1)

    with pytest.raises(ValueError):
        db.find_date(db.tree, 12/12/2025)

def test_invalid_date_type_str():
    """
    Tests that find_date correctly raises ValueError when passed an invalid date type of str
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Adds dates
    add_date_helper(db, 1)

    with pytest.raises(ValueError):
        db.find_date(db.tree, "12/12/2025")

# ------------------ Tests the include_days_of_week functionality ------------------

def test_include_all_days_of_week():
    """
    Tests to see if all the days of week have been added successfully
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Includes all dates
    db.include_days_of_week(include_all=True)

    # Retrieves the list of added days of week
    results: list[int] = db.included_days

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
    db: DateBuilder = builder()

    # Includes all dates
    db.include_days_of_week(exclude_all=True)

    # Retrieves the list of added days of week
    results: list[int] = db.included_days

    # Checks for 0 dow elements in list
    assert len(results) == 0

def test_days_of_week_both_include_exclude_true():
    """
    Tests to see if a ValueError exception is correctly raised when both include_all and exclude_all are marked True
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Includes all dates
    with pytest.raises(ValueError):
        db.include_days_of_week(include_all=True, exclude_all=True)

def test_days_of_week_both_include_all_and_day_true():
    """
    Tests to see if a ValueError exception is correctly raised when both include_all and a day of week are marked True
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Includes all dates
    with pytest.raises(ValueError):
        db.include_days_of_week(include_all=True, monday=True)

def test_days_of_week_both_exclude_all_and_day_true():
    """
    Tests to see if a ValueError exception is correctly raised when both exclude_all and a day of week are marked True
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Includes all dates
    with pytest.raises(ValueError):
        db.include_days_of_week(exclude_all=True, monday=True)

def test_add_remove_dow():
    """
    Tests including single days of the week
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    def remove_and_test():
        """
        Removes and tests that dows have been removed
        """
        db.include_days_of_week(exclude_all=True)
        result: int = len(db.included_days)

        # Checks for no days included
        assert result == 0

    # Includes days and checks it has been included then removes days and checks it has been removed
    # Include Monday (0)
    db.include_days_of_week(monday=True)
    result: int = db.included_days[0]

    assert result == 0

    # Remove Monday
    remove_and_test()

    # Include Tuesday (1)
    db.include_days_of_week(tuesday=True)
    result: int = db.included_days[0]

    assert result == 1

    # Remove Tuesday
    remove_and_test()

    # Include Wednesday (2)
    db.include_days_of_week(wednesday=True)
    result: int = db.included_days[0]

    assert result == 2

    # Remove Wednesday
    remove_and_test()

    # Include Thursday (3)
    db.include_days_of_week(thursday=True)
    result: int = db.included_days[0]

    assert result == 3

    # Remove Thursday
    remove_and_test()

    # Include Friday (4)
    db.include_days_of_week(friday=True)
    result: int = db.included_days[0]

    assert result == 4

    # Remove Friday
    remove_and_test()

    # Include Saturday (5)
    db.include_days_of_week(saturday=True)
    result: int = db.included_days[0]

    assert result == 5

    # Remove Saturday
    remove_and_test()

    # Include Sunday (6)
    db.include_days_of_week(sunday=True)
    result: int = db.included_days[0]

    assert result == 6

    # Remove Sunday
    remove_and_test()

def test_add_remove_multi_dow():
    """
    Tests including multiple days of the week and excluding them
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    def remove_and_test():
        """
        Removes and tests that dows have been removed
        """
        db.include_days_of_week(exclude_all=True)
        result: int = len(db.included_days)

        # Checks for no days included
        assert result == 0

    # Include Monday (0) and Tuesday (1)
    db.include_days_of_week(monday=True)
    db.include_days_of_week(tuesday=True)

    result_mon: int = db.included_days[0]
    assert result_mon == 0

    result_tue: int = db.included_days[1]
    assert result_tue == 1

    result_count: int = len(db.included_days)
    assert  result_count == 2

    remove_and_test()

def test_reset_after_add():
    """
    Tests that day of week tracker is reset after each add instance
    """
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()

    # Includes 3 days
    db.include_days_of_week(monday=True, wednesday=True, friday=True)

    # Determines date range
    first: datetime.date = datetime.date(2025, 1, 1)
    last: datetime.date = datetime.date(2025, 1, 31)

    # Checks that there are 3 days of week
    result = len(db.included_days)
    assert result == 3

    # Adds dates in range based on day of week
    db.add_dates(first, last)

    # Checks for reset
    result = len(db.included_days)
    assert result == 0

# --------------- Below tests the display_dates functionality ---------------

def test_display_dates_non_empty_tree():
    """
    Tests display date for a non-empty tree. This is a manual test where the dates 2025/01/01, 2025/01/02,
    2025/01/03, 2025/01/04, 2025/01/05 should appear in the terminal
    """
    # Sets up tree with added dates so display dates can be tested
    # Sets up the date builder with a tree and date object
    db: DateBuilder = builder()
    tree: RBTree = db.tree

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
    db: DateBuilder = builder()

    # Tries to display dates of an empty tree
    with pytest.raises(ValueError):
        db.display_dates(db.tree)

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