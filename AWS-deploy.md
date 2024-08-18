# Deploying Sentiment Analysis Web Application on AWS

## Overview

This guide provides instructions for deploying the Sentiment Analysis Web Application on Amazon Web Services (AWS) using Docker and Elastic Beanstalk. The application, built with Django and PostgreSQL, allows users to perform real-time sentiment analysis. It is fully containerized using Docker, making it easy to manage and deploy.

## Prerequisites

Before starting, ensure you have the following:

- **AWS Account:** An active AWS account.
- **Docker Installed:** Ensure Docker is installed and running on your local machine.
- **AWS CLI and EB CLI Installed:** AWS Command Line Interface (CLI) and Elastic Beanstalk CLI (EB CLI) must be installed and configured with your AWS credentials.

## AWS Deployment Steps

### 1. Set Up AWS Elastic Beanstalk

Elastic Beanstalk simplifies the deployment process by managing the infrastructure for the application.

- **Initialize Elastic Beanstalk:**

  In the project directory, initialize Elastic Beanstalk with:

  ```bash
  eb init
  ```

  Follow the prompts:

  - Select the appropriate AWS region.
  - Choose "Docker" as the platform since the application is containerized.

- **Create an Elastic Beanstalk Environment:**

  Create a new environment and deploy the application:

  ```bash
  eb create sentiment-analysis-env
  ```

  Elastic Beanstalk will automatically handle provisioning, load balancing, and scaling.

### 2. Docker Configuration

The project is already containerized with Docker. Ensure the Dockerfile and Docker Compose configurations are correctly set up.

- **Dockerfile:**

  The `Dockerfile` defines the environment for your Django application:

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

- **Docker Compose (For Local Testing):**

  Docker Compose orchestrates your application and database containers locally:

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
      command: >
        sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
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

### 3. Deploy the Application

After configuring Elastic Beanstalk and Docker, deploy the application with:

```bash
eb deploy
```

This command will package the application, push it to Elastic Beanstalk, and deploy it in your environment.

### 4. Set Up PostgreSQL on RDS (Optional)

If you prefer using AWS RDS for PostgreSQL instead of a containerized database:

- **Create an RDS Instance:**

  - Log in to the AWS Management Console.
  - Navigate to RDS and create a PostgreSQL instance.
  - Note the endpoint, username, and password.

- **Update Django Settings:**
  - Modify `DATABASES` in `settings.py` to connect to the RDS instance using the provided credentials.

### 5. Environment Variables and Secrets

Elastic Beanstalk allows to securely manage environment variables:

- **Set Environment Variables:**

  Use the Elastic Beanstalk console or CLI to set environment variables like `DJANGO_SECRET_KEY`, `DATABASE_URL`, etc.:

  ```bash
  eb setenv DJANGO_SECRET_KEY=your_secret_key DATABASE_URL=your_rds_database_url
  ```

### 6. Monitoring and Scaling

Elastic Beanstalk provides built-in monitoring and scaling:

- **Monitoring:**

  - Use AWS CloudWatch, integrated with Elastic Beanstalk, to monitor application health and logs.

- **Auto-Scaling:**
  - Elastic Beanstalk automatically scales the application based on traffic, ensuring high availability.

## Accessing the Application

Once deployed, the application will be accessible via the Elastic Beanstalk environment URL. To find this URL:

```bash
eb status
```

Visit the provided URL to access your application.

## Conclusion

This guide outlines the steps required to deploy the Django-based Sentiment Analysis Web Application on AWS using Elastic Beanstalk. By leveraging Elastic Beanstalk, the deployment process is streamlined, allowing to focus on application while AWS manages the underlying infrastructure.
