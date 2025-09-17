import sqlite3
import os
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_name="job_applications.db", username=None):
        if username:
            # Create user-specific database
            db_name = f"job_applications_{username}.db"
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    status TEXT NOT NULL,
                    deadline TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON applications(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_deadline ON applications(deadline)')
            
            conn.commit()
    
    def add_application(self, application):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO applications (company, role, status, deadline, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (application.company, application.role, application.status, 
                  application.deadline, application.notes))
            conn.commit()
            return cursor.lastrowid
    
    def update_application(self, application):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE applications 
                SET company=?, role=?, status=?, deadline=?, notes=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (application.company, application.role, application.status, 
                  application.deadline, application.notes, application.id))
            conn.commit()
    
    def delete_application(self, application_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM applications WHERE id=?', (application_id,))
            conn.commit()
    
    def get_all_applications(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM applications ORDER BY deadline')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_applications_by_status(self, status):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM applications WHERE status=? ORDER BY deadline', (status,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_upcoming_deadlines(self, days=7):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            future_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            cursor.execute('''
                SELECT * FROM applications 
                WHERE deadline BETWEEN ? AND ?
                ORDER BY deadline
            ''', (today, future_date))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def search_applications(self, search_term):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            search_pattern = f'%{search_term}%'
            cursor.execute('''
                SELECT * FROM applications 
                WHERE company LIKE ? OR role LIKE ? OR notes LIKE ?
                ORDER BY deadline
            ''', (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]