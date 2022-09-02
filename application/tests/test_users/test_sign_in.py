import unittest
from unittest import mock

from fastapi.exceptions import HTTPException

from application.main import users
from application.db import schemas


config = {"jwt_secret": "STRONG_SECRET", "token_duration_seconds": 86400}


@mock.patch("application.routers.users.logger", new=mock.Mock())
@mock.patch("application.routers.users.config", new=config)
class TestUsers(unittest.TestCase):
    def test_get_user_1(self):
        # wrong login token
        ex = users.jwt.exceptions.DecodeError
        token = "wrong_token"
        with mock.patch.object(users.jwt, "decode", side_effect=ex) as jwt_mocked:
            with self.assertRaises(HTTPException) as httpex:
                users.get_user(token=token)

        jwt_mocked.assert_called_once_with(
            token, config["jwt_secret"], algorithms=["HS256"]
        )
        users.logger.error.assert_called_once_with("wrong jwt token was given")

    def test_get_user_2(self):
        # token has expired
        token = "expired_token"
        with mock.patch.object(
            users.jwt, "decode", return_value={"user_id": 1, "expires_at": 1}
        ) as jwt_mocked:
            with self.assertRaises(HTTPException):
                users.get_user(token=token)

        jwt_mocked.assert_called_once_with(
            token, config["jwt_secret"], algorithms=["HS256"]
        )
        self.assertEqual(
            users.logger.error.call_args.args, ("expired jwt token was given",)
        )

    def test_get_user_3(self):
        # happy path
        token = "good_token"
        user_id = 1
        with mock.patch.object(
            users.jwt,
            "decode",
            return_value={"user_id": user_id, "expires_at": 100000000000},
        ) as jwt_mocked:
            res = users.get_user(token=token)

        jwt_mocked.assert_called_once_with(
            token, config["jwt_secret"], algorithms=["HS256"]
        )
        self.assertEqual(res, user_id)

    def test_login_1(self):
        # incorrect username or password
        user = schemas.UserCreate(username="username", password="password")
        with mock.patch.object(
            users.crud, "get_user_by_username", return_value=None
        ) as crud_mocked:
            with self.assertRaises(HTTPException) as httpex:
                users.login(user, None)

        crud_mocked.assert_called_once_with(None, user.username)
        self.assertEqual(users.logger.info.call_args.args, ("user did not exist",))

    def test_login_2(self):
        # wrong password
        class UserTest:
            def __init__(self, username, password):
                self.username = username
                self.hashed_password = password

        user = schemas.UserCreate(username="username", password="wrong_password")
        with mock.patch.object(
            users.crud,
            "get_user_by_username",
            return_value=UserTest(username="username", password="correct_password"),
        ) as crud_mocked:
            with self.assertRaises(HTTPException) as httpex:
                users.login(user, None)

        crud_mocked.assert_called_once_with(None, user.username)
        self.assertEqual(
            users.logger.info.call_args.args, ("user had entered a wrong password",)
        )

    def test_login_3(self):
        # happy path
        class UserInDB:
            "the user object that will be fetched from db. it will be used in mocking db"

            def __init__(self, username, hashed_password):
                self.username = username
                self.hashed_password = hashed_password
                self.id = 1

        class UserForm:
            "the user form that will be sent to the login api"

            def __init__(self, username, password):
                self.username = username
                self.password = password

        class HashedData:
            "used in mocking hashlib.sha256"

            def __init__(self, data):
                self.data = data

            def hexdigest(self):
                return self.data

        username = "username"
        password = "correct_password"
        hashed_password = "salthashed_password"
        user_db = UserInDB(username=username, hashed_password=hashed_password)
        user_form = UserForm(username=username, password=password)
        with mock.patch.object(
            users.crud,
            "get_user_by_username",
            return_value=user_db,
        ) as crud_mocked:
            with mock.patch.object(
                users, "sha256", return_value=HashedData(hashed_password[4:])
            ):
                with mock.patch.object(users.jwt, "encode", return_value="token"):
                    res = users.login(user_form, None)

        crud_mocked.assert_called_once_with(None, user_form.username)
        self.assertTrue("access_token" in res)
