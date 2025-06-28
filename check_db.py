import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        
        # Get table information
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tables in database:")
        for table in tables:
            print(f"\nTable: {table[0]}")
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # Show sample data
            cursor.execute(f"SELECT * FROM {table[0]} LIMIT 1")
            sample = cursor.fetchone()
            if sample:
                print("\nSample row:")
                for col, val in zip(columns, sample):
                    print(f"  {col[1]}: {val}")
        
        conn.close()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_database() 