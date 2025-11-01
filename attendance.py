import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import cv2
import os
import numpy as np
import mysql.connector
import csv
import datetime
import threading
import time
from tkcalendar import DateEntry
import pandas as pd

class Attendance:
    def __init__(self, root):
        logging.info("Initializing Attendance class")
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance System")
        self.root.configure(bg="white")

        # Database config
        self.db_config = {
            'host': "localhost",
            'username': "root",
            'password': "babu1234",
            'database': "face_recognizer"
        }

        # File paths
        self.model_path = "trainer.yml"
        self.cascade_path = "haarcascade_frontalface_default.xml"
        self.attendance_csv = "attendance.csv"

        # Variables
        self.var_teacher = StringVar()
        self.var_credits = StringVar()
        self.var_start_date = StringVar()
        self.var_end_date = StringVar()
        self.var_total_classes = StringVar()
        self.var_filter_date = StringVar()

        # Recognition variables
        self.is_marking = False
        self.cap = None
        self.recognizer = None
        self.face_classifier = None
        self.attendance_records = []

        # ============ GUI SETUP =================

        # --- Top Banner Images ---
        try:
            logging.debug("Loading top banner images for Attendance")
            # First image
            img_top1 = Image.open(r"college_images\↑↑↑ Larger size on website 🔸 A glowing blue cube….jpeg")
            img_top1 = img_top1.resize((510, 130), Image.Resampling.LANCZOS)
            self.photoimg_top1 = ImageTk.PhotoImage(img_top1)

            top_label1 = Label(self.root, image=self.photoimg_top1)
            top_label1.place(x=0, y=0, width=510, height=130)

            # Second image
            img_top2 = Image.open(r"college_images\49f04747-34cb-4f43-b932-78c9cb594a7c.jpeg")
            img_top2 = img_top2.resize((510, 130), Image.Resampling.LANCZOS)
            self.photoimg_top2 = ImageTk.PhotoImage(img_top2)

            top_label2 = Label(self.root, image=self.photoimg_top2)
            top_label2.place(x=510, y=0, width=510, height=130)

            # Third image
            img_top3 = Image.open(r"college_images\I'm trying but I'm so tired and it's late and I'm….jpeg")
            img_top3 = img_top3.resize((510, 130), Image.Resampling.LANCZOS)
            self.photoimg_top3 = ImageTk.PhotoImage(img_top3)

            top_label3 = Label(self.root, image=self.photoimg_top3)
            top_label3.place(x=1020, y=0, width=510, height=130)
            logging.debug("Top banner images loaded successfully")
        except Exception as e:
            logging.error(f"Error loading top banners: {e}")
            top_label = Label(self.root, bg="lightblue", text="Banner Images (1530x130)", font=("arial", 20))
            top_label.place(x=0, y=0, width=1530, height=130)

        # --- Main Title ---
        title_lbl = Label(self.root, text="ATTENDANCE SYSTEM", font=("arial", 30, "bold"), bg="#2c3e50", fg="#27ab83")
        title_lbl.place(x=0, y=130, width=1530, height=50)

        # --- Main Frame ---
        main_frame = Frame(self.root, bg="white", relief="ridge", bd=3)
        main_frame.place(x=0, y=180, width=1530, height=610)

        # --- Left Frame: Configuration ---
        left_frame = LabelFrame(main_frame, text="Configuration", font=("arial", 16, "bold"),
                                bg="white", fg="#2c3e50", relief="ridge", bd=4, padx=5, pady=5)
        left_frame.place(x=10, y=10, width=760, height=590)

        # --- Configuration Content ---
        # Teacher Selection
        Label(left_frame, text="Select Teacher:", font=("arial", 12, "bold"), bg="white").place(x=20, y=20)
        teachers = ["Dr. Smith", "Prof. Johnson", "Ms. Lee", "Dr. Brown", "Prof. Davis", "Ms. Wilson", "Dr. Taylor", "Prof. Anderson"]
        teacher_combo = ttk.Combobox(left_frame, textvariable=self.var_teacher, font=("arial", 11), state="readonly", values=teachers)
        teacher_combo.set("Select Teacher")
        teacher_combo.place(x=150, y=20, width=200, height=30)

        # Course Credits
        Label(left_frame, text="Course Credits:", font=("arial", 12, "bold"), bg="white").place(x=20, y=70)
        credits_combo = ttk.Combobox(left_frame, textvariable=self.var_credits, font=("arial", 11), state="readonly", values=["1", "2", "3", "4"])
        credits_combo.set("Select Credits")
        credits_combo.place(x=150, y=70, width=200, height=30)

        # Semester Start Date
        Label(left_frame, text="Start Date:", font=("arial", 12, "bold"), bg="white").place(x=20, y=120)
        start_date_entry = DateEntry(left_frame, textvariable=self.var_start_date, font=("arial", 11), date_pattern='yyyy-mm-dd')
        start_date_entry.place(x=150, y=120, width=200, height=30)

        # Semester End Date
        Label(left_frame, text="End Date:", font=("arial", 12, "bold"), bg="white").place(x=20, y=170)
        end_date_entry = DateEntry(left_frame, textvariable=self.var_end_date, font=("arial", 11), date_pattern='yyyy-mm-dd')
        end_date_entry.place(x=150, y=170, width=200, height=30)

        # Calculate Classes Button
        calc_btn = Button(left_frame, text="Calculate Total Classes", command=self.calculate_classes,
                          font=("arial", 12, "bold"), bg="#28a745", fg="white", width=20)
        calc_btn.place(x=20, y=220, width=330, height=40)

        # Total Classes Display
        Label(left_frame, text="Total Classes:", font=("arial", 12, "bold"), bg="white").place(x=20, y=280)
        total_classes_entry = Entry(left_frame, textvariable=self.var_total_classes, font=("arial", 11), state="readonly")
        total_classes_entry.place(x=150, y=280, width=200, height=30)

        # Start Attendance Button
        start_btn = Button(left_frame, text="START ATTENDANCE MARKING", command=self.start_attendance_marking,
                           font=("arial", 14, "bold"), bg="#dc3545", fg="white", width=25)
        start_btn.place(x=20, y=330, width=330, height=50)

        # Status Label
        self.status_label = Label(left_frame, text="Ready", font=("arial", 12), bg="white", fg="green")
        self.status_label.place(x=20, y=400)

        # Progress Bar
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(left_frame, variable=self.progress_var, maximum=100, mode='determinate', length=330)
        self.progress_bar.place(x=20, y=440)

        # --- Right Frame: Attendance View ---
        right_frame = LabelFrame(main_frame, text="Attendance Records", font=("arial", 16, "bold"),
                                 bg="white", fg="#2c3e50", relief="ridge", bd=4, padx=5, pady=5)
        right_frame.place(x=780, y=10, width=740, height=590)

        # Filter Section
        filter_frame = Frame(right_frame, bg="white")
        filter_frame.place(x=10, y=10, width=720, height=60)

        Label(filter_frame, text="Filter by Date:", font=("arial", 11, "bold"), bg="white").place(x=10, y=15)
        filter_date_entry = DateEntry(filter_frame, textvariable=self.var_filter_date, font=("arial", 10), date_pattern='yyyy-mm-dd')
        filter_date_entry.place(x=120, y=15, width=120, height=25)

        filter_btn = Button(filter_frame, text="Filter", command=self.filter_attendance,
                           font=("arial", 10, "bold"), bg="#007bff", fg="white", width=8)
        filter_btn.place(x=250, y=12, width=80, height=30)

        show_all_btn = Button(filter_frame, text="Show All", command=self.load_attendance_data,
                             font=("arial", 10, "bold"), bg="#6c757d", fg="white", width=8)
        show_all_btn.place(x=340, y=12, width=80, height=30)

        export_btn = Button(filter_frame, text="Export to Excel", command=self.export_to_excel,
                           font=("arial", 10, "bold"), bg="#28a745", fg="white", width=12)
        export_btn.place(x=430, y=12, width=120, height=30)

        refresh_btn = Button(filter_frame, text="Refresh", command=self.load_attendance_data,
                            font=("arial", 10, "bold"), bg="#17a2b8", fg="white", width=8)
        refresh_btn.place(x=560, y=12, width=80, height=30)

        # Attendance Table
        table_frame = Frame(right_frame, bg="white", relief="ridge", bd=2)
        table_frame.place(x=10, y=80, width=720, height=490)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(table_frame,
                                             columns=("serial", "id", "name", "phone", "date", "time", "teacher", "credits", "total_classes", "percentage"),
                                             xscrollcommand=scroll_x.set,
                                             yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        # Define Headings
        self.attendance_table.heading("serial", text="Serial No")
        self.attendance_table.heading("id", text="Student ID")
        self.attendance_table.heading("name", text="Name")
        self.attendance_table.heading("phone", text="Phone")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("time", text="Time")
        self.attendance_table.heading("teacher", text="Teacher")
        self.attendance_table.heading("credits", text="Credits")
        self.attendance_table.heading("total_classes", text="Total Classes")
        self.attendance_table.heading("percentage", text="Attendance %")

        self.attendance_table["show"] = "headings"

        # Set Column Widths
        self.attendance_table.column("serial", width=80)
        self.attendance_table.column("id", width=100)
        self.attendance_table.column("name", width=150)
        self.attendance_table.column("phone", width=120)
        self.attendance_table.column("date", width=100)
        self.attendance_table.column("time", width=100)
        self.attendance_table.column("teacher", width=120)
        self.attendance_table.column("credits", width=80)
        self.attendance_table.column("total_classes", width=100)
        self.attendance_table.column("percentage", width=100)

        self.attendance_table.pack(fill=BOTH, expand=1)

        # Tag configuration for color coding
        self.attendance_table.tag_configure("low_attendance", background="red", foreground="white")

        # Initialize face recognition components
        init_thread = threading.Thread(target=self.initialize_recognition, daemon=True)
        init_thread.start()

        # Load initial attendance data
        self.load_attendance_data()

        logging.info("Attendance class initialization complete")

    def calculate_classes(self):
        """Calculate total classes based on credits"""
        try:
            credits = int(self.var_credits.get())
            if credits == 1:
                total_classes = 8
            elif credits == 2:
                total_classes = 12
            elif credits == 3:
                total_classes = 16
            elif credits == 4:
                total_classes = 22
            else:
                messagebox.showerror("Error", "Please select valid credits (1-4)", parent=self.root)
                return

            self.var_total_classes.set(str(total_classes))
            messagebox.showinfo("Calculated", f"Total classes for {credits} credits: {total_classes}", parent=self.root)
        except ValueError:
            messagebox.showerror("Error", "Please select credits first", parent=self.root)

    def initialize_recognition(self):
        """Initialize face recognition components"""
        try:
            self.status_label.config(text="Loading trained model...", fg="blue")
            self.progress_var.set(10)
            logging.info("Loading trained model...")
            if os.path.exists(self.model_path):
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.recognizer.read(self.model_path)
                logging.info("Trained model loaded successfully")
            else:
                logging.error(f"Trained model '{self.model_path}' not found.")
                self.status_label.config(text="Error: Model not found", fg="red")
                return

            self.status_label.config(text="Loading face classifier...", fg="blue")
            self.progress_var.set(50)
            logging.info("Loading face classifier...")
            if not os.path.exists(self.cascade_path):
                self.cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")

            self.face_classifier = cv2.CascadeClassifier(self.cascade_path)

            if self.face_classifier.empty():
                logging.error("Could not load face classifier.")
                self.status_label.config(text="Error: Classifier not found", fg="red")
                return

            self.progress_var.set(100)
            self.status_label.config(text="System Ready", fg="green")
            logging.info("Face recognition components initialized")

        except AttributeError:
            logging.critical("cv2.face.LBPHFaceRecognizer_create() not found!")
            self.status_label.config(text="Error: Wrong OpenCV version", fg="red")
        except Exception as e:
            logging.error(f"Error initializing recognition: {e}")
            self.status_label.config(text="Initialization Error", fg="red")

    def start_attendance_marking(self):
        """Start attendance marking process"""
        if self.recognizer is None or self.face_classifier is None:
            messagebox.showerror("Error", "Recognition system is not ready", parent=self.root)
            return

        if self.var_teacher.get() == "Select Teacher":
            messagebox.showerror("Error", "Please select a teacher", parent=self.root)
            return

        if not self.var_total_classes.get():
            messagebox.showerror("Error", "Please calculate total classes first", parent=self.root)
            return

        self.is_marking = True
        self.status_label.config(text="Marking attendance...", fg="orange")
        self.progress_var.set(0)

        # Start attendance marking in a separate thread
        marking_thread = threading.Thread(target=self.mark_attendance_loop, daemon=True)
        marking_thread.start()

    def mark_attendance_loop(self):
        """Main attendance marking loop"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                logging.error("Could not open camera")
                messagebox.showerror("Camera Error", "Could not open camera", parent=self.root)
                self.root.after(0, self.stop_attendance_marking)
                return

            logging.info("Camera opened for attendance marking")
            self.root.after(0, lambda: self.status_label.config(text="Camera active - Look at camera", fg="blue"))

            recognized_students = set()
            start_time = time.time()

            while self.is_marking and (time.time() - start_time) < 30:  # 30 seconds timeout
                ret, frame = self.cap.read()
                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]

                    try:
                        id, confidence = self.recognizer.predict(face_roi)
                        confidence_percent = 100 - confidence

                        if confidence_percent > 60 and id not in recognized_students:
                            # Get student details from database
                            student_details = self.get_student_details(id)
                            if student_details:
                                self.mark_attendance(student_details)
                                recognized_students.add(id)
                                logging.info(f"Attendance marked for Student ID: {id}")
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                cv2.putText(frame, f"ID: {id} - Marked", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                            else:
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        elif confidence_percent > 40:
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                            cv2.putText(frame, f"ID: {id}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

                    except cv2.error:
                        continue

                cv2.imshow("Attendance Marking - Press 'q' to stop", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.is_marking = False
                    break

            logging.info("Attendance marking loop finished")

        except Exception as e:
            logging.error(f"Error in attendance marking: {e}")
            messagebox.showerror("Error", f"Attendance marking error: {str(e)}", parent=self.root)

        finally:
            if self.cap and self.cap.isOpened():
                self.cap.release()
            cv2.destroyAllWindows()
            self.root.after(0, self.stop_attendance_marking)

    def stop_attendance_marking(self):
        """Stop attendance marking"""
        self.is_marking = False
        self.status_label.config(text="Attendance marking stopped", fg="green")
        self.progress_var.set(0)
        self.load_attendance_data()  # Refresh the table

    def get_student_details(self, student_id):
        """Get student details from database"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            my_cursor = conn.cursor()
            query = "SELECT StudentId, Name, Phone FROM student WHERE StudentId=%s"
            my_cursor.execute(query, (student_id,))
            result = my_cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            logging.error(f"Error getting student details: {e}")
            return None

    def mark_attendance(self, student_details):
        """Mark attendance for a student"""
        try:
            student_id, name, phone = student_details
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            teacher = self.var_teacher.get()
            credits = self.var_credits.get()
            total_classes = self.var_total_classes.get()

            # Calculate serial number
            serial_no = len(self.attendance_records) + 1

            # Store in memory
            record = [serial_no, student_id, name, phone, date, time_str, teacher, credits, total_classes]
            self.attendance_records.append(record)

            # Write to CSV
            with open(self.attendance_csv, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(record)

            # Save to database
            self.save_to_database(student_id, name, phone, date, time_str, teacher, credits, total_classes)

            # Auto-generate Excel file with attendance and date in filename
            self.auto_export_to_excel()

            logging.info(f"Attendance marked: {record}")

        except Exception as e:
            logging.error(f"Error marking attendance: {e}")

    def save_to_database(self, student_id, name, phone, date, time_str, teacher, credits, total_classes):
        """Save attendance record to database"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            my_cursor = conn.cursor()

            # Create attendance table if not exists
            my_cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id VARCHAR(20),
                    name VARCHAR(100),
                    phone VARCHAR(20),
                    date DATE,
                    time TIME,
                    teacher VARCHAR(100),
                    credits INT,
                    total_classes INT
                )
            """)

            # Insert record
            query = """
                INSERT INTO attendance (student_id, name, phone, date, time, teacher, credits, total_classes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (student_id, name, phone, date, time_str, teacher, credits, total_classes)
            my_cursor.execute(query, values)
            conn.commit()

            logging.info(f"Attendance saved to database for Student ID: {student_id}")

        except mysql.connector.Error as e:
            logging.error(f"Database error: {e}")
        except Exception as e:
            logging.error(f"Error saving to database: {e}")
        finally:
            if conn:
                conn.close()

    def load_attendance_data(self):
        """Load attendance data from CSV and display in table"""
        try:
            self.attendance_table.delete(*self.attendance_table.get_children())

            if not os.path.exists(self.attendance_csv):
                return

            with open(self.attendance_csv, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 6:
                        serial = row[0]
                        id = row[1]
                        name = row[2]
                        phone = row[3]
                        date = row[4]
                        time_str = row[5]
                        teacher = row[6] if len(row) > 6 else "N/A"
                        credits = row[7] if len(row) > 7 else "N/A"
                        total_classes = row[8] if len(row) > 8 else "N/A"

                        # Calculate attendance percentage (simplified - in real system would be more complex)
                        # For demo, we'll assume each record is one attendance
                        percentage = "100%"  # Placeholder

                        # Color code based on percentage
                        tags = ()
                        try:
                            perc_value = float(percentage.rstrip('%'))
                            if perc_value < 75:
                                tags = ("low_attendance",)
                        except ValueError:
                            pass

                        self.attendance_table.insert("", END, values=(serial, id, name, phone, date, time_str, teacher, credits, total_classes, percentage), tags=tags)

        except Exception as e:
            logging.error(f"Error loading attendance data: {e}")

    def filter_attendance(self):
        """Filter attendance records by date"""
        try:
            filter_date = self.var_filter_date.get()
            if not filter_date:
                messagebox.showerror("Error", "Please select a date to filter", parent=self.root)
                return

            self.attendance_table.delete(*self.attendance_table.get_children())

            if not os.path.exists(self.attendance_csv):
                return

            with open(self.attendance_csv, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 6:
                        serial = row[0]
                        id = row[1]
                        name = row[2]
                        phone = row[3]
                        date = row[4]
                        time_str = row[5]
                        teacher = row[6] if len(row) > 6 else "N/A"
                        credits = row[7] if len(row) > 7 else "N/A"
                        total_classes = row[8] if len(row) > 8 else "N/A"
                        if date == filter_date:
                            percentage = "100%"  # Placeholder
                            tags = ()
                            try:
                                perc_value = float(percentage.rstrip('%'))
                                if perc_value < 75:
                                    tags = ("low_attendance",)
                            except ValueError:
                                pass

                            self.attendance_table.insert("", END, values=(serial, id, name, phone, date, time_str, teacher, credits, total_classes, percentage), tags=tags)

        except Exception as e:
            logging.error(f"Error filtering attendance: {e}")

    def auto_export_to_excel(self):
        """Auto-export attendance data to Excel file with date in filename"""
        try:
            if not os.path.exists(self.attendance_csv):
                return

            # Read CSV data
            df = pd.read_csv(self.attendance_csv, header=None, names=["Serial No", "Student ID", "Name", "Phone", "Date", "Time", "Teacher", "Credits", "Total Classes"])

            # Add attendance percentage column (placeholder)
            df["Attendance %"] = "100%"

            # Generate filename with current date
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            filename = f"attendance_{current_date}.xlsx"

            # Save to current directory
            df.to_excel(filename, index=False)
            logging.info(f"Auto-exported attendance to {filename}")

        except Exception as e:
            logging.error(f"Error in auto-export to Excel: {e}")

    def export_to_excel(self):
        """Export attendance data to Excel file"""
        try:
            if not os.path.exists(self.attendance_csv):
                messagebox.showerror("Error", "No attendance data to export", parent=self.root)
                return

            # Read CSV data
            df = pd.read_csv(self.attendance_csv, header=None, names=["Serial No", "Student ID", "Name", "Phone", "Date", "Time", "Teacher", "Credits", "Total Classes"])

            # Add attendance percentage column (placeholder)
            df["Attendance %"] = "100%"

            # Ask for save location
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                                   title="Save Attendance Report")

            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Attendance report exported to {file_path}", parent=self.root)

        except Exception as e:
            logging.error(f"Error exporting to Excel: {e}")
            messagebox.showerror("Error", f"Export failed: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
