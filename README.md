# ClassParty
#### Video Demo:  <[URL HERE](https://www.youtube.com/watch?v=5dXbvohzlT0)>
#### Description:


- **Project Overview**:
  A simple class participation management platform for teaching assistants or lecturers to track their students participations in class.

- **Motivation**:
  During my undergraduate studies, I worked as a teaching assistant for a few different classes. Usually, to keep track of the students' participation points, I utilise the excel file with the student list. If I were to add notes or comments during class, I would have to add columns or rows along the way, which makes for a cumbersome procedure. This can be done with a less user-friendly interface that consists solely of Excel cells. The problem of many files in folders would be exacerbated if a person took multiple classes. Furthermore, because inputs are not timestamped, it is challenging to keep track of the complete history. I was looking for a better approach to gather this data so that it may be utilised for analysis in the future. This could involve tracking when students are most engaged in class, perhaps making word clouds to summarise the most intersting topics that were discussed, etc.

## Features

- **Key Features**:
    - Directly upload csv file of student list (name, id, group) onto the platform
    - Manage multiple classes on the platform
    - Intutive user-interface - students are displayed in their groups
    - Add participation scores and comments
    - Export class participation activity for further analysis and grading

## Installation

- **Requirements**:
  - Python
  - Flask
  - Flask-SQLAlchemy
  - pytz
  - Werkzeug

- **Installation**:
  - pip install -r requirements.txt

## Usage

- **Getting Started**:
  To begin, sign up for an account, then login to the page. From the homepage, you can head to the classes page to add your first class. To do so, simply click on the "Add New Class" button, and a pop-up form will appear. Input your class name and upload your class list with students details such as their name, id and groupings. Ensure that the csv. uploaded contains these exact headers: name, id, group. Once the class is created, you can click on "Start Class", and be redirected to the homepage. Students will be displayed in their groups in three columns. Beside their names, there will be a "+" icon. Simply tap on the icon to add their participation. Upon tapping, a pop-up form will appear, where you can add in their score (1-10) and input any remarks or comments about their class contribution and then click add participation. Once the class has ended, simply click on "End Class" on the top right. To export the participation records, simply go back to classes page. From there, click on "Export", and a csv file containing the participation will be downloaded. If you want to delete your class, you can also click on "Delete". This will remove all data related to the class, such as the students and participation.

## Project Structure

- **File Organization**:
  - run.py: This is the entry point of the app.
  - init.py: Initialises the app, modules such as the database, loginmanager, etc.
  - models.py: Contains models used (User, Class, Students, Participation).
  - helper.py: Contains helper functions.
  - errors.py: To redirect to a nicer looking page if there are 404 or 500 errors
  - blueprints: Folder that contains major components such as authentication, class management, and the homepage
    - auth: Folder for auth routes
      - routes.py: login, logout, signup components
    - classes: Folder for classes routes
      - routes.py: create class, start class, end class, delete class, add participation, export participation
    - general: Folder for home page route
      - routes.py: index page displaying home page, and interface when class is started
  - templates:
    - auth_layout.html: layout for auth pages
    - layout.html: layout for home page and classes page (includes things like nav bar)
    - index.html
    - login.html
    - signup.html
    - classes.html
    - 404.html
    - 500.html
  - uploads: Folder for student list csv files

## Design Choices

- **Technological Choices**:
   - Flask framework as backend. Used Flask-SQLAlchemy (ORM) for easier coding experience. Website is largely styled using Bootstrap's classes.

- **Architecture**:
  - Separated different core components of the app (e.g. auth, classes, models) into different folders. Utilise Flask-Blueprint to better manage these components.

## Contributions

- **Acknowledgments**:
  - Stack Overflow, Reddit, ChatGPT
