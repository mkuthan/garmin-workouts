class TrainingPlan(object):
    _TRAININGPLAN_ID_FIELD = 'id'
    _TRAININGPLAN_TYPE_FIELD = 'type'
    _TRAININGPLAN_LEVEL_FIELD = 'level'
    _TRAININGPLAN_VERSION_FIELD = 'version'
    _TRAININGPLAN_NAME_FIELD = 'name'

    @staticmethod
    def extract_trainingplan_id(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_ID_FIELD]

    @staticmethod
    def extract_trainingplan_type(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_TYPE_FIELD]

    @staticmethod
    def extract_trainingplan_level(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_LEVEL_FIELD]

    @staticmethod
    def extract_trainingplan_version(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_VERSION_FIELD]

    @staticmethod
    def extract_trainingplan_name(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_NAME_FIELD]

    @staticmethod
    def print_trainingplan_summary(tp) -> None:
        tp_: dict = TrainingPlan.export_trainingplan(tp)
        tp_id: str = TrainingPlan.extract_trainingplan_id(tp_)
        tp_name: str = TrainingPlan.extract_trainingplan_name(tp_)
        tp_type: str = TrainingPlan.extract_trainingplan_type(tp_)
        tp_level: str = TrainingPlan.extract_trainingplan_level(tp_)
        tp_version: str = TrainingPlan.extract_trainingplan_version(tp_)
        print("{0} {1:15} {2} {3} {4}".format(tp_id, tp_name, tp_type, tp_level, tp_version))

    @staticmethod
    def export_trainingplan(tp) -> dict:
        trainingplan: dict = {}

        trainingplan['id'] = tp['trainingPlanId']
        trainingplan['type'] = tp['trainingType']['typeKey']
        trainingplan['subtype'] = tp['trainingSubType']['subTypeKey']
        trainingplan['level'] = tp['trainingLevel']['levelKey']
        trainingplan['version'] = tp['trainingVersion']['versionName']
        trainingplan['name'] = tp['name']
        trainingplan['description'] = tp['description']
        trainingplan['durationInWeeks'] = tp['durationInWeeks']
        trainingplan['avgWeeklyWorkouts'] = tp['avgWeeklyWorkouts']

        return trainingplan
