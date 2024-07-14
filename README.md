# Wallet Test Task

This is a Python project that uses Django and Docker for development and testing.

## Running the Application

### Via docker-compose

1. Clone the repository:
    ```
    git clone https://github.com/ccdsad/wallet-test-task.git
    ```

2. Navigate to the project directory:
    ```
    cd wallet-test-task
    ```

3. Prepare the environment file. For example prod.env containing:
    ```
    MYSQL_DATABASE=wallet
    MYSQL_USER=wallet
    MYSQL_PASSWORD=wallet123
    MYSQL_ROOT_PASSWORD=root123
    SECRET_KEY=qwerasdf123
    ```

4. Build and start the Docker containers:
    ```
    docker-compose --env-file local.env --project-name wallet up -d --build
    ```

5. Migration:
    ```
    docker-compose --env-file local.env --project-name wallet run web python manage.py migrate
    ```

The application should now be running at `http://localhost:8000`.

## Running the Tests

To run the tests, execute the following command:
    ```
    ./manage.py test
    ```

## Running tests with coverage

1. Run tests with code coverage:
    ```
    coverage run --source=apps.wallet ./manage.py test apps.wallet
    ```

2. Generate the coverage report:
    ```
    coverage html -d htmlcov
    ```
   
3. Open the coverage report (index.html) in browser:
    
## Running the Linters

To run the linters, execute the following command:

1. Code formatting:
    ```
    ruff format src
    ```

2. Type checking with mypu:
    ```
    mypy --config-file mypy.ini --python-version 3.12 --install-types \
     --non-interactive --show-error-context --show-column-numbers --pretty src
    ```

3. Static analysis with ruff:
    ```
     ruff check --output-format concise --fix src
    ```
