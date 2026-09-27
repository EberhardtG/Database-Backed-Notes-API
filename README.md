
# 📘 **Note API — README**

A FastAPI + SQLAlchemy project for creating, retrieving, filtering, and deleting notes.  
This API demonstrates proper database modeling, schema validation, ORM integration, and clean routing design.

---

## 🚀 Overview

The Note API supports:

- Creating notes  
- Listing notes with filters  
- Retrieving a single note  
- Deleting notes  
- SQLAlchemy 2.0 typed ORM models  
- Pydantic v2 schemas with `from_attributes=True`  
- SQLite database persistence  

Swagger UI is available at:

```
/docs
```

---

## 🧱 Project Structure

```
app/
│
├── main.py
│
├── database.py
│
├── models/
│   └── note.py
│
├── schemas/
│   ├── notecreate.py
│   └── noteresponse.py
│
└── routers/
    └── notes_route.py
```

---

## ⚙️ Database Setup (`database.py`)

The project uses:

- SQLite database  
- SQLAlchemy 2.0 typed ORM  
- SessionLocal dependency (`get_db`)  
- DeclarativeBase for model definitions  

The database connection is created once and shared across the application.

---

## 🧩 SQLAlchemy Model (`models/note.py`)

The `Note` model includes:

- `id`: integer primary key  
- `title`: string (max 200, required)  
- `content`: text (required)  
- `category`: string (max 50, optional)  
- `is_pinned`: boolean (default False)  
- `created_at`: auto‑generated timestamp  

Typed ORM fields (`Mapped`, `mapped_column`) ensure compatibility with Pydantic v2.

---

## 📦 Pydantic Schemas

### **NoteCreate**  
Used for POST `/notes`.

Fields:

- `title`: required, 1–200 chars  
- `content`: required, min_length=1  
- `category`: optional, max_length=50  
- `is_pinned`: optional, default False  

### **NoteResponse**  
Returned by all endpoints.

Includes:

- `id`  
- `title`  
- `content`  
- `category`  
- `is_pinned`  
- `created_at`  

Configured with:

```
model_config = ConfigDict(from_attributes=True)
```

This allows Pydantic to serialize SQLAlchemy ORM objects directly.

---

## 🔌 Endpoints

### **POST /notes**

Creates a new note.

- Validates using `NoteCreate`  
- Persists to database  
- Returns `NoteResponse`  
- Status: **201 Created**

---

### **GET /notes**

Lists notes with optional filters:

| Parameter | Type | Description |
|----------|------|-------------|
| category | str | Filter by category |
| is_pinned | bool | Filter pinned/unpinned notes |

Results are ordered by `created_at` descending.

---

### **GET /notes/{note_id}**

Retrieves a single note by ID.

- Returns 404 if not found  
- Returns `NoteResponse`

---

### **DELETE /notes/{note_id}**

Deletes a note.

- Returns 404 if not found  
- Returns **204 No Content**

---

## 🧪 Validation Behavior

The API returns clear `422 Unprocessable Entity` errors for:

- Invalid field types  
- Title or content too short  
- Category exceeding 50 characters  

And `404 Not Found` for:

- Nonexistent note IDs  
- Delete attempts on missing notes  

---

## 🏁 Running the API

Start the server:

```
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://localhost:8000/docs
```

---

## 🧠 WHY / DESIGN Commentary

This project demonstrates:

- Clean separation of database, schemas, and routing  
- SQLAlchemy 2.0 typed ORM for strong typing  
- Pydantic v2 integration using `from_attributes=True`  
- Predictable CRUD behavior  
- Clear validation rules  
- Proper use of FastAPI dependency injection (`Depends(get_db)`)  

The API is intentionally simple, predictable, and easy to extend.

---

## 📌 Next Steps

- Add update endpoint  
- Add pagination  
- Add search by title/content  
- Add user accounts + authentication
