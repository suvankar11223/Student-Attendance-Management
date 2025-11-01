import os
from tkinter import *
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk

class HelpDesk:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Help Desk - Face Recognition Attendance System")
        self.root.configure(bg="#f0f0f0")  # Set a light background for the main window

        # --- Define Fonts and Colors ---
        self.font_title = ("Segoe UI", 24, "bold")
        self.font_header = ("Segoe UI", 18, "bold")
        self.font_normal_bold = ("Segoe UI", 12, "bold")
        self.font_normal = ("Segoe UI", 11)
        
        self.color_primary_dark = "#2c3e50"  # Dark Blue/Charcoal
        self.color_primary_light = "#34495e" # Lighter Dark Blue
        self.color_accent = "#27ab83"       # Green
        self.color_text = "#ecf0f1"         # Light Gray/White
        self.color_bg = "#ffffff"           # White

        # --- Setup Styles ---
        self.setup_styles()

        # --- Create GUI ---
        self.create_banner()
        self.create_title()
        self.create_main_content()

    def setup_styles(self):
        """Creates all the ttk styles for the application."""
        style = ttk.Style()
        style.theme_use('default')

        # Main frame style
        style.configure("Main.TFrame", background=self.color_bg)
        
        # Title bar style
        style.configure("Title.TLabel", 
                        background=self.color_primary_dark, 
                        foreground=self.color_accent, 
                        font=self.font_title,
                        anchor=CENTER,
                        padding=(0, 10)) # top/bottom padding
        
        # Help content header style
        style.configure("Header.TLabel", 
                        background=self.color_bg, 
                        foreground=self.color_primary_dark, 
                        font=self.font_header,
                        anchor=W) # West (left) align
        
        # Helpline frame style
        style.configure("Helpline.TFrame", 
                        background="#f5f5f5", 
                        relief="solid", 
                        borderwidth=1,
                        bordercolor="#dddddd")
        
        style.configure("Helpline.TLabel", 
                        background="#f5f5f5", 
                        font=self.font_normal,
                        anchor=W)
        
        style.configure("Helpline.Header.TLabel", 
                        background="#f5f5f5", 
                        foreground="#c0392b", # Red color
                        font=self.font_normal_bold,
                        anchor=CENTER)

    def create_banner(self):
        """Creates the top banner with three images or fallbacks."""
        banner_frame = ttk.Frame(self.root, height=130)
        banner_frame.place(x=0, y=0, width=1530, height=130)

        img_paths = [
            r"college_images\↑↑↑ Larger size on website 🔸 A glowing blue cube….jpeg",
            r"college_images\49f04747-34cb-4f43-b932-78c9cb594a7c.jpeg",
            r"college_images\I'm trying but I'm so tired and it's late and I'm….jpeg"
        ]
        
        fallback_colors = ["#34495e", "#2c3e50", "#34495e"] # Dark theme fallbacks
        
        for i, (path, color) in enumerate(zip(img_paths, fallback_colors)):
            try:
                img = Image.open(path)
                img = img.resize((510, 130), Image.Resampling.LANCZOS)
                
                # Keep a reference to the image
                photo_img = ImageTk.PhotoImage(img)
                setattr(self, f"photoimg_top{i+1}", photo_img) # e.g., self.photoimg_top1
                
                lbl = Label(banner_frame, image=photo_img, borderwidth=0)
                lbl.place(x=i*510, y=0, width=510, height=130)
            
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                # Fallback label if image fails
                fallback_lbl = Label(banner_frame, 
                                     bg=color, 
                                     text=f"Image {i+1} (510x130)",
                                     font=("Segoe UI", 16),
                                     fg=self.color_text)
                fallback_lbl.place(x=i*510, y=0, width=510, height=130)

    def create_title(self):
        """Creates the main title bar below the banner."""
        title_lbl = ttk.Label(self.root, 
                              text="HELP DESK - FACE RECOGNITION ATTENDANCE SYSTEM", 
                              style="Title.TLabel")
        title_lbl.place(x=0, y=130, width=1530, height=50)

    def create_main_content(self):
        """Creates the main frame that holds the help content."""
        main_frame = ttk.Frame(self.root, style="Main.TFrame", padding=15)
        main_frame.place(x=0, y=180, width=1530, height=610)

        # Title for Help Content
        help_title = ttk.Label(main_frame, 
                               text="📚 Complete User Guide & Procedures", 
                               style="Header.TLabel")
        help_title.pack(fill=X, pady=(0, 10)) # Space below

        # Scrolled Text Widget
        self.help_text = scrolledtext.ScrolledText(main_frame, 
                                                   wrap=WORD, 
                                                   font=self.font_normal, 
                                                   bg=self.color_bg, 
                                                   fg="black", 
                                                   relief="solid", 
                                                   bd=1,
                                                   padx=10, 
                                                   pady=10)
        self.help_text.pack(fill=BOTH, expand=True)

        # --- Define text styles (tags) for Markdown ---
        self.help_text.tag_configure("h1", 
                                     font=("Segoe UI", 18, "bold"), 
                                     foreground=self.color_primary_dark,
                                     spacing3=10) # Space after paragraph
        
        self.help_text.tag_configure("h2", 
                                     font=("Segoe UI", 14, "bold"), 
                                     foreground=self.color_primary_light,
                                     spacing3=8)
        
        self.help_text.tag_configure("bold", 
                                     font=self.font_normal_bold)
        
        self.help_text.tag_configure("error", 
                                     font=self.font_normal, 
                                     foreground="red")

        # Load and display README content
        self.load_and_parse_readme()

        # Helpline Information at Bottom
        helpline_frame = ttk.Frame(main_frame, style="Helpline.TFrame", padding=10)
        helpline_frame.pack(fill=X, pady=(15, 0)) # Space above

        helpline_label = ttk.Label(helpline_frame, 
                                   text="🚨 TECHNICAL SUPPORT HELPLINE 🚨", 
                                   style="Helpline.Header.TLabel")
        helpline_label.pack(pady=5, fill=X)

        helpline_details = (
            "📞 Contact: +1-800-FACE-HELP (1-800-322-3435)\n"
            "📧 Email: support@facerecognition.edu\n"
            "🕒 Hours: Monday-Friday, 9 AM - 6 PM EST"
        )
        helpline_number = ttk.Label(helpline_frame, 
                                    text=helpline_details, 
                                    style="Helpline.TLabel",
                                    justify=CENTER) # Center the multi-line text
        helpline_number.pack(pady=5, fill=X)


    def load_and_parse_readme(self):
        """Load README.md, parse basic Markdown, and display it."""
        try:
            readme_path = "README.md"
            if os.path.exists(readme_path):
                with open(readme_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        
                        # --- Markdown Parsing Logic ---
                        if line.startswith("# "):
                            self.help_text.insert(END, line[2:] + "\n", "h1")
                        elif line.startswith("## "):
                            self.help_text.insert(END, line[3:] + "\n", "h2")
                        elif line.startswith("* "):
                            self.help_text.insert(END, "  • " + line[2:] + "\n")
                        elif "**" in line:
                            # Simple bold handling (handles one pair per line)
                            parts = line.split('**')
                            for i, part in enumerate(parts):
                                if i % 2 == 1: # Odd parts are bold
                                    self.help_text.insert(END, part, "bold")
                                else:
                                    self.help_text.insert(END, part)
                            self.help_text.insert(END, "\n")
                        else:
                            self.help_text.insert(END, line + "\n")
                        
                        self.help_text.insert(END, "\n") # Add spacing between paragraphs
            else:
                self.help_text.insert(END, "❌ README.md file not found.\n\n", "error")
                self.help_text.insert(END, "Please ensure the documentation file is present in the project directory.")
        
        except Exception as e:
            self.help_text.insert(END, f"❌ Error loading help content: {str(e)}", "error")
        
        finally:
            self.help_text.config(state=DISABLED) # Make it read-only


if __name__ == "__main__":
    root = Tk()
    obj = HelpDesk(root)
    root.mainloop()