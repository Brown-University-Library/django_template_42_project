# purpose

Template for new django projects.


# local-install

```
$ mdir ./foo_stuff_directory   # doesn't matter what it's named
$ cd ./foo_stuff_directory/
$ /path/to/python3.8 -m venv ./venv
(venv) $ git clone git@github.com:birkin/django_template_42_project.git ./foo_project
(venv) $ cd ./foo_project/
(venv) $ pip install -r ./config/requirements/base.txt
(venv) $ python ./manage.py runserver
```

Then open a browser to <http://127.0.0.1:8000/>.
