# 📈 Market Pulse — Real-Time Financial Telemetry & Dashboard

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0%2B-092E20?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Asynchronous-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Message_Broker-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-Data_Viz-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)
![Linux](https://img.shields.io/badge/Ubuntu-24.04_LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

**Market Pulse** is an asynchronous financial monitoring engine and live analytics dashboard. It streams real-time asset telemetry (Cryptocurrencies, Gold, Oil) without blocking HTTP threads, leveraging periodic worker queues, and renders interactive SVG/Canvas charts and on-the-fly currency arbitrage conversions.

---

## ⚡ Key Architectural Features

- **Decoupled Asynchronous Ingestion:** Uses **Celery Beat** to schedule non-blocking price-fetching tasks offloading heavy network I/O from Django WSGI/ASGI workers.
- **Message Broker Architecture:** Integrated with **Redis** for distributed task orchestration and volatile state buffering.
- **High-Frequency Chart Telemetry:** Frontend polling loop consuming optimized JSON endpoints rendering sub-second line charts with **Chart.js**.
- **Real-Time Currency Arbitrage / Converter:** Instant asset-to-asset evaluation engine computing live cross-rates based on in-memory dynamic prices.
- **Bilingual & Responsive UI:** Fully customizable Dark-mode interface supporting English and Persian (RTL) locales.

---

## 🛠 Tech Stack & Dependencies

- **Backend:** Python 3.12+, Django, Django-Celery-Beat
- **Task Queue & Broker:** Celery, Redis
- **Database:** SQLite3 (Configurable for PostgreSQL)
- **Frontend:** Vanilla HTML5/CSS3 (Modern Glassmorphism & Custom Properties), JavaScript (ES6+), Chart.js
- **Platform:** Ubuntu Linux 24.04 LTS

---

## 🚀 Quick Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/market-pulse.git
cd market-pulse
2. Set up virtual environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Database Migration & Seed Initial Data

python manage.py migrate
python manage.py loaddata initial_data.json
4. Run Redis Broker
Ensure Redis is active on your Linux machine:

sudo systemctl start redis-server
5. Launch Workers & Beat Scheduler
Open a separate terminal instance and start Celery:


# Terminal 1: Celery Worker
celery -A core worker -l info

# Terminal 2: Celery Beat
celery -A core beat -l info
6. Start Django Development Server
bash
python manage.py runserver
Visit http://127.0.0.1:8000 in your web browser.

👨‍💻 Author
Taha Nemati

Focus: Python / Django Backend Development & Distributed Systems
OS: Ubuntu Linux
License: MIT


---

