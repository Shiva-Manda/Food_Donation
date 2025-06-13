# Food_Donation
This Django-based web application connects food donors (such as restaurants or individuals) with food receivers (like NGOs or orphanages). It facilitates efficient food sharing and donation management.
Features

Donor Side:
 Add food donation details
 View, update, or delete donations
 Receive and manage food requests (accept or decline)

Receiver Side:
  Search food by location
  Send request for available food
  Get notified when request is accepted or declined
  View donor contact on acceptance

Other Features:
  User signup/login using Django authentication
  Notification system for both parties
  Responsive UI using Bootstrap
  Data consistency and request conflict prevention (e.g. only one accepted request per       food item)

Tech Stack
Frontend: HTML, CSS, Bootstrap
Backend: Python, Django
Database: SQLite (for development)
Authentication: Django built-in auth system


Key Functionalities
 Prevent donors from requesting their **own food**
 Ensure only **one receiver can be approved** per donation
 Track **pickup status** and show relevant updates to all parties
 Maintain clean, intuitive navigation with buttons for:
   Donate Food
   Pickup Request
   Donation Status
   Pickup Status
   Logout

##  Setup Instructions 

# Clone the repo
git clone https://github.com/Shiva-Manda/Food_Donation.git
cd Food_Donation

# Set up virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver


# Clone the repository
git clone https://github.com/Shiva-Manda/Food_Donation.git



