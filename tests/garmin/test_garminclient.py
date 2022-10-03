import unittest
from unittest.mock import mock_open, patch

import requests
from pytest_httpserver import HTTPServer

from garminworkouts.garmin.garminclient import GarminClient


class GarminClientTestCase(unittest.TestCase):
    _ANY_WORKOUT = [{"foo1": "bar1"}]

    def setUp(self):
        self.httpserver = HTTPServer()
        self.httpserver.start()
        self.addCleanup(self.httpserver.stop)

        # simulate authenticated user
        self.httpserver \
            .expect_request("/modern/settings") \
            .respond_with_data()

        url = f"http://{self.httpserver.host}:{self.httpserver.port}"
        self.client = GarminClient(
            connect_url=url,
            sso_url=url,
            username="any username",
            password="any password",
            cookie_jar=None  # don't store session cookies in a jar
        )

    def test_list_workouts(self):
        batch_size = 10
        any_workouts = [{"foo1": "bar1"}, {"foo2": "bar2"}]
        empty_response = []

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"
        params1 = {"start": str(0), "limit": str(batch_size)}
        params2 = {"start": str(batch_size), "limit": str(batch_size)}

        self.httpserver.expect_request(url, query_string=params1).respond_with_json(any_workouts)
        self.httpserver.expect_request(url, query_string=params2).respond_with_json(empty_response)

        with self.client as connection:
            workouts = connection.list_workouts(batch_size)
            self.assertEqual(list(workouts), any_workouts)

    def test_list_workouts_error_handling(self):
        batch_size = 10

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workouts"
        params = {"start": str(0), "limit": str(batch_size)}

        self.httpserver.expect_request(url, query_string=params).respond_with_data(status=500)

        with self.client as connection:
            with self.assertRaises(requests.exceptions.HTTPError):
                # list_workouts returns generator, evaluate it using next()
                next(connection.list_workouts(batch_size))

    def test_get_workout(self):
        workout_id = 1

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.httpserver.expect_request(url).respond_with_json(GarminClientTestCase._ANY_WORKOUT)

        with self.client as connection:
            workout = connection.get_workout(workout_id)
            self.assertEqual(workout, GarminClientTestCase._ANY_WORKOUT)

    def test_get_workout_error_handling(self):
        workout_id = 1

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.httpserver.expect_request(url).respond_with_data(status=500)

        with self.client as connection:
            self.assertRaises(requests.exceptions.HTTPError, connection.get_workout, workout_id)

    def test_download_workout(self):
        workout_id = 1
        file = "workout.fit"
        content = "any content"

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/FIT/{workout_id}"
        self.httpserver.expect_request(url).respond_with_data(content)

        with self.client as connection:
            with patch('builtins.open', mock_open()) as mocked_file:
                connection.download_workout(workout_id, file)

                mocked_file.assert_called_once_with(file, 'wb')
                mocked_file().write.assert_called_once_with(content.encode())

    def test_download_workout_error_handling(self):
        workout_id = 1
        file = "workout.fit"

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/FIT/{workout_id}"
        self.httpserver.expect_request(url).respond_with_data(status=500)

        with self.client as connection:
            self.assertRaises(requests.exceptions.HTTPError, connection.download_workout, workout_id, file)

    def test_save_workout(self):
        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout"
        self.httpserver \
            .expect_request(url, method="POST", json=GarminClientTestCase._ANY_WORKOUT) \
            .respond_with_data()

        with self.client as connection:
            connection.save_workout(GarminClientTestCase._ANY_WORKOUT)

    def test_save_workout_error_handling(self):
        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout"
        self.httpserver \
            .expect_request(url, method="POST", json=GarminClientTestCase._ANY_WORKOUT) \
            .respond_with_data(status=500)

        with self.client as connection:
            self.assertRaises(requests.exceptions.HTTPError, connection.save_workout, GarminClientTestCase._ANY_WORKOUT)

    def test_update_workout(self):
        workout_id = 1

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.httpserver \
            .expect_request(url, method="PUT", json=GarminClientTestCase._ANY_WORKOUT) \
            .respond_with_data()

        with self.client as connection:
            connection.update_workout(workout_id, GarminClientTestCase._ANY_WORKOUT)

    def test_update_workout_error_handling(self):
        workout_id = 1

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.httpserver \
            .expect_request(url, method="PUT", json=GarminClientTestCase._ANY_WORKOUT) \
            .respond_with_data(status=500)

        with self.client as connection:
            self.assertRaises(requests.exceptions.HTTPError, connection.update_workout, workout_id,
                              GarminClientTestCase._ANY_WORKOUT)

    def test_delete_workout(self):
        workout_id = 1

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.httpserver \
            .expect_request(url, method="DELETE") \
            .respond_with_data()

        with self.client as connection:
            connection.delete_workout(workout_id)

    def test_delete_workout_error_handling(self):
        workout_id = 1

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}"
        self.httpserver \
            .expect_request(url, method="DELETE") \
            .respond_with_data(status=500)

        with self.client as connection:
            self.assertRaises(requests.exceptions.HTTPError, connection.delete_workout, workout_id)

    def test_schedule_workout(self):
        workout_id = 1
        date = "any date"

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        self.httpserver \
            .expect_request(url, method="POST", json={"date": date}) \
            .respond_with_data()

        with self.client as connection:
            connection.schedule_workout(workout_id, date)

    def test_schedule_workout_error_handling(self):
        workout_id = 1
        date = "any date"

        url = f"{GarminClient._WORKOUT_SERVICE_ENDPOINT}/schedule/{workout_id}"
        self.httpserver \
            .expect_request(url, method="POST", json={"date": date}) \
            .respond_with_data(status=500)

        with self.client as connection:
            self.assertRaises(requests.exceptions.HTTPError, connection.schedule_workout, workout_id, date)


if __name__ == '__main__':
    unittest.main()
