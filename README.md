# myadmin

MyAdmin is a web application that prototypes some basic analysis of repositories. It uses the pydriller (https://github.com/ishepard/pydriller) to analyze and mining data from software repositories. It is possible to integrate this application with other application or service via rest API implementation by updating ./myapp/services

It was created using the flask framework (https://flask.palletsprojects.com) and the AdminLTE (Free Bootstrap Admin Template) as UI interation.

1. Clone the repository

2. Configure email client
```
echo "export SENDGRID_API_KEY='YOUR_API_KEY'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
```

3. Install dependencies
```
pip install pydriller
pip install wordcloud
pip install sendgrid
```
3. Set environment variables
```
. setvariables.sh
```

4. Restart database (optional)
```
flask init-db
```

5. Run application
```
flask run
```

6. How to perform application testing in myadmin app?
```
pip install pytest pytest-html
pip install coverage
cd tests
./my_testes.sh
```

7. Functional regression tests that must be performed:

7.1 Login (OK)

7.2 I forgot my password

7.3 Register a new user

7.4 Check all elements of the dashboard

7.5 List members (OK)

7.6 List of repositories of the logged in user (OK)

7.7 View details of the first repository in the list of repositories

7.8 Check all elements of the visualized repository

7.9 View user profile

7.10 Change user name and email

7.11 Change user image

7.12 Create new repository

7.13 View created repository

7.14 Change repository name

7.15 Delete repository
