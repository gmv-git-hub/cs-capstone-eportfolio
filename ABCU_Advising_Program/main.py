# ============================================================================
# Title         CS499 Capstone
# Name          main.py
# Author        Gianmarco Vendramin
# Version       1.2
# Date          June 7, 2025
# Description   This is the project main file that contains the main function
#               executed upon launching the file.
# ============================================================================


# Modules imports
import time  # The time module is loaded to check the execution time
from services.mdb_api import (insert_course,
                              find_course_by_number,
                              list_courses_sorted,
                              clear_courses,
                              insert_user,
                              find_user_by_email,
                              add_completed_course,
                              get_users_list)  # Import the MongoDB access functions
from utils.data_loader import (load_courses_from_csv_file,
                               csv_to_json_courses,
                               load_courses_from_json_file)  # Load the data loader function utility
from models.user import User  # Import the User class definition

# Function to print the course given as a parameter
def display_course(course):
    print("------------------------------------------------------")
    print(f"{course.number}, {course.name}")
    # Check if the course has prerequisites and print them
    if course.prerequisites:
        print("Prerequisites: " + ", ".join(course.prerequisites))
    print("------------------------------------------------------")


# Function to display the menu for the user
def display_menu_student():
    print("\n  1. Print Course List.")
    print("  2. Print Course.")
    print("  3. Add completed course")
    print("  4. Print Completed Courses.")
    print("  5. Check if can take a course.")
    print("  20. Exit\n")


# Function to display the menu for the admin
def display_menu_admin():
    print("\n  1. Print Course List.")
    print("  2. Print Course.")
    print("  3. Add completed course")
    print("  4. Print Completed Courses.")
    print("  5. Check if can take a course.")
    print("  6. Create a new user.")
    print("  7. List users.")
    print("  8. Load Data from CSV file.")
    print("  9. Load Data from JSON file.")
    print("  10. Convert CSV data file to JSON data file.")
    print("  11. Empty the data structure (MongoDB Courses Collection).")
    print("  20. Exit\n")


# Program starting point
def main():
    courses: list = []  # Define an empty list to hold the data loaded

    # User login stage
    print("Welcome to the course planner. Please login...")
    # Request username/email and password to access the system.
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    # Find the user in the database collection and load the data.
    logged_user = find_user_by_email(email)
    if logged_user is None:  # If user not found, give a message and exit the application.
        print("User not found!")
        return
    if not logged_user.check_password(password):  # If password wrong, give a message and exit the application.
        print("Wrong password!")
        return

    # Set the admin flag if the user is an admin.
    is_admin = False
    if logged_user.role == "admin":
        is_admin = True

    # Main loop that prints the menu for the user and exit only when option 9 is chosen.
    while True:
        if is_admin:
            display_menu_admin()
        else:
            display_menu_student()

        # Collect the user choice
        choice = input("What would you like to do? ")

        # Based on the user chosen menu item, perform the required action.
        match choice:

            # 1. Print Course List.
            case '1':
                # Traverse the database courses collection and print the courses in ascending order.
                print("------------------------------------------------------")
                for course in list_courses_sorted():
                    print(f"{course.number}, {course.name}")
                print("------------------------------------------------------")

            # 2. Print Course.
            case '2':
                # Ask a course number to be printed stripping the white spaces and
                # transforming the string to upper case to avoid missing a match if
                # the user uses lower case characters.
                course_number = input("What course do you want to know about? ").strip().upper()
                # Save the current time to be used to measure the search time.
                start = time.time()
                course = find_course_by_number(course_number)
                elapsed = time.time() - start
                # If the course is found, print it with description and prerequisites
                if course:
                    display_course(course)
                else:
                    print(f"Course number {course_number} not found.")
                print(f"time: {elapsed:.6f} seconds")  # print the search time

            # 3. Add completed course
            case '3':
                # Add a completed course to the completed course list of the current user.
                # Ask a course number stripping the white spaces and
                # transforming the string to upper case to avoid missing a match if
                # the user uses lower case characters.
                course_number = input("What course do you want to add? ").strip().upper()
                course = find_course_by_number(course_number)
                # If the course is found, add it to the student courses list.
                if course:
                    add_completed_course(logged_user.email, course_number)  # Add the course to the user in the database
                    logged_user.completed_courses.append(course_number)  # Align current logged user
                    print(f"Course number {course_number} added.")
                else:
                    print(f"Course number {course_number} not found.")

            # 4. Print Completed Courses.
            case '4':
                # Print the list of user completed courses.
                if not logged_user.completed_courses:  # Check if there are completed courses.
                    print("No completed courses yet!")
                # Traverse the completed courses list and print each single course.
                for course_no in logged_user.completed_courses:
                    course = find_course_by_number(course_no)
                    print(f"{course.number}: {course.name}")

            # 5. Check if can take a course.
            case '5':
                # Check if the current student can take a specific course.
                course_number = input("What course do you want to check? ").strip().upper()
                course = find_course_by_number(course_number)
                # If the course exist, perform the checking.
                if course:
                    # Extract the missing prerequisites list
                    missing_prereqs = [prereq for prereq in course.prerequisites
                                       if prereq not in logged_user.completed_courses]
                    # Check if there are missing prerequisites and give user feedback
                    if not missing_prereqs:
                        print(f"You can take {course_number}.")
                    else:
                        print(f"You cannot take {course_number}.")
                else:
                    print(f"Course number {course_number} not found.")

            # 6. Create a new user.
            case '6':
                if is_admin:
                    # Create a new admin or student user.
                    # For safety reasons the first admin user must be manually created in the database.
                    name = input("First Name: ").strip()
                    surname = input("Last Name: ").strip()
                    email = input("Email: ").strip()
                    password = input("Password: ").strip()
                    role = input("Role [student or admin]: ").strip().lower()
                    # Check if given role is correct
                    if role not in ("student", "admin"):
                        print("Role not valid, saving as student!")
                        role = "student"
                    # Create the user object
                    user = User.create(name, surname, email, password, role)
                    # Check if the user already exist.
                    if find_user_by_email(email) is None:
                        # Insert new user in the database
                        insert_user(user)
                        print("User correctly added!")
                    else:
                        print("User already exist!")
                else:
                    print("You need admin role to use this function!!")

            # 7. List users.
            case '7':
                if is_admin:
                    # List the user present int the database collection.
                    users = get_users_list()
                    for user in users:
                        name = user.get("name", "")
                        surname = user.get("surname", "")
                        email = user.get("email", "")
                        role = user.get("role", "student")
                        print(f"Name: {name} {surname}, Email: {email}, Role: {role}")
                else:
                    print("You need admin role to use this function!!")

            # 7. Load Data from CSV file.
            case '8':
                if is_admin:
                    # Ask the user the file name and filter out the leading and trailing spaces.
                    file_name = input("File name: ").strip()
                    # Save the current time to be used for loading time measurement.
                    start = time.time()
                    # Call the data loading function saving the output in the courses list.
                    courses = load_courses_from_csv_file(file_name)
                    # Cycle through each courses rows and insert each course inside the
                    # MongoDB database courses collection.
                    for course in courses:
                        insert_course(course)
                    elapsed = time.time() - start
                    print(f"time: {elapsed:.6f} seconds")  # print the loading time
                else:
                    print("You need admin role to use this function!!")

            # 9. Load Data from JSON file.
            case '9':
                if is_admin:
                    # Ask the user the file name and filter out the leading and trailing spaces.
                    file_name = input("File name: ").strip()
                    # Save the current time to be used for loading time measurement.
                    start = time.time()
                    # Call the data loading function saving the data directly into the database courses collection.
                    load_courses_from_json_file(file_name, insert_course)
                    elapsed = time.time() - start
                    print(f"time: {elapsed:.6f} seconds")  # print the loading time
                else:
                    print("You need admin role to use this function!!")

            # 10. Convert CSV data file to JSON data file.
            case '10':
                if is_admin:
                    # Ask the user the CSV and JSON file names and filter out the leading and trailing spaces.
                    csv_file_name = input("CSV File name: ").strip()
                    json_file_name = input("JSON File name: ").strip()
                    # Save the current time to be used for loading time measurement.
                    start = time.time()
                    # Call the file conversion function.
                    csv_to_json_courses(csv_file_name, json_file_name)
                    elapsed = time.time() - start
                    print(f"time: {elapsed:.6f} seconds")  # print the loading time
                else:
                    print("You need admin role to use this function!!")

            # 11. Empty the data structure.
            case '11':
                if is_admin:
                    clear_courses()
                    print("Data deleted")
                else:
                    print("You need admin role to use this function!!")

            # 20. Exit
            case '20':
                print("Thank you for using the course planner!")
                break

            # Default case
            case _:
                print(f"{choice} is not a valid option.")


if __name__ == "__main__":
    main()
