from typing import List, TypedDict, cast

from asgiref.sync import sync_to_async
from django.contrib.auth.models import Permission
from django.test import TestCase
from strawberry import ID
from strawberry_django.utils import is_strawberry_type

from storefront_backend.api.relay.connection import Connection
from storefront_backend.api.relay.node import Node
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list
from users.api.types.permission_type import PermissionType
from users.api.types.role_type import RoleType
from users.api.types.user_type import UserType
from users.models import Role, User


class RoleTypeDefaultValues(TypedDict):
    id: ID
    name: str


class TestRoleType(TestCase):
    def setUp(self) -> None:
        self.default_values: RoleTypeDefaultValues = {
            "id": cast(ID, "1"),
            "name": "Role1",
        }

    async def test_is_gql_type(self) -> None:
        self.assertTrue(is_strawberry_type(RoleType))

    async def test_is_node(self) -> None:
        self.assertTrue(issubclass(RoleType, Node))

    async def test_name(self) -> None:
        user_type_name = RoleType(**self.default_values).name
        expected: str = self.default_values["name"]
        self.assertEqual(user_type_name, expected)

    async def test_permissions(self) -> None:
        role: Role = cast(Role, await Role.objects.acreate(name="Role1"))
        permissions: List[Permission] = await get_lazy_query_set_as_list(Permission.objects.filter()[:2])
        await sync_to_async(role.permissions.add)(*permissions)

        role_type = await RoleType.from_model_instance(role)

        role_type_permission: Connection[PermissionType] = await role_type.permissions()

        # Test of total count is correct
        self.assertEqual(role_type_permission.page_info.total_count, 2)
        self.assertEqual(role_type_permission.total_count, 2)

        # Test if all the edged are returned
        self.assertEqual(role_type_permission.page_info.edges_count, 2)
        self.assertEqual(len(role_type_permission.edges), 2)

        # Test if the returned permissions are correct
        ids_of_perm_in_type = [RoleType.decode_id(i.node.id)["instance_id"] for i in role_type_permission.edges]
        for perm in permissions:
            self.assertIn(str(perm.id), ids_of_perm_in_type)

    async def test_users(self) -> None:
        create_user_func = sync_to_async(User.objects.create_user)
        users = [await create_user_func(username=f"user{i}", password=f"{i}") for i in range(5)]

        role: Role = cast(Role, await Role.objects.acreate(name="Role1"))
        await sync_to_async(role.user_set.add)(*users[:4])

        role_type = await RoleType.from_model_instance(role)
        role_type_users_con: Connection[UserType] = await role_type.users()

        # Test of total count is correct
        self.assertEqual(role_type_users_con.page_info.total_count, 4)
        self.assertEqual(role_type_users_con.total_count, 4)

        # Test if all the edged are returned
        self.assertEqual(role_type_users_con.page_info.edges_count, 4)
        self.assertEqual(len(role_type_users_con.edges), 4)

        # Test if the returned permissions are correct
        ids_of_user_in_type = [UserType.decode_id(i.node.id)["instance_id"] for i in role_type_users_con.edges]
        for user in users[:4]:
            self.assertIn(str(user.id), ids_of_user_in_type)

    async def test_from_model_instance(self) -> None:
        role: Role = cast(Role, await Role.objects.acreate(name="Role156"))
        permissions: List[Permission] = await get_lazy_query_set_as_list(Permission.objects.filter()[:2])
        await sync_to_async(role.permissions.add)(*permissions)

        role_type = await RoleType.from_model_instance(role)

        # Test fields
        self.assertIsNotNone(role_type.id)
        self.assertEqual(role_type.name, role.name)

        # Test permission connection
        permission_connection: Connection[PermissionType] = await role_type.permissions()
        self.assertIsNotNone(permission_connection)
        self.assertGreater(len(permission_connection.edges), 0)
        self.assertGreater(permission_connection.total_count, 0)

        self.assertIsNotNone(permission_connection.page_info.total_count)
        if permission_connection.page_info.total_count:
            self.assertGreater(permission_connection.page_info.total_count, 0)
