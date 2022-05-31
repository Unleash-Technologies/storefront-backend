from typing import List, Optional

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ItemCreateInput, CreateItemPayload
from inventory.api.types.item.inputs.item_activate_input import ItemActivateInput
from inventory.api.types.item.inputs.item_deactivate_input import ItemDeactivateInput
from inventory.api.types.item.payload_types import DeactivateItemPayload, ActivateItemPayload
from inventory.models import Item, ItemDetail
from storefront_backend.api.types import UserError


@gql.type
class Mutation:

    @gql.field
    async def item_create(self, input: ItemCreateInput) -> CreateItemPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        item: Optional[Item] = None
        if not errors:
            item = await sync_to_async(Item.objects.create)(
                is_service=input.is_service
            )
            await sync_to_async(ItemDetail.objects.create)(
                name=input.name,
                sku=input.sku,
                barcode=input.barcode,
                cost=input.cost,
                markup=input.markup,
                root_item=item,

            )
        return CreateItemPayload(item=item, user_errors=errors)

    @gql.field
    async def item_deactivate(self, input: ItemDeactivateInput) -> DeactivateItemPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        item: Optional[Item] = None
        if not errors:
            item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
            item.is_active = False
            await sync_to_async(item.save)()
        return DeactivateItemPayload(deactivated_item=item, user_errors=errors)

    @gql.field
    async def item_activate(self, input: ItemActivateInput) -> ActivateItemPayload:
        errors: List[UserError] = await input.validate_and_get_errors()
        item: Optional[Item] = None
        if not errors:
            item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
            item.is_active = True
            await sync_to_async(item.save)()
        return ActivateItemPayload(activated_item=item, user_errors=errors)
