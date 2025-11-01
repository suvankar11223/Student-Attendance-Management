import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import cv2
import os
import numpy as np
from threading import Thread

class Train:
    def __init__(self, root):
        logging.info("Initializing Train class")
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Student Attendance System")
        self.root.configure(bg="white")

        # Variables for training status
        self.training_status = StringVar()
        self.training_status.set("Ready to train")
        self.progress_var = DoubleVar()

        # ============ GUI SETUP =================

        # --- Top Banner Images (Three images side by side) ---
        try:
            logging.debug("Loading top banner images for Train")
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
            logging.debug("Top banner images loaded successfully for Train")
        except Exception as e:
            logging.error(f"Error loading top banners for Train: {e}")
            top_label = Label(self.root, bg="lightblue", text="Banner Images (1530x130)", font=("arial", 20))
            top_label.place(x=0, y=0, width=1530, height=130)

        # --- Main Title ---
        title_lbl = Label(self.root, text="TRAIN DATA SET",
                          font=("arial", 30, "bold"), bg="#2c3e50", fg="#27ab83")
        title_lbl.place(x=0, y=130, width=1530, height=50)

        # Main Content Frame
        main_frame = Frame(self.root, bg="white", relief="ridge", bd=3)
        main_frame.place(x=0, y=180, width=1530, height=610)

        # Left Frame - Training Interface
        left_frame = LabelFrame(main_frame, text="Training Interface",
                                font=("arial", 16, "bold"),
                                bg="white", fg="#2c3e50", relief="ridge", bd=4, padx=5, pady=5)
        left_frame.place(x=10, y=10, width=760, height=590)

        # Right Frame - Training Status
        right_frame = LabelFrame(main_frame, text="Training Status",
                                 font=("arial", 16, "bold"),
                                 bg="white", fg="#2c3e50", relief="ridge", bd=4, padx=5, pady=5)
        right_frame.place(x=780, y=10, width=740, height=590)

        # ================= LEFT FRAME CONTENT =================
        self.create_left_frame_content(left_frame)

        # ================= RIGHT FRAME CONTENT =================
        self.create_right_frame_content(right_frame)

        logging.info("Train class initialization complete")

    def create_left_frame_content(self, parent):
        """Create training interface content"""
        logging.debug("Creating left frame content for Train")

        # --- Left Banner Image ---
        try:
            logging.debug("Loading left banner image for Train")
            img_left_banner = Image.open(r"college_images\Face recognition technology in the modern….jpeg")
            img_left_banner = img_left_banner.resize((700, 100), Image.Resampling.LANCZOS)
            self.photoimg_left_banner = ImageTk.PhotoImage(img_left_banner)

            left_banner_label = Label(parent, image=self.photoimg_left_banner)
            left_banner_label.place(x=15, y=5, width=700, height=100)
            logging.debug("Left banner image loaded successfully for Train")
        except Exception as e:
            logging.error(f"Error loading left banner for Train: {e}")
            left_banner_label = Label(parent, bg="lightgray", text="Left Banner (700x100)", font=("arial", 16))
            left_banner_label.place(x=15, y=5, width=700, height=100)

        # Progress Frame
        progress_frame = LabelFrame(parent, text="Training Progress",
                                    font=("arial", 14, "bold"),
                                    bg="white", fg="#2c3e50", relief="ridge", bd=2, padx=5, pady=5)
        progress_frame.place(x=5, y=110, width=740, height=200)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, mode='determinate')
        self.progress_bar.place(x=15, y=10, width=700, height=40)

        # Status Label
        self.status_label = Label(progress_frame, textvariable=self.training_status,
                                 font=("arial", 12), bg="white", fg="blue")
        self.status_label.place(x=15, y=60, width=700, height=30)

        # Instructions Label
        instructions_label = Label(progress_frame,
                                 text="Click 'START TRAINING' to train the face recognition model.\n"
                                      "Make sure you have face images in the 'data' folder.",
                                 font=("arial", 10), bg="white", fg="gray", justify=LEFT)
        instructions_label.place(x=15, y=100, width=700, height=60)

        # Train Button Frame
        button_frame = Frame(parent, bg="white", bd=0)
        button_frame.place(x=0, y=320, width=750, height=50)

        # Train Button
        self.train_button = Button(button_frame, text="START TRAINING", command=self.start_training,
                                  font=("arial", 14, "bold"), bg="#28a745", fg="white",
                                  width=20, height=2, relief="raised", bd=5)
        self.train_button.place(x=250, y=5)

    def create_right_frame_content(self, parent):
        """Create training status and information content"""
        logging.debug("Creating right frame content for Train")

        # --- Right Banner Image ---
        try:
            logging.debug("Loading right banner image for Train")
            img_right_banner = Image.open(r"college_images\Facial recognition technology is changing law….jpeg")
            img_right_banner = img_right_banner.resize((700, 100), Image.Resampling.LANCZOS)
            self.photoimg_right_banner = ImageTk.PhotoImage(img_right_banner)

            right_banner_label = Label(parent, image=self.photoimg_right_banner)
            right_banner_label.place(x=15, y=5, width=700, height=100)
            logging.debug("Right banner image loaded successfully for Train")
        except Exception as e:
            logging.error(f"Error loading right banner for Train: {e}")
            right_banner_label = Label(parent, bg="lightgray", text="Right Banner (700x100)", font=("arial", 16))
            right_banner_label.place(x=15, y=5, width=700, height=100)

        # Status Information Frame
        status_info_frame = LabelFrame(parent, text="Training Details",
                                       font=("arial", 14, "bold"),
                                       bg="white", fg="#2c3e50", relief="ridge", bd=2, padx=5, pady=5)
        status_info_frame.place(x=5, y=110, width=730, height=450)

        # Status Text Area
        self.status_text = Text(status_info_frame, font=("arial", 10), bg="lightgray",
                               wrap=WORD, state=DISABLED)
        scrollbar = ttk.Scrollbar(status_info_frame, command=self.status_text.yview)
        self.status_text.config(yscrollcommand=scrollbar.set)

        self.status_text.place(x=10, y=10, width=680, height=400)
        scrollbar.place(x=690, y=10, width=20, height=400)

        # Initial status message
        self.update_status("Welcome to Face Recognition Training System!\n\n"
                          "This system will train a face recognition model using the LBPH (Local Binary Patterns Histograms) algorithm.\n\n"
                          "Requirements:\n"
                          "- Face images stored in 'data/' directory\n"
                          "- Images named as 'user.<id>.<count>.jpg'\n"
                          "- At least 2 different people with multiple images each\n\n"
                          "Click 'START TRAINING' to begin the training process.")

    def update_status(self, message):
        """Update the status text area"""
        self.status_text.config(state=NORMAL)
        self.status_text.insert(END, message + "\n")
        self.status_text.see(END)
        self.status_text.config(state=DISABLED)
        self.root.update_idletasks()

    def start_training(self):
        """Start the training process in a separate thread"""
        logging.info("Training started")
        self.train_button.config(state=DISABLED, text="TRAINING...")
        self.progress_var.set(0)
        self.training_status.set("Initializing training...")

        # Start training in a separate thread to avoid freezing the GUI
        training_thread = Thread(target=self.train_model)
        training_thread.daemon = True
        training_thread.start()

    def get_images_and_labels(self, data_dir):
        """Load images and labels from the data directory"""
        self.update_status(f"Loading images from {data_dir}...")
        self.training_status.set("Loading images...")
        self.progress_var.set(10)

        image_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.jpg')]
        faces = []
        labels = []

        if len(image_paths) == 0:
            raise ValueError("No images found in the data directory")

        for i, image_path in enumerate(image_paths):
            # Extract label from filename (e.g., user.22331.0.jpg -> 22331)
            try:
                label = int(os.path.split(image_path)[-1].split(".")[1])
            except (IndexError, ValueError):
                self.update_status(f"Warning: Skipping invalid filename: {os.path.basename(image_path)}")
                continue

            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                self.update_status(f"Warning: Could not read image: {os.path.basename(image_path)}")
                continue

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces.append(gray)
            labels.append(label)

            # Update progress
            progress = 10 + (i / len(image_paths)) * 40
            self.progress_var.set(progress)
            self.training_status.set(f"Loading images... {i+1}/{len(image_paths)}")

        self.update_status(f"Loaded {len(faces)} face images from {len(set(labels))} unique individuals")
        return faces, labels

    def train_model(self):
        """Train the face recognition model"""
        try:
            data_dir = "data"

            # Check if data directory exists
            if not os.path.exists(data_dir):
                raise FileNotFoundError(f"Data directory '{data_dir}' does not exist")

            self.update_status("Starting face recognition training...")
            self.training_status.set("Preparing data...")
            self.progress_var.set(5)

            # Load images and labels
            faces, labels = self.get_images_and_labels(data_dir)

            if len(faces) == 0:
                raise ValueError("No valid face images found for training")

            if len(set(labels)) < 2:
                raise ValueError("Need at least 2 different people for training")

            self.update_status(f"Training model with {len(faces)} images from {len(set(labels))} individuals...")
            self.training_status.set("Training model...")
            self.progress_var.set(50)

            # Check if cv2.face is available
            try:
                # Try the standard OpenCV 4.x way
                recognizer = cv2.face.LBPHFaceRecognizer_create()
            except AttributeError:
                try:
                    # Try alternative import for some OpenCV installations
                    import cv2.cv2 as cv2_alt
                    recognizer = cv2_alt.face.LBPHFaceRecognizer_create()
                except (AttributeError, ImportError):
                    raise ImportError("OpenCV face recognition module not available. "
                                    "Please install opencv-contrib-python: pip install opencv-contrib-python")

            # Train the recognizer
            recognizer.train(faces, np.array(labels))

            self.progress_var.set(80)
            self.training_status.set("Saving model...")

            # Save the trained model
            model_path = "trainer.yml"
            recognizer.save(model_path)

            self.progress_var.set(100)
            self.training_status.set("Training completed successfully!")

            self.update_status(f"✓ Training completed successfully!\n"
                              f"✓ Model saved as '{model_path}'\n"
                              f"✓ Trained with {len(faces)} images from {len(set(labels))} individuals\n"
                              f"✓ Ready for face recognition!")

            messagebox.showinfo("Success", "Face recognition model trained successfully!", parent=self.root)

        except Exception as e:
            error_msg = f"Training failed: {str(e)}"
            logging.error(error_msg)
            self.update_status(f"✗ {error_msg}")
            self.training_status.set("Training failed")
            messagebox.showerror("Training Error", error_msg, parent=self.root)

        finally:
            self.train_button.config(state=NORMAL, text="START TRAINING")


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()