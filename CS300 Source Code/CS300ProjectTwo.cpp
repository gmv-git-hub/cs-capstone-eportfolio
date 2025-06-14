//============================================================================
// Title        : CS 300 Project Two
// Name         : CS300ProjectTwo.cpp
// Author       : Gianmarco Vendramin
// Version      : 1.0
// Date         : April 13, 2024
//============================================================================

#include <iostream>
#include <time.h>
#include <fstream>
#include <algorithm>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

//============================================================================
// Global definitions visible to all methods and classes
//============================================================================

// Structure to hold single course data
struct Course {
    string number;
    string name;
    vector<string> prerequisites;

    // Default constructor
    Course() {
        number = "";
        name = "";
        prerequisites.clear();
    }
};

// Forward declarations
void displayCourse(Course course);

// BST node definition to hold course data
struct Node {
    Course course;
    Node* left;
    Node* right;

    // Default constructor
    Node() {
        left = nullptr;
        right = nullptr;
    }

    // Initialize with a course
    Node(Course aCourse) : Node() {
        this->course = aCourse;
    }
};

//============================================================================
// Courses file loading function definition
//============================================================================
static void coursesFileLoad(string csvPath, vector<Course> &fileContentVector) {
    vector<string> fileLinesVector;
    ifstream inputFile; // Input file stream
    int dfIndex;
    string dataField;
    bool prerequisiteFound;
 
    // Attempting to open the file for read and exit the program if fail
    inputFile.open(csvPath);
    if (!inputFile.is_open()) {
        cout << "-------------------------------------------------------------------------------" << endl;
        cout << "ERROR: Could not open file \"" << csvPath << "\"!!" << endl;
        cout << "-------------------------------------------------------------------------------" << endl;
        return;
    }

    // Load data from external file
    string fileRow;

    // Read first item from stream
    getline(inputFile, fileRow);

    // Read items until file stream empty 
    while (!inputFile.fail()) {
        fileLinesVector.push_back(fileRow);
        getline(inputFile, fileRow); // Attempt to read next item
    }

    // Close the opened file
    inputFile.close();

    // Load course vector structure with data from rows in fileLinesVector 
    for (string row : fileLinesVector) {
        dfIndex = 0;
        stringstream str(row); // Creates a string stream to extract data from row
        Course course; // Prepare a course structure
        // Parse each comma separated field and store in current course structure
        while (getline(str, dataField, ',')) {
            if (!dataField.empty()) {
                switch (dfIndex) {
                case 0:
                    course.number = dataField;
                    break;
                case 1:
                    course.name = dataField;
                    break;
                default:
                    course.prerequisites.push_back(dataField);
                    break;
                }
                dfIndex++;
            }
        }

        // Return with error if row not complete
        if (dfIndex < 2) {
            cout << "-------------------------------------------------------------------------------" << endl;
            cout << "ERROR: Invalid file rows format!" << endl;
            cout << "-------------------------------------------------------------------------------" << endl;
            return;
        }

        // Store current course in the fileContentVector
        fileContentVector.push_back(course);
    }

    // Check if all the prerequisites are present
    for (Course course : fileContentVector) {
        for (string preRq : course.prerequisites) {
            prerequisiteFound = false;
            for (Course courseCheck : fileContentVector) {
                if (courseCheck.number == preRq) {
                    prerequisiteFound = true;
                    break;
                }
            }
            if (!prerequisiteFound) {
                cout << "-------------------------------------------------------------------------------" << endl;
                cout << "ERROR: Missing prerequisite!" << endl;
                cout << "-------------------------------------------------------------------------------" << endl;
                return;
            }
        }
    }

}


////============================================================================
//// Binary Search Tree class definition
////============================================================================

class BinarySearchTree {

private:
    Node* root;

    void addNode(Node* node, Course course);
    void inOrder(Node* node);
    void deleteTree(Node* node);

public:
    BinarySearchTree();
    virtual ~BinarySearchTree();
    void InOrder();
    void Insert(Course course);
    Course Search(string courseNumber);
};


///**
// * Default constructor
// */
BinarySearchTree::BinarySearchTree() {
    // Initialize housekeeping variables
    // root is equal to nullptr
    this->root = nullptr;
}


///**
// * Destructor
// */
BinarySearchTree::~BinarySearchTree() {
    // recourse from root deleting every node
    deleteTree(this->root);
}


///**
//* Tree deletion
//*/
void BinarySearchTree::deleteTree(Node* node) {
    // If the node is NULL, just return
    if (node == nullptr)
    {
        return;
    }

    // Remove the nodes from left subtree
    deleteTree(node->left);
    // Remove the nodes from right subtree
    deleteTree(node->right);

    // perform deletion on the node
    delete node;
}


///**
// * Traverse the tree in order
// */
void BinarySearchTree::InOrder() {
    // Call inOrder private fuction and pass root
    inOrder(root);
}


///**
// * Insert a course
// */
void BinarySearchTree::Insert(Course course) {
    // Implements inserting a course into the tree
    // if root equal to null ptr
    if (root == nullptr) {
        // root is equal to new node course
        root = new Node(course);
    }
    else {
        // add Node root and course
        addNode(root, course);
    }
}


///**
// * Search for a course
// */
Course BinarySearchTree::Search(string courseNumber) {
    // Implements searching the tree for a course
    // Set current node equal to root
    Node* current = root;

    // Keep looping downwards until bottom reached or matching course number found
    while (current != nullptr) {
        // If current node equals passed course number
        if (current->course.number.compare(courseNumber) == 0) {
            // Return current course
            return current->course;
        }

        // If passed course number is smaller than current node then traverse left
        if (courseNumber.compare(current->course.number) < 0) {
            current = current->left;
        }
        // Else it is larger so traverse right
        else {
            current = current->right;
        }
    }

    Course course;
    return course;
}


///**
// * Add a course to some node (recursive)
// *
// * @param node Current node in tree
// * @param course to be added
// */
void BinarySearchTree::addNode(Node* node, Course course) {
    // Implements inserting a course into the tree
    // If node is not NULL and larger then the course number, add to left subtree
    if (node != nullptr && node->course.number.compare(course.number) > 0) {
        // If no left node
        if (node->left == nullptr) {
            // The passed course creates a new left node
            node->left = new Node(course);
            return;
        }
        else {
            // Recourse down the left node
            addNode(node->left, course);
        }
    }
    // If node is not NULL and smaller then the course number, add to right subtree
    else if (node != nullptr && node->course.number.compare(course.number) < 0) {
        // If no right node
        if (node->right == nullptr) {
            // The passed course creates a new right node
            node->right = new Node(course);
            return;
        }
        else {
            // Recourse down the right node
            addNode(node->right, course);
        }
    }
}


// Traverse the BST in order
void BinarySearchTree::inOrder(Node* node) {
    // If node is not equal to null ptr
    if (node != nullptr)
    {
        // inOrder to the left
        inOrder(node->left);
        // Print course data
        cout << node->course.number << ", " << node->course.name << endl;
        // inOder to the right
        inOrder(node->right);
    }
}


////============================================================================
//// Static methods used for testing
////============================================================================

/**
 * Display the course information to the console
 *
 * @param course struct containing the course info
 */
void displayCourse(Course course) {
    unsigned int i;

    cout << course.number << ", " << course.name << endl;

    if (!course.prerequisites.empty()) {
        cout << "Prerequisites: ";
        for (i = 0; i < (course.prerequisites.size() - 1); i++) {
            cout << course.prerequisites.at(i) << ", ";
        }
        cout << course.prerequisites.at(i) << endl;
    }

    return;
}


/**
 * Load courses from vector structure to BST structure
 *
 * @param fileContentVector: the vector structure to load the data from
 * @param bst: the binary search tree
 */
void loadCourses(vector<Course> &fileContentVector, BinarySearchTree* bst) {
    
    for (Course course : fileContentVector) {
        bst->Insert(course);
    }
}



/*
 * main() method
 */
int main(int argc, char* argv[]) {

    // Manage program arguments and defaults
    string coursesFileName;
    
    // Define a timer variable
    clock_t ticks;

    // Structure to hold lines read during file reading
    vector<Course> fileContentVector;
    
    // Define a binary search tree to hold all courses
    BinarySearchTree* bst;
    bst = new BinarySearchTree();

    string courseNumber;
    Course course;
 
    cout << "Welcome to the course planner." << endl;

    int choice = 0;
    while (choice != 9) {
        cout << endl;
        cout << "  1. Load Data Structure." << endl;
        cout << "  2. Print Course List." << endl;
        cout << "  3. Print Course." << endl;
        cout << "  9. Exit" << endl;
        cout << endl;
        cout << "What would you like to do? ";
        cin >> choice;

        switch (choice) {

        case 1: // 1. Load Data Structure.
            fileContentVector.clear();
            delete bst;
            bst = new BinarySearchTree();

            cout << "File name: ";
            cin >> coursesFileName;
           
            // Initialize a timer variable before loading courses
            ticks = clock();

            coursesFileLoad(coursesFileName, fileContentVector);
            loadCourses(fileContentVector, bst);

            // Calculate elapsed time and display result
            ticks = clock() - ticks; // current clock ticks minus starting clock ticks
            cout << "time: " << ticks << " clock ticks" << endl;
            cout << "time: " << ticks * 1.0 / CLOCKS_PER_SEC << " seconds" << endl;
            break;

        case 2: // 2. Print Course List.
            bst->InOrder();
            break;

        case 3: // 3. Print Course.
            cout << "What course do you want to know about? ";
            cin >> courseNumber;
            std::transform(courseNumber.begin(), courseNumber.end(), courseNumber.begin(), ::toupper);
            
            ticks = clock();
            
            course = bst->Search(courseNumber);

            ticks = clock() - ticks; // current clock ticks minus starting clock ticks

            if (!course.number.empty()) {
                displayCourse(course);
            }
            else {
                cout << "Course number " << courseNumber << " not found." << endl;
            }

            cout << "time: " << ticks << " clock ticks" << endl;
            cout << "time: " << ticks * 1.0 / CLOCKS_PER_SEC << " seconds" << endl;
            break;

        case 9: // 9. Exit
            cout << "Thank you for using the course planner!" << endl;
            break;

        default:
            cout << choice << " is not a valid option." << endl;
        }
    }

    delete bst;
    return 0;
}

