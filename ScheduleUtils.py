import enum

class ScheduleType(enum.Enum):
    BIWEEKLY = "biweekly"
    WEEKLY = "weekly"

class ScheduleUtils:
    @staticmethod
    def get_schedule_type(schedule_type_str):
        if schedule_type_str == "biweekly":
            return ScheduleType.BIWEEKLY
        elif schedule_type_str == "weekly":
            return ScheduleType.WEEKLY
        else:
            raise Exception(schedule_type_str + " is not support debit schedule")

