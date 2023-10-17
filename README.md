📝 README.md file for the project "Create Blog with Django Rest Framework"

# Create Blog with Django Rest Framework

Welcome to the "Create Blog with Django Rest Framework" project! This project aims to create a blog application using Django and Django Rest Framework.

## Overview

The "Create Blog with Django Rest Framework" project is a web application that allows users to create, read, update, and delete blog posts. It provides a comprehensive RESTful API for managing blog posts and associated functionalities.

## Features

- User Registration and Authentication: Users can register, login, and manage their account.
- Blog Post CRUD Operations: Users can create, read, update, and delete blog posts.
- Commenting System: Users can comment on blog posts.

## Installation

Follow these steps to set up the project:

1. Clone or download the repository: `git clone https://github.com/elibaqani/weblog.git`
2. Navigate to the project directory: `cd weblog`
3. Create a virtual environment: `python3 -m venv env`
4. Activate the virtual environment:
   - For Windows: `env\Scripts\activate.bat`
   - For Linux/Mac: `source env/bin/activate`
5. Install the project dependencies: `pip install -r requirements.txt`
6. Configure the database settings in the `settings.py` file.
7. Perform database migrations: `python manage.py migrate`
8. Run the development server: `python manage.py runserver`
9. Access the application at `http://localhost:8000`

## API Documentation

The API documentation is available at `/api` when the application is running. It provides detailed information about the available endpoints, request/response formats, and authentication requirements.
