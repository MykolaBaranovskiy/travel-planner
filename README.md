# HOW TO START APPLICATION
To start application, you need to: 
- Clone the GitHub repo.
- Put the envs directory at the same level as the backend directory.
- Build the docker containers (docker compose build).
- Launch containers (docker compose up -d).
- Use migrations in backend container (python manage.py migrate).
- Fetch places in backend container (python manage.py fetch_places).
And then you can test the project.