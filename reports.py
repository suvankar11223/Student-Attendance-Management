from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import calendar

class Reports:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Reports - Face Recognition Attendance System")

        # ============ DATABASE CONNECTION =================
        self.db_config = {
            'host': "localhost",
            'username': "root",
            'password': "your_password",  # Update with your MySQL password
            'database': "face_recognizer"
        }

        # ============ GUI SETUP =================

        # --- Top Banner Images ---
        try:
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
        except Exception as e:
            top_label = Label(self.root, bg="lightblue", text="Banner Images (1530x130)", font=("arial", 20))
            top_label.place(x=0, y=0, width=1530, height=130)

        # --- Main Title ---
        title_lbl = Label(self.root, text="📊 ATTENDANCE REPORTS & ANALYTICS", font=("arial", 25, "bold"), bg="#2c3e50", fg="#27ab83")
        title_lbl.place(x=0, y=130, width=1530, height=50)

        # --- Main Frame ---
        main_frame = Frame(self.root, bg="white", relief="ridge", bd=3)
        main_frame.place(x=0, y=180, width=1530, height=610)

        # --- Tab Control ---
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # --- Daily Attendance Tab ---
        self.daily_tab = Frame(self.tab_control, bg="white")
        self.tab_control.add(self.daily_tab, text="📅 Daily Attendance View")

        # --- Individual Reports Tab ---
        self.individual_tab = Frame(self.tab_control, bg="white")
        self.tab_control.add(self.individual_tab, text="👤 Individual Student Reports")

        # Initialize tabs
        self.setup_daily_tab()
        self.setup_individual_tab()

    def setup_daily_tab(self):
        """Setup the Daily Attendance View tab"""
        # Date Selection Frame
        date_frame = LabelFrame(self.daily_tab, text="Select Date", bg="white", fg="#2c3e50", font=("arial", 12, "bold"))
        date_frame.place(x=10, y=10, width=400, height=100)

        # Date Entry
        Label(date_frame, text="Date (YYYY-MM-DD):", bg="white", font=("arial", 10)).grid(row=0, column=0, padx=10, pady=10)
        self.date_entry = Entry(date_frame, font=("arial", 10), width=15)
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        # Generate Report Button
        generate_btn = Button(date_frame, text="📊 Generate Report", command=self.generate_daily_report,
                            bg="#27ab83", fg="white", font=("arial", 10, "bold"), relief="raised", bd=3)
        generate_btn.grid(row=0, column=2, padx=10, pady=10)

        # Results Frame
        results_frame = LabelFrame(self.daily_tab, text="Attendance Report", bg="white", fg="#2c3e50", font=("arial", 12, "bold"))
        results_frame.place(x=10, y=120, width=1500, height=450)

        # Treeview for attendance data
        columns = ("Student ID", "Name", "Phone", "Status", "Time")
        self.daily_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)

        # Define headings
        for col in columns:
            self.daily_tree.heading(col, text=col, anchor=CENTER)
            self.daily_tree.column(col, width=150, anchor=CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=VERTICAL, command=self.daily_tree.yview)
        self.daily_tree.configure(yscrollcommand=scrollbar.set)

        self.daily_tree.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=RIGHT, fill=Y, pady=10)

        # Summary Labels
        summary_frame = Frame(results_frame, bg="white")
        summary_frame.pack(fill=X, padx=10, pady=5)

        self.present_label = Label(summary_frame, text="Present: 0", bg="white", fg="green", font=("arial", 12, "bold"))
        self.present_label.pack(side=LEFT, padx=20)

        self.absent_label = Label(summary_frame, text="Absent: 0", bg="white", fg="red", font=("arial", 12, "bold"))
        self.absent_label.pack(side=LEFT, padx=20)

        self.total_label = Label(summary_frame, text="Total Students: 0", bg="white", fg="blue", font=("arial", 12, "bold"))
        self.total_label.pack(side=LEFT, padx=20)

    def setup_individual_tab(self):
        """Setup the Individual Student Reports tab"""
        # Search Frame
        search_frame = LabelFrame(self.individual_tab, text="Student Search", bg="white", fg="#2c3e50", font=("arial", 12, "bold"))
        search_frame.place(x=10, y=10, width=400, height=100)

        # Search Entry
        Label(search_frame, text="Student Name/ID:", bg="white", font=("arial", 10)).grid(row=0, column=0, padx=10, pady=10)
        self.search_entry = Entry(search_frame, font=("arial", 10), width=20)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        # Search Button
        search_btn = Button(search_frame, text="🔍 Search", command=self.search_student,
                          bg="#3498db", fg="white", font=("arial", 10, "bold"), relief="raised", bd=3)
        search_btn.grid(row=0, column=2, padx=10, pady=10)

        # Student Info Frame
        info_frame = LabelFrame(self.individual_tab, text="Student Information", bg="white", fg="#2c3e50", font=("arial", 12, "bold"))
        info_frame.place(x=10, y=120, width=400, height=200)

        # Student details labels
        self.student_name_label = Label(info_frame, text="Name: ", bg="white", font=("arial", 10))
        self.student_name_label.pack(anchor=W, padx=10, pady=5)

        self.student_id_label = Label(info_frame, text="ID: ", bg="white", font=("arial", 10))
        self.student_id_label.pack(anchor=W, padx=10, pady=5)

        self.student_phone_label = Label(info_frame, text="Phone: ", bg="white", font=("arial", 10))
        self.student_phone_label.pack(anchor=W, padx=10, pady=5)

        self.attendance_percentage_label = Label(info_frame, text="Attendance %: ", bg="white", font=("arial", 12, "bold"), fg="blue")
        self.attendance_percentage_label.pack(anchor=W, padx=10, pady=10)

        # Calendar Frame
        calendar_frame = LabelFrame(self.individual_tab, text="Attendance Calendar", bg="white", fg="#2c3e50", font=("arial", 12, "bold"))
        calendar_frame.place(x=420, y=10, width=1090, height=450)

        # Month/Year selection
        month_frame = Frame(calendar_frame, bg="white")
        month_frame.pack(fill=X, padx=10, pady=5)

        Label(month_frame, text="Month:", bg="white", font=("arial", 10)).pack(side=LEFT, padx=5)
        self.month_var = StringVar()
        self.month_combo = ttk.Combobox(month_frame, textvariable=self.month_var, width=10,
                                      values=[calendar.month_name[i] for i in range(1, 13)])
        self.month_combo.pack(side=LEFT, padx=5)
        self.month_combo.set(calendar.month_name[datetime.now().month])

        Label(month_frame, text="Year:", bg="white", font=("arial", 10)).pack(side=LEFT, padx=20)
        self.year_var = StringVar()
        self.year_combo = ttk.Combobox(month_frame, textvariable=self.year_var, width=8,
                                     values=[str(i) for i in range(2020, 2031)])
        self.year_combo.pack(side=LEFT, padx=5)
        self.year_combo.set(str(datetime.now().year))

        # Generate Calendar Button
        gen_cal_btn = Button(month_frame, text="📅 Generate Calendar", command=self.generate_calendar,
                           bg="#e74c3c", fg="white", font=("arial", 10, "bold"), relief="raised", bd=3)
        gen_cal_btn.pack(side=LEFT, padx=20)

        # Calendar display area
        self.calendar_frame = Frame(calendar_frame, bg="white")
        self.calendar_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Legend
        legend_frame = Frame(calendar_frame, bg="white")
        legend_frame.pack(fill=X, padx=10, pady=5)

        Label(legend_frame, text="🟢 Present", bg="white", fg="green", font=("arial", 9)).pack(side=LEFT, padx=10)
        Label(legend_frame, text="🔴 Absent", bg="white", fg="red", font=("arial", 9)).pack(side=LEFT, padx=10)
        Label(legend_frame, text="⚪ No Data", bg="white", fg="gray", font=("arial", 9)).pack(side=LEFT, padx=10)

    def generate_daily_report(self):
        """Generate daily attendance report"""
        selected_date = self.date_entry.get().strip()

        if not selected_date:
            messagebox.showerror("Error", "Please enter a date")
            return

        try:
            # Clear existing data
            for item in self.daily_tree.get_children():
                self.daily_tree.delete(item)

            # Connect to database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Get all students
            cursor.execute("SELECT StudentId, Name, Phone FROM student")
            all_students = cursor.fetchall()

            # Get present students for the date
            cursor.execute("""
                SELECT student_id, name, phone, time
                FROM attendance
                WHERE date = %s
            """, (selected_date,))
            present_students = cursor.fetchall()

            conn.close()

            # Create present students dict for quick lookup
            present_dict = {student[0]: student for student in present_students}

            present_count = 0
            absent_count = 0

            # Process each student
            for student in all_students:
                student_id, name, phone = student

                if student_id in present_dict:
                    # Present
                    time_attended = present_dict[student_id][3]
                    self.daily_tree.insert("", END, values=(student_id, name, phone, "Present", time_attended))
                    present_count += 1
                else:
                    # Absent
                    self.daily_tree.insert("", END, values=(student_id, name, phone, "Absent", "-"))
                    absent_count += 1

            # Update summary
            self.present_label.config(text=f"Present: {present_count}")
            self.absent_label.config(text=f"Absent: {absent_count}")
            self.total_label.config(text=f"Total Students: {len(all_students)}")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to generate report: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def search_student(self):
        """Search for a student by name or ID"""
        search_term = self.search_entry.get().strip()

        if not search_term:
            messagebox.showerror("Error", "Please enter a student name or ID")
            return

        try:
            # Connect to database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Search for student
            cursor.execute("""
                SELECT StudentId, Name, Phone FROM student
                WHERE StudentId = %s OR Name LIKE %s
            """, (search_term, f"%{search_term}%"))

            student = cursor.fetchone()

            if student:
                student_id, name, phone = student

                # Update student info
                self.student_name_label.config(text=f"Name: {name}")
                self.student_id_label.config(text=f"ID: {student_id}")
                self.student_phone_label.config(text=f"Phone: {phone}")

                # Calculate attendance percentage
                cursor.execute("""
                    SELECT COUNT(*) FROM attendance WHERE student_id = %s
                """, (student_id,))
                attended_days = cursor.fetchone()[0]

                # Get total possible days (assuming 30 days per month for simplicity)
                # In a real system, you'd calculate based on actual class days
                total_days = 30  # This could be made configurable

                if total_days > 0:
                    percentage = (attended_days / total_days) * 100
                    self.attendance_percentage_label.config(text=f"Attendance %: {percentage:.1f}%")
                else:
                    self.attendance_percentage_label.config(text="Attendance %: N/A")

                # Store current student for calendar generation
                self.current_student_id = student_id

                messagebox.showinfo("Success", f"Student found: {name}")
            else:
                messagebox.showerror("Not Found", "Student not found")
                self.clear_student_info()

            conn.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to search student: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def generate_calendar(self):
        """Generate attendance calendar for the selected student"""
        if not hasattr(self, 'current_student_id'):
            messagebox.showerror("Error", "Please search for a student first")
            return

        month_name = self.month_var.get()
        year = int(self.year_var.get())

        # Convert month name to number
        month_names = list(calendar.month_name)
        month = month_names.index(month_name)

        try:
            # Connect to database
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Get attendance data for the month
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]}"

            cursor.execute("""
                SELECT DATE(date) as attendance_date
                FROM attendance
                WHERE student_id = %s AND date BETWEEN %s AND %s
            """, (self.current_student_id, start_date, end_date))

            attendance_dates = [row[0] for row in cursor.fetchall()]
            conn.close()

            # Clear previous calendar
            for widget in self.calendar_frame.winfo_children():
                widget.destroy()

            # Create calendar grid
            cal = calendar.monthcalendar(year, month)

            # Days of week header
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            for i, day in enumerate(days):
                Label(self.calendar_frame, text=day, bg="#f8f9fa", font=("arial", 10, "bold"),
                      relief="ridge", bd=1).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

            # Calendar days
            for week_num, week in enumerate(cal, 1):
                for day_num, day in enumerate(week):
                    if day == 0:
                        # Empty cell
                        Label(self.calendar_frame, text="", bg="white").grid(row=week_num, column=day_num, sticky="nsew", padx=1, pady=1)
                    else:
                        # Check if student was present on this day
                        current_date = f"{year}-{month:02d}-{day:02d}"
                        if current_date in [str(d) for d in attendance_dates]:
                            # Present - Green
                            bg_color = "#d4edda"
                            fg_color = "#155724"
                        else:
                            # Absent - Red
                            bg_color = "#f8d7da"
                            fg_color = "#721c24"

                        Label(self.calendar_frame, text=str(day), bg=bg_color, fg=fg_color,
                              font=("arial", 10), relief="ridge", bd=1).grid(row=week_num, column=day_num, sticky="nsew", padx=1, pady=1)

            # Configure grid weights
            for i in range(7):
                self.calendar_frame.grid_columnconfigure(i, weight=1)
            for i in range(len(cal) + 1):
                self.calendar_frame.grid_rowconfigure(i, weight=1)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to generate calendar: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_student_info(self):
        """Clear student information labels"""
        self.student_name_label.config(text="Name: ")
        self.student_id_label.config(text="ID: ")
        self.student_phone_label.config(text="Phone: ")
        self.attendance_percentage_label.config(text="Attendance %: ")

if __name__ == "__main__":
    root = Tk()
    obj = Reports(root)
    root.mainloop()
