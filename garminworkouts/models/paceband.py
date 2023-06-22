from datetime import date
from garminworkouts.models.duration import Duration
from garminworkouts.models.event import Event


class PaceBand(object):
    _PACEBAND_ID_FIELD = "paceBandPk"
    _PACEBAND_NAME_FIELD = "name"
    _PACEBAND_SPLITS_FIELD = "paceBandSplits"

    def __init__(
            self,
            config
            ):

        self.name = config['name']
        self.profile = config['profile'] if 'profile' in config else None
        self.date = date(config['date']['year'], config['date']['month'], config['date']['day'])
        self.url = config['url'] if 'url' in config else None
        self.location = config['location'] if 'location' in config else None
        self.time = config['time'] if 'time' in config else None
        self.distance = config['distance']
        self.goal = Duration(config['goal']).to_seconds() if 'goal' in config else None
        self.pace_strategy = float(config['paceStrategy']) if 'paceStrategy' in config else float(0)
        self.upHill_strategy = float(config['uphillStrategy']) if 'uphillStrategy' in config else float(0)
        self.split_strategy = config['splitStrategy'] if 'splitStrategy' in config else 'Distance'
        self.course = config['course'] if 'course' in config else None
        self.sport = config['sport']

    @staticmethod
    def extract_paceband_id(paceband):
        return paceband[PaceBand._PACEBAND_ID_FIELD]

    @staticmethod
    def extract_paceband_name(paceband):
        return paceband[PaceBand._PACEBAND_NAME_FIELD]

    @staticmethod
    def extract_paceband_splits(paceband):
        return paceband[PaceBand._PACEBAND_SPLITS_FIELD]

    def split_definition(self):
        if self.split_strategy.lower() == 'distance':
            return 'DISTANCE_KILOMETER'
        elif self.split_strategy.lower() == 'elevation':
            return 'ELEVATION'
        else:
            return 'DISTANCE_KILOMETER'

    def pacing_strategy(self):
        if abs(self.pace_strategy) > 5:
            return float(0)
        else:
            return self.pace_strategy

    def uphill_strategy(self):
        if abs(self.upHill_strategy) > 2.5:
            return float(0)
        else:
            return self.upHill_strategy

    def create_paceband(self, paceband_id=None):
        return {
            self._PACEBAND_ID_FIELD: paceband_id,
            'paceBandSummary': {
                self._PACEBAND_ID_FIELD: paceband_id,
                self._PACEBAND_NAME_FIELD: self.name,
                Event._COURSE_FIELD: self.course,
                'userProfilePk': self.profile,
                'splitType': self.split_definition(),
                'distanceUnit': None,
                'uphillEffort': self.uphill_strategy(),
                'pacingStrategy': self.pacing_strategy(),
                'goalTime': self.goal,
                # 'eventDate':  str(self.date),
                'elevationSegmentationTolerance': 50.0,
                'elevationSegmentMinLength': 1700.0,
                'paceFactor': 2.0
                }
            }

    @staticmethod
    def print_paceband_summary(paceband):
        paceband_id = PaceBand.extract_paceband_id(paceband)
        paceband_name = PaceBand.extract_paceband_name(paceband)
        paceband_splits = PaceBand.extract_paceband_splits(paceband)
        print("{0} {1:20}".format(paceband_id, paceband_name))

        index = int(1)
        for split in paceband_splits:
            pace = 1000/(60 * float(split['splitAvgSpeed']))
            pace_min = int(pace // 1)
            pace_seg = int(60 * (pace % 1))
            print(index, 'Duration:', float(split['splitDistance'])/1000, 'Pace:', pace_min, ':', pace_seg)
            index += 1
