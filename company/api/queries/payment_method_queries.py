from typing import Iterable, Optional

from asgiref.sync import sync_to_async
from strawberry_django_plus import gql

from company.api.types.paymeny_method_type.payment_method_filter import PaymentMethodFilter
from company.api.types.paymeny_method_type.payment_method_type import PaymentMethodType
from company.models import PaymentMethod
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@gql.relay.connection
async def payment_method_connection(self, filter: Optional[PaymentMethodFilter] = None) -> Iterable[PaymentMethodType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    payment_methods = PaymentMethod.objects.filter(**filter_temp)
    await sync_to_async(len)(payment_methods)
    return payment_methods
