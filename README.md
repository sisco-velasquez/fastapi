# Social Network API (FastAPI + SQLModel)

A high-performance, async RESTful API built with **FastAPI** and **PostgreSQL**. This application serves as a backend for a social media platform where users can create accounts, post content, and vote (like) on posts.

##  Features

* **Authentication:** Secure user registration and login using **JWT (JSON Web Tokens)**.
* **Users:** User profile management and password hashing (bcrypt).
* **Posts:** Full CRUD (Create, Read, Update, Delete) operations for posts.
* **Voting System:** Users can like/unlike posts (Many-to-Many relationship).
* **Validation:** Data validation using **Pydantic** models.
* **Database:** **PostgreSQL** interaction using **SQLModel** (SQLAlchemy wrapper).
* **Relationships:** Automatic fetching of post owners and vote counts via SQL Joins.

## Tech Stack

* **Language:** Python 3.10+
* **Framework:** FastAPI
* **ORM:** SQLModel (SQLAlchemy + Pydantic)
* **Database:** PostgreSQL
* **Security:** OAuth2 (JWT Tokens) & Passlib (Password Hashing)

##  Project Structure

```text
app/
├── main.py           # Entry point: App initialization & Router inclusion
├── models.py         # Database Tables (SQLModel)
├── schemas.py        # Pydantic Models (Request/Response validation)
├── database.py       # Database connection logic
├── oauth2.py         # JWT Token creation and verification
├── utils.py          # Password hashing utilities
└── routers/          # API Route logic
    ├── auth.py       # Login endpoint
    ├── user.py       # User CRUD
    ├── post.py       # Post CRUD
    └── vote.py       # Voting logic
