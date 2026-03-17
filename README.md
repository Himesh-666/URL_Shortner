# 🔗 URL Shortener

A simple and efficient **URL Shortener web application built using Django and SQLite**.
This project converts long URLs into short, easy-to-share links and redirects users to the original URL when the short link is accessed.

The goal of this project is to demonstrate **backend development, database management, and web routing** using the Django framework.

---

## 🚀 Features

* Convert long URLs into short links
* Fast redirection to the original URL
* Clean and responsive user interface
* Unique short code generation
* Database storage of URL mappings
* Modular Django project structure
* Ready for future extensions like analytics and link expiration

---

## 🏗️ Project Architecture

The project follows a **modular Django architecture**:

```
URL_SHORTNER
│
├── shortener        # Core URL shortening logic
├── analytics        # Click tracking (future feature)
├── expiration       # Link expiry system (future feature)
├── URL_Shortner     # Project configuration
└── db.sqlite3       # SQLite database
```

---

## ⚙️ Tech Stack

* **Backend:** Django (Python)
* **Database:** SQLite
* **Frontend:** HTML, Bootstrap
* **Version Control:** Git & GitHub

---

## 🧠 How It Works

1. User enters a long URL.
2. The system generates a **unique short code**.
3. The mapping between the original URL and the short code is stored in the database.
4. When the short URL is accessed, the server looks up the original URL.
5. The user is automatically redirected to the original website.

Example:

```
Original URL:
https://youtube.com/watch?v=example

Generated Short URL:
http://localhost:8000/aB92kL
```

---

## 💻 Installation & Setup

Clone the repository:

```bash
git clone https://github.com/Himesh-666/URL_Shortner.git
cd URL_Shortner
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## 📌 Future Improvements

* Click analytics dashboard
* URL expiration feature
* Custom short URLs
* User authentication
* API endpoints for programmatic access
* Deployment with HTTPS support

---

## 👨‍💻 Author

**Himeshwar**

Computer Science student passionate about backend development, system design, and building real-world projects.

GitHub:
https://github.com/Himesh-666
