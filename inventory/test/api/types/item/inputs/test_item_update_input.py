from typing import List

from asgiref.sync import async_to_sync
from django.test import TestCase

from inventory.api.types.item import ItemNotExistError, ItemIsNotActiveError
from inventory.api.types.item.inputs import ItemUpdateInput
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.types import UserError


class ItemUpdateInputTest(TestCase):
    def setUp(self):
        items = async_to_sync(create_bulk_of_item)(1)
        self.item = items[0]

        inactive_items = async_to_sync(create_bulk_of_item)(1, active=False, seed="not")
        self.inactive_item = inactive_items[0]

    async def test_validate_and_get_errors(self):
        # Test not existing id
        not_existing_item_type = ItemUpdateInput(id=Node.encode_id(type_name='ItemType', node_id='3549'), data={})
        expected_not_exist_error: List[UserError] = await not_existing_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], ItemNotExistError)

        # Test already inactivate item
        inactive_item_type = ItemUpdateInput(
            id=Node.encode_id(type_name='ItemType', node_id=f"{self.inactive_item.id}"), data={})
        expected_is_not_active_error: List[UserError] = await inactive_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_is_not_active_error[0], ItemIsNotActiveError)

        # Test no errors
        item_type = ItemUpdateInput(id=Node.encode_id(type_name='ItemType', node_id=f"{self.item.id}"), data={})
        expected_no_error: List[UserError] = await item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
