# purpose

Lightweight template for new django projects.

Includes a few nice-practices such as: 
- log-entries showing function and line-number.
- git branch/commit url that avoids `dubious ownership` error.
- includes a couple of client-get tests that respond differentially to dev and prod settings.
- dev-only error-check url (enables confirmation that email-admins-on-error is set up correctly).
- uses python-dotenv.
- uses requirements tilde-comparators in the `.in` files for stable upgrades.
- uses layered `base.in` and `server.in` files for clarity re what's in the venv. 
- ensures compatible urllib3 and mysqlclient versions for reliable deployment.

--- 


# local-install

This template project has references to `foo_project` and `foo_app`.

The instructions below show how to use the template-repo to create a project named `x_project` with an app `x_app`.

```
$ mkdir ./x_project_stuff
$ cd ./x_project_stuff/
$ mkdir ./logs
$ mkdir ./DBs
$ /path/to/python3.8 -m venv ./venv
$ git clone git@github.com:birkin/django_template_42_project.git ./x_project
$ cd ./x_project/

## the line below is a single command, all on one line (clarifying in case it wraps)
$ python ./update_project_and_app_references.py --target_dir "/full/path/to/x_project/" --new_project_name x_project --new_app_name x_app  

$ cp ./config/dotenv_example_file.txt ../.env
$ source ../venv/bin/activate
(venv) $ pip install -r ./config/requirements/requirements_base.txt
(venv) $ python ./manage.py runserver
```

Then open a browser to <http://127.0.0.1:8000/>.

---
