from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
from student import Student
from photos import Photos
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from help_desk import HelpDesk
from reports import Reports

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root

        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Background Image
        bg_img = Image.open(r"college_images\fb354153-7adb-403a-937c-5bafb7226061.jpeg")
        bg_img = bg_img.resize((1530, 790), Image.Resampling.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.photoimg_bg)
        bg_label.place(x=0, y=0, width=1530, height=790)

        # Title Label
        title_lbl = Label(bg_label, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="white", fg="blue")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # Top Images
        img1 = Image.open(r"college_images\3a690346-15b9-4145-ac65-24e2b90d98e4.jpeg")
        img1 = img1.resize((300, 150), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        img2 = Image.open(r"college_images\Facial Recognition (or more aptly named, Computer….jpeg")
        img2 = img2.resize((300, 150), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        img3 = Image.open(r"college_images\portrait-man-face-scann.jpg")
        img3 = img3.resize((300, 150), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        img4 = Image.open(r"college_images\Facial recognition… coming to a supermarket near….jpeg")
        img4 = img4.resize((300, 150), Image.Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        img5 = Image.open(r"college_images\f0f28c5e-d78c-4824-84b3-fbd66421c748.jpeg")
        img5 = img5.resize((300, 150), Image.Resampling.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)

        # Place images side by side at the top, no space
        img1_label = Label(bg_label, image=self.photoimg1)
        img1_label.place(x=0, y=45, width=300, height=150)

        img2_label = Label(bg_label, image=self.photoimg2)
        img2_label.place(x=300, y=45, width=300, height=150)

        img3_label = Label(bg_label, image=self.photoimg3)
        img3_label.place(x=600, y=45, width=300, height=150)

        img4_label = Label(bg_label, image=self.photoimg4)
        img4_label.place(x=900, y=45, width=300, height=150)

        img5_label = Label(bg_label, image=self.photoimg5)
        img5_label.place(x=1200, y=45, width=300, height=150)

        # Subtitle Label
        subtitle_lbl = Label(bg_label, text="Face Recognition Software", font=("times new roman", 30, "bold"), bg="lightblue", fg="darkblue")
        subtitle_lbl.place(x=0, y=200, width=1530, height=60)

        # Load button images
        img_btn1 = Image.open(r"college_images\_Time is a layer to be drafted_ Cosmic Architect’s….jpeg").resize((150, 150), Image.Resampling.LANCZOS)
        self.photo_btn1 = ImageTk.PhotoImage(img_btn1)

        img_btn2 = Image.open(r"college_images\3a690346-15b9-4145-ac65-24e2b90d98e4.jpeg").resize((150, 150), Image.Resampling.LANCZOS)
        self.photo_btn2 = ImageTk.PhotoImage(img_btn2)

        img_btn3 = Image.open(r"college_images\Abstract Fingerprint Scanner in Progress - Identity Verification Concept Stock Vector - Illustration of print, investigation_ 153275227.jpeg").resize((150, 150), Image.Resampling.LANCZOS)
        self.photo_btn3 = ImageTk.PhotoImage(img_btn3)

        img_btn4 = Image.open(r"college_images\Blockchain safety and blockchain hacker.jpeg").resize((150, 150), Image.Resampling.LANCZOS)
        self.photo_btn4 = ImageTk.PhotoImage(img_btn4)

        img_btn5 = Image.open(r"college_images\download.jpeg").resize((150, 150), Image.Resampling.LANCZOS)
        self.photo_btn5 = ImageTk.PhotoImage(img_btn5)

        img_btn6 = Image.open(r"college_images\f4e6f876-144f-40e8-8453-e4627017088b.jpeg").resize((150, 150), Image.Resampling.LANCZOS)
        self.photo_btn6 = ImageTk.PhotoImage(img_btn6)

        img_btn7 = Image.open(r"college_images\25688a49-8016-4e10-98ea-8e62c5ec71b7.jpeg").resize((150, 150), Image.Resampling.LANCZOS)
        self.photo_btn7 = ImageTk.PhotoImage(img_btn7)

        img_btn8 = Image.open(r"college_images\This is the Plexus Live Wallpaper (same version of….jpeg").resize((150, 150), Image.Resampling.LANCZOS)
        self.photo_btn8 = ImageTk.PhotoImage(img_btn8)

        # Create buttons in 2 rows of 4
        btn1 = Button(bg_label, image=self.photo_btn1, text="Student Details", compound="top", font=("times new roman", 14, "bold"), bg="lightgray", fg="black", relief="raised", bd=5, command=self.student_details)
        btn1.place(x=150, y=300, width=250, height=180)

        btn2 = Button(bg_label, image=self.photo_btn2, text="Face Recognition", compound="top", font=("times new roman", 14, "bold"), bg="lightgray", fg="black", relief="raised", bd=5, command=self.face_recog)
        btn2.place(x=450, y=300, width=250, height=180)

        btn3 = Button(bg_label, image=self.photo_btn3, text="Attendance", compound="top", font=("times new roman", 14, "bold"), bg="lightgray", fg="black", relief="raised", bd=5, command=self.attendance)
        btn3.place(x=750, y=300, width=250, height=180)

        btn4 = Button(bg_label, image=self.photo_btn4, text="Help Desk", compound="top", font=("times new roman", 14, "bold"), bg="lightgray", fg="black", relief="raised", bd=5, command=self.help_desk)
        btn4.place(x=1050, y=300, width=250, height=180)

        btn5 = Button(bg_label, image=self.photo_btn5, text="Train Data", compound="top", font=("times new roman", 14, "bold"), bg="lightgray", fg="black", relief="raised", bd=5, command=self.train_data)
        btn5.place(x=150, y=500, width=250, height=180)

        btn6 = Button(bg_label, image=self.photo_btn6, text="Photos", compound="top", font=("times new roman", 14, "bold"), bg="lightgray", fg="black", relief="raised", bd=5, command=self.photos)
        btn6.place(x=450, y=500, width=250, height=180)

        btn7 = Button(bg_label, image=self.photo_btn7, text="Reports", compound="top", font=("times new roman", 14, "bold"), bg="lightgray", fg="black", relief="raised", bd=5, command=self.reports)
        btn7.place(x=750, y=500, width=250, height=180)

        btn8 = Button(bg_label, image=self.photo_btn8, text="Exit", compound="top", font=("times new roman", 14, "bold"), bg="red", fg="white", relief="raised", bd=5, command=self.exit_app)
        btn8.place(x=1050, y=500, width=250, height=180)

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def face_recog(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def help_desk(self):
        self.new_window = Toplevel(self.root)
        self.app = HelpDesk(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def photos(self):
        self.new_window = Toplevel(self.root)
        self.app = Photos(self.new_window)

    def reports(self):
        self.new_window = Toplevel(self.root)
        self.app = Reports(self.new_window)

    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
    