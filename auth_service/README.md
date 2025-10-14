# Synaptiq (Contxta)

> Turn your study session into a showdown. An AI-powered microservices application that transforms static documents into interactive quizzes and competitive challenges.

[![Django CI](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/django-ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/django-ci.yml)

_**Note:** To get the CI badge link above, go to your repository on GitHub -> Actions -> Django CI, and click "Create status badge"._

---

## About The Project

This project is a microservices-based application designed to revolutionize the way we study. Instead of passively reading documents, users can engage with them through AI-powered chat, generate quizzes on the fly, and compete with friends in real-time knowledge duels.

The architecture is built to be scalable and maintainable, with each business capability isolated in its own dedicated service.

### Tech Stack

* **Architecture:** Microservices
* **Backend Services:**
    * **User Service:** Django, Django Rest Framework
    * **Future Services:** FastAPI
* **Database:** MySQL
* **Authentication:** Djoser, JWT (SimpleJWT)
* **Package Management:** `uv`
* **CI/CD:** GitHub Actions
* **Future Containerization:** Docker, Kubernetes

---

## Getting Started

This section guides you through setting up and running the **UserAuth** service, which is the first completed component of the project.

### Prerequisites

* Python 3.10+
* `uv` package manager (`pip install uv`)
* A running MySQL server

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  **Create and activate the virtual environment:**
    ```bash
    # Create the venv
    uv venv

    # Activate it (macOS/Linux)
    source .venv/bin/activate

    # Activate it (Windows)
    .venv\Scripts\activate
    ```

3.  **Set up your environment variables:**
    * Copy the example file to create your own local environment file. This file is ignored by Git and will store your secret keys.
        ```bash
        cp .env.example .env
        ```
    * Open the newly created `.env` file and fill in your `SECRET_KEY` and MySQL database credentials.

4.  **Install project dependencies:**
    * This command reads the `uv.lock` file to install the exact versions of all required packages, ensuring a consistent environment.
        ```bash
        uv pip sync
        ```

5.  **Run database migrations:**
    * This will apply the database schema, including creating the user tables.
        ```bash
        python manage.py migrate
        ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The UserAuth API is now running and accessible at `http://127.0.0.1:8000`.

---

## Project Status & Current Implementation

The project is currently in the initial phase of development. The foundational service for user authentication is complete and fully functional.

### ✅ Completed: UserAuth Service

This is the first microservice, built with Django. It acts as the central authority for user identity and authentication across the entire application.

**Responsibilities:**
* Handles new user registration (Email/Password).
* Manages user login and issues JWT access/refresh tokens.
* Provides secure endpoints to view and manage user profiles.

**Key API Endpoints Available:**
* `POST /api/users/` - Register a new user.
* `POST /api/auth/jwt/create/` - Log in and receive JWT tokens.
* `GET /api/users/me/` - Get the current user's profile data (requires authentication).

---

## 🗺️ Roadmap: Future Features

The next steps involve building the core features of the application as separate FastAPI microservices that will communicate with the UserAuth service.

* **- [ ] 📄 Document Service (FastAPI):**
    * Responsible for uploading and managing user documents (PDF, DOCX).
    * Will handle secure storage and metadata management.

* **- [ ] 🤖 AI & Quiz Generation Service (FastAPI):**
    * The core of the "Solo Study Mode".
    * Will integrate with a Large Language Model (LLM) to:
        * Enable the "Talk with your Doc" feature.
        * Instantly generate MCQs and other questions from document content.

* **- [ ] ⚔️ Competition Service (FastAPI):**
    * Will power the interactive and social features.
    * **1-vs-1 Duel Mode:** Allow a user to challenge a friend on a specific document.
    * **Group Study Mode:** Enable multiple users to compete simultaneously with a live leaderboard.

* **- [ ] 🐳 Deployment & Containerization:**
    * Dockerize each microservice for consistent deployment.
    * Set up a Kubernetes cluster to manage and orchestrate the services in production.