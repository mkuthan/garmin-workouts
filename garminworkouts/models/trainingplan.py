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
        tp_id, tp_name, tp_type, tp_level, tp_version = (tp_[field] for field in [
            'id',
            'name',
            'type',
            'level',
            'version'])
        print("{0} {1:15} {2} {3} {4}".format(tp_id, tp_name, tp_type, tp_level, tp_version))

    @staticmethod
    def export_trainingplan(tp) -> dict:
        trainingplan: dict = {
            'id': tp['trainingPlanId'],
            'type': tp['trainingType']['typeKey'],
            'subtype': tp['trainingSubType']['subTypeKey'],
            'level': tp['trainingLevel']['levelKey'],
            'version': tp['trainingVersion']['versionName'],
            'name': tp['name'],
            'description': tp['description'],
            'durationInWeeks': tp['durationInWeeks'],
            'avgWeeklyWorkouts': tp['avgWeeklyWorkouts']
        }
        return trainingplan
