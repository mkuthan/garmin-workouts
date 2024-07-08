
from datetime import datetime
from garminworkouts.garmin.garminwellness import GarminWellness


class GarminChallenge(GarminWellness):
    _BADGE_CHALLENGE_ENDPOINT = "/badgechallenge-service"

    def list_challenge(self) -> None:
        url: str = f"{self._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/available"
        challenges: dict = self.get(url).json()
        for challenge in challenges:
            url: str = (
                f"{self._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/"
                f"{challenge.get('uuid')}/optIn/"
                f"{datetime.today().strftime('%Y-%m-%d')}"
                )

            self.post(url)
