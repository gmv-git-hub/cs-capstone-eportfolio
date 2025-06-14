# ============================================================================
# Title         CS499 Capstone
# Name          data_loader.py
# Author        Gianmarco Vendramin
# Version       1.2
# Date          June 7, 2025
# Description   This module contains the functions needed to load the data
#               from source and save it inside a vector
# ============================================================================


# Modules imports
import csv  # Import the helper module to work with CSV files
import json  # Import the helper module to work with JSON files
import os  # File management functions for code portability
from models.course import Course  # Import the Course class


# Function to load the courses into the list of courses from the supplied CSV file.
def load_courses_from_csv_file(csv_path: str) -> list[Course]:
    courses: list[Course] = []  # List that will contain the loaded courses

    # Using a try-except block to correctly manage the event of a file open error.
    try:
        # Open the CSV file
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)  # Create the CSV reader
            # Cycle through each row of the file
            for row in reader:
                # A row must have at minimum two fields, the course number and description
                # so if there is less than two fields the row is invalid.
                if len(row) < 2:
                    raise ValueError("Each row must contain at least course number and name.")
                # Create a new course object and loads the read data from the CSV row.
                course = Course(
                    number=row[0].strip(),
                    name=row[1].strip(),
                    # Load the prerequisites in the list by first removing leading and trailing spaces
                    # iterate each field starting from the third one and remove leading and trailing spaces
                    # from each prerequisite loaded. Do not include empty fields.
                    prerequisites=[field.strip() for field in row[2:] if field.strip()]
                )
                # Add the course object to the courses list.
                courses.append(course)
    except FileNotFoundError:
        # Manage the file reading error gracefully by giving a message to the user.
        print(f"ERROR: Could not open file '{csv_path}'!!")
        return []

    # Ensure that each prerequisite is also present as a course inside the list.
    # Prepare a set of course numbers.
    all_course_numbers = {crs.number for crs in courses}
    # Iterate each course of the list
    for course in courses:
        # Iterate each prerequisite of the current course
        for prereq in course.prerequisites:
            # If the prerequisite is not present inside the set of courses give error and return an empty vector.
            if prereq not in all_course_numbers:
                print("ERROR: Missing prerequisite:", prereq)
                return []

    return courses  # Return the loaded course list


# Function that takes a CSV courses file and convert it to JSON format.
def csv_to_json_courses(csv_path: str, json_path: str) -> None:
    courses = []  # Contains the list of the courses
    course_numbers = set()  # A set to keep all the course numbers.
    data_rows = []  # Intermediary storage for data validation

    if not os.path.exists(csv_path):
        print(f"File not found!: {csv_path}")
        return

    # Reading and parsing the CSV file with sanity checks
    try:  # Use try/except block to safely work with files
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            # Iterate through rows to extract the data
            for index, row in enumerate(reader, start=1):
                if len(row) < 2:
                    print(f"Malformed row found, skipping at {index}: {row}")
                    continue
                # Extract and save the course number, description and prerequisites
                course_number = row[0].strip()
                course_description = row[1].strip()
                prerequisites = [pr.strip() for pr in row[2:] if pr.strip()]
                # Check that the CSV row has data inside
                if not course_number or not course_description:
                    print(f"Course number or description missing at {index}: {row}")
                    continue
                # Save the course in the list of course numbers.
                course_numbers.add(course_number)
                data_rows.append((course_number, course_description, prerequisites))
    # Manage the exception of failing to open and reading the file.
    except Exception as e:
        print(f"CSV file read fail: {e}")
        return

    # Check the named prerequisites are also present as courses in the list and store the courses list.
    for course_number, course_description, prerequisites in data_rows:
        # Check if single course prerequisite is a valid course.
        invalid_prerq = [prerq for prerq in prerequisites if prerq not in course_numbers]
        if invalid_prerq:
            print(f"The course number '{course_number}' has non existent prerequisites: {invalid_prerq}")
        # Save the well-formed course inside the list of courses
        course = {  # JSON format scheme
            "code": course_number,
            "title": course_description,
            "prerequisites": prerequisites
        }
        courses.append(course)

    # Save the courses data structure in a JSON formatted file
    try:  # Use try/except block to safely work with files
        with open(json_path, mode='w', encoding='utf-8') as json_file:
            json.dump(courses, json_file, indent=4)
        print(f"JSON file data written to '{json_path}'")

    except Exception as e:
        print(f"An error occurred while writing the JSON file: {e}")


# Loads the course data from a JSON file and insert it with the provided functions as a parameter.
def load_courses_from_json_file(json_path: str, insert_function) -> None:
    # Reading and parsing the CSV file with sanity checks
    try:  # Use try/except block to safely work with files
        with open(json_path, mode='r', encoding='utf-8') as json_file:
            courses = json.load(json_file)  # Load all the courses using JSON module helper.

        # Create a list of all the courses codes available.
        available_courses = {course.get("code") for course in courses if course.get("code")}

        # For each course extract the data and store in the passed binary search tree object.
        for course in courses:
            course_code = course.get("code")
            course_description = course.get("title")
            course_prereq = course.get("prerequisites", [])

            # Course entry sanity check
            if not course_code or not course_description:
                print(f"Course number or description missing at: {course}")
                continue

            # Check if all prerequisites exist of the actual course
            invalid_prerq = [prerq for prerq in course_prereq if prerq not in available_courses]
            if invalid_prerq:
                print(f"The course number '{course_code}' has non existent prerequisites: {invalid_prerq}")

            course = Course(
                number=course_code,
                name=course_description,
                prerequisites=course_prereq
            )
            # Insert the course using the function provided as parameter
            insert_function(course)

    except Exception as e:
        print(f"An error occurred while reading the JSON file: {e}")

