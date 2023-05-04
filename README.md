# Welcome to Fit Track

## This project was developed utilizing:

* ####  Backend: Python/Flask

* #### Frontend: React/Redux/JS/HTML/CSS

* #### DB: SQLITE
* #### ORM: SQLAlchemy

* ####  Hosted on AWS/GCP
[Fit Track](/)

## Wiki Links:

* [Database Schema](https://github.com/EdgarMLee/Fit_Track/wiki/DB-Schema)
* [User Stories](https://github.com/EdgarMLee/Fit_Track/wiki/User-Stories)
* [API Routes](https://github.com/EdgarMLee/Fit_Track/wiki/API-Routes)
* [Redux State Shape](https://github.com/EdgarMLee/Fit_Track/wiki/Redux-State-Shape)
* [App Features](https://github.com/EdgarMLee/Fit_Track/wiki/App-Features)

***

## How to run Fit Track Locally:
* Clone the repository in your terminal: ```git clone https://github.com/EdgarMLee/Fit_Track.git```
* cd into Fit_Track folder and run ```pipenv install```
* Open two terminal paths for both Fit_Track and react-app.
* Under Fit_Track run ```pipenv shell``` then ```flask run```, for react-app run ```npm install```
* Create a ```.env``` file under the root of the backend folder with the following contents:
```
REACT_APP_BASE_URL=http://localhost:5000
```
* In the terminal under Fit_Track, migrate and seed files as follows:
```
flask db upgrade
flask seed all
```
* Now, run ```flask run``` under Fit_Track and ```npm start``` under react-app

### Your local host should be running with full functionality now!

