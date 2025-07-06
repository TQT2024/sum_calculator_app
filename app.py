import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql
from datetime import datetime

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql.SQL("""
        CREATE TABLE IF NOT EXISTS {} (
            id SERIAL PRIMARY KEY,
            numbers_input TEXT NOT NULL,
            sum_result INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """).format(sql.Identifier('sums')))
    conn.commit()
    cur.close()
    conn.close()

    init_db()

@app.route('/', methods=['GET'])
def index():
  
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT numbers_input, sum_result, created_at FROM sums ORDER BY created_at DESC")
    past_sums = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', past_sums=past_sums)

@app.route('/calculate_sum', methods=['POST'])
def calculate_sum():
   
    numbers_str = request.form['numbers']
    try:
       
        numbers = [int(n.strip()) for n in numbers_str.split(',') if n.strip()]
        total_sum = sum(numbers)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql.SQL("INSERT INTO {} (numbers_input, sum_result) VALUES (%s, %s)").format(sql.Identifier('sums')),
                    (numbers_str, total_sum))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))
    except ValueError:
    
        return "Lỗi: Vui lòng nhập các số nguyên cách nhau bởi dấu phẩy.", 400
    except Exception as e:
        
        return f"Đã xảy ra lỗi: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
