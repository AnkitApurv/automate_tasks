# Automate Tasks

## Documentation

Where's the documentation?

Steps to access the documentation:

__NOTE__: First 2 steps need to be followed only once on any new system, the last 2 steps should be followed whenever one want to access the documentation.

1. Create a new python venv and activate it.

    ```shell
    python venv .venv
    chmod 755 ./.venv/bin/activate
    . ./.venv/bin/activate
    ```

2. Install dependencies via pip.

    ```shell
    pip install -r ./requirements-docs.txt
    ```

3. Start documentation server.

    ```shell
    mkdocs serve
    ```

4. Access documentation website: command executed in the previous step will emit a line similar to the one below, that's the link to our documentation website.

    ```log
    Serving on http://127.0.0.1:8000/
    ```
