# 📊 Portfolio Analyzer

A Django-based web application to track, analyze, and manage investment portfolios with features like stock tracking, price alerts, and AI-powered insights.

---

## 🚀 Features

* 📈 Track stock investments and holdings
* 💰 Buy & sell assets with transaction history
* 🔔 Set price alerts for stocks
* 🤖 AI-powered insights (portfolio_ai module)
* 📊 Dashboard with portfolio overview
* 👤 User authentication system
* 📋 Watchlist management

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** PostgreSQL (also used for the cache and sessions)
* **Other Tools:** webhint (code quality), Git

---

## 📁 Project Structure

```
ai_portfolio/
│
├── ai/                # AI-related logic
├── portfolio/         # Core portfolio app
├── portfolio_ai/      # AI integration
├── stocks/            # Stock-related features
├── users/             # Authentication & users
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── manage.py          # Django entry point
├── Schema.sql         # Database schema
└── README.md
```

---

## ⚙️ Installation & Setup

### Use python 3.12 version for few packages to support

### 1. Clone the repository

```bash
git clone https://github.com/UnK3N0wN/Portfolio-Analyzer.git
cd Portfolio-Analyzer
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the environment

Copy `.env.example` to `.env` and fill in the PostgreSQL credentials (`DB_*`).

### 5. Run migrations and create the cache table

```bash
python manage.py migrate
python manage.py createcachetable
```

### 6. Run server

```bash
python manage.py runserver
```

---

## 📸 Screenshots

<img width="1502" height="836" alt="Profile" src="https://github.com/user-attachments/assets/b05df704-68ff-4f8c-ae8a-d4358f07e8d7" />
<img width="1528" height="647" alt="Portfolio" src="https://github.com/user-attachments/assets/1ad6e507-4e92-45d8-90fd-4bfe39ce3bbf" />
<img width="1643" height="895" alt="Dashboard" src="https://github.com/user-attachments/assets/097cbbb1-079c-487b-9c6a-3b6be7d57dbd" />
<img width="1487" height="781" alt="ai_chat" src="https://github.com/user-attachments/assets/e3ee3675-3d2b-4908-a2e0-7c9643495284" />
<img width="1491" height="622" alt="alerts" src="https://github.com/user-attachments/assets/5f8dd53a-2b43-4f3b-b692-30b9dfdddb4a" />


---

## 📌 Future Improvements

* 🔐 Add JWT authentication
* ☁️ Deploy on cloud (AWS/Render)
* 📊 Advanced analytics & charts
* 📡 Live stock API integration

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and submit a pull request.

---

## 📄 License

This project is for educational purposes.

---

## 👨‍💻 Author

**Blesson**
GitHub: https://github.com/UnK3N0wN

---

⭐ If you like this project, consider giving it a star!
