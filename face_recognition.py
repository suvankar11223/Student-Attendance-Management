import logging
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import cv2
import os
import numpy as np
import mysql.connector
import threading
import time
import pyttsx3

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class Face_Recognition:
    def __init__(self, root):
        logging.info("Initializing Face Recognition class")
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
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
        self.data_dir = "data"

        # Variables for recognition
        self.is_recognizing = False
        self.cap = None
        self.recognizer = None
        self.face_classifier = None

        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level

        # ============ GUI SETUP =================

        # --- Top Banner (Using a single frame for a clean look) ---
        top_frame = Frame(self.root, bg="#2c3e50")
        top_frame.place(x=0, y=0, width=1530, height=130)
        
        # --- Main Title (Moved to top frame) ---
        title_lbl = Label(top_frame, text="FACE RECOGNITION",
                            font=("arial", 30, "bold"), bg="#2c3e50", fg="#27ab83")
        title_lbl.place(x=600, y=40)

        # --- NEW: Back Button (from your screenshot) ---
        # Note: This assumes you have a function `self.close_window` 
        # or similar to go back to a main menu.
        # I'll make it just close this window for now.
        back_btn = Button(top_frame, text="Back",
                          command=self.on_closing,
                          font=("arial", 12, "bold"), bg="#f8f9fa", fg="#2c3e50",
                          relief="flat", bd=0, cursor="hand2")
        back_btn.place(x=1450, y=10, width=70, height=30)


        # Main Content Frame (for images and button)
        main_frame = Frame(self.root, bg="white")
        main_frame.place(x=0, y=130, width=1530, height=660) # Adjusted height

        # --- Left Side Image (as per screenshot proportion) ---
        try:
            logging.debug("Loading left recognition image")
            # Using your image path
            img_left = Image.open(r"college_images\—Pngtree—intelligent face recognition advertising background_957037.jpg")
            # Resized to ~60% of width (screenshot layout)
            img_left = img_left.resize((920, 580), Image.Resampling.LANCZOS) 
            self.photoimg_left = ImageTk.PhotoImage(img_left)

            left_img_label = Label(main_frame, image=self.photoimg_left, bg="white", relief="ridge", bd=3)
            left_img_label.place(x=10, y=10, width=920, height=580)
            logging.debug("Left recognition image loaded successfully")
        except Exception as e:
            logging.error(f"Error loading left recognition image: {e}")
            left_img_label = Label(main_frame, bg="lightgray", text="Main Image\n(920x580)", font=("arial", 16))
            left_img_label.place(x=10, y=10, width=920, height=580)

        # --- Right Side Image (as per screenshot proportion) ---
        try:
            logging.debug("Loading right recognition image")
            # Using your second image path
            img_right = Image.open(r"college_images\b993a3d3-2a12-4699-ab3c-7b9e4a1c2293.jpeg")
            # Resized to ~40% of width (screenshot layout)
            img_right = img_right.resize((580, 580), Image.Resampling.LANCZOS) 
            self.photoimg_right = ImageTk.PhotoImage(img_right)

            right_img_label = Label(main_frame, image=self.photoimg_right, bg="white", relief="ridge", bd=3)
            right_img_label.place(x=940, y=10, width=580, height=580)
            logging.debug("Right recognition image loaded successfully")
        except Exception as e:
            logging.error(f"Error loading right recognition image: {e}")
            right_img_label = Label(main_frame, bg="lightgray", text="Scanner Image\n(580x580)", font=("arial", 16))
            right_img_label.place(x=940, y=10, width=580, height=580)

        # --- Control Panel Frame (Cleaned up) ---
        control_frame = Frame(main_frame, bg="#f8f9fa", relief="ridge", bd=2)
        control_frame.place(x=10, y=600, width=1510, height=50) # Spans full width

        # --- Status Label ---
        self.status_label = Label(control_frame, text="System Ready", font=("arial", 12, "bold"),
                                  bg="#f8f9fa", fg="green")
        self.status_label.place(x=20, y=10)

        # --- "START SCAN" Button (Centered) ---
        self.scan_button = Button(control_frame, text="START FACE RECOGNITION",
                                    command=self.start_recognition,
                                    font=("arial", 14, "bold"), bg="#28a745", fg="white",
                                    width=25, height=1, relief="raised", bd=3, cursor="hand2")
        self.scan_button.place(relx=0.5, y=8, anchor="n") # Centered

        # --- Progress Bar (For initialization) ---
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var,
                                            maximum=100, mode='determinate', length=200)
        self.progress_bar.place(x=1290, y=15)

        # Initialize face recognition components
        init_thread = threading.Thread(target=self.initialize_recognition, daemon=True)
        init_thread.start()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        logging.info("Face Recognition class initialization complete")


    def initialize_recognition(self):
        """Initialize face recognition components in a background thread"""
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
                messagebox.showerror("Error", f"Trained model '{self.model_path}' not found. Please train the model first.", parent=self.root)
                self.scan_button.config(state=DISABLED, text="MODEL NOT FOUND")
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
                messagebox.showerror("Error", "Could not load 'haarcascade_frontalface_default.xml'.", parent=self.root)
                self.scan_button.config(state=DISABLED, text="CLASSIFIER FAILED")
                self.status_label.config(text="Error: Classifier not found", fg="red")
                return

            self.progress_var.set(100)
            self.status_label.config(text="System Ready", fg="green")
            logging.info("Face recognition components initialized")

        except AttributeError:
             logging.critical("cv2.face.LBPHFaceRecognizer_create() not found!")
             messagebox.showerror("Environment Error", "OpenCV 'face' module not available. Please install 'opencv-contrib-python'", parent=self.root)
             self.scan_button.config(state=DISABLED, text="INSTALL CONTRIB")
             self.status_label.config(text="Error: Wrong OpenCV version", fg="red")
        except Exception as e:
            logging.error(f"Error initializing recognition: {e}")
            messagebox.showerror("Initialization Error", f"An error occurred: {str(e)}", parent=self.root)
            self.status_label.config(text="Initialization Error", fg="red")

    def start_recognition(self):
        """Start the face recognition process"""
        if self.recognizer is None or self.face_classifier is None:
            messagebox.showerror("Error", "Recognition system is not ready. Check model and classifier files.", parent=self.root)
            return

        self.is_recognizing = True
        self.scan_button.config(state=DISABLED, text="RECOGNIZING...")
        self.status_label.config(text="Recognition in progress...", fg="orange")
        self.progress_var.set(0) # Reset progress bar for scanning

        # Start recognition in a separate thread
        recognition_thread = threading.Thread(target=self.recognize_faces_loop, daemon=True)
        recognition_thread.start()

    def stop_recognition(self):
        """Stop the face recognition process"""
        self.is_recognizing = False
        self.scan_button.config(state=NORMAL, text="START FACE RECOGNITION")
        self.status_label.config(text="System Ready", fg="green")
        self.progress_var.set(0)

        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        logging.info("Face recognition stopped.")

    def recognize_faces_loop(self):
        """Main face recognition loop that runs in a thread"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                logging.error("Could not open camera")
                messagebox.showerror("Camera Error", "Could not open camera. Is it in use?")
                self.root.after(0, self.stop_recognition) # Stop from main thread
                return

            logging.info("Camera opened. Recognition in progress...")
            self.root.after(0, lambda: self.status_label.config(text="Camera active - Looking for faces...", fg="blue"))

            last_recognized_id = -1
            recognition_start_time = time.time()
            
            # --- ENHANCEMENT: Variables for 'Scanning... X%' effect ---
            scan_progress = 0

            start_time = time.time()
            while self.is_recognizing and (time.time() - start_time) < 8:  # Limit to 8 seconds
                ret, frame = self.cap.read()
                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_classifier.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

                # --- ENHANCEMENT: Update progress bar based on activity ---
                if len(faces) > 0:
                    # When a face is seen, jump progress to 50%
                    if scan_progress < 50:
                        scan_progress = 50
                    self.root.after(0, lambda: self.status_label.config(text="Face Detected! Analyzing...", fg="orange"))
                else:
                    # If no face, slowly increment progress to simulate "scanning"
                    scan_progress = (scan_progress + 0.5) % 40
                    self.root.after(0, lambda: self.status_label.config(text=f"Scanning... {int(scan_progress)}%", fg="blue"))

                self.root.after(0, lambda p=scan_progress: self.progress_var.set(p))


                for (x, y, w, h) in faces:
                    # --- ENHANCEMENT: Cleaner OpenCV UI ---
                    face_roi = gray[y:y+h, x:x+w]

                    try:
                        id, confidence = self.recognizer.predict(face_roi)
                        confidence_percent = 100 - confidence

                        if confidence_percent > 50:
                            id_str = f"ID: {id}"
                            conf_str = f"Conf: {confidence_percent:.1f}%"
                            color = (0, 255, 0) # Green for recognized
                            # Set progress to 75% when confidence is > 50
                            self.root.after(0, self.progress_var.set, 75)
                        else:
                            id_str = "Unknown"
                            conf_str = ""
                            color = (0, 0, 255) # Red for unknown

                        # Draw main rectangle
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        # Draw text background
                        cv2.rectangle(frame, (x, y-35), (x+w, y), color, cv2.FILLED)
                        # Draw text
                        cv2.putText(frame, id_str, (x+6, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        if conf_str:
                             cv2.putText(frame, conf_str, (x+5, y-20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (255, 255, 255), 1)

                        # --- Successful Recognition Logic ---
                        if confidence_percent > 70: # High confidence threshold
                            self.root.after(0, self.progress_var.set, 100)
                            if id != last_recognized_id or (time.time() - recognition_start_time > 5):
                                logging.info(f"Face recognized! ID: {id}, Confidence: {confidence_percent:.1f}%")
                                # Get student name for TTS
                                student_name = self.get_student_name(id)
                                if student_name:
                                    # Speak the welcome message
                                    tts_thread = threading.Thread(target=self.speak_welcome, args=(student_name,), daemon=True)
                                    tts_thread.start()
                                # Schedule the results window on the main thread
                                self.root.after(0, self.show_recognition_results, id, confidence_percent)
                                self.is_recognizing = False # Stop the loop
                                last_recognized_id = id
                                recognition_start_time = time.time()
                                break # Exit inner 'for' loop

                    except cv2.error:
                        logging.warning("Prediction error, likely on a very small/blurry face.")
                        continue # Skip this frame

                cv2.imshow("Face Recognition System - Press 'q' to Quit", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.is_recognizing = False
                    break

            logging.info("Recognition loop finished.")

        except Exception as e:
            logging.error(f"Error in face recognition thread: {e}", exc_info=True)
            messagebox.showerror("Recognition Error", f"An error occurred: {str(e)}", parent=self.root)

        finally:
            if self.cap and self.cap.isOpened():
                self.cap.release()
            cv2.destroyAllWindows()
            if self.is_recognizing:
                self.root.after(0, self.stop_recognition)
            self.is_recognizing = False # Ensure flag is reset


    def show_recognition_results(self, student_id, confidence):
        """
        Create a new Toplevel window to show all details of the recognized student.
        """
        # Stop the main window's scanning state
        self.stop_recognition()
        logging.info(f"Creating results window for Student ID: {student_id}")

        # --- Create New Window (Enhanced Design) ---
        details_window = Toplevel(self.root)
        details_window.title("Recognition Result - Student Details")
        details_window.geometry("900x650+250+50")
        details_window.configure(bg="#f8f9fa")
        details_window.resizable(False, False)
        details_window.grab_set()

        # --- Header Frame ---
        header_frame = Frame(details_window, bg="#2c3e50", height=80)
        header_frame.pack(fill=X)
        title_label = Label(header_frame, text="STUDENT RECOGNITION SUCCESSFUL",
                            font=("arial", 20, "bold"), bg="#2c3e50", fg="#27ab83")
        title_label.pack(pady=20)

        # Main frame for details
        details_frame = Frame(details_window, bg="#f8f9fa")
        details_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # --- Fetch Full Student Details ---
        try:
            conn = mysql.connector.connect(**self.db_config)
            my_cursor = conn.cursor()
            query = "SELECT * FROM student WHERE StudentId=%s"
            my_cursor.execute(query, (student_id,))
            result = my_cursor.fetchone()

            if not result:
                logging.warning(f"ID {student_id} recognized, but not found in database.")
                messagebox.showerror("Database Error", f"Student ID {student_id} was recognized but is not in the database.", parent=details_window)
                details_window.destroy()
                return

            # --- Left Frame (Student Photo & Confidence) ---
            left_panel = Frame(details_frame, bg="white", bd=2, relief=RIDGE)
            left_panel.place(x=20, y=20, width=300, height=500)

            # Photo section
            photo_frame = Frame(left_panel, bg="white")
            photo_frame.pack(fill=X, pady=10)
            Label(photo_frame, text="Recognized Student", font=("arial", 14, "bold"), bg="#2c3e50", fg="white").pack(fill=X)

            try:
                student_img_path = ""
                for file in os.listdir(self.data_dir):
                    if file.startswith(f"user.{student_id}."):
                        student_img_path = os.path.join(self.data_dir, file)
                        break
                
                if student_img_path:
                    img_data = Image.open(student_img_path)
                    img_data = img_data.resize((250, 250), Image.Resampling.LANCZOS)
                    self.student_photo = ImageTk.PhotoImage(img_data)
                    photo_label = Label(photo_frame, image=self.student_photo, bg="white")
                    photo_label.pack(pady=10)
                else:
                    photo_label = Label(photo_frame, text="No Photo Found", font=("arial", 12), bg="lightgray", width=20, height=10)
                    photo_label.pack(pady=10)
            except Exception as e:
                logging.error(f"Error loading student photo: {e}")
                photo_label = Label(photo_frame, text="Photo Error", font=("arial", 12), bg="lightgray", width=20, height=10)
                photo_label.pack(pady=10)

            # Confidence section
            conf_frame = Frame(left_panel, bg="#e9ecef", bd=1, relief=SOLID)
            conf_frame.pack(fill=X, padx=10, pady=10)
            Label(conf_frame, text="Recognition Confidence", font=("arial", 12, "bold"), bg="#e9ecef").pack(pady=5)
            
            conf_percent_str = f"{confidence:.1f}%"
            conf_color = "#28a745" if confidence > 80 else "#ffc107" if confidence > 70 else "#dc3545"
            conf_label = Label(conf_frame, text=conf_percent_str, font=("arial", 24, "bold"), fg=conf_color, bg="#e9ecef")
            conf_label.pack(pady=5)
            time_label = Label(conf_frame, text=f"Recognized at: {time.strftime('%H:%M:%S')}", font=("arial", 10), bg="#e9ecef", fg="gray")
            time_label.pack(pady=5)

            # --- Right Frame (Student Info) ---
            info_panel = Frame(details_frame, bg="white", bd=2, relief=RIDGE)
            info_panel.place(x=340, y=20, width=520, height=500)
            Label(info_panel, text="Student Information", font=("arial", 14, "bold"), bg="#2c3e50", fg="white").pack(fill=X)

            info_content = Frame(info_panel, bg="white")
            info_content.pack(fill=BOTH, expand=True, padx=10, pady=10)

            fields = ["Department", "Course", "Year", "Semester", "Student ID", "Name",
                      "Division", "Roll No", "Gender", "Date of Birth", "Email", "Phone",
                      "Address", "Teacher"]

            for i, (field, value) in enumerate(zip(fields, result)):
                row_frame = Frame(info_content, bg="white")
                row_frame.pack(fill=X, pady=2)
                
                field_label = Label(row_frame, text=f"{field}:", font=("arial", 11, "bold"), bg="white", anchor="w", width=15)
                field_label.pack(side=LEFT)
                
                display_value = str(value) if value else "N/A"
                if field == "Phone" and len(display_value) == 10:
                    display_value = f"{display_value[:5]} {display_value[5:]}"

                value_label = Label(row_frame, text=display_value, font=("arial", 11), bg="white", anchor="w", wraplength=300)
                value_label.pack(side=LEFT, fill=X, expand=True)

            # --- Bottom Buttons ---
            button_frame = Frame(details_window, bg="#f8f9fa")
            button_frame.pack(fill=X, pady=20)

            # --- NEW FEATURE: View Attendance Button ---
            info_button = Button(button_frame, text="VIEW ATTENDANCE",
                                 command=lambda: self.show_attendance_details(student_id),
                                 font=("arial", 12, "bold"), bg="#17a2b8", fg="white",
                                 width=20, height=1, relief="raised", bd=3, cursor="hand2")
            info_button.pack(side=LEFT, padx=(200, 10)) # Adjusted padding

            # Close Button
            close_button = Button(button_frame, text="CLOSE",
                                  command=details_window.destroy,
                                  font=("arial", 12, "bold"), bg="#dc3545", fg="white",
                                  width=20, height=1, relief="raised", bd=3, cursor="hand2")
            close_button.pack(side=RIGHT, padx=(10, 200)) # Adjusted padding

            conn.close()

        except Exception as e:
            logging.error(f"Error fetching/displaying student details: {e}", exc_info=True)
            messagebox.showerror("Database Error", f"Error loading student details: {str(e)}", parent=details_window)
            details_window.destroy()

    def get_student_name(self, student_id):
        """Fetch the student's name from the database"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            my_cursor = conn.cursor()
            query = "SELECT Name FROM student WHERE StudentId=%s"
            my_cursor.execute(query, (student_id,))
            result = my_cursor.fetchone()
            conn.close()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            logging.error(f"Error fetching student name: {e}")
            return None

    def speak_welcome(self, student_name):
        """Speak a welcome message using TTS"""
        try:
            welcome_message = f"Welcome, {student_name}!"
            self.tts_engine.say(welcome_message)
            self.tts_engine.runAndWait()
        except Exception as e:
            logging.error(f"Error in TTS: {e}")

    def show_attendance_details(self, student_id):
        """Placeholder for showing attendance"""
        # This is where you would open a new window or show data
        # for the 'attendance' module.
        messagebox.showinfo("Attendance", f"Attendance details for Student ID {student_id}\n\nThis feature is under construction.", parent=self.root)

    def on_closing(self):
        """Handle the main window close event"""
        logging.info("Application closing...")
        self.is_recognizing = False # Stop any background threads
        time.sleep(0.1) # Give thread a moment to stop
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()


if __name__ == "__main__":
    logging.info("Face Recognition Application started")
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
    logging.info("Face Recognition Application closed")