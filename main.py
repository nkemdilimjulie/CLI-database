from dbase import create_family_db, get_data, create_first_name_contraint

def main():
    """Generates a family Database from CLI"""
    create_family_db()
    create_first_name_contraint()

    number_of_records_to_enter = int(
        input("Enter number of persons to enter their data ")
    )
    if number_of_records_to_enter == 0:
        print("No record to enter!")
        return None
    count = 1
    while count <= number_of_records_to_enter:
        get_data()

        count += 1


if __name__ == '__main__':
    main()
