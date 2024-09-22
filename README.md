# purpose

Lightweight template for new django projects.

Includes a few nice-practices: 
- nothing private is in the project-repo; fostering public repos.
- shows pattern to keep views.py functions short-ish manager functions (eg views.version()).
- log-formatting shows useful stuff.
- git branch/commit url is constructed in a way that avoids the new `dubious ownership` error.
- includes a couple of client-get tests that respond differentially to dev and prod settings.
- dev-only error-check url (enables confirmation that email-admins-on-error is set up correctly).
- uses python-dotenv.
- uses tilde-comparators in the `.in` requirements files for stable upgrades.
- uses layered `base.in` and `server.in` requirements files for clarity re what's really in the venv. 
- ensures compatible urllib3 and mysqlclient versions for reliable deployment.

--- 


# local-install

Notes about the install instructions...
- The instructions below reference `x_project_stuff`, `x_project`, and `x_app`. In all cases replace with the name of your project, like: `isbn_api_project_stuff`, `isbn_api_project`, and `isbn_api_app`.
- Sensible suggestion: use the version of python used by the oldest server on which you'll be running the code. (Django 4.2x requires at least Python 3.8.)
- The `update_project_and_app_references.py` script ([link](https://github.com/Brown-University-Library/django_template_42_project/blob/main/update_project_and_app_references.py)) deletes the cloned `.git` directory. Why? So you don't accidentally start building away and commit to the template repo. After this installation, creating a new git repo is one of the first things you should do.
- When you run the `pip istall ...` command, you may get a message about upgrading pip, with instructions. That's always a good idea, but not necessary for this install.
- When you start the webapp via `runserver`, you'll get a message that there are migrations that need to be run, with instructions. You can go ahead and do that, or do it later (this is a one-time thing).

```bash
$ mkdir ./x_project_stuff
$ cd ./x_project_stuff/
$ mkdir ./logs
$ mkdir ./DBs
$ /path/to/python3.8 -m venv ./venv
$ git clone https://github.com/Brown-University-Library/django_template_42_project.git
$ cd ./django_template_42_project/

## the line below is a single command, all on one line (clarifying in case it wraps)
$ /path/to/python3.8 ./update_project_and_app_references.py --target_dir "/full/path/to/x_project/" --new_project_name x_project --new_app_name x_app  

## get back into the correct directory (the command above changed the name)
cd ../x_project/

$ cp ./config/dotenv_example_file.txt ../.env
$ source ../venv/bin/activate
(venv) $ pip install -r ./config/requirements/requirements_base.txt
(venv) $ python ./manage.py runserver
```

That's it!

---

# Stuff to try

Open a browser to <http://127.0.0.1:8000/>.

Try <http://127.0.0.1:8000/error_check/>. You'll see the intentionally-raised error in the browser (would result in a `404` on production), but if you want to confirm that this really would send an email, open another terminal window and type:

```bash
$ python3 -m smtpd -n -c DebuggingServer localhost:1026
```

You won't initially see anything, but if you reload the error-check url, and then check this terminal window again, you'll see the email-data that would have been sent.

Trry <http://127.0.0.1:8000/version/>. Once you `git init`, `git add --all`, and `git commit -am "initial commit"`, it'll show the branch and commit -- super-handy for dev and prod confirmations.

Try `(venv) $ python ./manage.py test`. There are two simple tests that should pass.

Check out the logs (`project_stuff/logs/`). The envar log-level is `DEBUG`, easily changed. On the servers that should be `INFO` or higher, and remember to rotate them, not via python's log-rotate -- but by the server's log-rotate.

Next -- well, the sky's the limit!

---
