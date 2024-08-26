# purpose

Template for new django projects.


# local-install

This template project has references to `foo_project` and `foo_app`.

The instructions below show how to use the template to create a project named `x_project` with an app `x_app`.

```
$ mkdir ./x_project_stuff
$ cd ./x_project_stuff/
$ mkdir ./logs
$ mkdir ./DBs
$ /path/to/python3.8 -m venv ./venv
$ git clone git@github.com:birkin/django_template_42_project.git ./x_project
$ cd ./x_project/
$ python ./update_project_and_app_references.py --target_dir "/full/path/to/x_project/" --new_project_name x_project --new_app_name x_app  # all on one line
$ cp ./config/dotenv_example_file.txt ../.env
$ source ../venv/bin/activate
(venv) $ pip install -r ./config/requirements/requirements_base.txt
(venv) $ python ./manage.py runserver
```

Then open a browser to <http://127.0.0.1:8000/>.
