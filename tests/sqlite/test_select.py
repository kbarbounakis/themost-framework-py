import pytest
from themost_framework.sqlite import SqliteAdapter
from themost_framework.common import object
from themost_framework.query import DataColumn, QueryEntity, QueryExpression, select, TestUtils
from unittest import TestCase
import re

Products = QueryEntity('ProductData')
People = QueryEntity('PersonData')
Orders = QueryEntity('OrderData')
PostalAddresses = QueryEntity('PostalAddressData', 'address')
Customers = QueryEntity('PersonData', 'customer')
db = None

@pytest.fixture()
def db() -> SqliteAdapter:
    return SqliteAdapter(object(database='tests/db/local.db'))

def test_select_and_join(db):
    items = db.execute(QueryExpression(People).select(
        lambda x,address: (x.id, x.familyName, x.givenName, address.addressLocality)
    ).join(PostalAddresses).on(
        lambda x,address: x.address == address.id
        ))
    TestCase().assertGreater(len(items), 0)

def test_select_with_nested_filter(db):
    items = db.execute(QueryExpression().select(
        lambda x,customer,address: (x.orderedItem,
                customer.familyName,
                customer.givenName,
                address.addressLocality)
    ).from_collection(Orders).join(Customers).on(
        lambda x,customer: x.customer == customer.id
        ).join(PostalAddresses).on(
        lambda x,address: x.customer.address == address.id
        ).where(
            lambda x: x.orderStatus == 1
        )
        )
    TestCase().assertGreater(len(items), 0)