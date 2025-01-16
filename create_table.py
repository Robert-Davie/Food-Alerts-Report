import sqlite3

conn = sqlite3.connect("food_alerts.db")
cursor = conn.cursor()
cursor.execute('''
    DROP TABLE IF EXISTS food_alerts;
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry INT,
        type TEXT,
        date DATE,
        business TEXT,
        pathogen TEXT,
        allergen TEXT,
        risk_statement TEXT,
        number_products_affected INT,
        is_published BOOLEAN
    );
''')
conn.commit()
conn.close()
