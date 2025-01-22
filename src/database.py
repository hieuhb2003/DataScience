import sqlite3
import pandas as pd
from langchain_community.utilities.sql_database import SQLDatabase
from src.few_shot import SQLQueryGenerator
def setup_database():
    # Đọc CSV
    df = pd.read_csv('data/output_file.csv')
    
    # Tạo connection với SQLite
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    
    # Tạo bảng
    cursor.execute('''CREATE TABLE IF NOT EXISTS data_items (
        BRAND TEXT,
        MODEL TEXT,
        SCREEN_SIZE FLOAT,
        CPU TEXT,
        CPU_SPEED FLOAT,
        RAM FLOAT,
        MEMORY FLOAT,
        GPU TEXT,
        GRAPHICS_CARD_DESCRIPTION TEXT,
        OPERATING_SYSTEM TEXT,
        WEIGHT TEXT,
        PRICE FLOAT,
        LINK_AMAZON TEXT,
        WIDTH FLOAT,
        HEIGHT FLOAT,
        IMAGE_LINK TEXT
    )''')
    
    # Import dữ liệu từ DataFrame vào SQLite
    df.to_sql('data_items', conn, if_exists='replace', index=False)
    
    # Tạo SQLDatabase instance
    db = SQLDatabase.from_uri(
        "sqlite:///data/database.db",
        max_string_length=32000,
    )
    
    return db

class DatabaseManager:
    def __init__(self):
        self.db = setup_database()
        self.sql_generator = SQLQueryGenerator()
        
    def get_context_sql(self, question, llm):
        """
        Generates SQL context using few-shot learning
        """
        return self.sql_generator.generate_sql_query(question, llm, self.db)