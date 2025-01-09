# from datetime import date
from decimal import Decimal
import psycopg as pg
from psycopg import IntegrityError

CONN = pg.connect(dbname="dci", user="postgres", password="postgres")

def create_family_db():
    '''generates a family database from console'''
    query = """
    CREATE TABLE IF NOT EXISTS nuclear_family(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    email TEXT,
    gender TEXT,
    salary DECIMAL);
    """
    with CONN.cursor() as cursor:
        cursor.execute(query)
        CONN.commit()

def create_first_name_contraint():
    """updates nuclear_family table by adding constraints to the required field"""
    query = """
        DO $$
        BEGIN
            -- Check if the constraint exists
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'unique_nuclear_family'   -- constraint name (see below: ADD CONSTRAINT statement) "conname" - constraint name
                AND conrelid = 'nuclear_family'::regclass -- Table name "conrelid" - constraint related id 
            ) THEN
                -- Add the unique constraint
                ALTER TABLE nuclear_family
                ADD CONSTRAINT unique_nuclear_family UNIQUE (first_name);
            END IF;
        END $$;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query)
        CONN.commit()

def insert_data_into_table(data: tuple[str, str, str, str, str, str]):
    """inserts user data into an existing table from console or command line prompt"""
    query = """
        INSERT INTO nuclear_family
        VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (first_name) DO NOTHING
        RETURNING *;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query, data)
        inserted_family = cursor.fetchone()
        CONN.commit()
        return inserted_family

def get_data():
    '''interactive data entry into an existing table'''
    data = []
    for field, state in [
        ("first_name", "r"),
        ("last_name", "o"),
        ("date_of_birth", "r"),
        ("email", "r"),
        ("gender", "o"),
        ("salary", "o")
        ]:
        input_data = input(
            f"{field} {'(Default None)' if state == 'o' else ''}{'(year-month-day)' if field == 'date_of_birth' else '' }"
        )
        if len(input_data) == 0 and state =="o":
            input_data = None
        data.append(input_data) 
    print(f"input data entered by user {data}")
    result = insert_data_into_table(data)
    print(result)
