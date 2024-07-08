from datetime import date, timedelta
import logging
from typing import Any
from requests import Response
from garminworkouts.garmin.garmindownload import GarminDownload


class GarminActivity(GarminDownload):
    _ACTIVITY_LIST_SERVICE_ENDPOINT = "/activitylist-service"

    def get_activity(self, activity_id) -> dict:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}"
        return self.get(url).json()

    def get_activity_workout(self, activity_id) -> Any:
        url: str = f"{self._ACTIVITY_SERVICE_ENDPOINT}/activity/{activity_id}/workouts"
        a: dict = self.get(url).json()
        return [] if len(a) == 0 else a[0]

    def get_activities_by_date(self,
                               startdate=None, enddate=None,
                               activitytype=None,
                               minDistance=None, maxDistance=None,  # meters
                               minDuration=None, maxDuration=None,  # seconds
                               minElevation=None, maxElevation=None,  # meters
                               ) -> list[dict]:
        """
        Fetch available activities between specific dates
        :param startdate: String in the format YYYY-MM-DD
        :param enddate: String in the format YYYY-MM-DD
        :param activitytype: (Optional) Type of activity you are searching
                             Possible values are [cycling, running, swimming,
                             multi_sport, fitness_equipment, hiking, walking, other]
        :return: list of JSON activities
        """

        activities: list = []
        start = 0
        limit = 20
        # mimicking the behavior of the web interface that fetches 20 activities at a time
        # and automatically loads more on scroll
        url: str = f"{self._ACTIVITY_LIST_SERVICE_ENDPOINT}/activities/search/activities"

        params: dict = {
            "startDate": str(startdate) if startdate else None,
            "endDate": str(enddate) if enddate else None,
            "start": str(start),
            "limit": str(limit),
            "activityType": str(activitytype) if activitytype else None,
            "minDistance": int(minDistance) if minDistance else None,
            "maxDistance": int(maxDistance) if maxDistance else None,
            "minDuration": int(minDuration) if minDuration else None,
            "maxDuration": int(maxDuration) if maxDuration else None,
            "minElevation": int(minElevation) if minElevation else None,
            "maxElevation": int(maxElevation) if maxElevation else None,
        }

        logging.info(f"Requesting activities by date from {startdate} to {enddate}")
        while True:
            params["start"] = str(start)
            logging.info(f"Requesting activities {start} to {start+limit}")
            act: Response = self.get(url, params=params).json()
            if act:
                activities.extend(act)
                start: int = start + limit
            else:
                break

        return activities

    def activity_list(self) -> None:
        start_date: date = date.today() - timedelta(days=7)
        end_date: date = date.today()
        activities: list[dict] = self.get_activities_by_date(
            startdate=start_date, enddate=end_date, activitytype='running')
        for activity in activities:
            id: str = activity.get('activityId', '')
            logging.info("Downloading activity '%s'", id)
            self.download_activity(id)
