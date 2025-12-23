# tests/test_delete_dates.py
import datetime
import pytest
from unittest.mock import MagicMock, patch

from date_builder._delete_dates import DeleteDates
from date_builder.date_builder import DateBuilder


def test_delete_date_tree_success():

    mock_find = MagicMock()
    mock_tree = MagicMock()

    date_str = "2024-01-15"
    parsed_date = datetime.datetime(2024, 1, 15)

    mock_find.find_date.return_value = True

    with patch("DeleteDates.HelperMethods.str_to_date", return_value=parsed_date):
        deleter = DeleteDates(mock_find, mock_tree)

        # Act
        result = deleter.delete_date_tree(date_str)

        # Assert
        mock_find.find_date.assert_called_once_with(date_str)
        mock_tree.remove.assert_called_once_with(parsed_date)
        assert result == mock_tree


def test_delete_date_tree_date_not_found_raises():
    # Arrange
    mock_find = MagicMock()
    mock_tree = MagicMock()
    mock_find.find_date.return_value = False

    deleter = DeleteDates(mock_find, mock_tree)

    # Act / Assert
    with pytest.raises(ValueError, match="Date is not found"):
        deleter.delete_date_tree("2024-01-15")

    mock_tree.remove_items.assert_not_called()


def test_delete_date_tree_calls_str_to_date():
    # Arrange
    mock_find = MagicMock()
    mock_tree = MagicMock()
    mock_find.find_date.return_value = True

    with patch("DeleteDates.HelperMethods.str_to_date") as mock_str_to_date:
        mock_str_to_date.return_value = datetime.datetime(2024, 1, 15)

        deleter = DeleteDates(mock_find, mock_tree)

        # Act
        deleter.delete_date_tree("2024-01-15")

        # Assert
        mock_str_to_date.assert_called_once_with("2024-01-15")


def test_delete_date_tree_integration_real_tree():
    # Optional integration-ish test (uses a real RBTree)
    from bintrees import RBTree

    tree = RBTree()
    date = datetime.datetime(2024, 1, 15)
    tree.insert(date, "event")

    mock_find = MagicMock()
    mock_find.find_date.return_value = True

    with patch("DeleteDates.HelperMethods.str_to_date", return_value=date):
        deleter = DeleteDates(mock_find, tree)


        deleter.delete_date_tree("2024-01-15")

    assert date not in tree