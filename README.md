# purpose

Template for new django projects.


# local-install

```
$ mkdir ./foo_stuff_directory   # doesn't matter what it's named
$ cd ./foo_stuff_directory/
$ mkdir ./logs
$ mkdir ./DBs
$ /path/to/python3.8 -m venv ./venv
$ git clone git@github.com:birkin/django_template_42_project.git ./foo_project
$ cd ./foo_project/
$ python ./update_project_and_app_references.py --target_dir "/full/path/to/foo_project/" --new_project_name bar_project --new_app_name bar_app  # all on one line
$ cp ./config/dotenv_example_file.txt ../.env
$ source ../venv/bin/activate
(venv) $ pip install -r ./config/requirements/requirements_base.txt
(venv) $ python ./manage.py runserver
```

Then open a browser to <http://127.0.0.1:8000/>.
