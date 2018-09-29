# arkav-is

## How to run

### API

Prerequisites: Python 3.6, Pipenv

1. `cd` to the repo's directory
2. For the first run, `pipenv install` to download dependencies
3. `pipenv shell`
4. For the first run, `python manage.py migrate` to run DB migrations (create DB tables)
5. For the first run, `python manage.py createsuperuser` to create a superuser for testing
6. To run, `python manage.py runserver`

#### Notes
- The admin interface can be accessed at `/admin`
- After editing any model or pulling changes which include changes to migrations, you need to run migrations again (`python manage.py migrate`)
- After adding/removing packages (editing Pipfile) or pulling changes which include changes to the Pipfile, you need to run `pipenv update`

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
