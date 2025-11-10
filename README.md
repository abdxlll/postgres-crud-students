# PostgreSQL CRUD Application – Students Database

---

## Demonstration Video

📺 **Video Link:** [https://youtu.be/PAwqZ9YUo8E]  
The video demonstrates:

- Execution of each CRUD function (Add, List, Update, Delete)
- Verifying changes in pgAdmin

---

## Overview

This project is a simple **CRUD (Create, Read, Update, Delete)** application built with **Python** and **PostgreSQL**.  
It demonstrates how to connect a Python program to a PostgreSQL database and perform all four CRUD operations on a `students` table.

---

## Database Setup

1. **Create the database** in pgAdmin or using psql:

   ```sql
   CREATE DATABASE students_db;
   ```

2. **Run the schema script** to create the table:

   ```sql
   \i db/schema.sql
   ```

3. **(Optional)** Run the seed script to insert the initial data:
   ```sql
   \i db/seed.sql
   ```

This will create and populate the `students` table with:

```
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
```

---

## Setup Instructions

1. **Clone this repository:**

   ```bash
   git clone https://github.com/abdxlll/postgres-crud-students.git
   cd postgres-crud-students
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate       # on Windows
   # OR
   source venv/bin/activate      # on macOS/Linux
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Update the database connection** inside `app.py` if needed:
   ```python
   conn = psycopg2.connect(
       host="localhost",
       port=5432,
       dbname="students_db",
       user="postgres",
       password="your_password_here"
   )
   ```

---

## Running the Application

Each operation is performed via command-line arguments.

### 1️⃣ Retrieve all students

```bash
python app.py list
```

### 2️⃣ Add a new student

```bash
python app.py add --first Alice --last Lee --email alice.lee@example.com --date 2024-09-01
```

### 3️⃣ Update a student’s email

```bash
python app.py update-email --id 4 --email alice.new@example.com
```

### 4️⃣ Delete a student by ID

```bash
python app.py delete --id 4
```

---

## Example Output

```
ID   First Name   Last Name    Email                          Enrollment Date
------------------------------------------------------------------------------
1    John         Doe          john.doe@example.com            2023-09-01
2    Jane         Smith        jane.smith@example.com          2023-09-01
3    Jim          Beam         jim.beam@example.com            2023-09-02
```

---

## Repository Structure

```
postgres-crud-students/
├── app.py              # Main Python application
├── requirements.txt    # Dependencies (psycopg2-binary)
├── README.md           # Project setup + instructions
└── db/
    ├── schema.sql      # Table creation script
    └── seed.sql        # Initial data insert script
```

## Author

**Abdulrahman Odejayi (101306498)**  
Carleton University – COMP 3005 Course Assignment
