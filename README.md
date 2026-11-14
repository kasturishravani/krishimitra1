# KrishiMitra – Smart Farmer Assistance Platform (కృషిమిత్ర)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)](https://palletsprojects.com/p/flask/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![Web Speech API](https://img.shields.io/badge/Web_Speech_API-Bilingual-teal.svg)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

> **College Mini-Project:** Full-Stack Agritech Web Application for Indian Farmers with Crop Tracking, Pest Diagnostics, Mandi Prices, Localized Weather Advisories, and a Bilingual AI Voice Assistant supporting **English** and **Telugu (తెలుగు)**.

---

## 🌾 Project Overview

**KrishiMitra (కృషిమిత్ర)** is an end-to-end, full-stack smart agricultural assistance platform built specifically to support smallholder Indian farmers. It consolidates daily agricultural decision-making into a clean, modern, high-contrast, responsive green-and-white dashboard.

The application does **not require paid APIs or third-party paid subscriptions**. All weather advisories, APMC mandi commodity rates, and government schemes are managed through optimized local datasets, while the AI Chatbot and Voice Assistant utilize rule-based keyword intent matching and native browser Web Speech APIs (`SpeechRecognition` and `SpeechSynthesis`).

---

## 🚀 Key Modules Implemented

| # | Module | Description |
|---|---|---|
| **1** | **Farmer Registration & Login** | Secure account creation with field details (mobile, land size in acres, soil type, district), password hashing with Werkzeug `scrypt`, session management, and validation. |
| **2** | **Farmer Profile & Dashboard** | Agricultural dashboard with personalized greetings, quick action cards, plot metric statistics, weather preview, live mandi rates ticker, and Chart.js analytics. |
| **3** | **Crop Advisory & Crop Tracking (CRUD)** | Complete CRUD operations for farm plots: Add Crop, View Crop List & Progress Timeline, Update Stage & Health, Record Field Activities (Irrigation, Fertilizer, Sprays), and Delete Records. Soil-based advisory engine. |
| **4** | **Pest & Crop Disease Camera Scanner** | Live device camera scanner (`getUserMedia`) and image upload diagnostic engine. Captures photos of affected leaves/crops, detects pathogen/disease, computes confidence scores, and prescribes biological (Neem/Jeevamrutha) and chemical treatments. |
| **5** | **Weather Information & Advisories** | District-wise current temperature, humidity, wind velocity, precipitation probability, 5-day agro-forecast, and actionable daily spraying and irrigation advisories. |
| **6** | **Market Prices (Mandi Bhav)** | APMC mandi commodity price tracker with minimum, maximum, and modal prices per quintal, price change trends (↑/↓), 6-month historical price trend charts (Chart.js), and official MSP tables. |
| **7** | **Government Schemes Directory** | Detailed guides for PM-KISAN, PMFBY (Crop Insurance), PMKSY (Micro-irrigation), Soil Health Card, KCC, SMAM (Machinery subsidy), and Rythu Bandhu with eligibility and application steps. |
| **8** | **Farming Tips & Natural Agronomy** | Best practices covering Jeevamrutha preparation, Alternate Wetting & Drying (AWD) water conservation, 5% Neem Seed Kernel Extract (NSKE), and legume intercropping. |
| **9** | **Emergency Help & SOS Center** | Direct click-to-call for National Kisan Call Center (1800-180-1551) and District Agriculture Officers, plus an urgent SOS ticket submission system with live status tracking. |
| **10** | **Nearby Agricultural Services** | Directory of Krishi Vigyan Kendras (KVK), soil testing labs, authorized fertilizer dealers, cold storages, and custom machinery rental centers. |
| **11** | **AI Farmer Chatbot** | Rule-based and keyword-driven intelligent assistant answering queries in **English** and **Telugu**, complete with clickable recommendation chips and auto-scroll typing interface. |
| **12** | **Bilingual Voice Assistant** | Interactive speech assistant utilizing browser Web Speech API (`SpeechRecognition` & `SpeechSynthesis`). Supports English (`en-IN`) and Telugu (`te-IN`) for voice input and vocal spoken answers. |

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4, Vanilla JavaScript (ES6+)
- **Backend:** Python 3.10+, Flask 3.1+
- **Database:** MySQL 8.0 / MariaDB (with transparent SQLite fallback if MySQL is offline)
- **Database Driver:** PyMySQL
- **Voice Engine:** Browser Native Web Speech API (`webkitSpeechRecognition` / `SpeechRecognition`) & `window.speechSynthesis` (`SpeechSynthesisUtterance`)
- **Chatbot Engine:** Multi-intent pattern matching and bilingual translation dictionary (`chatbot_engine.py`)

---

## 📁 Project Directory Structure

```
krishimitra/
├── app.py                     # Main Flask routes, controllers, and APIs
├── config.py                  # Database & environment configurations
├── database.py                # Database connection helper & SQLite fallback
├── database.sql               # MySQL DDL schema and seed records
├── chatbot_engine.py          # Bilingual rule-based chatbot & voice processor
├── sample_data.py             # Realistic local datasets (Weather, Mandi, Diseases, Schemes)
├── start_app.sh               # One-click startup execution script
├── requirements.txt           # Python package dependencies
├── README.md                  # Comprehensive documentation and execution guide
├── static/
│   ├── css/
│   │   ├── style.css          # Agricultural theme colors, cards, floating widgets
│   │   └── dashboard.css      # Dashboard layout, sidebar, tables, timelines
│   └── js/
│       ├── main.js            # Tooltips, flash auto-dismiss, form validation
│       ├── chatbot.js         # Chat drawer widget, quick chips, message handling
│       ├── voice_assistant.js # Web Speech recognition & SpeechSynthesis in EN & TE
│       └── charts.js          # Chart.js analytics for crop health and mandi trends
└── templates/
    ├── base.html              # Master layout with responsive navbar, footer & modals
    ├── index.html             # Landing page with hero banner & live widgets
    ├── auth/
    │   ├── login.html         # Farmer sign in with demo autofill
    │   └── register.html      # Farmer registration with land and soil details
    ├── dashboard/
    │   ├── index.html         # Farmer dashboard with stats, crops preview & charts
    │   └── profile.html       # Profile management and password updates
    ├── crops/
    │   ├── list.html          # Tracked crops list with search & filters
    │   ├── add.html           # Add new crop plot form
    │   ├── edit.html          # Edit crop details form
    │   ├── detail.html        # Individual crop lifecycle timeline & activities log
    │   └── advisory.html      # Soil & season-based crop advisory engine
    ├── diseases/
    │   ├── index.html         # Crop disease directory & symptom matcher
    │   └── detail.html        # Full treatment protocol (biological & chemical)
    ├── weather/
    │   └── index.html         # 5-day weather forecast & spraying advisory
    ├── market/
    │   └── index.html         # Mandi Bhav prices, historical chart & MSP guide
    ├── schemes/
    │   └── index.html         # Government schemes directory & category filter
    │   └── detail.html        # Step-by-step application checklist
    ├── tips/
    │   └── index.html         # Natural farming best practices & recipes
    ├── emergency/
    │   └── index.html         # Kisan Call Center & rapid SOS ticket portal
    ├── services/
    │   └── index.html         # Nearby KVK, fertilizer retailers & machinery rentals
    └── chatbot/
        └── index.html         # Dedicated full-page bilingual AI Chatbot
```

---

## 🗄️ Database Design & Schema (`database.sql`)

The application stores farmer and plot data in MySQL (`krishimitra` database):

1. **`farmers` Table**:
   - `id` (INT, PK, Auto Increment)
   - `full_name` (VARCHAR 100)
   - `mobile` (VARCHAR 15, Unique)
   - `email` (VARCHAR 100)
   - `password_hash` (VARCHAR 255)
   - `state`, `district`, `village`
   - `land_size_acres` (DECIMAL 5,2)
   - `soil_type` (VARCHAR 50)
   - `preferred_language` (VARCHAR 20)
   - `created_at`, `updated_at`

2. **`crops` Table**:
   - `id` (INT, PK)
   - `farmer_id` (FK referencing `farmers.id`)
   - `crop_name`, `variety`
   - `sowing_date`, `expected_harvest_date`
   - `area_acres` (DECIMAL 5,2)
   - `soil_type`
   - `stage` (`Sowing`, `Germination`, `Vegetative`, `Flowering`, `Yield Formation`, `Ripening`, `Harvested`)
   - `health_status` (`Healthy`, `At Risk`, `Diseased`)
   - `notes` (TEXT)

3. **`crop_activities` Table**:
   - `id` (INT, PK)
   - `crop_id` (FK referencing `crops.id`)
   - `activity_type` (`Irrigation`, `Fertilizer`, `Pesticide Spray`, `Weeding`, `Harvesting`, `Inspection`)
   - `activity_date` (DATE)
   - `notes` (VARCHAR 255)

4. **`emergency_sos` Table**:
   - `id` (INT, PK)
   - `farmer_id`, `farmer_name`, `contact_number`, `district`, `village`
   - `issue_type`, `severity` (`Low`, `Medium`, `High`, `Critical`)
   - `description` (TEXT)
   - `status` (`Pending`, `In Progress`, `Resolved`)

5. **`chat_logs` Table**:
   - `id` (INT, PK)
   - `farmer_id`, `user_message`, `bot_response`, `language`, `created_at`

---

## 💻 Installation & Local Execution Guide

### 1. Prerequisites
- **Python 3.10** or higher
- **MySQL 8.0+** or MariaDB (Note: An automatic SQLite fallback is included if MySQL is not installed on your machine)
- Web Browser: Google Chrome, Microsoft Edge, or Safari (for Web Speech API support)

---

### 2. Clone or Navigate to Project
```bash
cd /home/rgukt-basar/Documents/krishimitra
```

---

### 3. Create & Activate Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows (Command Prompt):
python -m venv venv
venv\Scripts\activate
```

---

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 5. Set Up MySQL Database
Make sure your MySQL service is running, then load the database schema:
```bash
mysql -u root -p < database.sql
```
*(If your MySQL user has no password, simply run `mysql -u root < database.sql`)*.

Optional `.env` configuration (if your MySQL port or password differs):
```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=krishimitra
SECRET_KEY=krishimitra-secret-key-2026-agro-secure
```

---

### 6. Run the Application
You can start the server using either the startup script or standard Python:

```bash
# Option A: One-click script
./start_app.sh

# Option B: Direct Python
python3 app.py
```

The application will start on **`http://127.0.0.1:5000`**. Open this URL in your web browser.

---

## 🔑 Demo Account Credentials

A pre-seeded demonstration farmer is loaded in the database for instant evaluation:

| Field | Value |
|---|---|
| **Mobile Number** | `9876543210` |
| **Password** | `farmer123` |
| **Farmer Name** | Ramesh Patel |
| **District** | Nirmal, Telangana |
| **Tracked Crops** | Paddy (Rice), Bt Cotton, Chilli |

*On the Login page, you can also click the **"Auto-Fill Demo Credentials"** button for 1-click access.*

---

## 🎙️ Using the Bilingual Voice Assistant

1. Click the floating green **Microphone Button** on the bottom-right or the **"Voice / వాయిస్"** pill in the top navigation bar.
2. Select your preferred voice language:
   - **English (India)** 🇮🇳
   - **తెలుగు (Telugu)** 🇮🇳
3. Tap the central microphone icon and speak clearly.
4. **Sample Voice Commands to Try:**
   - *"Open dashboard"* / *"డాష్‌బోర్డ్"*
   - *"Check weather"* / *"వాతావరణం"*
   - *"Mandi prices today"* / *"మార్కెట్ ధరలు"*
   - *"Paddy blast disease remedy"* / *"వరి తెగులు నివారణ"*
   - *"How to cure cotton pink bollworm?"*
   - *"Tell me about PM-KISAN scheme"* / *"పీఎం కిసాన్"*
   - *"Emergency helpline number"* / *"సహాయం"*
   - *"How to prepare Jeevamrutha?"* / *"జీవామృతం"*
5. The assistant transcribes your voice, matches the agricultural intent, and reads the answer aloud using browser speech synthesis!

---

## 🧪 Testing the Application

An automated integration test suite is included. Run it anytime using:

```bash
./venv/bin/python3 -c "
import app, json
client = app.app.test_client()

# 1. Login
res = client.post('/login', data={'login_id': '9876543210', 'password': 'farmer123'}, follow_redirects=True)
assert res.status_code == 200

# 2. Check Dashboard
res = client.get('/dashboard')
assert res.status_code == 200

# 3. Test Chatbot API
res = client.post('/api/chat', json={'message': 'Paddy blast cure'})
assert res.status_code == 200
assert 'Tricyclazole' in json.loads(res.data)['response_text']

print('All automated tests passed successfully!')
"
```

---

## 🎓 Academic Mini-Project Viva Notes

- **Architecture:** Model-View-Controller (MVC) paradigm implemented via Flask routes (Controllers), Jinja2 templates (Views), and MySQL tables with PyMySQL (Models).
- **Security:** Passwords are never stored in plaintext; salted and hashed using `werkzeug.security.generate_password_hash` (`scrypt`). Sessions use signed HTTP-only cookies.
- **Accessibility:** Large buttons, high contrast badges, simple card layouts, and speech accessibility designed for rural Indian farmers with diverse literacy levels.
- **Zero-Cost Design:** No third-party API keys (e.g. OpenAI or Google Cloud APIs) are required; standard Web APIs and calibrated local agronomy datasets allow 100% offline-compatible, free operation.

---

## 📄 License
This project is developed as an academic college mini-project. Open for educational and non-commercial agricultural development.
# krishimitra
