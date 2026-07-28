# Security-flaws

This repository contains a web app containing 5 common security flaws and their fixes. The app is a basic note taking web app with basic user functionality and features for adding notes, reading notes and searching for them.

## Notes app
The notes app has the following functionalities
- User registering, login and logout
- Add note with title, content and timestamp
- Read note
- Search for notes
- Two users can be initialized to the app using a Django management command

### Installing the Notes app
Create a new virtual environment (here called .venv) for the app by running

`$ python -m venv .venv`

Activate the virtual environment by

`$ source .venv/bin/activate`

Install required dependencies by running

`$ pip install -r requirements.txt`

Make the database for storing notes and users by

`$ python manage.py migrate`

Initialize the database with two users called "bob" and "alice" and example notes by (this is not required but it will help to demonstrate the flaws)

`$ python manage.py initialize_db`

Run the app by

`$ python manage.py runserver`

Open the app in your browser by copying the link provided in the terminal and appending `/notes` to it (for example `http://127.0.0.1:8000/notes`).

## Security flaws in the app
The following security flaws and their fixes are implemented in the code
1. SQL injection
2. Cross-site request forgery (CSRF)
3. Broken access control
4. Vulnerable and outdated components
5. Security misconfiguration

By default, the code contains all the flaws and the fixes are commented out.

The flaws can be easily demonstrated using the two users initialized in the database by the separate command. Their usernames and passwords are
| Username | Password |
| --- | --- |
| alice | redqueen|
| bob | squarepants |

Screenshots demonstrating the flaws are included in `screenshots/`. Detailed explanations of the flaws and their fixes are provided in `flaw_descriptions.pdf`.

### CSRF attack
The app repository also contains a separate python program csrf_attack.py that can be used to demonstrate the CSRF attack. To perform the demonstration, first run the Notes app and then run the CSRF program by

`$ python csrf_attack.py`

Open the provided link in the browser, login to a user in the Notes app and click the button on the CSRF page. You may need to change the port in the file if the default port is unavailable. After a succesful demonstration, you should see a new note in the Notes app that was added by the CSRF attack.

If the demonstration fails with `Server error 5000`, you need to make sure the addresses used are not mixed within the Notes app and the CSRF code. Avoid using `localhost` and prefer `127.0.0.1` to make it work with the default CSRF code.
