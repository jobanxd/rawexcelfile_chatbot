import sqlite3
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent

class InsuranceDatabase:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = BASE_DIR / "insurance.db"

        self.db_path = db_path
        self._connection = None

    def get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
        return self._connection
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            logger.info("SQL Query: %s", query)
            logger.info("SQL Params: %s", params)

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            logger.info("Query Results: %s", [dict(row) for row in rows])
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error("Database query error: %s", e)
            logger.error("Query: %s", query)
            logger.error("Params: %s", params)
            raise

db = InsuranceDatabase()