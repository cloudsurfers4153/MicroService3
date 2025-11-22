# MS3 – Reviews Service (Linux Deployment Guide)

FastAPI + MySQL microservice running on a Linux VM (e.g., Ubuntu 22.04).
Simple, reliable, no Docker.



## 1. Prerequisites

* OS: Ubuntu 22.04 (or other Debian-based Linux)
* Sudo access
* Code directory: `/home/zh2701/ms3-reviews`
* Python 3.10+
* Local MySQL running on the same VM
* Service port: `8000` (Uvicorn)



## 2. Install system packages


Start MySQL:

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```



## 3. Create virtual environment

```bash
cd /home/zh2701/ms3-reviews

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```



## 4. MySQL setup

### 4.1 Create database

```bash
sudo mysql
```

Inside MySQL:

```sql
CREATE DATABASE IF NOT EXISTS ms3_reviews
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 4.2 Create app user

```sql
CREATE USER 'ms3_app'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL PRIVILEGES ON ms3_reviews.* TO 'ms3_app'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4.3 Import schema and data

```bash
sudo mysql ms3_reviews < /home/zh2701/ms3-reviews/data.sql
```



## 5. Database URL

Recommended connection string:

```
mysql+pymysql://ms3_app:StrongPassword123!@localhost:3306/ms3_reviews
```

This can be set through an environment variable or systemd service.



## 6. Test service with Uvicorn

```bash
cd /home/zh2701/ms3-reviews
source .venv/bin/activate

uvicorn main:app --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Swagger UI:

```
http://<server-ip>:8000/docs
```



## 7. Systemd service (background process)

Create `/etc/systemd/system/ms3-reviews.service`:

```ini
[Unit]
Description=MS3 Reviews FastAPI Service
After=network.target mysql.service

[Service]
User=zh2701
Group=zh2701
WorkingDirectory=/home/zh2701/ms3-reviews
Environment="DATABASE_URL=mysql+pymysql://ms3_app:StrongPassword123!@localhost:3306/ms3_reviews"
Environment="PATH=/home/zh2701/ms3-reviews/.venv/bin"
ExecStart=/home/zh2701/ms3-reviews/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ms3-reviews
sudo systemctl start ms3-reviews
```


