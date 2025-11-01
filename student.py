import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import mysql.connector
from tkcalendar import DateEntry
import cv2
import os

class Student:
    def __init__(self, root):
        logging.info("Initializing Student class")
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Student Attendance System")
        self.root.configure(bg="white")
        
        # --- Store DB config (DO NOT CONNECT YET) ---
        self.db_config = {
            'host': "localhost",
            'username': "root",
            'password': "babu1234",  # Using your password
            'database': "face_recognizer"
        }
        logging.debug("Root window configured")

        # ============ Variables =================
        # Left Frame
        self.var_dept = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar() # Re-added
        self.var_roll = StringVar() # Re-added
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar() # Re-added
        self.var_teacher = StringVar()
        self.var_radio1 = StringVar()

        # Right Frame
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()



        # --- Top Banner Images (Three images side by side) ---
        try:
            logging.debug("Loading top banner images")
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
        title_lbl = Label(self.root, text="STUDENT MANAGEMENT SYSTEM", 
                          font=("arial", 30, "bold"), bg="#2c3e50", fg="#27ab83") 
        title_lbl.place(x=0, y=130, width=1530, height=50)

        # Main Content Frame
        main_frame = Frame(self.root, bg="white", relief="ridge", bd=3)
        main_frame.place(x=0, y=180, width=1530, height=610) # Adjusted main frame height to fit everything better

        # Left Frame - Student Details
        left_frame = LabelFrame(main_frame, text="Student Details",
                                font=("arial", 16, "bold"),
                                bg="white", fg="#2c3e50", relief="ridge", bd=4, padx=5, pady=5) # Added padding
        left_frame.place(x=10, y=10, width=760, height=590)

        # Right Frame - Student Details (Search & Table)
        right_frame = LabelFrame(main_frame, text="Student Details",
                                 font=("arial", 16, "bold"),
                                 bg="white", fg="#2c3e50", relief="ridge", bd=4, padx=5, pady=5) # Added padding
        right_frame.place(x=780, y=10, width=740, height=590)

        # ================= LEFT FRAME CONTENT =================
        self.create_left_frame_content(left_frame)

        # ================= RIGHT FRAME CONTENT =================
        self.create_right_frame_content(right_frame)

        # --- Fetch initial data AFTER UI is built ---
        self.fetch_data()
        logging.info("Student class initialization complete")

    def create_left_frame_content(self, parent):
        """Create organized left frame content based on the screenshot"""
        logging.debug("Creating left frame content")

        # --- Left Banner Image ---
        try:
            logging.debug("Loading left banner image")
            img_left_banner = Image.open(r"college_images\Face recognition technology in the modern….jpeg")
            img_left_banner = img_left_banner.resize((700, 100), Image.Resampling.LANCZOS)
            self.photoimg_left_banner = ImageTk.PhotoImage(img_left_banner)

            left_banner_label = Label(parent, image=self.photoimg_left_banner)
            left_banner_label.place(x=15, y=5, width=700, height=100)
            logging.debug("Left banner image loaded successfully")
        except Exception as e:
            logging.error(f"Error loading left banner: {e}")
            left_banner_label = Label(parent, bg="lightgray", text="Left Banner (700x100)", font=("arial", 16))
            left_banner_label.place(x=15, y=5, width=700, height=100)

        # Current Course Information
        course_frame = LabelFrame(parent, text="Current Course Information", 
                                  font=("arial", 14, "bold"), 
                                  bg="white", fg="#2c3e50", relief="ridge", bd=2, padx=5, pady=5)
        course_frame.place(x=5, y=110, width=740, height=120) # Adjusted width and x for padding

        # Department
        Label(course_frame, text="Department", font=("arial", 11, "bold"), 
              bg="white", anchor="w").place(x=15, y=5, width=90, height=30)
        departments = ["Select Department", "Computer Science", "Information Technology", "Electrical Engineering",
                       "Mechanical Engineering", "Civil Engineering"] 
        dept_combo = ttk.Combobox(course_frame, textvariable=self.var_dept, font=("arial", 11), state="readonly", values=departments)
        dept_combo.set("Select Department")
        dept_combo.place(x=115, y=5, width=220, height=30)

        # Course
        Label(course_frame, text="Course", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=360, y=5, width=80, height=30)
        course_combo = ttk.Combobox(course_frame, textvariable=self.var_course, font=("arial", 11), state="readonly",
                                    values=["Select Course", "B.Tech", "M.Tech", "B.Sc", "M.Sc"])
        course_combo.set("Select Course")
        course_combo.place(x=450, y=5, width=220, height=30)

        # Year
        Label(course_frame, text="Year", font=("arial", 11, "bold"), 
              bg="white", anchor="w").place(x=15, y=50, width=80, height=30)
        year_combo = ttk.Combobox(course_frame, textvariable=self.var_year, font=("arial", 11), state="readonly",
                                  values=["Select Year", "2023", "2024", "2025", "2026"])
        year_combo.set("Select Year")
        year_combo.place(x=115, y=50, width=220, height=30)

        # Semester
        Label(course_frame, text="Semester", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=360, y=50, width=80, height=30)
        semester_combo = ttk.Combobox(course_frame, textvariable=self.var_semester, font=("arial", 11), state="readonly",
                                      values=["Select Semester", "Semester 1", "Semester 2", "Semester 3", "Semester 4"])
        semester_combo.set("Select Semester")
        semester_combo.place(x=450, y=50, width=220, height=30)

        # Class Student Information Form
        student_frame = LabelFrame(parent, text="Class Student Information", 
                                   font=("arial", 14, "bold"), 
                                   bg="white", fg="#2c3e50", relief="ridge", bd=2, padx=5, pady=5)
        student_frame.place(x=5, y=240, width=740, height=330) 

        # --- Column 1 ---
        # Student ID
        Label(student_frame, text="StudentID:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=15, y=5, width=120, height=25)
        Entry(student_frame, textvariable=self.var_std_id, font=("arial", 11), relief="solid", bd=1).place(x=140, y=5, width=200, height=28)

        # Class Division 
        Label(student_frame, text="Class Division:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=15, y=45, width=120, height=25)
        Entry(student_frame, textvariable=self.var_div, font=("arial", 11), relief="solid", bd=1).place(x=140, y=45, width=200, height=28)
        
        # Gender
        Label(student_frame, text="Gender:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=15, y=85, width=120, height=25)
        gender_combo = ttk.Combobox(student_frame, textvariable=self.var_gender, font=("arial", 11), state="readonly",
                                    values=["Select Gender", "Male", "Female", "Rather not to answer"])
        gender_combo.set("Select Gender")
        gender_combo.place(x=140, y=85, width=200, height=28)

        # Email
        Label(student_frame, text="Email:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=15, y=125, width=120, height=25)
        Entry(student_frame, textvariable=self.var_email, font=("arial", 11), relief="solid", bd=1).place(x=140, y=125, width=200, height=28)

        # Address 
        Label(student_frame, text="Address:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=15, y=165, width=120, height=25)
        Entry(student_frame, textvariable=self.var_address, font=("arial", 11), relief="solid", bd=1).place(x=140, y=165, width=200, height=28)


        # --- Column 2 ---
        # Student Name
        Label(student_frame, text="Student Name:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=360, y=5, width=120, height=25)
        Entry(student_frame, textvariable=self.var_std_name, font=("arial", 11), relief="solid", bd=1).place(x=490, y=5, width=200, height=28)

        # Roll No 
        Label(student_frame, text="Roll No:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=360, y=45, width=120, height=25)
        Entry(student_frame, textvariable=self.var_roll, font=("arial", 11), relief="solid", bd=1).place(x=490, y=45, width=200, height=28)

        # DOB
        Label(student_frame, text="DOB:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=360, y=85, width=120, height=25)
        DateEntry(student_frame, textvariable=self.var_dob, font=("arial", 11), date_pattern='yyyy-mm-dd', relief="solid", bd=1).place(x=490, y=85, width=200, height=28)

        # Phone No
        Label(student_frame, text="Phone No:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=360, y=125, width=120, height=25)
        Entry(student_frame, textvariable=self.var_phone, font=("arial", 11), relief="solid", bd=1).place(x=490, y=125, width=200, height=28)

        # Teacher Name
        Label(student_frame, text="Teacher Name:", font=("arial", 11, "bold"),
              bg="white", anchor="w").place(x=360, y=165, width=120, height=25)
        Entry(student_frame, textvariable=self.var_teacher, font=("arial", 11), relief="solid", bd=1).place(x=490, y=165, width=200, height=28)

        # Radio Buttons
        ttk.Radiobutton(student_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes").place(x=15, y=205)
        ttk.Radiobutton(student_frame, variable=self.var_radio1, text="No Photo Sample", value="No").place(x=170, y=205)
        self.var_radio1.set("No") # Default value

        # Button Frame - Using grid for clean alignment
        btn_frame = Frame(student_frame, bg="white", bd=0)
        btn_frame.place(x=0, y=235, width=730, height=40) # Adjusted height for one row

        button_width = 9 # Adjusted width for 5 buttons

        # First row of buttons
        Button(btn_frame, text="Save", command=self.add_data, font=("arial", 10, "bold"), bg="#28a745", fg="white", width=button_width).grid(row=0, column=0, padx=2, pady=5)
        Button(btn_frame, text="Update", command=self.update_data, font=("arial", 10, "bold"), bg="#007bff", fg="white", width=button_width).grid(row=0, column=1, padx=2, pady=5)
        Button(btn_frame, text="Delete", command=self.delete_data, font=("arial", 10, "bold"), bg="#dc3545", fg="white", width=button_width).grid(row=0, column=2, padx=2, pady=5)
        Button(btn_frame, text="Reset", command=self.reset_data, font=("arial", 10, "bold"), bg="#6c757d", fg="white", width=button_width).grid(row=0, column=3, padx=2, pady=5)
        Button(btn_frame, text="Take Photo Sample", command=self.take_photo_sample, font=("arial", 10, "bold"), bg="#17a2b8", fg="white", width=button_width).grid(row=0, column=4, padx=2, pady=5)




    def create_right_frame_content(self, parent):
        """Create organized right frame content (Search & Table)"""
        logging.debug("Creating right frame content")

        # --- Right Banner Image ---
        try:
            logging.debug("Loading right banner image")
            img_right_banner = Image.open(r"college_images\Facial recognition technology is changing law….jpeg")
            img_right_banner = img_right_banner.resize((700, 100), Image.Resampling.LANCZOS)
            self.photoimg_right_banner = ImageTk.PhotoImage(img_right_banner)

            right_banner_label = Label(parent, image=self.photoimg_right_banner)
            right_banner_label.place(x=15, y=5, width=700, height=100)
            logging.debug("Right banner image loaded successfully")
        except Exception as e:
            logging.error(f"Error loading right banner: {e}")
            right_banner_label = Label(parent, bg="lightgray", text="Right Banner (700x100)", font=("arial", 16))
            right_banner_label.place(x=15, y=5, width=700, height=100)
        
        # Search System Frame
        search_frame = LabelFrame(parent, text="Search System", 
                                  font=("arial", 14, "bold"), 
                                  bg="white", fg="#2c3e50", relief="ridge", bd=2, padx=5, pady=5)
        search_frame.place(x=5, y=110, width=730, height=80)

        Label(search_frame, text="Search By:", font=("arial", 11, "bold"), 
              bg="white", anchor="w").place(x=10, y=10, width=90, height=30) 
        
        search_combo = ttk.Combobox(search_frame, textvariable=self.var_search_by, font=("arial", 11), state="readonly",
                                    values=["Select", "Roll No", "Student ID", "Name"])
        search_combo.set("Select")
        search_combo.place(x=100, y=10, width=150, height=30) 

        search_entry = Entry(search_frame, textvariable=self.var_search_txt, font=("arial", 11), relief="solid", bd=1)
        search_entry.place(x=260, y=10, width=180, height=30) 

        Button(search_frame, text="Search", font=("arial", 10, "bold"), 
               bg="#007bff", fg="white", width=10).place(x=450, y=8, width=120, height=35) 
        Button(search_frame, text="Show All", font=("arial", 10, "bold"), 
               bg="#6c757d", fg="white", width=10).place(x=590, y=8, width=120, height=35) 

        # Table Frame (Treeview)
        table_frame = Frame(parent, bg="white", relief="ridge", bd=2)
        table_frame.place(x=5, y=195, width=730, height=370)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # --- (FIXED) --- Changed columns to match 14-column database
        self.student_table = ttk.Treeview(table_frame,
                                          columns=("dep", "course", "year", "sem", "id", "name", "div", "roll", "gender", "dob", "email", "phone", "address", "teacher"),
                                          xscrollcommand=scroll_x.set,
                                          yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Define Headings
        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="Student ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("div", text="Division")
        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        # --- (FIXED) --- Removed PhotoSample heading
        # self.student_table.heading("photo", text="PhotoSample") 

        self.student_table["show"] = "headings"

        # Set Column Widths
        self.student_table.column("dep", width=120)
        self.student_table.column("course", width=90)
        self.student_table.column("year", width=70)
        self.student_table.column("sem", width=70)
        self.student_table.column("id", width=90)
        self.student_table.column("name", width=120)
        self.student_table.column("div", width=80)
        self.student_table.column("roll", width=80)
        self.student_table.column("gender", width=80)
        self.student_table.column("dob", width=90)
        self.student_table.column("email", width=120)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=120)
        self.student_table.column("teacher", width=120)
        # --- (FIXED) --- Removed PhotoSample column
        # self.student_table.column("photo", width=90)

        self.student_table.pack(fill=BOTH, expand=1)

        # --- (ADDED) --- Bind the click event to the table
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)
        
        # --- (REMOVED) --- Do not fetch here, fetch at end of __init__
        # self.fetch_data() 


    # ================= BUTTON COMMAND METHODS =================
    
    def add_data(self):
        """Add student data to the MySQL database"""
        logging.info("Add data button clicked")

        # --- Validation ---
        if self.var_dept.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        # Phone number validation
        phone = self.var_phone.get()
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Error", "Phone number must be exactly 10 digits", parent=self.root)
            return
        
        try:
            # --- 1. Connect (local connection) ---
            logging.debug("Connecting to DB for add_data")
            conn = mysql.connector.connect(**self.db_config)
            my_cursor = conn.cursor()
            
            # --- 2. Execute (FIXED QUERY) ---
            # Using the column names from your image
            query = """INSERT INTO student (Department, Course, Year, Semester, StudentId, Name, Division, Roll, Gender, DOB, Email, Phone, Address, Teacher)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            # (FIXED VALUES - removed the 15th item)
            values = (
                self.var_dept.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_std_id.get(),
                self.var_std_name.get(),
                self.var_div.get(),
                self.var_roll.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_email.get(),
                self.var_phone.get(),
                self.var_address.get(),
                self.var_teacher.get()
                # self.var_radio1.get() <-- Removed this, as the column doesn't exist
            )
            
            my_cursor.execute(query, values)
            
            # --- 3. Commit and Close ---
            conn.commit()
            conn.close()
            
            logging.info(f"Successfully added student ID: {self.var_std_id.get()}")
            messagebox.showinfo("Success", "Student details have been added successfully", parent=self.root)
            
            self.fetch_data() # Refresh the table
            self.reset_data() # Clear the form
        
        except mysql.connector.Error as err:
            if err.errno == 1062: # Duplicate entry
                logging.warning(f"Failed to add duplicate Student ID: {self.var_std_id.get()}")
                messagebox.showerror("Error", f"Student ID {self.var_std_id.get()} already exists.", parent=self.root)
            else:
                logging.error(f"Database error in add_data: {err}")
                messagebox.showerror("Database Error", f"An error occurred: {str(err)}", parent=self.root)
        except Exception as e:
            logging.error(f"Unexpected error in add_data: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", parent=self.root)

    def fetch_data(self):
        """Fetch all student data from database and populate the table"""
        logging.debug("Connecting to DB for fetch_data")
        try:
            conn = mysql.connector.connect(**self.db_config)
            my_cursor = conn.cursor()
            
            my_cursor.execute("SELECT * FROM student")
            data = my_cursor.fetchall()
            
            if len(data) != 0:
                # Clear existing table data
                self.student_table.delete(*self.student_table.get_children())
                # Insert new data
                for row in data:
                    self.student_table.insert("", END, values=row)
                logging.info(f"Fetched and displayed {len(data)} records")
            else:
                self.student_table.delete(*self.student_table.get_children())
                logging.info("No records found in database")
            
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error in fetch_data: {e}")
            messagebox.showerror("Error", f"An error occurred while fetching data: {str(e)}", parent=self.root)

    def get_cursor(self, event=""):
        """Get data from the clicked row in the table and load it into the form"""
        logging.debug("Table row clicked, calling get_cursor")
        try:
            cursor_row = self.student_table.focus()
            if not cursor_row: # Do nothing if no row is selected
                return
                
            content = self.student_table.item(cursor_row)
            data = content["values"]
            
            if data: # Check if data is not empty
                # --- (FIXED) --- Data now has 14 columns
                self.var_dept.set(data[0])
                self.var_course.set(data[1])
                self.var_year.set(data[2])
                self.var_semester.set(data[3])
                self.var_std_id.set(data[4])    # This is StudentId
                self.var_std_name.set(data[5])  # This is StudentName
                self.var_div.set(data[6])
                self.var_roll.set(data[7])      # This is Roll
                self.var_gender.set(data[8])
                self.var_dob.set(data[9])
                self.var_email.set(data[10])
                self.var_phone.set(data[11])
                self.var_address.set(data[12])
                self.var_teacher.set(data[13])
                
                # --- (FIXED) --- Removed data[14] and set radio to default
                self.var_radio1.set("No") 

        except Exception as e:
            logging.error(f"Error in get_cursor (likely clicking empty table or index error): {e}")

    def update_data(self):
        """Update existing student data"""
        logging.info("Update data button clicked")
        if self.var_dept.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All fields are required to update", parent=self.root)
            return

        # Phone number validation
        phone = self.var_phone.get()
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Error", "Phone number must be exactly 10 digits", parent=self.root)
            return
            
        try:
            Update = messagebox.askyesno("Update", "Do you want to update this student's details?", parent=self.root)
            if Update:
                logging.debug("Connecting to DB for update_data")
                conn = mysql.connector.connect(**self.db_config)
                my_cursor = conn.cursor()
                
                # --- (FIXED QUERY) --- Using 14 columns and correct names
                sql_query = """
                UPDATE student SET
                Department=%s, Course=%s, Year=%s, Semester=%s, Name=%s,
                Division=%s, Roll=%s, Gender=%s, DOB=%s, Email=%s,
                Phone=%s, Address=%s, Teacher=%s
                WHERE StudentId=%s
                """
                
                # --- (FIXED TUPLE) --- Removed radio button
                data_tuple = (
                    self.var_dept.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_std_id.get()  # StudentId is the last one for the WHERE clause
                )
                
                my_cursor.execute(sql_query, data_tuple)
                
                conn.commit()
                conn.close()
                
                logging.info(f"Successfully updated student ID: {self.var_std_id.get()}")
                messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)
                
                self.fetch_data() 
                self.reset_data() 
            else:
                logging.info("User cancelled update operation")
                return
        
        except Exception as e:
            logging.error(f"Error in update_data: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)

    def delete_data(self):
        """Delete student data from database"""
        logging.info("Delete data button clicked")
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required to delete", parent=self.root)
            return
            
        try:
            Delete = messagebox.askyesno("Delete", "Are you sure you want to delete this student?", parent=self.root)
            if Delete:
                logging.debug("Connecting to DB for delete_data")
                conn = mysql.connector.connect(**self.db_config)
                my_cursor = conn.cursor()
                
                # --- (FIXED QUERY) ---
                sql_query = "DELETE FROM student WHERE StudentId=%s"
                id_tuple = (self.var_std_id.get(),)
                
                my_cursor.execute(sql_query, id_tuple)
                
                conn.commit()
                conn.close()
                
                logging.info(f"Successfully deleted student ID: {self.var_std_id.get()}")
                messagebox.showinfo("Success", "Student deleted successfully", parent=self.root)
                
                self.fetch_data() 
                self.reset_data() 
            else:
                logging.info("User cancelled delete operation")
                return
        except Exception as e:
            logging.error(f"Error in delete_data: {e}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)

    def take_photo_sample(self):
        """Take photo sample for face recognition using OpenCV"""
        logging.info("Take photo sample button clicked")
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required to take a photo sample.", parent=self.root)
            return

        if self.var_radio1.get() != "Yes":
            messagebox.showinfo("Skipped", "Photo sample radio button is set to 'No'. Skipping...", parent=self.root)
            return

        cap = None
        try:
            student_id = self.var_std_id.get()
            logging.debug(f"Starting photo sample logic for ID: {student_id}")
            messagebox.showinfo("Starting Camera", f"Taking photo sample for Student ID: {student_id}. Look at the camera.", parent=self.root)

            # Create data directory if it doesn't exist
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            # Initialize camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open camera", parent=self.root)
                return

            # Load face classifier
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            if face_classifier.empty():
                messagebox.showerror("Error", "Could not load face classifier", parent=self.root)
                return

            img_count = 0
            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Convert to grayscale for face detection
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Detect faces
                    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                    for (x, y, w, h) in faces:
                        # Draw rectangle around face
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                        # Crop face region
                        face_roi = gray[y:y+h, x:x+w]

                        # Save face sample
                        cv2.imwrite(f"{data_dir}/user.{student_id}.{img_count}.jpg", face_roi)
                        img_count += 1

                    # Display the frame
                    cv2.imshow("Taking Samples...", frame)

                    # Break if Enter key pressed or 100 samples taken
                    if cv2.waitKey(1) == 13 or img_count >= 100:
                        break
            except KeyboardInterrupt:
                logging.warning("Photo sample collection interrupted by user")
                messagebox.showinfo("Interrupted", "Photo sample collection was interrupted", parent=self.root)

            logging.info(f"Photo samples taken for {student_id}: {img_count} samples")
            messagebox.showinfo("Success", f"{img_count} photo samples taken for {student_id}", parent=self.root)

        except KeyboardInterrupt:
            logging.warning("Photo sample collection interrupted by user")
            messagebox.showinfo("Interrupted", "Photo sample collection was interrupted", parent=self.root)
        except Exception as e:
            logging.error(f"Error in take_photo_sample: {e}")
            messagebox.showerror("Error", f"An error occurred while taking photo: {str(e)}", parent=self.root)
        finally:
            # Ensure camera is released even if error occurs mid-loop
            if cap is not None and cap.isOpened():
                cap.release()
            cv2.destroyAllWindows() # Close any lingering OpenCV windows

    def update_photo_sample(self):
        """Update photo sample for face recognition (Same logic as take_photo)"""
        logging.info("Update photo sample button clicked")
        # This function is often identical to take_photo_sample,
        # as it just overwrites existing samples.
        self.take_photo_sample()

    def reset_data(self):
        """Reset all form fields to their default values"""
        logging.info("Reset data button clicked")
        self.var_dept.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("")
        self.var_roll.set("")
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("No")
        logging.debug("Form fields reset")




if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()