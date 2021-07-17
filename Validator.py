# Online Python - IDE, Editor, Compiler, Interpreter

import json
from datetime import date, datetime, timedelta

from abc import ABC, abstractmethod


from DayUtils import DayUtils, ValidWeekDays
from ScheduleUtils import ScheduleUtils, ScheduleType

class PaymentValidator(object): 

    @staticmethod
    def validate_payment_day(day):
        if (not isinstance(day, int)):
            raise Exception("The system expects an integer date")

        if day >= 1 and day <= 28:
            return 
        else:
            raise Exception("Debit start day must be btw 1st and 28th of the month")

    @staticmethod
    def validate_payment_amount(amount):
        if (not isinstance(amount, int) and 
            not isinstance(amount, float)):
            raise Exception("Payment amount is not a valid number")

        if amount < 0:
            raise Exception("Payment amount is not a valid number")

class DebitDateValidator(object): 

    @staticmethod
    def validate_debit_start_date_and_day(date, day):
        debit_start_date_obj = datetime.strptime(date, "%Y-%m-%d")
        debit_start_day = day

        weekday = DayUtils.convert_day_to_weekday(debit_start_day)

        if weekday != debit_start_date_obj.weekday():
            raise Exception("Debit start day not matching with debit start date")

        if weekday not in [e.value for e in ValidWeekDays]:
            raise Exception("Debit start day is not a valid week day")

        print(weekday)


class ScheduleTypeValidator(object):
    @staticmethod
    def validate_schedule_type(schedule_type):
        list_of_schedule_types = [e.value for e in ScheduleType]
        str_schedules = ",".join(list_of_schedule_types)
        if schedule_type not in list_of_schedule_types:
            raise Exception("Currently only supported schedule types are " + \
                            str_schedules)

class LoanValidator:

    @staticmethod
    def validate_loan_containing_all_info(loan):
        
        items_to_validate = ["monthly_payment_amount",
                             "payment_due_day",
                             "schedule_type",
                             "debit_start_date",
                             "debit_day_of_week"]

        for item in items_to_validate:
            if item not in loan:
                print("Item:" + item + " not present in loan")
                raise Exception("Loan doesn't contain enough information")
   
    @staticmethod
    def validate_loan_info(loan_dict):

        loan = loan_dict["loan"]
        LoanValidator.validate_loan_containing_all_info(loan)

        debit_start_date = loan["debit_start_date"]
        debit_day_of_week = loan["debit_day_of_week"]

        DebitDateValidator.validate_debit_start_date_and_day(debit_start_date,
                                                             debit_day_of_week)

        payment_due_day = loan["payment_due_day"]
        monthly_payment_amount = loan["monthly_payment_amount"]
        PaymentValidator.validate_payment_day(payment_due_day)
        PaymentValidator.validate_payment_amount(monthly_payment_amount)
        
        schedule_type = loan["schedule_type"]
        ScheduleTypeValidator.validate_schedule_type(schedule_type)

        return loan

