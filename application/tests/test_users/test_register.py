import unittest
from unittest import mock

from fastapi.exceptions import HTTPException

from application.main import users
from application.db import schemas


@mock.patch("application.routers.users.logger", new=mock.Mock())
class TestUsers(unittest.TestCase):
    def test_register_1(self):
        # user already exists
        user = schemas.UserCreate(username="username", password="pass")
        with mock.patch.object(
            users.crud, "get_user_by_username", return_value={"username": "username"}
        ) as crud_mocked:
            with self.assertRaises(HTTPException) as httpex:
                users.create_user(user=user, db=None)

        crud_mocked.assert_called_once_with(None, username="username")
        self.assertEqual(httpex.exception.detail, "username already registered")

    def test_register_2(self):
        # register happy path
        user = schemas.UserCreate(username="username", password="pass")
        with mock.patch.object(
            users.crud, "get_user_by_username", return_value=None
        ) as crud_mocked_get:
            with mock.patch.object(users.crud, "create_user") as crud_mocked_create:
                users.create_user(user=user, db=None)

        crud_mocked_get.assert_called_once_with(None, username="username")
        crud_mocked_create.assert_called_once_with(db=None, user=user)
