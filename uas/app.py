from flask import Flask, render_template, request, redirect, url_for

from controller import main_controler

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(main_controler)

# Data penyimpanan transaksi sederhana
transactions = []

# @app.route('/')
# def index():
#     return render_template('index.html', transactions=transactions)

# @app.route('/add', methods=['POST'])
# def add_transaction():
#     if request.method == 'POST':
#         amount = request.form['amount']
#         description = request.form['description']
#         transaction_type = request.form['type']  # Ambil tipe transaksi
#         date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#         transactions.append({
#             'id': len(transactions) + 1,
#             'amount': float(amount),
#             'description': description,
#             'type': transaction_type,  # Simpan tipe transaksi
#             'date': date
#         })
#         return redirect(url_for('index'))

# @app.route('/edit/<int:id>', methods=['GET', 'POST'])
# def edit_transaction(id):
#     transaction = next((t for t in transactions if t['id'] == id), None)
#     if request.method == 'POST':
#         transaction['amount'] = float(request.form['amount'])
#         transaction['description'] = request.form['description']
#         return redirect(url_for('index'))
#     return render_template('edit.html', transaction=transaction)

# @app.route('/delete/<int:id>')
# def delete_transaction(id):
#     global transactions
#     transactions = [t for t in transactions if t['id'] != id]
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



