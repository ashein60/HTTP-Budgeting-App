import pytest

from backend.category_groups.category_group import CategoryGroup
from backend.message_catalog import MessageCatalog

FILE_PATH = "backend/tests_unit/message_catalog/data/messages.json"


def test_get_fail():
    messageCatalog = MessageCatalog(FILE_PATH)

    with pytest.raises(KeyError):
        messageCatalog.get("FOO")


def test_get_no_kwargs():
    messageCatalog = MessageCatalog(FILE_PATH)
    message = messageCatalog.get("IMPORT_FAIL")

    assert message == {"success": False, "code": 400, "message": "Invalid Import file"}


def test_get_with_kwargs():
    messageCatalog = MessageCatalog(FILE_PATH)
    message = messageCatalog.get("IMPORT_SUCCESS", items="Transactions")

    assert message == {
        "success": True,
        "code": 201,
        "message": "'Transactions' were imported successfully",
    }


def test_get_with_data():
    categoryGroups = [CategoryGroup("Income")]

    messageCatalog = MessageCatalog(FILE_PATH)
    message = messageCatalog.get("GET_SUCCESS", categoryGroups, items="Transactions")

    assert message.get("data") == [{"name": "Income"}]
