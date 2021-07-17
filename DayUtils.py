from datetime import date, datetime, timedelta
import enum

class DayUtils:

    @staticmethod
    def convert_day_to_weekday(day):
        DAY_OF_WEEK = {
                        "MONDAY": 0,
                        "TUESDAY": 1,
                        "WEDNESDAY": 2,
                        "THURSDAY": 3,
                        "FRIDAY": 4,
                        "SATURDAY": 5,
                        "SUNDAY": 6
                       }

        if day.upper() not in DAY_OF_WEEK:
            raise Exception("Not a valid day")
        return DAY_OF_WEEK[day.upper()]
    


class ValidWeekDays(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4

