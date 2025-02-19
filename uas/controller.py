from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from model import User, Transaction
from datetime import datetime

main_controler = Blueprint('main_controler', __name__)

transactions = []

@main_controler.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('main_controler.login'))
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'asc')
    
    if search_query:
        Transactions = Transaction.search_transactions(search_query)
    else:
        Transactions = Transaction.get_all_transactions(page=page, sort_by=sort_by, sort_order=sort_order)

    total_Transactions = Transaction.count_transactions()
    total_pages = (total_Transactions // 10) + (1 if total_Transactions % 10 > 0 else 0)

    return render_template('index.html', Transactions=Transactions, page=page, total_pages=total_pages, sort_by=sort_by, sort_order=sort_order)
    

@main_controler.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.verify_password(username, password):
            session['username'] = username
            return redirect(url_for('main_controler.dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@main_controler.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main_controler.login'))

@main_controler.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create_user(username, password)
        return redirect(url_for('main_controler.login'))
    return render_template('register.html')

@main_controler.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('main_controler.login'))
    if request.method == 'POST':
        username = session['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if User.verify_password(username, old_password):
            User.update_password(username, new_password)
            flash('Password changed successfully', 'success')
            return redirect(url_for('main_controler.dashboard'))
        else:
            flash('Old password is incorrect', 'error')
    return render_template('change_password.html')

# @app.route('/')
# def index():
#     return render_template('index.html', transactions=transactions)

@main_controler.route('/add', methods=['POST'])
def add_transaction():
    if 'username' not in session:
        return redirect(url_for('book_controller.login'))
    if request.method == 'POST':
        amount = request.form['amount']
        description = request.form['description']
        transaction_type = request.form['type']  # Ambil tipe transaksi
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_transaction = Transaction(date, amount, description, transaction_type)
        Transaction.create_transaction(new_transaction)
        
        return redirect(url_for('main_controler.dashboard'))

@main_controler.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    transaction = Transaction.get_transaction(id)
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form['description']
        transaction_type = request.form['type']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_transaction = Transaction(date, amount, description, transaction_type)
        Transaction.update_transaction(id, new_transaction)
        return redirect(url_for('main_controler.dashboard'))
    return render_template('edit.html', transaction=transaction)

@main_controler.route('/delete/<int:id>')
def delete_transaction(id):
    Transaction.delete_transaction(id)
    return redirect(url_for('main_controler.dashboard'))