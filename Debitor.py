from Loan import Loan
import json
from datetime import date, datetime, timedelta
import calendar
import enum
from abc import ABC, abstractmethod
from ScheduleUtils import ScheduleType

class Debitor(ABC):

    @abstractmethod
    def get_days_between_debits(self):
        pass

    @abstractmethod
    def generate_schedules(self, loan):
        pass

    @abstractmethod
    def max_debits_per_month():
        pass

    # max loan years - used in subclasses for debug/addl info
    max_loan_years = 30

    # Returns next debit and the amount during the debt
    # 1. Find the next debit date  using current date and the days 
    # since last debit
    # 2. Find other debits in the same period as next debit date
    # 3. Per pay period debt = montly payment / num debits this period
    def get_next_debit(self, loan):

        #todays_dt = datetime.strptime("2021-06-05", "%Y-%m-%d")

        todays_dt = datetime.combine(date.today(), datetime.min.time())
        
        time_delta_todays_debit_start = todays_dt - loan.debit_start_date

        days_since_last_debit = time_delta_todays_debit_start.days % \
                                self.get_days_between_debits()

        prev_debit_date = todays_dt - \
                          timedelta(days=days_since_last_debit)


        print("Prev Debit Date:" + str(prev_debit_date))

        
        next_debit_date = prev_debit_date + \
                          timedelta(days=self.get_days_between_debits())
        print("Next Debit Date:" + str(next_debit_date))


        # For a monthly payment day of 28
        # Next Payment Date will be 6/28
        # Prev Payment Date will be 5/28
        next_payment_date = next_debit_date + timedelta(days=1)
        while next_payment_date.day != loan.payment_due_day:
            next_payment_date = next_payment_date + timedelta(days=1)

        prev_payment_date = next_debit_date
        while prev_payment_date.day != loan.payment_due_day:
            prev_payment_date = prev_payment_date - timedelta(days=1)

        print("Prev payment date:" + str(prev_payment_date))
        print("Next payment date:" + str(next_payment_date))

        #Find the number of days in this pay period
        #1 because of the next_debit_date is already included
        num_debits_this_period = 1 

        debit_later = next_debit_date +\
            timedelta(days=self.get_days_between_debits())

        debit_before = next_debit_date -\
            timedelta(days=self.get_days_between_debits())

        while debit_later < next_payment_date:
            print("Debits after:" + str(debit_later))
            num_debits_this_period += 1
            debit_later = debit_later + \
                    timedelta(days=self.get_days_between_debits())

        while debit_before >= prev_payment_date:
            print("Debits before:" + str(debit_before))
            num_debits_this_period += 1
            debit_before = debit_before - \
                    timedelta(days=self.get_days_between_debits())
           

        #Use decimal value if required
        amount = int(loan.monthly_payment_amount/num_debits_this_period)
        debit_date = next_debit_date.strftime("%Y-%m-%d")
        print("Amount:" + str(int(amount)))
        print("Next Debit Date:" + debit_date)

        return amount, debit_date


class WeeklyDebitor(Debitor):


    def get_days_between_debits(self):
        return 7

    def max_debits_per_month(self):
        return 5

    def generate_schedules(self, loan):
        max_debits = self.max_debits_per_month() * self.max_loan_years

        list_of_schedules = []

        current_date = loan.debit_start_date

        while max_debits > 0: 
            list_of_schedules.append(current_date)
            current_date = current_date + \
                timedelta(days=self.get_days_between_debits())
            max_debits -= 1

        return list_of_schedules



class BiWeeklyDebitor(Debitor):

    def get_days_between_debits(self):
        return 14

    def max_debits_per_month(self):
        return 3
    
    def generate_schedules(self, loan):
        max_debits = self.max_debits_per_month() * self.max_loan_years

        list_of_schedules = []

        current_date = loan.debit_start_date


        while max_debits > 0: 
            list_of_schedules.append(current_date)
            current_date = current_date + \
                timedelta(days=self.get_days_between_debits())
            max_debits -= 1

        return list_of_schedules



class DebitorFactory:
    @staticmethod
    def get_debitor(loan):
        if loan.schedule_type == ScheduleType.BIWEEKLY:
            return BiWeeklyDebitor()
        elif loan.schedule_type == ScheduleType.WEEKLY:
            return WeeklyDebitor()

