# MS3 – Reviews Service

## Secure Two-VM Deployment Guide (Internal VPC Networking)

* **Database VM (DB VM)**

  * External IP: `34.170.75.146` (optional, not required for app connectivity)
  * Internal IP: `10.128.0.3`

* **Service VM (App VM)**

  * External IP: `34.61.43.139` (used to access the HTTP API/docs)
  * Internal IP: `10.128.0.4`

The Reviews service runs as a Python/FastAPI application on the **Service VM**, and connects to a MySQL database on the **Database VM** using **internal VPC networking**, not the public internet.

---

## 1. Architecture & Requirements

### 1.1 High-Level Architecture

* The **Service VM** exposes an HTTP API on port **8000** (FastAPI + Uvicorn).
* The **Database VM** runs **MySQL 8.x** and is only accessible:

  * on its **internal IP `10.128.0.3`**, and
  * from the **Service VM internal IP `10.128.0.4`**.
* Connectivity between the two VMs uses **VPC internal IPs**.
* The database is **not exposed on the public internet**.

### 1.2 Prerequisites

#### Database VM (`10.128.0.3` / `34.170.75.146`)

* Ubuntu 22.04
* MySQL 8.x installed
* MySQL service enabled

#### Service VM (`10.128.0.4` / `34.61.43.139`)

* Ubuntu 22.04
* Python 3.10+
* MySQL **not** running locally
* Application code directory: `/home/zh2701/MicroService3`
* Service port: `8000`

---

## 2. Disable MySQL on the Service VM

The Service VM should not host its own MySQL instance. It must connect only to the **DB VM**.

On the **Service VM** (`10.128.0.4`):

```bash
sudo systemctl stop mysql
sudo systemctl disable mysql
sudo systemctl status mysql
```

`status` should show MySQL as **inactive/disabled**.

---

## 3. Configure the Database VM

All commands in this section are run on the **Database VM** (`10.128.0.3`).

### 3.1 Start & Enable MySQL

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

Verify:

```bash
sudo systemctl status mysql
```

MySQL should be **active (running)**.

---

### 3.2 Enter MySQL Shell

```bash
sudo mysql
```

You should get a `mysql>` prompt.

---

### 3.3 Create Database

Inside the MySQL shell:

```sql
CREATE DATABASE IF NOT EXISTS MicroService3
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

---

### 3.4 Create Application User (Internal-Only)

We restrict the MySQL user so that only the **Service VM internal IP `10.128.0.4`** can connect.

Still inside the MySQL shell:

```sql
-- Clean up any overly-permissive user
DROP USER IF EXISTS 'ms3user'@'%';

-- Create a user restricted to the Service VM internal IP
CREATE USER 'ms3user'@'10.128.0.4'
IDENTIFIED BY 'StrongPassword123!';

GRANT ALL PRIVILEGES ON MicroService3.* TO 'ms3user'@'10.128.0.4';

FLUSH PRIVILEGES;
```

> If  temporarily want to allow any internal 10.x address, one could use `'ms3user'@'10.%'`, but the recommended and most secure configuration is to restrict it to the specific IP: `10.128.0.4`.

---

### 3.5 Bind MySQL to the Internal IP Only

By default, MySQL may bind to `127.0.0.1` or `0.0.0.0`. To prevent public exposure, we explicitly bind it to the **internal VPC IP** of the DB VM: `10.128.0.3`.

On the **Database VM**:

```bash
hostname -I
# Expected to include: 10.128.0.3 ...
```

Edit the MySQL config:

```bash
sudo sed -i 's/^bind-address.*/bind-address = 10.128.0.3/' /etc/mysql/mysql.conf.d/mysqld.cnf
```

One should now see something like:

```bash
grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf
# bind-address = 10.128.0.3
# mysqlx-bind-address     = 127.0.0.1
```

Restart MySQL:

```bash
sudo systemctl restart mysql
```

This change ensures MySQL is **only** listening on the internal IP and is **not reachable** from the public internet, even if the VM has an external IP.

---

### 3.6 Import Schema and Data

Still on the **Database VM**:

```bash
sudo mysql MicroService3 < /home/zh2701/database4153/ms3_mysql/data.sql
```

If this completes without errors, the schema and initial data are imported.

---

## 4. Network & Firewall Configuration (GCP)

> This section describes the *intended* firewall behavior. Exact click-steps depend on the cloud console, but the goal is:

* Allow **only** `10.128.0.4 → 10.128.0.3:3306`.
* Deny / avoid `0.0.0.0/0 → 3306`.

### 4.1 Desired Firewall Rule

* **Direction**: Ingress
* **Target**: Database VM (e.g., via a network tag like `ms3-db`)
* **Source IP ranges**: `10.128.0.4/32`
* **Allowed protocols/ports**: `tcp:3306`

If there are any existing rules that allow `tcp:3306` from `0.0.0.0/0`, they should be disabled or removed to avoid public database exposure.

---

## 5. Service VM Setup (Application)

All commands in this section are run on the **Service VM** (`10.128.0.4`).

### 5.1 Create and Activate Python Virtual Environment

```bash
cd /home/zh2701/MicroService3

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install cryptography
```

---

## 6. Application Database Configuration (Internal IP)

The application must connect to the database using the **internal IP** of the DB VM: `10.128.0.3`, not the external IP.

### 6.1 Connection URL

```text
mysql+pymysql://ms3user:StrongPassword123!@10.128.0.3:3306/MicroService3
```

Example environment variable:

```env
DATABASE_URL="mysql+pymysql://ms3user:StrongPassword123!@10.128.0.3:3306/MicroService3"
```

One can export it directly in the shell for testing:

```bash
export DATABASE_URL="mysql+pymysql://ms3user:StrongPassword123!@10.128.0.3:3306/MicroService3"
```

---

## 7. Connectivity Test (Service VM → DB VM via Internal IP)

Before starting the application, verify that the Service VM can reach the database on the internal IP.

On the **Service VM (`10.128.0.4`)**:

```bash
telnet 10.128.0.3 3306
# or, if telnet is not installed:
nc -vz 10.128.0.3 3306
```

Expected:

* A successful TCP connection to port **3306**.
* If the connection fails, check:

  * MySQL is running on the DB VM.
  * `bind-address = 10.128.0.3` is set and MySQL restarted.
  * GCP firewall rules allow `10.128.0.4 → 10.128.0.3:3306`.

---

## 8. Run the Reviews Service

On the **Service VM**:

```bash
cd /home/zh2701/MicroService3
source .venv/bin/activate

# Ensure DATABASE_URL is set in the environment
export DATABASE_URL="mysql+pymysql://ms3user:StrongPassword123!@10.128.0.3:3306/MicroService3"

uvicorn main:app --host 0.0.0.0 --port 8000
```

### 8.1 Health Check (Local on Service VM)

```bash
curl http://127.0.0.1:8000/health
```

Expected: a JSON response indicating the service is healthy (e.g. `{"status":"ok"}`).

### 8.2 API Documentation (From Browser)

From the local machine/browser, access the Service VM’s **external IP**:

```text
http://34.61.43.139:8000/docs
```

One should see the FastAPI Swagger UI with the Reviews service endpoints.

---

## 9. Security Verification

After deployment, perform these security checks:

1. **Database not reachable from the public internet**

   From the local machine (or any host outside the VPC):

   ```bash
   telnet 34.170.75.146 3306
   # or
   nc -vz 34.170.75.146 3306
   ```

   Expected: **connection fails**.
   If it succeeds, one still have a firewall or bind-address misconfiguration exposing MySQL publicly.

2. **Database reachable from the Service VM only**

   Already tested in section 7 using:

   ```bash
   telnet 10.128.0.3 3306
   ```

3. **Service HTTP reachable publicly**

   From the browser:

   ```text
   http://34.61.43.139:8000/health
   http://34.61.43.139:8000/docs
   ```

   One should see correct responses and API docs.

---

## 10. Summary of Key Settings

* **Database VM (10.128.0.3)**

  * MySQL:

    * `bind-address = 10.128.0.3`
    * MySQL user: `'ms3user'@'10.128.0.4'`
    * DB name: `MicroService3`
  * MySQL is **not** exposed to the public internet.

* **Service VM (10.128.0.4)**

  * No local MySQL running.
  * App uses:

    ```text
    DATABASE_URL="mysql+pymysql://ms3user:StrongPassword123!@10.128.0.3:3306/MicroService3"
    ```
  * FastAPI/Uvicorn runs on `0.0.0.0:8000`.

* **Network / Security**

  * DB VM only accepts MySQL traffic from `10.128.0.4:3306`.
  * External users access only the HTTP API on `34.61.43.139:8000`.

