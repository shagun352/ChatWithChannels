# ChatWithChannels

A real-time chat application built with Django Channels and WebSockets.

## Features

- Real-time chat rooms
- User authentication
- Message persistence in the database
- Online/offline user status
- Support for multiple chat rooms and workspaces

## Requirements

- Python 3.8+
- Django 3.2+
- Channels 3+
- PostgreSQL or SQLite (for database)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/shagun352/ChatWithChannels.git
   cd ChatWithChannels


# Create and activate a virtual environment

python -m venv env
source env/bin/activate      # On Linux/Mac
env\Scripts\activate         # On Windows


# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver

# Running with Channels
uvicorn chatapplication.asgi:application --reload
