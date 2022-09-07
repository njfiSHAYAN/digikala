import unittest
from unittest import mock
# delete

from fastapi.exceptions import HTTPException

from application.main import users


config = {"jwt_secret": "STRONG_SECRET", "token_duration_seconds": 86400}


@mock.patch("application.routers.users.logger", new=mock.Mock())
@mock.patch("application.routers.users.config", new=config)
class TestUsers(unittest.TestCase):
    def test_login_1(self):
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

    def test_login_2(self):
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
