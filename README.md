# myadmin

MyAdmin is a web application that prototypes some basic analysis of repositories. It uses the pydriller (https://github.com/ishepard/pydriller) to analyze and mining data from software repositories. It is possible to integrate this application with other application or service via rest API implementation by updating ./myapp/services

It was created using the flask framework (https://flask.palletsprojects.com) and the AdminLTE (Free Bootstrap Admin Template) as UI interation.

1. Clone the repository

2. Configure environment variables
```
export FLASK_APP=myapp
export FLASK_ENV=development
```

3. Configure email client
```
echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
```

4. Install dependencies
```
pip install pydriller
pip install wordcloud
pip install sendgrid
```

5. Restart database
```
flask init-db
```

6. Run application
```
flask run
```

7. How to perform application testing in myadmin app?
```
pip install pytest pytest-html
pip install coverage
cd tests
./my_testes.sh
```

8. Functional regression tests that must be performed:

8.1 Login (OK)

8.2 I forgot my password

8.3 Register a new user

8.4 Check all elements of the dashboard

8.5 List members (OK)

8.6 List of repositories of the logged in user (OK)

8.7 View details of the first repository in the list of repositories

8.8 Check all elements of the visualized repository

8.9 View user profile

8.10 Change user name and email

8.11 Change user image

8.12 Create new repository

8.13 View created repository

8.14 Change repository name

8.15 Delete repository
