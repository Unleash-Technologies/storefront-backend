from abc import ABC
from datetime import datetime
from typing import List

from strawberry_django_plus import gql

from inventory.models import Product, ModifyStockDocument


# TODO Find a way to test all the custom fields isolated from the query, just testing the class.
#     The problem I have is that in the custom field, the instance is passed as self, but i cannot find
#     a way to replicate this behavior when instantiating the type by itself outside of a query request.
@gql.django.type(Product)
class ProductType(gql.Node, ABC):
    id: gql.auto
    sku: gql.auto
    is_service: gql.auto
    is_active: gql.auto

    @gql.field
    def name(self: Product) -> str:
        return self.current_detail.name

    @gql.field
    def barcode(self: Product) -> str:
        return self.current_detail.barcode

    @gql.field
    def cost(self: Product) -> float:
        return self.current_detail.cost

    @gql.field
    def markup(self: Product) -> float:
        return self.current_detail.markup

    @gql.field
    def last_modified_date(self: Product) -> datetime:
        return self.current_detail.date

    @gql.field
    def current_stock(self: Product) -> float:
        stock_changes: List[ModifyStockDocument] = self.stock_changes.all()
        stock = 0
        for i in stock_changes:
            stock += i.quantity_modified
        return stock
