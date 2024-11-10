import sqlite3
from datetime import datetime

class CrowdingDatabase:
    def __init__(self, db_name="bus_crowding.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crowding_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bus_id TEXT NOT NULL,
                passenger_count INTEGER NOT NULL,
                occupancy_rate REAL NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')
        self.conn.commit()
        
    def log_crowding(self, bus_id, passenger_count, occupancy_rate):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO crowding_data (bus_id, passenger_count, occupancy_rate, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (bus_id, passenger_count, occupancy_rate, datetime.now()))
        self.conn.commit()
        
    def get_crowding_history(self, bus_id, start_date=None, end_date=None):
        cursor = self.conn.cursor()
        query = "SELECT * FROM crowding_data WHERE bus_id = ?"
        params = [bus_id]
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
            
        cursor.execute(query, params)
        return cursor.fetchall() 