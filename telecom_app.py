import sqlite3
from datetime import datetime

DB_PATH = "telecom_complaints.sqlite3"

class TelecomComplaintSystem:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def view_complaints(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = "SELECT id, customer_name, contact_number, category, description, status, created_at FROM complaints"
            cursor.execute(query)

            rows = cursor.fetchall()

            if not rows:
                print("\nNo complaints found.")
                return
            
            print("\n--- Complaints ---")
            for row in rows:
                print(f"\nID: {row[0]}")
                print(f"Name: {row[1]}")
                print(f"Contact: {row[2]}")
                print(f"Category: {row[3]}")
                print(f"Description: {row[4]}")
                print(f"Status: {row[5]}")
                print(f"Created At: {row[6]}")
                print("-" * 40)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if conn:
                conn.close()

    def raise_complaint(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            print("\n--- Raise a new complaint ---")

            customer_name = input("Enter your name: ").strip()
            contact_number = input("Enter your contact number: ").strip()
            category = input("Enter complaint category (e.g., Network, Billing, Service, SIM Activation, Data speed etc.): ").strip()
            description = input("Enter complaint description: ").strip()
            status = "Pending"
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            insert_query = '''
                INSERT INTO complaints (customer_name, contact_number, category, description, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                '''

            cursor.execute(insert_query, (customer_name, contact_number, category, description, status, created_at))
            conn.commit()

            print("\n Complaint raise successfully!")
            print(f"Complaint ID: {cursor.lastrowid}")
            print("Status: Pending")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if conn:
                conn.close()

    def main_menu(self):
        while True:
            print("\n--- Telecom Complaints Management System ---")
            print("1. View all complaints")
            print("2. Raise a complaint")
            print("3. Exit")

            choice = input("Enter your choice (1-3): ").strip()

            if choice == "1":
                self.view_complaints()
            elif choice == "2":
                self.raise_complaint()
            elif choice == "3":
                print("\nExiting the application!")
                break
            else:
                print("\nInvalid choice. Please try within the given ones.")

if __name__ == "__main__":
    app = TelecomComplaintSystem(DB_PATH)
    app.main_menu()
