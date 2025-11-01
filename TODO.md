# Student Portal Implementation TODO

## Database Schema Updates
- [x] Add 'password' column to student table (VARCHAR(255) for hashed passwords)
- [x] Create 'correction_requests' table with columns: id (AUTO_INCREMENT PRIMARY KEY), student_id (VARCHAR(20)), date (DATE), reason (TEXT), status (ENUM('pending', 'approved', 'rejected') DEFAULT 'pending')

## Student Portal Development
- [ ] Create student_portal.py with Streamlit app
- [ ] Implement login page (StudentId + password authentication)
- [ ] Build attendance history view with calendar visualization
- [ ] Add attendance percentage calculation using pandas
- [ ] Implement correction request submission form
- [ ] Add view for submitted correction requests

## Admin Dashboard Integration
- [ ] Add "Student Portal" button to main.py admin dashboard
- [ ] Update main.py to launch student portal in new window/process

## Setup & Testing
- [x] Install streamlit via pip
- [ ] Set default passwords for existing students (e.g., 'password123' hashed)
- [ ] Test login functionality
- [ ] Test attendance viewing and percentage calculation
- [ ] Test correction request submission
- [ ] End-to-end testing of portal features
