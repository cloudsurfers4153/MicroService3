# MS3 – Reviews (FastAPI + MySQL)

Simple Reviews microservice for movies.  
Framework: **FastAPI (Python)**, Database: **MySQL** (on VM or local).

This service exposes CRUD endpoints for the `reviews` table:

- `GET /reviews`
- `POST /reviews`
- `GET /reviews/{id}`
- `PUT /reviews/{id}`
- `DELETE /reviews/{id}`

OpenAPI docs (Swagger UI) are available at `/docs`.

---

## 1. Requirements

- macOS (tested conceptually on MacBook)
- Python **3.10+**
- MySQL server (local or on VM)
- Git (optional but convenient)

---

## 2. Database setup (MySQL)

1. Start your local MySQL server.

2. Create database (if it does not exist yet):

   ```bash
   mysql -uroot -p -e "CREATE DATABASE IF NOT EXISTS ms3_reviews CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   ```

   > If root has no password, just press **Enter** when prompted.

3. Import your existing SQL data file (schema + sample data):

   ```bash
   mysql -uroot -p ms3_reviews < /Users/huangziheng/PycharmProjects/MicroService3/data.sql
   ```

   - Adjust the path to `data.sql` if your file is in a different location.
   - The service expects a `reviews` table matching the schema you provided.

---

## 3. Project setup (Python)

 Install dependencies:

   ```bash
conda create -n MicroService3 python=3.11 -y
conda activate MicroService3
cd /home/zh2701/MicroService3/
 
pip install -r requirements.txt


   ```

---

## 4. Configuration


By default, the app connects to:

``` 
mysql+pymysql://root@localhost:3306/ms3_reviews
```

You can override this by setting `DATABASE_URL`:

```bash
export DATABASE_URL="mysql+pymysql://root@your-mysql-host:3306/ms3_reviews"
```

Examples:

- Local MySQL without password (default):  
  `mysql+pymysql://root@localhost:3306/ms3_reviews`
- MySQL with password:  
  `mysql+pymysql://root:yourpassword@localhost:3306/ms3_reviews`

---

## 5. Run the service

From inside the project directory (with venv activated):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- Swagger UI: <http://127.0.0.1:8000/docs>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

---

## 6. API overview and examples

### 6.1 Health

**Request**

```bash
curl http://127.0.0.1:8000/health
```

**Response**

```json
{"status": "ok"}
```

---

### 6.2 GET /reviews (list with filters and pagination)

Example: list first page of reviews for **movie_id = 1**:

```bash
curl "http://127.0.0.1:8000/reviews?movie_id=1&page=1&page_size=2"
```

---

### 6.3 POST /reviews (create)

Example: create a review for **movie_id 1, user_id 1**:

```bash
curl -X POST "http://127.0.0.1:8000/reviews"           -H "Content-Type: application/json"           -d '{
    "movie_id": 1,
    "user_id": 1,
    "rating": 5,
    "comment": "I was not prepared for how hard \"Tötet nicht mehr\" would hit me; watching the father break after his son is killed during a peaceful reading made the anti death penalty message feel painfully real."
  }'
```

---

### 6.4 GET /reviews/{id} (with optional ETag)

Example: get review `id = 1`:

```bash
curl "http://127.0.0.1:8000/reviews/1"
```

Example: use `If-None-Match` ETag:

1. First request (note the `ETag` header in the response).
2. Second request:

   ```bash
   curl "http://127.0.0.1:8000/reviews/1"              -H 'If-None-Match: W/"0123456789abcdef"'
   ```

If the ETag matches, you get `304 Not Modified`.

---

### 6.5 PUT /reviews/{id} (update rating/comment)

Example: update rating and comment of review `id = 1`:

```bash
curl -X PUT "http://127.0.0.1:8000/reviews/1"           -H "Content-Type: application/json"           -d '{
    "rating": 4,
    "comment": "\"Tötet nicht mehr\" stays with me even more after a second viewing."
  }'
```

---

### 6.6 DELETE /reviews/{id}

Example: delete review `id = 1`:

```bash
curl -X DELETE "http://127.0.0.1:8000/reviews/1"
```

Response status: `204 No Content`.

---

## 7. Notes

- Models are in `models.py`.
- Pydantic is using **v2 style** (`ConfigDict`, `from_attributes=True`), no `orm_mode`.
- Project structure is intentionally simple: a few Python files, no nested packages, no `v1` path, no empty `__init__.py`.
- You can deploy this on a **Compute Engine VM** and point `DATABASE_URL` to your VM MySQL instance.
