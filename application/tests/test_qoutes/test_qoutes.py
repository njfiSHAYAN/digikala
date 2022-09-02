import unittest
from unittest import mock

from fastapi.exceptions import HTTPException

from application.main import qoutes
from application.db import schemas


config = {"jwt_secret": "STRONG_SECRET", "token_duration_seconds": 86400}


@mock.patch("application.routers.qoutes.logger", new=mock.Mock())
class TestUsers(unittest.TestCase):
    def test_add_qoute(self):
        user = {"user_id": 10}
        qoute = schemas.QouteCreate(qoute="q", author="a", number=5, blockqoute="b")
        with mock.patch.object(qoutes, "crud") as crud_mocked:
            qoutes.add_qoute(None, user, qoute)

        crud_mocked.create_access_log.assert_called_once_with(None, user)
        crud_mocked.create_qoute.assert_called_once_with(None, qoute=qoute)

    def test_get_qoute(self):
        user = {"user_id": 10}
        qoute = schemas.QouteCreate(qoute="q", author="a", number=5, blockqoute="b")
        with mock.patch.object(qoutes, "crud") as crud_mocked:
            with mock.patch.object(qoutes.redis, "incr") as redis_mocked:
                qoutes.get_qoute(None, user)

        crud_mocked.create_access_log.assert_called_once_with(None, user)
        crud_mocked.get_some_qoutes.assert_called_once_with(None)
        args = redis_mocked.call_args_list
        self.assertEqual(args[0].args, ("counter",))
        self.assertEqual(args[1].args, (str(user) + ":counter",))
