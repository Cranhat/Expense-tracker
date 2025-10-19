# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown  pages, images and other files.

## Postgre sql commands
Start server:
    sudo service postgresql start

Close server:
    sudo service postgresql stop

Set password:
    sudo passwd postgres

To connect with postgresql shell:
    sudo -u postgres psql

To restart postgresql service:
    sudo systemctl restart postgresql

## Database structure
tables:
    - users:
        - 

    - accounts:
        - 
        
    - transactions:
        - 

