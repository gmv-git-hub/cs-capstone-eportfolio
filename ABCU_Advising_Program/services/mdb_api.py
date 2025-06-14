# ============================================================================
# Title         CS499 Capstone
# Name          mdb_api.py
# Author        Gianmarco Vendramin
# Version       1.0
# Date          June 7, 2025
# Description   Database integration API to move the data from the original
#               binary search tree structure to a MongoDB database.
# ============================================================================


# Modules imports
from pymongo import MongoClient, ASCENDING  # Import the Phyton MongoDB client
from models.course import Course  # Import the Course class
from dotenv import load_dotenv  # Import the environment variable loading tool
import os  # OS tools
from models.user import User  # Import the User class definition


# MongoDB object to connect to the local database
load_dotenv()  # Load environment variables
# Create database connection using the MONGODB_URI environment variable for safe connection with user and password
mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client_mdb = MongoClient(mongo_uri)

# Create or prepare the access to a database named "abcu_advising"
db = client_mdb["abcu_advising"]

# Create or prepare the access to the "courses" and "users" collection in the database.
courses_coll = db["courses"]
users_coll = db["users"]


# Function to insert a course inside the courses collection.
def insert_course(course: Course):
    # Insert the course by first converting it from a dataclass to a dictionary.
    courses_coll.insert_one(course.__dict__)


# Function to find and return a course finding it by its number.
def find_course_by_number(course_number: str) -> Course | None:
    # Query the database to find the specified course number.
    course_data = courses_coll.find_one({"number": course_number})

    # If course not found, return None
    if course_data is None:
        return None

    course_data.pop('_id', None)  # Remove the _id field that it is not necessary for the application.
    return Course(**course_data) # Convert course_data to a course object using unpacking (**).


# Function to return a sorted list of all the course present in the courses' collection.
def list_courses_sorted() -> list[Course]:
    # Temporary list to load the courses
    course_list = []

    # Scan the database courses collection in ascending order to populate the course list.
    for course_data in courses_coll.find().sort("number", ASCENDING):
        course_data.pop('_id', None)  # Remove the _id field that it is not necessary for the application.
        # Append the course to the list converting it back to a course object using unpacking (**)
        course_list.append(Course(**course_data))

    return course_list # Return the list


# This function empties the courses collection by deleting all the elements inside.
def clear_courses():
    # Using an empty filter, delete all the documents in the collection.
    courses_coll.delete_many({})


# Insert a new user inside the "users" database collection.
def insert_user(user: User):
    # Retrieve the user data and convert to dictionary before storing to the database collection.
    user_data = user.__dict__.copy()
    # The password hash is stored as a string, so it has to be converted to UTF-8.
    user_data["_password_hash"] = user_data["_password_hash"].decode('utf-8')
    users_coll.insert_one(user_data)


# Retrieve user data using the login string (email). It is used to check also if a user is already present.
def find_user_by_email(email: str) -> User | None:
    user_data = users_coll.find_one({"email": email})  # Query the database to find the user
    if not user_data:  # If user not found return None.
        return None
    user_data["_password_hash"] = user_data["_password_hash"].encode('utf-8')  # Revert the hashed password to bytes
    user_data.pop('_id', None)  # Remove the _id field before storing the data in the user object.
    return User(**user_data)


# Adds a completed course to a specific user identified by its email.
def add_completed_course(email: str, course_number: str) -> bool:
    # Retrieve current user data
    user_data = users_coll.find_one({"email": email})

    # Calling this function is normally done by the logged user,
    # however we check the user existence in the case this module is used differently.
    if not user_data:
        print("User not found.")
        return False

    # Be sure that the course we are adding dows not already exist
    completed = user_data.get("completed_courses", [])  # Load the completed courses list.
    if course_number in completed:
        return True  # We return "gracefully" in the case the course is already present.

    # Add course to the list and update the record.
    completed.append(course_number)  # Add the new course to the completed list.
    # Launch the database query to write the updated courses list.
    result = users_coll.update_one(
        {"email": email},
        {"$set": {"completed_courses": completed}}
    )

    return result.modified_count > 0  # When modified count is greater than zero, return True.


# Function to retrieve the list of all the user.
def get_users_list() -> list[dict]:
    # Query the database with an empty parameter to get all the users.
    return list(users_coll.find({}, {"_id": 0}))