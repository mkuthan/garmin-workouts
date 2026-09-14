import unittest
from unittest.mock import Mock, call, mock_open, patch

import requests

from garminworkouts.garmin.garminclient import GarminClient


class GarminClientTestCase(unittest.TestCase):
    _ANY_WORKOUT = [{"foo1": "bar1"}]

    def setUp(self):
        self.connect_url = "https://connect.garmin.com"
        self.session_file = "/tmp/garmin-session"
        self.client = GarminClient(
            connect_url=self.connect_url,
            sso_url="https://sso.garmin.com",
            username="any username",
            password="any password",
            cookie_jar=self.session_file,
        )
        self.api = Mock()
        self.http = Mock()
        self.api.garth = self.http

    def _enter_connection(self, connect_mock):
        connect_mock.return_value = self.api
        return self.client.__enter__()

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_list_workouts(self, connect_mock):
        batch_size = 10
        any_workouts = [{"foo1": "bar1"}, {"foo2": "bar2"}]
        self.api.get_workouts.side_effect = [any_workouts, []]

        connection = self._enter_connection(connect_mock)
        workouts = connection.list_workouts(batch_size)

        self.assertEqual(list(workouts), any_workouts)
        self.api.get_workouts.assert_has_calls([call(0, batch_size), call(batch_size, batch_size)])

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_list_workouts_error_handling(self, connect_mock):
        batch_size = 10
        self.api.get_workouts.side_effect = requests.exceptions.HTTPError

        connection = self._enter_connection(connect_mock)
        with self.assertRaises(requests.exceptions.HTTPError):
            # list_workouts returns generator, evaluate it using next()
            next(connection.list_workouts(batch_size))

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_get_workout(self, connect_mock):
        workout_id = 1
        self.api.get_workout_by_id.return_value = GarminClientTestCase._ANY_WORKOUT

        connection = self._enter_connection(connect_mock)
        workout = connection.get_workout(workout_id)
        self.assertEqual(workout, GarminClientTestCase._ANY_WORKOUT)
        self.api.get_workout_by_id.assert_called_once_with(workout_id)

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_get_workout_error_handling(self, connect_mock):
        workout_id = 1
        self.api.get_workout_by_id.side_effect = requests.exceptions.HTTPError

        connection = self._enter_connection(connect_mock)
        self.assertRaises(requests.exceptions.HTTPError, connection.get_workout, workout_id)

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_download_workout(self, connect_mock):
        workout_id = 1
        file = "workout.fit"
        content = b"any content"
        self.api.download_workout.return_value = content

        connection = self._enter_connection(connect_mock)
        with patch("builtins.open", mock_open()) as mocked_file:
            connection.download_workout(workout_id, file)

            mocked_file.assert_called_once_with(file, "wb")
            mocked_file().write.assert_called_once_with(content)
        self.api.download_workout.assert_called_once_with(workout_id)

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_download_workout_error_handling(self, connect_mock):
        workout_id = 1
        file = "workout.fit"
        self.api.download_workout.side_effect = requests.exceptions.HTTPError

        connection = self._enter_connection(connect_mock)
        self.assertRaises(requests.exceptions.HTTPError, connection.download_workout, workout_id, file)

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_save_workout(self, connect_mock):
        connection = self._enter_connection(connect_mock)
        connection.save_workout(GarminClientTestCase._ANY_WORKOUT)
        self.api.upload_workout.assert_called_once_with(GarminClientTestCase._ANY_WORKOUT)

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_save_workout_error_handling(self, connect_mock):
        self.api.upload_workout.side_effect = requests.exceptions.HTTPError

        connection = self._enter_connection(connect_mock)
        self.assertRaises(requests.exceptions.HTTPError, connection.save_workout, GarminClientTestCase._ANY_WORKOUT)

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_update_workout(self, connect_mock):
        workout_id = 1
        response = Mock()
        self.http.put.return_value = response

        connection = self._enter_connection(connect_mock)
        connection.update_workout(workout_id, GarminClientTestCase._ANY_WORKOUT)

        self.http.put.assert_called_once_with(
            f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}",
            headers=GarminClient._REQUIRED_HEADERS,
            json=GarminClientTestCase._ANY_WORKOUT,
        )
        response.raise_for_status.assert_called_once_with()

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_update_workout_error_handling(self, connect_mock):
        workout_id = 1
        response = Mock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError
        self.http.put.return_value = response

        connection = self._enter_connection(connect_mock)
        self.assertRaises(
            requests.exceptions.HTTPError, connection.update_workout, workout_id, GarminClientTestCase._ANY_WORKOUT
        )

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_delete_workout(self, connect_mock):
        workout_id = 1
        response = Mock()
        self.http.delete.return_value = response

        connection = self._enter_connection(connect_mock)
        connection.delete_workout(workout_id)

        self.http.delete.assert_called_once_with(
            f"{self.connect_url}{GarminClient._WORKOUT_SERVICE_ENDPOINT}/workout/{workout_id}",
            headers=GarminClient._REQUIRED_HEADERS,
        )
        response.raise_for_status.assert_called_once_with()

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_delete_workout_error_handling(self, connect_mock):
        workout_id = 1
        response = Mock()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError
        self.http.delete.return_value = response

        connection = self._enter_connection(connect_mock)
        self.assertRaises(requests.exceptions.HTTPError, connection.delete_workout, workout_id)

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_schedule_workout(self, connect_mock):
        workout_id = 1
        date = "any date"
        connection = self._enter_connection(connect_mock)
        connection.schedule_workout(workout_id, date)
        self.api.schedule_workout.assert_called_once_with(workout_id, date)

    @patch("garminworkouts.garmin.garminclient.connect")
    def test_schedule_workout_error_handling(self, connect_mock):
        workout_id = 1
        date = "any date"
        self.api.schedule_workout.side_effect = requests.exceptions.HTTPError

        connection = self._enter_connection(connect_mock)
        self.assertRaises(requests.exceptions.HTTPError, connection.schedule_workout, workout_id, date)

    @patch("garminworkouts.garmin.garminclient.disconnect")
    @patch("garminworkouts.garmin.garminclient.connect")
    def test_context_manager_connects_and_disconnects_with_session_file(self, connect_mock, disconnect_mock):
        connect_mock.return_value = self.api

        with self.client as connection:
            self.assertIs(connection.session, self.api)

        connect_mock.assert_called_once_with(session_file=self.session_file)
        disconnect_mock.assert_called_once_with(self.api)


if __name__ == "__main__":
    unittest.main()
