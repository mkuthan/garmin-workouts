import unittest

from pytest_httpserver import HTTPServer

from garminworkouts.garmin.garminclient import GarminClient


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.httpserver = HTTPServer()
        self.httpserver.start()
        self.addCleanup(self.httpserver.stop)

        self.httpserver \
            .expect_request(GarminClient._SSO_LOGIN_ENDPOINT) \
            .respond_with_data('response_url = "https:\/\/connect.garmin.com\/modern?ticket=ANY-TICKET"')

        url = "http://{}:{}".format(self.httpserver.host, self.httpserver.port)
        self.client = GarminClient(
            connect_url=url,
            sso_url=url,
            username="any username",
            password="any_password",
            cookie_jar=None
        )

    def test_something(self):
        self.httpserver \
            .expect_oneshot_request(GarminClient._WORKOUT_SERVICE_ENDPOINT + "/workouts",
                                    query_string="start=0&limit=100") \
            .respond_with_json([{"foo1": "bar1"}, {"foo2": "bar2"}])

        self.httpserver \
            .expect_oneshot_request(GarminClient._WORKOUT_SERVICE_ENDPOINT + "/workouts",
                                    query_string="start=100&limit=100") \
            .respond_with_json([])

        with self.client as connection:
            for workout in connection.list_workouts():
                print(workout)


if __name__ == '__main__':
    unittest.main()
