# ecommerce--website
This is an Interactive Ecommerce Website for Ecommerce Products the use of code to make a website using AWS as my Cloud platform.

## Setting up PostgreSQL Database

1. Install PostgreSQL on your machine or use a cloud-based PostgreSQL service.
2. Create a new database named `ecommerce`.
3. Update the `DATABASE_URL` environment variable in the `config.py` file with your PostgreSQL connection string.

## Running the Application using Docker Compose

1. Make sure you have Docker and Docker Compose installed on your machine.
2. Navigate to the project directory.
3. Run the following command to start the application:

```bash
docker-compose up
```

4. The application will be accessible at `http://localhost:5000`.
