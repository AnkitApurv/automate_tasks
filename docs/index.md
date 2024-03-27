# Read Me

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    app/
        automate_tasks/
        config/
        crypto/
        manage_task_secrets/
        profile/
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.\
    logs/
    setup/
    systemd/
    web_server/
    ReadMe.md
    mkdocs.yml    # The configuration file.
    docker-compose.yaml
    login.dockerfile
    manage_creds.dockerfile

This is a python project which is meant to automate logging into Tradetron web platform.

## License and Disclaimer

__NOTE__: This is a private project, no party is authorized access to the source code or it's usage in any capacity unless explicitly grated access by the original author.

## Usage

The python scripts and assisting files are stored in _app_ folder, plese see readme.md within that folder.