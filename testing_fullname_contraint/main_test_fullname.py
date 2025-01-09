from dbase_testing_fullname_constraint import (
    create_family_db,
    create_first_name_contraint,
    drop_first_name_constraint,
    create_fullname_constraint,
    create_field_fullname,
    number_of_records_to_enter_with_fullname,
    number_of_records_to_enter_with_first_name,
    drop_fullname_constraint,
)

def main():
    create_family_db()

    use_fullname_constraint = input("Do you want to use unique fullname?(yes or no): ")
    if use_fullname_constraint in ["yes", "y", "Y", "YES"]:
        print(f"You are using unique fullname .... \n")
        create_field_fullname()
        drop_first_name_constraint()
        create_fullname_constraint()
        number_of_records_to_enter_with_fullname()
        #re_inserts_empty_last_name()

    if use_fullname_constraint in ["no", "n", "N", "NO"]:
        print("You are using unique first_name .... \n")
        drop_fullname_constraint()
        create_first_name_contraint()
        number_of_records_to_enter_with_first_name()


if __name__ == "__main__":
    main()
