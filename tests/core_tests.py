import datetime
import datetime as dt
from typing import Any

import date_builder
import pytest
from bintrees import RBTree

# import date_builder
from date_builder import DateBuilder
from date_builder._days_of_week import DaysOfWeek


# --- Dummies / helpers for tests -------------------------------------------------


class DummyDaysOfWeek:
    """Minimal stand-in for DaysOfWeek so no need to depend on real implementation."""
    def __init__(self):
        self._included = set()
        self.included_calls = []

    def get_included(self):
        return self._included

    def included_days(
        self,
        monday,
        tuesday,
        wednesday,
        thursday,
        friday,
        saturday,
        sunday,
        include_all,
        exclude_all,
    ):
        # Record the call so tests can assert it was invoked correctly
        self.included_calls.append(
            dict(
                monday=monday,
                tuesday=tuesday,
                wednesday=wednesday,
                thursday=thursday,
                friday=friday,
                saturday=saturday,
                sunday=sunday,
                include_all=include_all,
                exclude_all=exclude_all,
            )
        )
        # Return the internal set just to have a deterministic value
        return self._included


@pytest.fixture
def empty_builder() -> DateBuilder:
    """Provide a fresh DateBuilder with an empty RBTree and dummy DaysOfWeek."""
    tree = RBTree()
    dow: DaysOfWeek = DummyDaysOfWeek()
    builder = DateBuilder(tree=tree, date_obj="DEFAULT_VALUE", days_of_week=dow)
    return builder


# Testing Over Basic Behavior


def test_get_count(empty_builder: date_builder):
    builder = empty_builder
    assert builder.get_count == 0

    # Directly modify the underlying tree to verify the property tracks it
    today = dt.date(2025, 1, 1)
    builder.tree[today] = "X"
    assert builder.get_count == 1

    another = dt.date(2025, 1, 2)
    builder.tree[another] = "Y"
    assert builder.get_count == 2


# --- add_date_tree wiring to AddDates -------------------------------------------


def test_add_date_correct_arguments(monkeypatch: monkeypatch, empty_builder: date_builder):
    builder = empty_builder
    called: dict[Any, Any] = {}

    class FakeAddDates:
        last_instance = None

        def __init__(self, date_obj, tree, days_of_week):
            FakeAddDates.last_instance = self
            called["init"] = (date_obj, tree, days_of_week)

        @staticmethod
        def add_date(first_date, last_date, unique_obj):
            called["add_date"] = (first_date, last_date, unique_obj)
            return "SENTINEL_TREE"

    monkeypatch.setattr(date_builder, "AddDates", FakeAddDates)

    d1 = dt.date(2025, 1, 1)
    d2 = dt.date(2025, 1, 5)

    result = builder.add_date_tree(d1, d2, unique_obj="UNIQUE")

    # Return value is the helper's return value
    assert result == "SENTINEL_TREE"

    # Constructor was called correctly
    assert called["init"][0] == builder.date_obj
    assert called["init"][1] is builder.tree
    assert called["init"][2] is builder.days_of_week

    # Method was called with the same arguments we passed
    assert called["add_date"] == (d1, d2, "UNIQUE")


# --- find_date uses FindDate.find_date_exist ------------------------------------


def test_find_date(monkeypatch: monkeypatch, empty_builder: DateBuilder):
    builder = empty_builder
    called = {}

    class FakeFindDate:
        @staticmethod
        def find_date_exist(tree: RBTree, date: datetime.date):
            called["args"] = (tree, date)
            return True

    monkeypatch.setattr(builder, "FindDate", FakeFindDate)

    # Rebuild builder so its .find field uses FakeFindDate
    tree = RBTree()
    dow = DummyDaysOfWeek()
    builder = DateBuilder(tree=tree, date_obj="DEFAULT", days_of_week=dow)

    target = dt.date(2025, 1, 3)
    result = builder.find_date(target)

    assert result is True
    assert called["args"][0] is tree
    assert called["args"][1] == target


# --- delete_date wiring to DeleteDates.delete_date -------------------------------


def test_delete_date_calls_deletedates(monkeypatch, empty_builder):
    builder = empty_builder
    called = {}

    class FakeDeleteDates:
        last_instance = None

        def __init__(self, tree, days_of_week):
            FakeDeleteDates.last_instance = self
            called["init"] = (tree, days_of_week)

        def delete_date(self, date):
            called["delete_date"] = date
            return "TREE_WITH_DELETION"

    monkeypatch.setattr(date_builder, "DeleteDates", FakeDeleteDates)

    date_to_delete = dt.date(2025, 1, 10)
    result = builder.delete_date(date_to_delete)

    assert result == "TREE_WITH_DELETION"
    assert called["init"][0] is builder.tree
    assert called["init"][1] is builder.days_of_week
    assert called["delete_date"] == date_to_delete


# --- delete_date_range wiring ---------------------------------------------------


def test_delete_date_range_calls_deletedates_range(monkeypatch, empty_builder):
    builder = empty_builder
    called = {}

    class FakeDeleteDates:
        def __init__(self, tree, days_of_week):
            called["init"] = (tree, days_of_week)

        def delete_date_range(self, upper, lower):
            called["range"] = (upper, lower)
            return "RANGE_TREE"

    monkeypatch.setattr(date_builder, "DeleteDates", FakeDeleteDates)

    lower = dt.date(2025, 1, 1)
    upper = dt.date(2025, 1, 31)

    result = builder.delete_date_range(lower_date=lower, upper_date=upper)

    assert result == "RANGE_TREE"
    # Note: DateBuilder uses (upper_date, lower_date) order in the call
    assert called["range"] == (upper, lower)
    assert called["init"][0] is builder.tree
    assert called["init"][1] is builder.days_of_week


# --- filter_dates wiring to FilteredDates.get_filtered_dates ---------------------


def test_filter_dates_calls_filtered_dates(monkeypatch, empty_builder):
    builder = empty_builder
    called = {}

    class FakeFilteredDates:
        def __init__(self, tree, days_of_week):
            called["init"] = (tree, days_of_week)

        def get_filtered_dates(self, day, month, year):
            called["get_filtered_dates"] = (day, month, year)
            return "FILTERED_TREE"

    monkeypatch.setattr(date_builder, "FilteredDates", FakeFilteredDates)

    result = builder.filter_dates(day=1, month=2, year=2025)

    assert result == "FILTERED_TREE"
    assert called["init"][0] is builder.tree
    assert called["init"][1] is builder.days_of_week
    assert called["get_filtered_dates"] == (1, 2, 2025)


# --- filtered_date_range wiring to FilteredDates.get_filtered_date_range ---------


def test_filtered_date_range_calls_filtered_date_range(monkeypatch, empty_builder):
    builder = empty_builder
    called = {}

    class FakeFilteredDates:
        def __init__(self, tree, days_of_week):
            called["init"] = (tree, days_of_week)

        def get_filtered_date_range(self, days, months, years):
            called["get_filtered_date_range"] = (days, months, years)
            return "FILTERED_RANGE_TREE"

    monkeypatch.setattr(date_builder, "FilteredDates", FakeFilteredDates)

    result = builder.filtered_date_range(days=[1, 2], months=[1], years=[2025])

    assert result == "FILTERED_RANGE_TREE"
    assert called["init"][0] is builder.tree
    assert called["init"][1] is builder.days_of_week
    assert called["get_filtered_date_range"] == ([1, 2], [1], [2025])


# --- include_days_of_week staticmethod ------------------------------------------


def test_include_days_of_week_uses_days_of_week_class(monkeypatch):
    called = {}

    class FakeDaysOfWeek:
        def included_days(
            self,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
            include_all,
            exclude_all,
        ):
            called["args"] = dict(
                monday=monday,
                tuesday=tuesday,
                wednesday=wednesday,
                thursday=thursday,
                friday=friday,
                saturday=saturday,
                sunday=sunday,
                include_all=include_all,
                exclude_all=exclude_all,
            )
            return "INCLUDED_RESULT"

    monkeypatch.setattr(date_builder, "DaysOfWeek", FakeDaysOfWeek)

    result = DateBuilder.include_days_of_week(
        monday=True,
        wednesday=True,
        friday=True,
        include_all=False,
        exclude_all=False,
    )

    assert result == "INCLUDED_RESULT"
    assert called["args"]["monday"] is True
    assert called["args"]["wednesday"] is True
    assert called["args"]["friday"] is True
    # The others should default to False
    assert called["args"]["tuesday"] is False
    assert called["args"]["thursday"] is False
    assert called["args"]["saturday"] is False
    assert called["args"]["sunday"] is False


# --- display_dates staticmethod --------------------------------------------------


def test_display_dates_calls_showdates(monkeypatch):
    called = {}

    class FakeShowDates:
        @staticmethod
        def show_dates(tree):
            called["tree"] = tree

    monkeypatch.setattr(date_builder, "ShowDates", FakeShowDates)

    tree = RBTree()
    tree[dt.date(2025, 1, 1)] = "X"

    DateBuilder.display_dates(tree)

    assert called["tree"] is tree


# --- str_to_date staticmethod ----------------------------------------------------


def test_str_to_date(monkeypatch):
    called = {}

    class FakeHelperMethods:
        @staticmethod
        def str_to_date(date_str: str):
            called["arg"] = date_str
            # Return a sentinel date so we know this was used
            return dt.date(1999, 12, 31)

    monkeypatch.setattr(date_builder, "HelperMethods", FakeHelperMethods)

    result = DateBuilder.str_to_date("01/01/2025")
    assert result == dt.date(1999, 12, 31)
    assert called["arg"] == "01/01/2025"