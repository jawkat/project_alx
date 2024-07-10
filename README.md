
# TaskManager 🚀

TaskManager is a comprehensive task management application designed to streamline task assignment and collaboration among team members. It allows users to create tasks, assign collaborators, and add notes to tasks efficiently.


![TaskManger](/TaskManager/static/readme.png)



## Features ✨

- **User Authentication:** Secure login and registration using Flask-Login.
- **Task Management:** Create, update, view, and delete tasks.
- **Collaborator Assignment:** Assign multiple collaborators to tasks.
- **Notes:** Add and view notes for each task.
- **Real-Time Updates:** Real-time task updates using WebSockets.
- **Responsive Design:** Mobile-friendly interface.

## Installation 🔧

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
## Our Inspiration and Journey 🌟

### Inspiration 💡
The inspiration for TaskManager stems from a personal experience of constantly juggling multiple responsibilities and struggling to keep track of them. As students at ALX, we were often overwhelmed by the number of assignments, group projects, and personal tasks we had to manage. We realized that having a reliable tool to organize our tasks would significantly improve our productivity and reduce stress.

One day, while brainstorming ideas for our portfolio project, we thought about creating a solution to this problem and improving what we had learned during these 9 months. We wanted to build a task management application that not only helps users organize their tasks but also allows them to collaborate with others. This idea was driven by our own needs and the desire to create something that could benefit many people in similar situations.

We started developing TaskManager with the vision of creating a simple, intuitive, and efficient tool that can be used by anyone, whether they are students, professionals, or anyone in need of better task management. Throughout the development process, we kept user experience at the forefront, ensuring that the application is user-friendly and meets the needs of our target audience.

### Timeline 🗓️
- **Initial Brainstorming and Conceptualization:** We spent the first week discussing and refining our ideas. We identified the core features that TaskManager should have and created a roadmap for development.
- **Development Phase:** Over the next week, we worked tirelessly to bring our vision to life. We divided the tasks among team members, focusing on different aspects such as front-end design, back-end development, and database management.
- **Testing and Refinement:** Once we had a working prototype, we began rigorous testing. We sought feedback from peers and friends, which helped us identify and fix bugs and improve the overall functionality of the application.
- **Finalization and Launch:** After several iterations and improvements, we uploaded our TaskManager. It was a proud moment for us, knowing that we had created something useful from scratch.

TaskManager is not just a project for us; it represents our journey of learning, collaboration, and perseverance. We hope that this tool will help others manage their tasks more effectively and achieve their goals.


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

## Contact 📬

Feel free to reach out to us if you have any questions or feedback.

- [Jawad's LinkedIn](https://www.linkedin.com/in/jawadkatten/) 🔗
- [Jawad's GitHub](https://github.com/jawkat) 🐙
- [Abdelrahman's LinkedIn](#) 🔗
- [Abdelrahman's GitHub](#) 🐙
