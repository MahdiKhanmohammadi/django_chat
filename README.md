Django Chat

A simple real-time chat application built with Django and Django Channels.

This project was created as my first experience working with Django Channels and WebSockets. It provides basic messaging functionality where users can create accounts, manage their profiles, find other users, add them to contacts, and communicate in real time.

Features

- User registration and authentication
- Profile creation with:
  - First name
  - Last name
  - Profile picture
- Search users by username (email address)
- Add users to contacts
- AJAX-powered user search and contact management
- Private one-to-one conversations
- Real-time messaging using WebSockets
- Contact list management
- Dockerized development environment

Technologies Used

- Django
- Django Channels
- WebSockets
- Docker
- AJAX
- HTML
- CSS
- JavaScript
- SQLite

How It Works

After registering, users can complete their profile by adding their first name, last name, and profile picture.

Users can search for other users by their username (email address) and add them to their contact list. The search functionality and contact management system are implemented using AJAX, allowing users to interact with the application without reloading the page.

Once users are connected through contacts, they can start private conversations. Messages are delivered instantly through Django Channels and WebSockets, providing a real-time chat experience.

Getting Started

Clone the repository:

git clone https://github.com/MahdiKhanmohammadi/django_chat.git
cd django_chat

Build and run with Docker:

docker-compose up --build

Apply migrations:

python manage.py migrate

Create a superuser (optional):

python manage.py createsuperuser

Run the development server:

python manage.py runserver

Learning Goals

This project was developed to learn and practice:

- Django Channels
- WebSocket communication
- Real-time web applications
- Docker fundamentals
- AJAX requests
- User authentication and profile management in Django



Author

Mahdi Khanmohammadi

GitHub: https://github.com/MahdiKhanmohammadi
