# MS3 – Reviews Service (Two-VM Deployment Guide)

Database VM: **34.170.75.146**
Service VM: **34.61.43.139**

---

## 1. Prerequisites

### Database VM (34.170.75.146)

* Ubuntu 22.04
* MySQL 8.x
* Remote access enabled

### Service VM (34.61.43.139)

* Ubuntu 22.04
* Python 3.10+
* MySQL disabled
* Code directory: `/home/zh2701/MicroService3`
* Service port: `8000`

---

## 2. Disable MySQL on Service VM

```bash
sudo systemctl stop mysql
sudo systemctl disable mysql
sudo systemctl status mysql
```

---

## 3. Database Configuration (DB VM: 34.170.75.146)

### 3.1 Start MySQL

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 3.2 Enter MySQL

```bash
sudo mysql
```

### 3.3 Create Database

```sql
CREATE DATABASE IF NOT EXISTS MicroService3
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 3.4 Create Remote User

```sql
DROP USER IF EXISTS 'ms3user'@'%';

CREATE USER 'ms3user'@'%'
IDENTIFIED BY 'StrongPassword123!';

GRANT ALL PRIVILEGES ON MicroService3.* TO 'ms3user'@'%';

FLUSH PRIVILEGES;
```

### 3.5 Enable Remote Access

Edit:

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Change:

```
bind-address = 127.0.0.1
```

To:

```
bind-address = 0.0.0.0
```


OR

``` 
sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

```
Restart:

```bash
sudo systemctl restart mysql
```

### 3.6 Import Schema/Data

```bash
sudo mysql MicroService3 < /home/zh2701/database4153/ms3_mysql/data.sql
```

---

## 4. Service VM Setup

### 4.1 Create Virtual Environment

```bash

cd /home/zh2701/MicroService3

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install cryptography

```

---

## 5. Database URL (Use DB VM IP)

```
mysql+pymysql://ms3user:StrongPassword123!@34.170.75.146:3306/MicroService3
```

Example environment variable:

```env
DATABASE_URL="mysql+pymysql://ms3user:StrongPassword123!@34.170.75.146:3306/MicroService3"
```

---

## 6. Run Service

```bash
cd /home/zh2701/MicroService3
source .venv/bin/activate

uvicorn main:app --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Docs:

```
http://34.61.43.139:8000/docs
```

---

## 7. Connectivity Test

Run on Service VM:

```bash
telnet 34.170.75.146 3306
```

Expected: a successful TCP connection.
