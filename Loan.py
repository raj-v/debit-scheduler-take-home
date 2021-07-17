
from datetime import datetime

from Validator import LoanValidator
from DayUtils import DayUtils, ValidWeekDays
from ScheduleUtils import ScheduleUtils


class Loan:
    def __init__ (self, loan_dict):

        LoanValidator.validate_loan_info(loan_dict)

        loan = loan_dict["loan"]

        payment_due_day = loan["payment_due_day"]
        debit_start_date = loan["debit_start_date"]
        schedule_type = loan["schedule_type"]

        self.monthly_payment_amount = loan["monthly_payment_amount"]
        self.debit_start_date = datetime.strptime(debit_start_date, "%Y-%m-%d")
        self.schedule_type = ScheduleUtils.get_schedule_type(schedule_type)
        self.debit_day_of_week = DayUtils.convert_day_to_weekday(loan["debit_day_of_week"])
        self.payment_due_day = payment_due_day


    def __str__(self):
        return str(self.monthly_payment_amount) + " " + \
               str(self.payment_due_day) + " " + \
               str(self.schedule_type) + " " + \
               str(self.debit_start_date) + " " + \
               str(self.debit_day_of_week)

