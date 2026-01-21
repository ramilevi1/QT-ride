[![Python CI](https://github.com/ramilevi1/QT-ride/actions/workflows/python-app.yml/badge.svg)](https://github.com/ramilevi1/QT-ride/actions/workflows/python-app.yml)

# QT-ride
Carpooliong. features included:
1. sign up and log-in/log-out (authentication)
2. HTTPS support (currently with self sign certificate)
3. responsive front-end and backend
7. blog to share our progress and learnings
8. parsing blog for dynamic content and search functionality
9. newletter signin for anyone who wants to be notified of new posts
10. script to send weekly/monthly newsletter to registered users
11. unsubscrite functionality
12. contact us - Email sender (currently send to rami's personal email)


# Technology used : 
1. HTML 5
2. CSS 3
3. Javascript (vanilla)
4. Jquery
5. Bootstrap
6. MixItUp plugin
7. Flask - Python
8. Ajax for serving JS files
9. SQlite3
10. Playwright basic e2e tests
11. unit tests 

Next to do:
1. containerize (p1)
2. admin backoffice for managing users and blog posts (p2)
2. deploy to production using uWSGI ?! (p2)
3. github action setup for CI/CD (p0)
4. using web server NginX or Apache (p1)
5. SSL support (HTTP, HSTS) for security (p1)
6. RabbitMQ for serving email async and push notification later on live rides notification (p2)
7. MongoDB for serving images (p2)
8. sqlite3 database replication with the app and failover seperate service (p1)
9. create the offerRide and SearchRide as microservices (p0)


To start the web application:
python -m venv venv  OR 
python -m venv C:\xyz\venv\Scripts\python.exe
.\venv\Scripts\activate
$env:PATH = ".\venv\Scripts;" + $env:PATH 
flask db init     
flask db upgrade
flask db migrate
pip install Flask
set FLASK_APP=app.py flask run
pip install Flask-Mail
pip install Flask-SQLAlchemy      
pip install beautifulsoup4
pip install flask-migrate
pip install flask-login
pip install spacy
python -m spacy download en_core_web_sm
pip install WTForms
pip install Flask-WTF

# install selfsign certificate:
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=127.0.0.1'
# remove passcode: 
openssl rsa -in key.pem -out key_decrypted.pem        

$env:PATH = ".\venv\Scripts;" + $env:PATH   
export PYTHONPATH=/path/to/parent_directory:$PYTHONPATH
>> python scripts/parse_blogs.py
python -m venv C:\xyz\venv\Scripts\python.exe
.\venv\Scripts\activate   
python .\app.py -debug 
flask run
 
 
Architecture:
N-tier microservices arcitecture 
                        --------
                        |Client |
                        --------
                            |
                            |
                            |  
------------------------    -------------------    -------------------
|authentication service|    |offerRide service|   |searchRide service|
------------------------    -------------------   --------------------
            |                        |                    |
            |                        |                    |
      ------------            --------------         ----------
      |   DB     |            |     DB     |         |    DB   |
      ------------            -------------          ----------

# QT-ride Mac

A microservices-based ride-sharing application adapted for macOS.

## Services

- **Auth Service** (Port 5001): Handles user authentication
- **Search Service** (Port 5002): Manages ride searches
- **Offer Service** (Port 5004): Handles ride offers
- **User Profile Service**: Manages user profiles

## Setup

1. Create a Python virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
```

2. Install dependencies for each service:
```bash
cd auth_service
pip install Flask==3.0.2 Flask-SQLAlchemy==3.1.1 Flask-Migrate==4.0.7 PyJWT==2.8.0
```

3. Run the services:
```bash
# Auth Service
cd auth_service
python3 app.py

# Search Service
cd ../search_service
python3 app.py

# Offer Service
cd ../offer_service
python3 app.py
```

## API Endpoints

### Auth Service (localhost:5001)
- POST /signup - Create new user
- POST /signin - User login
- POST /signout - User logout

### Search Service (localhost:5002)
- GET /search - Search for rides

### Offer Service (localhost:5004)
- POST /offer - Create ride offer

## Requirements
- Python 3.11+
- Flask
- SQLAlchemy
- PyJWT
