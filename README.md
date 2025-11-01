# 🎓 Student Attendance Management System

## 📋 Project Overview

A comprehensive **Face Recognition Attendance System** built with Python, OpenCV, and MySQL. This intelligent system automatically detects and recognizes student faces using advanced machine learning algorithms, marks attendance in real-time, and maintains detailed records across multiple storage formats. Features a modern GUI interface for seamless management and monitoring.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

## ✨ Key Features

### 🔍 Face Recognition & Detection
- Real-time face detection using Haar cascades
- LBPH (Local Binary Patterns Histograms) face recognition
- Confidence-based matching (>60% confidence required)
- Automatic attendance marking upon successful recognition

### 💾 Data Management
- **Dual Storage**: Simultaneous saving to CSV and MySQL database
- **Auto Excel Export**: Automatic Excel file generation with date-based naming
- **Database Integration**: MySQL database for persistent storage
- **CSV Backup**: Local CSV files for quick access and backup

### 🎯 GUI Interface
- **Configuration Panel**: Teacher selection, course credits, date ranges
- **Real-time Monitoring**: Live status updates and progress indicators
- **Attendance Table**: View, filter, and export attendance records
- **Color-coded Display**: Visual indicators for attendance status

### 📊 Analytics & Reporting
- **Credit-based System**: Dynamic class calculation (1-4 credits)
- **Date Filtering**: Filter attendance by specific dates
- **Export Options**: Manual Excel export with custom filenames
- **Percentage Calculation**: Attendance percentage tracking

## 🛠️ System Requirements

### Hardware Requirements
- **Camera**: Webcam or external camera (tested with 480x640 resolution)
- **RAM**: Minimum 4GB (recommended 8GB)
- **Storage**: 500MB free space for models and data
- **Processor**: Intel i3 or equivalent (recommended i5+)

### Software Requirements
- **Operating System**: Windows 10/11, Linux, or macOS
- **Python**: Version 3.8 or higher
- **MySQL Server**: Version 5.7 or higher

## 📦 Installation & Setup

### 1. Python Environment Setup

```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 2. Install Dependencies

```bash
pip install opencv-python mysql-connector-python pandas tkcalendar pillow
```

### 3. MySQL Database Setup

#### Install MySQL Server
- Download and install MySQL from [mysql.com](https://www.mysql.com/)
- Or use XAMPP/WAMP for Windows users

#### Create Database and Tables

```sql
-- Create database
CREATE DATABASE face_recognizer;

-- Use the database
USE face_recognizer;

-- Create student table
CREATE TABLE student (
    StudentId VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(100),
    Address TEXT,
    Gender VARCHAR(10),
    DOB DATE,
    Photo BLOB
);

-- Create attendance table
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    name VARCHAR(100),
    phone VARCHAR(20),
    date DATE,
    time TIME,
    teacher VARCHAR(100),
    credits INT,
    total_classes INT
);
```

#### Database Configuration
Update the database credentials in `attendance.py`:

```python
self.db_config = {
    'host': "localhost",
    'username': "root",  # Your MySQL username
    'password': "your_password",  # Your MySQL password
    'database': "face_recognizer"
}
```

### 4. Project File Structure

```
Face_detection_Project/
├── attendance.py              # Main attendance system GUI
├── face_recognition.py        # Face recognition training module
├── student.py                 # Student management system
├── train.py                   # Model training script
├── main.py                    # Application launcher
├── photos.py                  # Photo capture utility
├── trainer.yml               # Trained face recognition model
├── haarcascade_frontalface_default.xml  # Face detection classifier
├── attendance.csv            # CSV attendance backup
├── attendance_YYYY-MM-DD.xlsx # Auto-generated Excel reports
├── college_images/           # Banner images
├── data/                     # Student photo storage
├── __pycache__/              # Python cache files
├── .venv/                    # Virtual environment
└── README.md                 # This documentation
```

## 🚀 Usage Guide

### Step 1: Launch the Application

```bash
python main.py
```

This opens the main menu with options for:
- Student Management
- Face Recognition Training
- Attendance System
- Photo Capture

### Step 2: Student Registration

1. **Add Students**: Use `student.py` to register students
2. **Capture Photos**: Use `photos.py` to take multiple photos per student
3. **Train Model**: Run `train.py` to train the face recognition model

### Step 3: Train the Recognition Model

```bash
python train.py
```

This will:
- Load student photos from `data/` folder
- Train the LBPH face recognizer
- Save the trained model to `trainer.yml`

### Step 4: Configure Attendance System

1. **Launch Attendance System**: Run `python attendance.py`
2. **Select Teacher**: Choose from dropdown (Dr. Smith, Prof. Johnson, etc.)
3. **Set Course Credits**: Select 1-4 credits
4. **Calculate Classes**: Click "Calculate Total Classes" button
5. **Set Date Range**: Optional semester start/end dates

### Step 5: Mark Attendance

1. **Start Attendance**: Click "START ATTENDANCE MARKING"
2. **Camera Activation**: System opens camera feed
3. **Face Detection**: Students look at camera
4. **Automatic Marking**: Attendance marked when face recognized (>60% confidence)
5. **Stop Process**: Press 'q' or wait 30 seconds

### Step 6: View & Export Records

- **View Table**: All attendance records displayed in GUI table
- **Filter by Date**: Use date picker to filter records
- **Auto Excel Export**: Files automatically created as `attendance_YYYY-MM-DD.xlsx`
- **Manual Export**: Use "Export to Excel" button for custom filenames

## 📊 Credit System Details

| Credits | Total Classes |
|---------|---------------|
| 1       | 8            |
| 2       | 12           |
| 3       | 16           |
| 4       | 22           |

## 🔧 Configuration Options

### Attendance Settings
- **Confidence Threshold**: 60% (configurable in code)
- **Camera Index**: 0 (default webcam)
- **Timeout**: 30 seconds per session
- **Face Detection Scale**: 1.3 (sensitivity)

### Database Settings
- **Host**: localhost
- **Database**: face_recognizer
- **Tables**: student, attendance

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. Camera Not Opening
**Error**: "Could not open camera"
**Solutions**:
- Check camera permissions
- Try different camera index: `cv2.VideoCapture(1)`
- Restart application
- Check camera hardware

#### 2. Face Not Detected
**Error**: No faces detected
**Solutions**:
- Ensure good lighting
- Position face clearly in frame
- Check camera angle
- Retrain model with better photos

#### 3. Database Connection Failed
**Error**: "Database error"
**Solutions**:
- Verify MySQL server is running
- Check credentials in code
- Ensure database and tables exist
- Check MySQL port (default 3306)

#### 4. Model Not Loading
**Error**: "Trained model not found"
**Solutions**:
- Run training script first
- Check `trainer.yml` exists
- Verify training completed successfully

#### 5. Excel Export Fails
**Error**: "Export failed"
**Solutions**:
- Install pandas: `pip install pandas`
- Check write permissions
- Ensure CSV file exists

### Performance Tips

1. **Training**: Use 10-20 photos per student for better accuracy
2. **Lighting**: Ensure consistent, bright lighting
3. **Distance**: Keep face 2-3 feet from camera
4. **Angle**: Face camera directly for best recognition
5. **Background**: Use plain background to reduce interference

## 📈 System Architecture

### Data Flow
1. **Input**: Camera feed → Face detection
2. **Processing**: Face recognition → Database lookup
3. **Output**: Attendance marking → CSV + Database + Excel export

### Components
- **GUI Layer**: Tkinter-based interface
- **Recognition Layer**: OpenCV face detection/recognition
- **Data Layer**: MySQL database + CSV files
- **Export Layer**: Pandas Excel generation

## 🔐 Security & Privacy

- Student photos stored locally in `data/` folder
- Database credentials should be secured
- Attendance data contains personal information
- Regular backup of database recommended

## 📞 Support & Maintenance

### Regular Maintenance Tasks
1. **Model Retraining**: Retrain model when adding new students
2. **Database Backup**: Regular backup of attendance records
3. **Photo Cleanup**: Remove old/unused student photos
4. **Log Review**: Check application logs for errors

### Log Files
- Application logs saved to console/terminal
- CSV files serve as backup
- Database provides persistent storage

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request

## 📜 License

This project is open-source. Please respect intellectual property rights.

## 👥 Credits

**Developed by**: Face Recognition Attendance System Team

**Technologies Used**:
- Python 3.8+
- OpenCV 4.x
- MySQL 5.7+
- Tkinter (GUI)
- Pandas (Data processing)

---

**Last Updated**: October 31, 2025
**Version**: 1.0.0

For additional support or questions, please refer to the troubleshooting section or check the application logs.
#   S t u d e n t - A t t e n d a n c e - M a n a g e m e n t  
 