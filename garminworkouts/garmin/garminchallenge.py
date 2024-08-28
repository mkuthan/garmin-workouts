
from datetime import datetime
import logging
from garminworkouts.garmin.garminwellness import GarminWellness


class GarminChallenge(GarminWellness):
    _BADGE_CHALLENGE_ENDPOINT = "/badgechallenge-service"

    def list_challenge(self) -> None:
        url: str = f"{self._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/available"
        challenges: dict = self.get(url).json()
        if challenges == []:
            logging.info("No new available challenges")
        else:
            for challenge in challenges:
                logging.info("Challenge sign up: '%s'", challenge)
                url: str = (
                    f"{self._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/"
                    f"{challenge.get('uuid')}/optIn/"
                    f"{datetime.today().strftime('%Y-%m-%d')}"
                    )

                self.post(url)
