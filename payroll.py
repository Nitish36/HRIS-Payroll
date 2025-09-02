from faker import Faker
import random
from datetime import timedelta
import pandas as pd
from faker.providers import BaseProvider

class BankProvider(BaseProvider):
    def bank_name(self):
        banks = ["State Bank of India","HDFC Bank","ICICI Bank","Axis Bank","Kotak Mahindra Bank","Punjab National Bank",
            "Bank of Baroda","Yes Bank"
        ]
        return self.random_element(banks)

fake = Faker()

# --- Models ---
def generate_employee(emp_id, company_id):
    return {
        "id": emp_id,
        "company_id": fake.uuid4(),
        "company_name": fake.company(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "city": fake.city(),
        "address": fake.address(),
        "hire_date": fake.date_between(start_date='-5y', end_date='today').isoformat(),
        "title": fake.job(),
        "department": random.choice(["Engineering", "Finance", "Sales", "HR", "Operations", "Analytics"]),
        "status": random.choice(["active", "terminated", "on_leave", "notice period"]),
        "start_date": fake.date_between(start_date='-5y', end_date='-1y').isoformat(),
        "end_date": None if random.random() > 0.2 else fake.date_between(start_date='-1y', end_date='today').isoformat()

    }

def generate_bank_info(emp_id):
    fake.add_provider(BankProvider)
    return {
        "id": fake.uuid4(),
        "employee_id": emp_id,
        "bank_name": fake.bank_name(),
        "account_number": fake.iban(),
        "routing_number": fake.swift11(),
        "is_primary": True
    }

def generate_employer_benefit(company_id, benefit_id):
    return {
        "id": fake.uuid4(),
        "company_id": company_id,
        "benefit_name": random.choice(["Health Insurance", "Dental", "Retirement", "Life Insurance"]),
        "benefit_type": random.choice(["health", "dental", "retirement", "life"]),
        "start_date": fake.date_between(start_date='-5y', end_date='today').isoformat(),
        "end_date": None if random.random() > 0.2 else fake.date_between(start_date='-1y', end_date='today').isoformat()
    }

def emp_performance(emp_id):
    return {
        "id": fake.uuid4(),
        "emp_id": emp_id,
        "score": random.randrange(1,10)
    }

def department_performance(company_id,department):
    return {
        "id": fake.uuid4(),
        "department": department,
        "department_score": random.randrange(1,10)
    }

def generate_employee_payroll(emp_id, payroll_run_id):
    base_salary = random.randint(30000, 120000)
    bonus = random.randint(1000, 10000)
    deductions = random.randint(500, 5000)
    return {
        "id": fake.uuid4(),
        "employee_id": emp_id,
        "payroll_run_id": payroll_run_id,
        "gross_pay": base_salary + bonus,
        "net_pay": base_salary + bonus - deductions
    }

def generate_time_off(emp_id):
    start = fake.date_between(start_date='-1y', end_date='today')
    return {
        "id": fake.uuid4(),
        "employee_id": emp_id,
        "start_date": start.isoformat(),
        "end_date": (start + timedelta(days=random.randint(1, 10))).isoformat(),
        "type": random.choice(["vacation", "sick", "personal"])
    }


employees_data = []
bank_info_data = []
employer_benefits_data = []
emp_performance_data = []
dept_performance_data = []
payroll_data = []
time_off_data = []

# Example simulation for 5 employees
company_id = fake.uuid4()
payroll_run_id = fake.uuid4()

for i in range(1, 6):
    emp = generate_employee(str(i), company_id)
    employees_data.append(emp)

    bank_info_data.append(generate_bank_info(emp["id"]))
    employer_benefits_data.append(generate_employer_benefit(company_id, fake.uuid4()))
    emp_performance_data.append(emp_performance(emp["id"]))
    dept_performance_data.append(department_performance(company_id, emp["department"]))
    payroll_data.append(generate_employee_payroll(emp["id"], payroll_run_id))
    time_off_data.append(generate_time_off(emp["id"]))

# Convert to DataFrames
df_employees = pd.DataFrame(employees_data)
df_bank_info = pd.DataFrame(bank_info_data)
df_employer_benefits = pd.DataFrame(employer_benefits_data)
df_emp_performance = pd.DataFrame(emp_performance_data)
df_dept_performance = pd.DataFrame(dept_performance_data)
df_payroll = pd.DataFrame(payroll_data)
df_time_off = pd.DataFrame(time_off_data)

print(df_bank_info)
