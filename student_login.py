import mysql.connector
import hashlib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'babu1234',
    'database': 'face_recognizer'
}

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_student(student_id, password):
    """
    Authenticate a student using StudentId and password.

    Args:
        student_id (str): The student's ID
        password (str): The plain text password

    Returns:
        dict or None: Student details if authentication successful, None otherwise
    """
    conn = None
    cursor = None

    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True, buffered=True)  # Use buffered cursor to avoid unread result errors

        # Single query to get student details and password
        query = "SELECT StudentId, Name, Department, Course, Year, Semester, Division, Roll, Gender, DOB, Email, Phone, Address, Teacher, password FROM student WHERE StudentId = %s"
        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

        if not student:
            logging.warning(f"Authentication failed: Student ID {student_id} not found")
            return None

        if not student['password']:
            logging.warning(f"Authentication failed: No password set for Student ID {student_id}")
            return None

        stored_hash = student['password']
        input_hash = hash_password(password)

        # Compare hashes
        if stored_hash == input_hash:
            logging.info(f"Authentication successful for Student ID {student_id}")
            # Remove password from returned data for security
            del student['password']
            return student
        else:
            logging.warning(f"Authentication failed: Invalid password for Student ID {student_id}")
            return None

    except mysql.connector.Error as err:
        logging.error(f"Database error during authentication: {err}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error during authentication: {e}")
        return None
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass  # Ignore errors when closing cursor
        if conn and conn.is_connected():
            conn.close()

def login_prompt():
    """
    Simple command-line login prompt for testing.
    In a real application, this would be integrated into a GUI or web interface.
    """
    print("=== Student Portal Login ===")

    try:
        student_id = input("Enter Student ID: ").strip()
        password = input("Enter Password: ").strip()

        if not student_id or not password:
            print("Student ID and password are required.")
            return

        student = authenticate_student(student_id, password)

        if student:
            print(f"\nLogin successful! Welcome, {student['Name']}")
            print(f"Department: {student['Department']}")
            print(f"Course: {student['Course']}")
            print(f"Year: {student['Year']}")
            print(f"Semester: {student['Semester']}")
            # Add more details as needed
        else:
            print("\nLogin failed. Please check your credentials.")
    except EOFError:
        print("\nInput interrupted. Exiting login prompt.")
    except KeyboardInterrupt:
        print("\nLogin cancelled by user.")

if __name__ == "__main__":
    # For testing purposes
    login_prompt()
