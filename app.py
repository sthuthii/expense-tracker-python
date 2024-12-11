import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

EXPENSE_FILE = "expenses.csv"

def create_file():
    try:
        with open(EXPENSE_FILE, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Category","Amount"])
    except FileExistsError:
        pass

def add_expense(date, description, category, amount):
    with open(EXPENSE_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, description, category, amount])

def get_expenses():
    expenses = []
    with open(EXPENSE_FILE, 'r') as file:
        reader = csv.reader()
        next(reader)
        for row in reader:
            expenses.append(row)
    return expenses

def get_expense_summary():
    category_totals = {}
    with open(EXPENSE_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            category = row[2]  
            amount = float(row[3])
            category_totals[category] = category_totals.get(category, 0) + amount      
    return category_totals

@app.route('/')
def index():
    expenses = get_expenses
    return render_template('./templates/index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        description = request.form['description']
        category = request.form['category']
        amount = float(request.form['amount'])
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        add_expense(date, description, category, amount)
        return redirect(url_for('index'))

@app.route('/summary')
def summary():
    summary_data = get_expense_summary()
    return render_template('summary.html', summary=summary)

if __name__=='__main__':
    create_file()
    app.run(debug=True)    