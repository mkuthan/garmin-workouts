class TrainingPlan(object):
    _TRAININGPLAN_ID_FIELD = 'id'
    _TRAININGPLAN_TYPE_FIELD = 'type'
    _TRAININGPLAN_LEVEL_FIELD = 'level'
    _TRAININGPLAN_VERSION_FIELD = 'version'
    _TRAININGPLAN_NAME_FIELD = 'name'

    @staticmethod
    def extract_trainingplan_id(tp):
        return tp[TrainingPlan._TRAININGPLAN_ID_FIELD]

    @staticmethod
    def extract_trainingplan_type(tp):
        return tp[TrainingPlan._TRAININGPLAN_TYPE_FIELD]

    @staticmethod
    def extract_trainingplan_level(tp):
        return tp[TrainingPlan._TRAININGPLAN_LEVEL_FIELD]

    @staticmethod
    def extract_trainingplan_version(tp):
        return tp[TrainingPlan._TRAININGPLAN_VERSION_FIELD]

    @staticmethod
    def extract_trainingplan_name(tp):
        return tp[TrainingPlan._TRAININGPLAN_NAME_FIELD]

    @staticmethod
    def print_trainingplan_summary(tp):
        tp = TrainingPlan.export_trainingplan(tp)
        tp_id = TrainingPlan.extract_trainingplan_id(tp)
        tp_name = TrainingPlan.extract_trainingplan_name(tp)
        tp_type = TrainingPlan.extract_trainingplan_type(tp)
        tp_level = TrainingPlan.extract_trainingplan_level(tp)
        tp_version = TrainingPlan.extract_trainingplan_version(tp)
        print("{0} {1:15} {2} {3} {4}".format(tp_id, tp_name, tp_type, tp_level, tp_version))

    @staticmethod
    def export_trainingplan(tp):
        trainingplan = {}

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
