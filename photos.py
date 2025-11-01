import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Photos:
    def __init__(self, root):
        logging.info("Initializing Photos class")
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Photos Gallery")
        self.root.configure(bg="white")

        # ============ Top Banner Images =================
        try:
            logging.debug("Loading top banner images for Photos")
            # First image
            img_top1 = Image.open(r"college_images\b307c458-17fb-4c05-826b-9790ce0eddb3.jpeg")
            img_top1 = img_top1.resize((510, 130), Image.Resampling.LANCZOS)
            self.photoimg_top1 = ImageTk.PhotoImage(img_top1)

            top_label1 = Label(self.root, image=self.photoimg_top1)
            top_label1.place(x=0, y=0, width=510, height=130)

            # Second image
            img_top2 = Image.open(r"college_images\b993a3d3-2a12-4699-ab3c-7b9e4a1c2293.jpeg")
            img_top2 = img_top2.resize((510, 130), Image.Resampling.LANCZOS)
            self.photoimg_top2 = ImageTk.PhotoImage(img_top2)

            top_label2 = Label(self.root, image=self.photoimg_top2)
            top_label2.place(x=510, y=0, width=510, height=130)

            # Third image
            img_top3 = Image.open(r"college_images\d227e189-5dd5-4ff7-bf19-f2e01fe97605.jpeg")
            img_top3 = img_top3.resize((510, 130), Image.Resampling.LANCZOS)
            self.photoimg_top3 = ImageTk.PhotoImage(img_top3)

            top_label3 = Label(self.root, image=self.photoimg_top3)
            top_label3.place(x=1020, y=0, width=510, height=130)
            logging.debug("Top banner images loaded successfully for Photos")
        except Exception as e:
            logging.error(f"Error loading top banners for Photos: {e}")
            top_label = Label(self.root, bg="lightblue", text="Banner Images (1530x130)", font=("arial", 20))
            top_label.place(x=0, y=0, width=1530, height=130)

        # ============ Main Title =================
        title_lbl = Label(self.root, text="PHOTOS GALLERY",
                          font=("arial", 30, "bold"), bg="#2c3e50", fg="#27ab83")
        title_lbl.place(x=0, y=130, width=1530, height=50)

        # ============ Main Content Frame =================
        main_frame = Frame(self.root, bg="white", relief="ridge", bd=3)
        main_frame.place(x=0, y=180, width=1530, height=610)

        # ============ Gallery Frame =================
        gallery_frame = LabelFrame(main_frame, text="Photo Gallery",
                                   font=("arial", 16, "bold"),
                                   bg="white", fg="#2c3e50", relief="ridge", bd=4, padx=5, pady=5)
        gallery_frame.place(x=10, y=10, width=1510, height=590)

        # ============ Scrollable Canvas for Images =================
        self.canvas = Canvas(gallery_frame, bg="white")
        self.scrollbar = ttk.Scrollbar(gallery_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # ============ Load and Display Images =================
        self.load_images()

        logging.info("Photos class initialization complete")

    def load_images(self):
        """Load images from the data folder and display 25 samples per student systematically"""
        logging.debug("Loading images from data folder")
        data_dir = "data"
        if not os.path.exists(data_dir):
            logging.warning("Data directory does not exist")
            no_images_label = Label(self.scrollable_frame, text="No images found in data folder",
                                    font=("arial", 20), bg="white", fg="red")
            no_images_label.pack(pady=50)
            return

        # Get all image files
        image_files = [f for f in os.listdir(data_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        image_files.sort()  # Sort for systematic display

        if not image_files:
            logging.info("No image files found in data folder")
            no_images_label = Label(self.scrollable_frame, text="No images found in data folder",
                                    font=("arial", 20), bg="white", fg="red")
            no_images_label.pack(pady=50)
            return

        # Group images by student ID and limit to 25 per student
        student_images = {}
        for image_file in image_files:
            try:
                # Extract student ID from filename (format: user.STUDENT_ID.NUMBER.jpg)
                parts = image_file.split('.')
                if len(parts) >= 3 and parts[0] == 'user':
                    student_id = parts[1]
                    if student_id not in student_images:
                        student_images[student_id] = []
                    if len(student_images[student_id]) < 25:  # Limit to 25 samples per student
                        student_images[student_id].append(image_file)
            except Exception as e:
                logging.error(f"Error parsing filename {image_file}: {e}")
                continue

        if not student_images:
            logging.info("No valid student images found")
            no_images_label = Label(self.scrollable_frame, text="No valid student images found",
                                    font=("arial", 20), bg="white", fg="red")
            no_images_label.pack(pady=50)
            return

        logging.info(f"Found images for {len(student_images)} students")

        # Display images in a grid, grouped by student
        row = 0
        col = 0
        max_cols = 5  # Number of images per row
        image_size = (120, 120)  # Size of each thumbnail

        for student_id, images in student_images.items():
            # Add student header
            student_label = Label(self.scrollable_frame, text=f"Student ID: {student_id} ({len(images)} samples)",
                                  font=("arial", 14, "bold"), bg="white", fg="#2c3e50")
            student_label.grid(row=row, column=0, columnspan=max_cols, pady=(20, 10), sticky="w", padx=10)
            row += 1
            col = 0

            for image_file in images:
                try:
                    img_path = os.path.join(data_dir, image_file)
                    img = Image.open(img_path)
                    img = img.resize(image_size, Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)

                    # Create a frame for each image with label
                    img_frame = Frame(self.scrollable_frame, bg="white", relief="ridge", bd=2)
                    img_frame.grid(row=row, column=col, padx=5, pady=5)

                    img_label = Label(img_frame, image=photo, bg="white")
                    img_label.image = photo  # Keep a reference
                    img_label.pack()

                    # Add sample number label below image
                    sample_num = image_file.split('.')[-2]  # Get the number before .jpg
                    name_label = Label(img_frame, text=f"Sample {sample_num}", font=("arial", 7), bg="white", fg="#666")
                    name_label.pack(pady=(0, 2))

                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1

                except Exception as e:
                    logging.error(f"Error loading image {image_file}: {e}")
                    continue

            # Move to next row after each student's images
            if col > 0:
                row += 1

        logging.info("Displayed student images in gallery")


if __name__ == "__main__":
    root = Tk()
    obj = Photos(root)
    root.mainloop()