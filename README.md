# E-shop
## Table of Contents

- Setup Instructions
- Postman Collection
## Setup instructions
- Make sure you have python installed
- Clone the repository
- In the folder where the repository was cloned create a virtual environment using virtualenv venv
- Activate the virtual environment by running (on Windows)

```
venv\Scripts\activate
```

- Install the dependencies using (the package manager pip)

```
pip install -r requirements.txt 
```
- Migrate existing database tables by running

```
python manage.py migrate
```
- Run the server using
```
python manage.py runserver
```
## Postman Collection
[Link to Postman Collection](https://www.getpostman.com/collections/8312baad9f7fe13790a3)
