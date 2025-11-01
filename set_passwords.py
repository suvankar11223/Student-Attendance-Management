import mysql.connector
import hashlib
import sys

# --- Database Connection Details ---
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'babu1234'
DB_NAME = 'face_recognizer'
DEFAULT_PASS = 'password123'

# --- Initialize connection variables ---
conn = None
cursor = None

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    cursor = conn.cursor()

    # 1. Get all student IDs
    cursor.execute('SELECT Studentid FROM student')
    students = cursor.fetchall()

    if not students:
        print("No students found in the table.")
        sys.exit() # Exit if there's nothing to do

    print(f"Found {len(students)} students. Setting default passwords...")

    # 2. Hash the password *once* outside the loop for efficiency
    hashed_password = hash_password(DEFAULT_PASS)

    # 3. Loop through and queue all updates
    for student in students:
        student_id = str(student[0])

        # Use parameterized query to prevent SQL injection
        update_query = 'UPDATE student SET password = %s WHERE Studentid = %s'
        cursor.execute(update_query, (hashed_password, student_id))
        print(f"Password update queued for student {student_id}")

    # 4. Commit ALL changes at once, *after* the loop is finished
    conn.commit()
    print(f"\nSuccess! All {len(students)} passwords have been set.")

except mysql.connector.Error as err:
    print(f"Database Error: {err}")
    if conn:
        print("Rolling back changes...")
        conn.rollback() # Undo changes if an error occurred

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # 5. Close cursor and connection in the 'finally' block
    #    This ensures they close even if an error happens.
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
        print("\n--- MySQL connection closed ---")
