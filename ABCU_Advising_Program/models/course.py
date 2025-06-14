# ============================================================================
# Title         CS499 Capstone
# Name          course.py
# Author        Gianmarco Vendramin
# Version       1.0
# Date          May 18, 2025
# Description   This module define the "Course" class
# ============================================================================


# Modules imports
from dataclasses import dataclass  # Import dataclass decorator
from dataclasses import field  # Import the field function


# Class to define the Course data structure
# The @dataclass decorator automatically adds boilerplate code like the constructor,
# string representation, and equality comparison.
@dataclass
class Course:
    number: str = ''  # Course number like: 'CS499'
    name: str = ''  # Course name like: 'Computer Science Capstone'
    # Define a list of strings and ensure that a new empty value is still list.
    prerequisites: list[str] = field(default_factory=list)
