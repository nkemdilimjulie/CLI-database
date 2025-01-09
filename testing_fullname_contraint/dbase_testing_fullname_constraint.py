# from datetime import date
from decimal import Decimal
import psycopg as pg
from psycopg import IntegrityError

CONN = pg.connect(dbname="dci", user="postgres", password="postgres")


def create_family_db():
    """creates a family database """
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
    """updates nuclear_family table by adding constraint to the first_name column """
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


def insert_data_into_table_conflict_fullname(data: tuple[str, str, str, str, str, str, str]):
    """inserts into an existing table user data entered from console or command line prompt"""
    query = """
        INSERT INTO nuclear_family
        VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (fullname) DO NOTHING
        RETURNING *;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query, data)
        inserted_family = cursor.fetchone()
        CONN.commit()
        return inserted_family


def insert_data_into_table_conflict_fullname(data: tuple[str, str, str, str, str, str, str]):
    """inserts into an existing table user data entered from console or command line prompt"""
    query = """
        INSERT INTO nuclear_family
        VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (fullname) DO NOTHING
        RETURNING *;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query, data)
        inserted_family = cursor.fetchone()
        CONN.commit()
        return inserted_family

def get_data_fullname():
    """interactive data entry into an existing table"""
    data = []
    for field, state in [
        ("first_name", "r"),
        ("last_name", "r"),
        ("date_of_birth", "r"),
        ("email", "r"),
        ("gender", "o"),
        ("salary", "o"),
    ]:
        input_data = input(
            f"{field} {'(Default None)' if state == 'o' else ''}{'(year-month-day)' if field == 'date_of_birth' else '' }"
        )
        if len(input_data) == 0 and state == "o":
            input_data = None
        data.append(input_data)
        print(f"input data entered by user {data}")
    return data


def get_data_first_name():
    """interactive data entry into an existing table"""
    data = []
    for field, state in [
        ("first_name", "r"),
        ("last_name", "o"),
        ("date_of_birth", "r"),
        ("email", "r"),
        ("gender", "o"),
        ("salary", "o"),
    ]:
        input_data = input(
            f"{field} {'(Default None)' if state == 'o' else ''}{'(year-month-day)' if field == 'date_of_birth' else '' }"
        )
        if len(input_data) == 0 and state == "o":
            input_data = None
        data.append(input_data)
    print(f"input data entered by user {data}")
    result = insert_data_into_table_conflict_first_name(data)
    print(result)


def append_input_data_with_fullname():
    """creates and appends fullname """
    data = get_data_fullname()
    fullname = (
        data[0] + " " + data[1]
    )  # OR, fullname = data[0][0:]+' '+data[1][0:] OR, fullname = f"{data[0]} {data[1]}"
    print(f"fullname {fullname}")
    data.append(fullname)
    print(f"fullname added to input data entered by user {data}")
    # Ensure the data matches the table columns
    if len(data) != 7:
        print("Error: Data does not match the expected format.")
        return None
    result = insert_data_into_table_conflict_fullname(tuple(data))
    print(f"Inserted record: {result}")


def insert_data_into_table_conflict_first_name(
    data: tuple[str, str, str, str, str, str, str]
):
    """inserts into an existing table user data entered from console or command line prompt"""
    query = """
        INSERT INTO nuclear_family
        VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (first_name) DO NOTHING
        RETURNING *;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query, data)
        inserted_family = cursor.fetchone()
        CONN.commit()
        return inserted_family


def create_field_fullname():
    """Adds a new column - fullname - to the existing database"""

    query = """
        ALTER TABLE IF EXISTS nuclear_family
        ADD COLUMN IF NOT EXISTS fullname VARCHAR(100);
    """
    with CONN.cursor() as cursor:
        cursor.execute(query)
        CONN.commit()

def create_fullname_constraint():
    """updates nuclear_family table by adding constraints to the required fields"""

    query = """
        DO $$
        BEGIN
            -- Check if the constraint exists
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'unique_fullname_nuclear_family'   -- constraint name (see below: ADD CONSTRAINT statement) "conname" - constraint name
                AND conrelid = 'nuclear_family'::regclass -- Table name "conrelid" - constraint related id 
            ) THEN
                -- Add the unique constraint
                ALTER TABLE nuclear_family
                ADD CONSTRAINT unique_fullname_nuclear_family UNIQUE (fullname);
            END IF;
        END $$;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query)
        CONN.commit()

    # def set_fullname_on_db():
    #     """generates fullname for all records in an existing database"""
        query = """
            UPDATE nuclear_family
            SET fullname = first_name||' '||last_name
            WHERE first_name IS NOT NULL AND last_name IS NOT NULL
            RETURNING *;
        """
    #     with CONN.cursor() as cursor:
    #         cursor.execute(query)
    #         fullname = cursor.fetchone()
    #         CONN.commit()
    # #         return fullname
    # """If any of first_name or last_name can be NULL, you may want to handle that case explicitly using COALESCE to avoid NULL results:
    # SET fullname = COALESCE(first_name, '') || ' ' || COALESCE(last_name, '');"""

# def extract_fullname():
#     row_of_fullname = set_fullname_on_db()
#     fullname = row_of_fullname[0][0]
#     return fullname


def drop_first_name_constraint():
    """Drops a constraint from the nuclear_family table if it exists"""

    query = """
        ALTER TABLE nuclear_family
        DROP CONSTRAINT IF EXISTS unique_nuclear_family;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query)
        CONN.commit()

def re_inserts_empty_last_name():
    """ re_fills empty last_name with values"""
    query = """
        UPDATE nuclear_family
        SET last_name = 'Chime'
        WHERE last_name IS NULL;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query)
        CONN.commit()

def number_of_records_to_enter_with_fullname():
    """ number of records to enter"""

    number_of_records_to_enter = int(
        input("Enter number of persons to enter their data ")
    )
    if number_of_records_to_enter == 0:
        print("No record to enter!")
        return None
    count = 1
    while count <= number_of_records_to_enter:
        append_input_data_with_fullname()
        count += 1
    return f"Entered {number_of_records_to_enter} persons"


def number_of_records_to_enter_with_first_name():
    """number of records to enter"""

    number_of_records_to_enter = int(
        input("Enter number of persons to enter their data ")
    )
    if number_of_records_to_enter == 0:
        print("No record to enter!")
        return None
    count = 1
    while count <= number_of_records_to_enter:
        get_data_first_name()
        count += 1
    return f"Entered {number_of_records_to_enter} persons"


def drop_fullname_constraint():
    """Drops a constraint from the nuclear_family table if it exists"""

    query = """
        ALTER TABLE nuclear_family
        DROP CONSTRAINT IF EXISTS unique_fullname_nuclear_family;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query)
        CONN.commit()
