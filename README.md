# Order_management_Api
A Flask Api to manage Orders by users

- [How to set up a Flask API with Flask-RESTX]
- Databases with Flask-SQLAlchemy
- JWT Authentication with Flask-JWT-Extended
- Environment variables with Python-Decouple
- Database migrations with Flask-Migrate
- How to write Unit Tests with Unittest and PyTest
- Documenting REST APIs with SwaggerUI and Flask-RESTX
- Error Handling with Werkzeug


## How to run the project
Clone the project repository
```
git clone https://github.com/riskymind/Order_management_Api.git

```

Enter the project folder and create a virtual environment
```
cd https://github.com/riskymind/Order_management_Api
$ python -m venv env

```

Activate the virtual environment
```
$ source env/bin/actvate #On linux Or Unix
$ source env/Scripts/activate #On Windows 

```

Install all requirement
```
$ pip install -r requirements.txt

```

Run the project in development
```
$ export FLASK_APP=api/
$ export FLASK_DEBUG=1
$ flask run

```

or 

```
 python runserver.py
 
```