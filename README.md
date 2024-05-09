# FastAPI ADDRESS BOOK

This project utilizes FastAPI, a modern, high-performance web framework for building APIs with Python 3.11+ based on standard Python type hints. It serves as an address book application where API users can perform various operations such as:

- **Create:** Users can create new addresses.
- **Update:** Users can update existing addresses.
- **Delete:** Users can delete addresses.
- **Retrieve Addresses:** Users can retrieve addresses based on various criteria, including proximity to specified location coordinates.

Additionally, this address book API provides a user-friendly interface for managing address data efficiently.


## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

Make sure you have the following installed on your local machine:

- Python 3.11+
- pip (Python package manager)

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```bash
    cd address_book
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:

- On Linux:

  ```bash
  source venv/bin/activate
  ```

5. Install dependencies:
    ```bash
    pip install -r requirements/dev.txt
    ```


### Running the Application
Before running the FastAPI application, you need to apply database migrations using Alembic. Follow these steps:
Apply the existing migration to the database:
```bash
alembic upgrade head
```



To start the FastAPI application, run the following command:


```bash
uvicorn src.main:app --reload
```


The `--reload` flag is optional and enables auto-reloading for development purposes.

Once the application is running, you can access the API documentation at `http://127.0.0.1:8000/`.


#### Accessing the Application

After starting the application, you can access the API documentation at http://127.0.0.1:8000/.
