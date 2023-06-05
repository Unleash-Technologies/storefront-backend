from abc import ABC
from datetime import datetime
from typing import List, Optional

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from inventory.api.types.item_category_type.item_category_type import ItemCategoryType
from inventory.models import Item


@gql.django.type(Item)
class ItemType(gql.Node, ABC):
    name: str
    cost: float
    markup: float
    price_c: float
    creation_date: datetime
    is_service: bool
    category: Optional[ItemCategoryType]

    @gql.field
    async def barcodes(self: Item) -> List[str]:
        bars = self.barcodes.all()
        await sync_to_async(len)(bars)
        return [bar.barcode for bar in bars]
