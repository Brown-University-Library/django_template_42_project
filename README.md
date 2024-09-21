# purpose

Lightweight template for new django projects.

Includes a few nice-practices: 
- nothing private is in the project-repo; fostering public repos.
- log-formatting showing function and line-number.
- git branch/commit url is constructed in a way that avoids the new `dubious ownership` error.
- includes a couple of client-get tests that respond differentially to dev and prod settings.
- dev-only error-check url (enables confirmation that email-admins-on-error is set up correctly).
- uses python-dotenv.
- uses requirements tilde-comparators in the `.in` files for stable upgrades.
- uses layered `base.in` and `server.in` files for clarity re what's in the venv. 
- ensures compatible urllib3 and mysqlclient versions for reliable deployment.

--- 


# local-install

Notes about the install instructions...
- The instructions below reference `x_project_stuff`, `x_project`, and `x_app`. In all cases replace with the name of your project, like: `isbn_api_project_stuff`, `isbn_api_project`, and `isbn_api_app`.
- Sensible suggestion: use the version of python used by the oldest server on which you'll be running the code. (Django 4.2x requires at least Python 3.8.)
- The `update_project_and_app_references.py` script ([link](update_project)) deletes the cloned `.git` directory. Why? So you don't accidentally start building away and commit to the template repo. After this installation, creating a new git repo is one of the first things you should do.
- When you starting the webapp via `runserver`, you'll get a message that there are migrations that need to be run. You can go ahead and do that, or do it another time.

```bash
$ mkdir ./x_project_stuff
$ cd ./x_project_stuff/
$ mkdir ./logs
$ mkdir ./DBs
$ /path/to/python3.8 -m venv ./venv
$ git clone git@github.com:birkin/django_template_42_project.git
$ cd ./django_template_42_project/

## the line below is a single command, all on one line (clarifying in case it wraps)
$ /path/to/python3.8 ./update_project_and_app_references.py --target_dir "/full/path/to/x_project/" --new_project_name x_project --new_app_name x_app  

$ cp ./config/dotenv_example_file.txt ../.env
$ source ../venv/bin/activate
(venv) $ pip install -r ./config/requirements/requirements_base.txt
(venv) $ python ./manage.py runserver
```

Then open a browser to <http://127.0.0.1:8000/>.

Also try <http://127.0.0.1:8000/error_check/>. You'll see the intentionally-raised error in the browser (would result in a `404` on production), but if you want to confirm that this really would send an email, open another terminal window and type:

```bash
$ python3 -m smtpd -n -c DebuggingServer localhost:1026
```

You won't initially see anything, but if you reload the error-check url, and then check this terminal window again, you'll see the email-data that would have been sent.

Finally, try <http://127.0.0.1:8000/version/>. Once you `git init`, it'll show the branch and commit, super-handy.

[update_project]: <https://github.com/Brown-University-Library/django_template_42_project/blob/main/update_project_and_app_references.py>

---
