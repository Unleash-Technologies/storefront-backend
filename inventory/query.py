from strawberry_django_plus import gql

from inventory.queries.item_category_queries import items_category_connection
from inventory.queries.item_queries import items_connection
from inventory.queries.stock_recount_document_queries import stock_recount_document_connection
from inventory.queries.warehouse_queries import warehouse_connection


@gql.type
class Query:
    items_connection = items_connection
    items_category_connection = items_category_connection

    warehouse_connection = warehouse_connection
    stock_recount_document_connection = stock_recount_document_connection
