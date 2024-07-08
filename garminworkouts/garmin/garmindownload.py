import os
from garminworkouts.garmin.garminchallenge import GarminChallenge


class GarminDownload(GarminChallenge):
    _DOWNLOAD_SERVICE = "/download-service/files"

    def download_activity(self, activity_id) -> bytes:
        url: str = f"{self._DOWNLOAD_SERVICE}/activity/{activity_id}"
        data: bytes = self.download(url)

        newpath: str = os.path.join('.', 'activities')
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        output_file: str = f"./activities/{str(activity_id)}.zip"
        with open(output_file, "wb") as fb:
            fb.write(data)
        return data
