# Emerald

Emerald retrieves emails that need to be sent from a database, generates the HTML for each email, then sends the emails.

## Run Locally

Prerequisites

- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Pipenv](https://pypi.org/project/pipenv/)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Taskfile](https://taskfile.dev/installation/)

1. Clone the repository

    ```bash
    git clone https://github.com/digitalsquid7/emerald
    ```
   
1. Change directory to the root emerald folder

    ```bash
    cd emerald
    ```

1. Install Python dependencies with Pipenv

   ```bash
   task install-python-dependencies
   ```

1. Setup docker containers with the taskfile

    ```bash
    task setup
    ```

1. Run main

    ```bash
    python main.py
    ```

## Links

Emerald logo designed with Adobe:
https://www.adobe.com/express/create/logo
