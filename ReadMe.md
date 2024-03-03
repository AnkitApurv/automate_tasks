# Documentation

replace with robot framework

For user auth:

replace with pywebio with basic auth for auth + 
pgp (using gnupg) + mozilla sops for saving password etc

For secrets management:

replace with either of the two
- for central sotre serving multiple remote deployments -> hashicorp vault [not recommended dure to extra dependencies and need to manage secure connection b/w this vault and deployemnt which needs to use it's sevice]
- for a mechnism isolated to an individual deployment -> pgp (using gnupg) + mozilla sops

Where's the documentation?
Uses materials for mkdocs

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
    pip install -r ./setup/pip_requirements.txt
    ```

3. Start documentation server.

    ```shell
    mkdocs serve --clean --config-file docs/mkdocs.yaml
    ```

4. Access documentation website: command executed in the previous step will emit a line similar to the one below, that's the link to our documentation website.

    ```log
    Serving on http://127.0.0.1:8000/
    ```
