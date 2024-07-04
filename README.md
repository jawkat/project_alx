
# TaskManager

TaskManager is a comprehensive task management application designed to streamline task assignment and collaboration among team members. It allows users to create tasks, assign collaborators, and add notes to tasks efficiently.


![TaskManger](/TaskManager/static/readme.png)


## Features

- **User Authentication:** Secure login and registration using Flask-Login.
- **Task Management:** Create, update, view, and delete tasks.
- **Collaborator Assignment:** Assign multiple collaborators to tasks.
- **Notes:** Add and view notes for each task.
- **Real-Time Updates:** Real-time task updates using WebSockets.
- **Responsive Design:** Mobile-friendly interface.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/TaskManager.git
    cd TaskManager
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python3 create_table
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Usage

1. **Register and Login:** Create an account or log in with an existing account.
2. **Create Tasks:** Navigate to the dashboard and create new tasks.
3. **Assign Collaborators:** Assign tasks to other users.
4. **Add Notes:** Add notes to tasks for additional context.
5. **Real-Time Updates:** Receive real-time updates on task progress.

## Technologies Used

- **Flask:** Web framework for Python.
- **SQLAlchemy:** ORM for database management.
- **Jinja2:** Templating engine for rendering HTML.
- **HTML/CSS:** For structuring and styling the web pages.
- **JavaScript:** For front-end interactivity.


## Architecture

TaskManager follows a client-server architecture with RESTful APIs for communication between the front-end and back-end. The front-end is designed to be responsive and mobile-friendly.

## Core Algorithms

Key algorithms include task assignment logic, collaborator management, and secure token-based authentication.

## Development Process

We used Agile methodology with weekly sprints, ensuring continuous integration and testing. Major challenges included implementing secure user authentication and real-time updates, both of which were successfully overcome.

## Learnings

Throughout the development of TaskManager, our team enhanced their skills in Flask, SQLAlchemy, and RESTful API design. The project also improved our understanding of real-time web applications and secure authentication methods.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss changes.

## License

This project is licensed under the ALX License.
