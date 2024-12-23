# enterprise mcp mvp demo
A test repo for demonstrating the very basic capabilities of the enterprise-mcp framework.

## Project Structure
.DS_Store .env .env.example .gitignore .mypy_cache/ .venv_be/ Dockerfile enterprise_mcp_mvp_demo/ list_of_server_paths.json README.md requirements.txt


### Directory and File Descriptions

- `.env.example`: Example environment variables file.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `Dockerfile`: Docker configuration file for containerizing the application.
- `enterprise_mcp_mvp_demo/`: Main application directory.
  - `__init__.py`: Initializes the package.
  - `configurations.json`: Configuration file for the application.
  - `db/`: Database-related files and scripts.
  - `main.py`: Entry point for the FastAPI application.
  - `mcp_client/`: Client-side code for interacting with MCP servers.
  - `pre_commit.sh`: Pre-commit hook script for code formatting and linting.
  - `routes/`: API route definitions.
  - `routing/`: Routing logic for the application.
- `list_of_server_paths.json`: JSON file listing paths to various mcp servers.
- `README.md`: This README file.
- `requirements.txt`: Python dependencies file.

## Setup and Installation

1. **Clone the repository:**
   ```sh
   git clone git@github.com:Fisseha-Estifanos/enterprise-mcp-mvp-demo.git
   cd enterprise-mcp-mvp-demo
   ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Setup environmental variables:**
    ```sh
    cp .env.example .env
    ```

## Running the Application
1. **Start the FastAPI application:**
    ```sh
    cd enterprise_mcp_mvp_demo/
    python main.py
    ```
2. **Access the API documentation:**
Open your browser and navigate to either
    1. http://127.0.0.1:8000/docs
    or
    1. http://127.0.0.1:8000/redoc

    to view the interactive API documentation.

    
## Docker usage
1. **Build the docker image:**
    ```sh
    docker build -t enterprise_mcp_mvp_demo .
    ```

2. **Run the docker container:**
    ```sh
    docker run -p 8000:8000 enterprise_mcp_mvp_demo
    ```

## Pre-commit Hook
The pre_commit.sh script is used to format and lint the code before committing. It runs black, autopep8, pylint, and flake8 with specified exclusions.

To use the pre-commit hook, run:
    ```
    ./enterprise_mcp_mvp_demo/pre_commit.sh
    ```

## Configuration
The application configuration is stored in configurations.json. Update this file to change settings such as database URL, allowed roles, and other parameters.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.