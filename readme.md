# Sentiment Analysis Web Application

## Overview

This project is a sentiment analysis web application that allows users to input text and receive real-time sentiment analysis using a basic machine learning model (TextBlob). The application is built with Django and uses PostgreSQL as its database. The project is fully containerized using Docker, making it easy to deploy and manage.

## Features

- **Real-time Sentiment Analysis:** Users can input text and receive immediate sentiment analysis results (polarity and subjectivity).
- **User Registration & Authentication:** Users can register and log in to save their analysis history.
- **Analysis History:** Logged-in users can view a history of all their past analyses.

## Technology Stack

- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Machine Learning:** TextBlob for sentiment analysis
- **Containerization:** Docker with Docker Compose

## Project Structure

- **`main` branch:** Contains the configuration for tools, final deployment, and final documentation.
- **`development` branch:** Used for major development work.
- **Feature branches:** Each new feature or bug fix is developed in its own branch.
- **GitHub Issues:** Used to track features and tasks from the beginning of the project.

## Installation and Setup

### Prerequisites

Ensure you have the following installed on your system:

- Docker
- Docker Compose

### Quick Start

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/sentiment-analysis-webapp.git
   cd sentiment-analysis-webapp
   ```

2. **Set Up Environment Variables:**

   Create a `.env` file based on the `.env.example` template:

   ```bash
   cp .env.example .env
   ```

   Then, fill in your PostgreSQL credentials:

   ```env
   POSTGRES_DB=sentiment_analysis_webapp
   POSTGRES_USER=your_postgres_username
   POSTGRES_PASSWORD=your_postgres_password
   ```

3. **Build and Run the Application:**

   Use Docker Compose to build and run the application:

   ```bash
   docker-compose up --build
   ```

   This command will:

   - Set up the PostgreSQL database in a container.
   - Set up the Django web application in another container.
   - Automatically run migrations to set up the database schema.

4. **Access the Application:**

   Once the application is running, you can access it in your web browser at:

   ```
   http://localhost:8000
   ```

## Usage

- **Text Analysis:** Input text in the provided form on the homepage to receive sentiment analysis results.
- **User Registration:** Sign up to save and view your analysis history.
- **View History:** If logged in, click on "View Analysis History" to see a list of all analyses you have performed.

## Project Details

### Technology Choices

- **Django:** Chosen for its robust web development features and ease of integration with PostgreSQL.
- **PostgreSQL:** A powerful, open-source object-relational database system that is well-suited for handling complex queries and large datasets.
- **TextBlob:** A simple library for processing textual data, providing an easy-to-use API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more. TextBlob was chosen for its simplicity and effectiveness for basic sentiment analysis.

### Docker Configuration

- **Dockerfile:**

  The `Dockerfile` is based on the `python:3.12-slim` image, which is lightweight and efficient. It includes necessary dependencies such as `libpq-dev` for PostgreSQL and `gcc` for compiling any additional C-based Python packages.

  ```Dockerfile
  FROM python:3.12-slim

  ENV PYTHONDONTWRITEBYTECODE=1
  ENV PYTHONUNBUFFERED=1

  WORKDIR /app

  RUN apt-get update && apt-get install -y \
      libpq-dev \
      gcc \
      && apt-get clean

  COPY requirements.txt .

  RUN pip install --upgrade pip
  RUN pip install -r requirements.txt

  COPY . .

  EXPOSE 8000

  CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
  ```

- **Docker Compose:**

  Docker Compose orchestrates the containers, ensuring the database is up and running before the web application starts. It uses health checks to ensure the database is ready.

  ```yaml
  services:
    db:
      image: postgres:16
      volumes:
        - postgres_data:/var/lib/postgresql/data/
      env_file:
        - .env
      ports:
        - '5432:5432'
      healthcheck:
        test: ['CMD-SHELL', 'pg_isready -U $POSTGRES_USER -d $POSTGRES_DB']
        interval: 10s
        retries: 5

    web:
      build: .
      command: python manage.py runserver 0.0.0.0:8000
      volumes:
        - .:/app
      ports:
        - '8000:8000'
      depends_on:
        db:
          condition: service_healthy
      env_file:
        - .env

  volumes:
    postgres_data:
  ```

### Versioning and Branch Management

- **main branch:** Used for the final deployment and for merging stable features.
- **development branch:** The primary branch for ongoing development.
- **Feature branches:** Each feature or bug fix is developed in its own branch, which is then merged into `development` and, once stable, into `main`.

### Testing

- **Unit Tests:** Ensure that the project’s functionality is correct and that new changes don’t introduce regressions.
- **Dockerized Testing:** Run tests within the Docker environment to ensure consistency across different development environments.
