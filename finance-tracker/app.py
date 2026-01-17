from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Ensure static folder exists
if not os.path.exists('static/css'):
    os.makedirs('static/css')

DATABASE = 'finance_tracker.db'

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            color TEXT DEFAULT '#3B82F6',
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, name)
        )
    ''')
    
    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    
    # Budgets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id),
            UNIQUE(user_id, category_id, month)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('register'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                         (username, password_hash, email))
            
            user_id = cursor.lastrowid
            
            # Add default categories
            default_categories = [
                ('Salary', 'income', '#10B981'),
                ('Freelance', 'income', '#34D399'),
                ('Food', 'expense', '#EF4444'),
                ('Transport', 'expense', '#F59E0B'),
                ('Entertainment', 'expense', '#8B5CF6'),
                ('Utilities', 'expense', '#6366F1'),
                ('Shopping', 'expense', '#EC4899')
            ]
            
            for name, cat_type, color in default_categories:
                cursor.execute('INSERT INTO categories (user_id, name, type, color) VALUES (?, ?, ?, ?)',
                             (user_id, name, cat_type, color))
            
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    # Get current month stats
    current_month = datetime.now().strftime('%Y-%m')
    
    # Total income this month
    income = cursor.execute('''
        SELECT COALESCE(SUM(t.amount), 0) as total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ? AND c.type = 'income' 
        AND strftime('%Y-%m', t.date) = ?
    ''', (user_id, current_month)).fetchone()['total']
    
    # Total expenses this month
    expenses = cursor.execute('''
        SELECT COALESCE(SUM(t.amount), 0) as total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ? AND c.type = 'expense' 
        AND strftime('%Y-%m', t.date) = ?
    ''', (user_id, current_month)).fetchone()['total']
    
    # Recent transactions
    transactions = cursor.execute('''
        SELECT t.*, c.name as category_name, c.type as category_type, c.color
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ?
        ORDER BY t.date DESC, t.created_at DESC
        LIMIT 10
    ''', (user_id,)).fetchall()
    
    # Expense breakdown by category
    category_breakdown = cursor.execute('''
        SELECT c.name, c.color, SUM(t.amount) as total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ? AND c.type = 'expense'
        AND strftime('%Y-%m', t.date) = ?
        GROUP BY c.id
        ORDER BY total DESC
    ''', (user_id, current_month)).fetchall()
    
    conn.close()
    
    balance = income - expenses
    
    return render_template('dashboard.html', 
                         income=income, 
                         expenses=expenses, 
                         balance=balance,
                         transactions=transactions,
                         category_breakdown=category_breakdown)

@app.route('/transactions')
@login_required
def transactions():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    # Get filter parameters
    category_filter = request.args.get('category', '')
    type_filter = request.args.get('type', '')
    month_filter = request.args.get('month', '')
    
    query = '''
        SELECT t.*, c.name as category_name, c.type as category_type, c.color
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ?
    '''
    params = [user_id]
    
    if category_filter:
        query += ' AND c.id = ?'
        params.append(category_filter)
    
    if type_filter:
        query += ' AND c.type = ?'
        params.append(type_filter)
    
    if month_filter:
        query += ' AND strftime("%Y-%m", t.date) = ?'
        params.append(month_filter)
    
    query += ' ORDER BY t.date DESC, t.created_at DESC'
    
    all_transactions = cursor.execute(query, params).fetchall()
    
    # Get categories for filter
    categories = cursor.execute('''
        SELECT * FROM categories WHERE user_id = ? ORDER BY name
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    return render_template('transactions.html', 
                         transactions=all_transactions,
                         categories=categories)

@app.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    user_id = session['user_id']
    
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        description = request.form.get('description')
        date = request.form.get('date')
        
        if not category_id or not amount or not date:
            flash('Category, amount, and date are required.', 'danger')
            return redirect(url_for('add_transaction'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (user_id, category_id, amount, description, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category_id, float(amount), description, date))
        conn.commit()
        conn.close()
        
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions'))
    
    conn = get_db()
    categories = conn.execute('SELECT * FROM categories WHERE user_id = ? ORDER BY type, name', 
                             (user_id,)).fetchall()
    conn.close()
    
    return render_template('add_transaction.html', categories=categories)

@app.route('/transactions/delete/<int:transaction_id>')
@login_required
def delete_transaction(transaction_id):
    user_id = session['user_id']
    conn = get_db()
    conn.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?', 
                (transaction_id, user_id))
    conn.commit()
    conn.close()
    
    flash('Transaction deleted.', 'info')
    return redirect(url_for('transactions'))

@app.route('/categories')
@login_required
def categories():
    user_id = session['user_id']
    conn = get_db()
    all_categories = conn.execute('SELECT * FROM categories WHERE user_id = ? ORDER BY type, name', 
                                 (user_id,)).fetchall()
    conn.close()
    
    return render_template('categories.html', categories=all_categories)

@app.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    user_id = session['user_id']
    name = request.form.get('name')
    cat_type = request.form.get('type')
    color = request.form.get('color', '#3B82F6')
    
    if not name or not cat_type:
        flash('Name and type are required.', 'danger')
        return redirect(url_for('categories'))
    
    conn = get_db()
    try:
        conn.execute('INSERT INTO categories (user_id, name, type, color) VALUES (?, ?, ?, ?)',
                    (user_id, name, cat_type, color))
        conn.commit()
        flash('Category added!', 'success')
    except sqlite3.IntegrityError:
        flash('Category name already exists.', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('categories'))

@app.route('/budgets')
@login_required
def budgets():
    user_id = session['user_id']
    current_month = datetime.now().strftime('%Y-%m')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get budgets with spending
    budget_data = cursor.execute('''
        SELECT 
            b.id,
            b.amount as budget_amount,
            b.month,
            c.name as category_name,
            c.color,
            c.id as category_id,
            COALESCE(SUM(t.amount), 0) as spent
        FROM budgets b
        JOIN categories c ON b.category_id = c.id
        LEFT JOIN transactions t ON t.category_id = c.id 
            AND t.user_id = b.user_id
            AND strftime('%Y-%m', t.date) = b.month
        WHERE b.user_id = ? AND b.month = ?
        GROUP BY b.id
    ''', (user_id, current_month)).fetchall()
    
    # Get expense categories without budgets
    categories = cursor.execute('''
        SELECT c.* FROM categories c
        WHERE c.user_id = ? AND c.type = 'expense'
        AND c.id NOT IN (
            SELECT category_id FROM budgets 
            WHERE user_id = ? AND month = ?
        )
        ORDER BY c.name
    ''', (user_id, user_id, current_month)).fetchall()
    
    conn.close()
    
    return render_template('budgets.html', 
                         budgets=budget_data,
                         categories=categories,
                         current_month=current_month)

@app.route('/budgets/add', methods=['POST'])
@login_required
def add_budget():
    user_id = session['user_id']
    category_id = request.form.get('category_id')
    amount = request.form.get('amount')
    month = request.form.get('month')
    
    conn = get_db()
    try:
        conn.execute('''
            INSERT INTO budgets (user_id, category_id, amount, month)
            VALUES (?, ?, ?, ?)
        ''', (user_id, category_id, float(amount), month))
        conn.commit()
        flash('Budget set!', 'success')
    except sqlite3.IntegrityError:
        flash('Budget already exists for this category and month.', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('budgets'))

@app.route('/reports')
@login_required
def reports():
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    # Monthly trends (last 6 months)
    monthly_data = cursor.execute('''
        SELECT 
            strftime('%Y-%m', t.date) as month,
            SUM(CASE WHEN c.type = 'income' THEN t.amount ELSE 0 END) as income,
            SUM(CASE WHEN c.type = 'expense' THEN t.amount ELSE 0 END) as expenses
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ?
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    # Reverse to show oldest first
    monthly_data = list(reversed(monthly_data))
    
    return render_template('reports.html', monthly_data=monthly_data)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)