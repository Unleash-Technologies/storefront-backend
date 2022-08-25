from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item import ItemType
from inventory.api.types.item.inputs import ItemCreateInput, ItemDeactivateInput, ItemActivateInput, \
    ItemUpdateInput, \
    ItemDeleteInput
from inventory.api.types.item.payload_types import ItemActivatePayload, ItemDeactivatePayload, ItemCreatePayload, \
    ItemUpdatePayload, ItemDeletePayload
from inventory.api.types.item_group.inputs.item_group_create_input import ItemGroupCreateInput
from inventory.api.types.item_group.item_group_type import ItemGroupType
from inventory.api.types.item_group.payload_types import ItemGroupCreatePayload
from inventory.models import Item, ItemDetail
from inventory.models import ItemGroup
from storefront_backend.api.utils import gql_mutation_payload


@gql.type
class Mutation:

    @gql_mutation_payload(
        input_type=ItemCreateInput,
        payload_type=ItemCreatePayload,
        returned_type=ItemType
    )
    async def item_create(self, input) -> ItemType:
        item = await sync_to_async(Item.objects.create)(
            is_service=input.is_service,
            sku=input.sku,
        )
        await sync_to_async(ItemDetail.objects.create)(
            name=input.name,
            barcode=input.barcode,
            cost=input.cost,
            markup=input.markup,
            root_item=item,

        )
        return item

    @gql_mutation_payload(
        input_type=ItemDeactivateInput,
        payload_type=ItemDeactivatePayload,
        returned_type=ItemType
    )
    async def item_deactivate(self, input) -> ItemType:
        item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
        item.is_active = False
        await sync_to_async(item.save)()
        return item

    @gql_mutation_payload(
        input_type=ItemActivateInput,
        payload_type=ItemActivatePayload,
        returned_type=ItemType
    )
    async def item_activate(self, input) -> ItemType:
        item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
        item.is_active = True
        await sync_to_async(item.save)()
        return item

    @gql_mutation_payload(
        input_type=ItemUpdateInput,
        payload_type=ItemUpdatePayload,
        returned_type=ItemType
    )
    async def item_update(self, input) -> ItemType:
        item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
        if input.sku:
            item.sku = input.sku
            item.save(update_fields=['sku'])

        current_item_detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(id=item.current_detail_id)
        current_item_detail_data = current_item_detail.__dict__
        # _state is not a field in the ItemDetail model
        current_item_detail_data.pop("_state")

        # Cleaning input data from None Fields
        input_data = {k: v for k, v in input.data.__dict__.items() if v}

        if input_data:
            new_detail_data = {
                **current_item_detail_data,
                "id": None,
                "date": None,
                **input_data,
            }
            detail = await sync_to_async(ItemDetail.objects.create)(**new_detail_data)
            # this is needed because the signal is not fast enough
            item.current_detail = detail

        return item

    @gql_mutation_payload(
        input_type=ItemDeleteInput,
        payload_type=ItemDeletePayload,
        returned_type=ItemType
    )
    async def item_delete(self, input) -> gql.Node:
        item: Item = await sync_to_async(Item.objects.get)(id=input.id.node_id)
        await sync_to_async(item.delete)()
        return item

    @gql_mutation_payload(
        input_type=ItemGroupCreateInput,
        payload_type=ItemGroupCreatePayload,
        returned_type=ItemGroupType
    )
    async def item_group_create(self, input: ItemGroupCreateInput) -> ItemGroupType:

        parent_node_id = None
        if parent_global_id := input.parent_id:
            parent_node_id = parent_global_id.node_id

        item_group: ItemGroupType = await sync_to_async(ItemGroup.objects.create)(
            name=input.name,
            group_parent_id=parent_node_id
        )
        
        return item_group