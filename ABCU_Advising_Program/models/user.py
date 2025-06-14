# ============================================================================
# Title         CS499 Capstone
# Name          user.py
# Author        Gianmarco Vendramin
# Version       1.0
# Date          June 8, 2025
# Description   User object with attributes and methods to manage
#               user login check and course that can be taken.
# ============================================================================


# Modules imports
from dataclasses import dataclass, field  # Import dataclass decorator
from typing import Literal  # To restrict user role typing
import bcrypt  # To hash the user password for safe storage in the database
from models.course import Course  # Import the Course class


# User class definition with attributes and methods
@dataclass
class User:
    name: str
    surname: str
    email: str
    _password_hash: bytes = field(repr=False)  # We store only hashed password not plain text
    # The user can have only one of the two following roles: admin and student.
    role: Literal["student", "admin"] = "student"
    # List of a student completed course. If the user is admin, this attributed remains unused.
    # However, an admin could be a senior student that is taking the last courses and so the list becomes useful.
    completed_courses: list[str] = field(default_factory=list)

    @classmethod
    # Create a new user object by filling the user data
    def create(cls, name: str, surname: str, email: str, password: str, role: str = "student"):
        # Hash password using bcrypt
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return cls(name, surname, email, password_hash, role)

    # Check user password for access
    def check_password(self, password: str) -> bool:
        # Verify if the given password of the current user object is valid by using hashing algorithm.
        return bcrypt.checkpw(password.encode(), self._password_hash)

    # Check if the given course can be taken by the student
    def can_take_course(self, course: Course) -> bool:
        # Return true if all the passed course prerequisite are present in the user completed courses list.
        return all(prereq in self.completed_courses for prereq in course.prerequisites)