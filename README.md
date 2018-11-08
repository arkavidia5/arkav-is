# arkav-is

## How to run

### API

Prerequisites: Python 3.6, Pipenv

1. `cd` to the repo's directory
2. For the first run, `pipenv install` to download dependencies
3. `pipenv shell`
4. Copy `.env.example` to `.env` and edit its contents as necessary
5. For the first run, `python manage.py migrate` to run DB migrations (create DB tables)
6. For the first run, `python manage.py createsuperuser` to create a superuser for testing
7. To run, `python manage.py runserver`

#### Notes for API

- The admin interface can be accessed at `/admin`
- To run tests, `python manage.py test`
- After editing any model or pulling changes which include changes to migrations, you need to run migrations again (`python manage.py migrate`)
- After adding/removing packages (editing Pipfile) or pulling changes which include changes to the Pipfile, you need to run `pipenv update`

### Web

Prerequisites: Node.js 8+

1. `cd` to the `arkav-is-web` directory
2. For the first run, `npm install` to download dependencies
3. To run using the dev server, `npm run serve`

#### Notes for web

- When running in development, you may need to adjust the API base URL in `src/api.js`
- The dev server supports hot-reload
- You can use Vue.js devtools Chrome extension to help with debugging
- To build the production bundle, run `npm run build`
- To run tests, `npm run test`
- To lint and fix code style problems, run `npm run lint`
- The linter will also automatically fix code style problems when committing
- After adding/removing packages (editing `package.json`) or pulling changes which include changes to the `package.json` file, you need to run `npm install` again

## How to contribute

1. Clone this repository and ensure you are on the master branch.
2. Create a new feature branch in Git: `git checkout -b <branch_name>` (note: bugfixes can be pushed straight to master)
3. Work on your changes (commit your changes in Git, use descriptive commit messages)
4. Don't forget to add tests; ensure all tests pass: `python manage.py test`
5. If you change any Django model class:
    - Update Django migration files: `python manage.py makemigrations`
    - Migrate your current DB: `python manage.py migrate`
6. When done, ensure all of your changes are committed, then push your branch to Github: `git push -u origin <branch_name>`
7. On the Github website, create a new pull request from your branch to master.
8. Wait for your pull request to be reviewed. If there is anything you need to fix, commit the fix and push it to Github.
9. When the reviewer approves your change, your branch will be merged to master.

## Deployment

- Set up a database
- Use `pipenv install --deploy` to install dependencies
- Copy `.env.example` to `.env` and adjust its contents as necessary
- Don't forget to `python manage.py migrate`
- Don't forget to `python manage.py collectstatic`
- Don't forget to `cd arkav-is-web`, then `npm run build`
- Ensure `MEDIA_ROOT` directory is writable by Django
- Run Django using a WSGI server, e.g. Gunicorn
- Set Gunicorn to run as a service, e.g. using systemd
- Ensure that the Gunicorn service loads environment variables from your `.env` file
- Set up a reverse proxy (e.g. Nginx):
    - Proxy `/api/` and `/admin` to Gunicorn
    - Serve `STATIC_ROOT` directory contents according to `STATIC_URL`
    - Serve `arkav-is-web/dist` directory contents
    - Direct any mismatched URLs to `arkav-is-web/dist/index.html`
    - Set up HTTPS, e.g. using Let's Encrypt and Certbot
- Don't forget to back up regularly
