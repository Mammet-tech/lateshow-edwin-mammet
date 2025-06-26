# 📺 Late Show API

This is a RESTful API built with Flask for tracking guests and episodes on a late night show.

---

## 📁 Project Structure

```
.
├── __pycache__/               
├── instance/                  
│   └── app.db                 
├── migrations/               
│   ├── versions/              
│   ├── env.py               
│   ├── README                
│   └── script.py.mako       
├── venv/                     
├── app.py                    
├── models.py                  
├── README.md                  
└── requirements.txt           
```

---

## ⚙️ Technologies Used

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Postman (for API testing)

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://git@github.com:Mammet-tech/lateshow-edwin-mammet.git
cd lateshow-edwin-mammet
```

### 2. Create Virtual Environment

```bash
pipenv install
pipenv shell
```

### 3. Set Flask Environment Variables

```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```

### 4. Run Migrations

```bash
flask db init
flask db migrate -m "Create tables"
flask db upgrade
```

### 5. Seed the Database

You may run your own `seed.py` or import the provided CSV file to populate the database.

---

## 🧪 API Endpoints

### ✅ GET /episodes

Returns all episodes:

```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  ...
]
```

---

### ✅ GET /episodes/<id>

Returns a single episode with its appearances:

```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "guest_id": 1,
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

If not found:

```json
{
  "error": "Episode not found"
}
```

---

### ✅ GET /guests

Returns all guests.

---

### ✅ POST /appearances

Creates a new guest appearance.

**Request Body**:

```json
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}
```

**Valid Response**:

```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

**Validation Error**:

```json
{
  "errors": ["validation errors"]
}
```

---

## 📬 Testing in Postman

1. Open Postman
2. Import the provided Postman collection:
   `challenge-4-lateshow.postman_collection.json`
3. Test all the endpoints using real or seed data.

---

## 🧑 Author

**Edwin Mammet**

---

## 📄 License

This project is licensed under the MIT License.