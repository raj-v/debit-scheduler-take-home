import json

from Loan import Loan
from Debitor import Debitor, DebitorFactory
       

s = '''
    { 
    "loan": {
        "monthly_payment_amount": 990, 
        "payment_due_day": 1, 
        "schedule_type": "biweekly", 
        "debit_start_date": "2021-05-03", 
        "debit_day_of_week": "monday"
        } 
    }
    '''

loan = Loan(s)
print(loan)

debitor = DebitorFactory.get_debitor(loan)
list_of_dates = debitor.generate_schedules(loan)
print(list_of_dates[:5])
debitor.get_next_debit(loan)
print(123)
#print(list_of_dates[:5])
#
