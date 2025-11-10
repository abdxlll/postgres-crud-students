import sys
import psycopg2
from psycopg2.extras import RealDictCursor
import argparse


def get_conn():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="students_db",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        print(f"ERROR: Could not connect to PostgreSQL: {e}")
        sys.exit(1)

# ---- CRUD functions ----

def getAllStudents():
    #Retrieve and print all students.
    with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT student_id, first_name, last_name, email, enrollment_date
            FROM students
            ORDER BY student_id;
        """)
        rows = cur.fetchall()
        if not rows:
            print("No students found.")
            return
        print(f"{'ID':<4} {'First Name':<12} {'Last Name':<12} {'Email':<30} {'Enrollment Date'}")
        print("-" * 80)
        for r in rows:
            date_str = r['enrollment_date'].strftime("%Y-%m-%d") if r['enrollment_date'] else ""
            print(f"{r['student_id']:<4} {r['first_name']:<12} {r['last_name']:<12} {r['email']:<30} {date_str}")

def addStudent(first_name, last_name, email, enrollment_date):
    #Insert a new student. enrollment_date can be YYYY-MM-DD or empty.
    with get_conn() as conn, conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
            """, (first_name, last_name, email, enrollment_date or None))
            new_id = cur.fetchone()[0]
            conn.commit()
            print(f"Inserted student_id={new_id}")
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            print("ERROR: Email already exists (unique constraint).")
        except Exception as e:
            conn.rollback()
            print(f"ERROR: Failed to insert: {e}")

def updateStudentEmail(student_id, new_email):
    #Update a student's email by id.
    with get_conn() as conn, conn.cursor() as cur:
        try:
            cur.execute("UPDATE students SET email=%s WHERE student_id=%s;", (new_email, student_id))
            if cur.rowcount == 0:
                print(f"No student found with ID {student_id}.")
            else:
                conn.commit()
                print(f"Updated student_id={student_id} email to {new_email}")
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            print("ERROR: Email already exists (unique constraint).")
        except Exception as e:
            conn.rollback()
            print(f"ERROR: Failed to update: {e}")

def deleteStudent(student_id):
    #Delete a student by id.
    with get_conn() as conn, conn.cursor() as cur:
        try:
            cur.execute("DELETE FROM students WHERE student_id=%s;", (student_id,))
            if cur.rowcount == 0:
                print(f"No student found with ID {student_id}.")
            else:
                conn.commit()
                print(f"Deleted student_id={student_id}")
        except Exception as e:
            conn.rollback()
            print(f"ERROR: Failed to delete: {e}")


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL CRUD demo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # list
    sub.add_parser("list", help="List all students")

    # add
    p_add = sub.add_parser("add", help="Add a new student")
    p_add.add_argument("--first", required=True)
    p_add.add_argument("--last", required=True)
    p_add.add_argument("--email", required=True)
    p_add.add_argument("--date", required=False, help="YYYY-MM-DD")

    # update-email
    p_upd = sub.add_parser("update-email", help="Update a student's email")
    p_upd.add_argument("--id", type=int, required=True)
    p_upd.add_argument("--email", required=True)

    # delete
    p_del = sub.add_parser("delete", help="Delete a student by id")
    p_del.add_argument("--id", type=int, required=True)

    args = parser.parse_args()

    if args.cmd == "list":
        getAllStudents()
    elif args.cmd == "add":
        addStudent(args.first, args.last, args.email, args.date)
    elif args.cmd == "update-email":
        updateStudentEmail(args.id, args.email)
    elif args.cmd == "delete":
        deleteStudent(args.id)

if __name__ == "__main__":
    main()