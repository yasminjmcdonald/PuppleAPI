PuppleAPI
=========

*PuppleAPI allows users to create, update, get, and delete dogs.*

Installation
------------

1. Create virtual environment and install requirements.txt:

```
python3 -m venv puppleAPI_venv
cd puppleAPI_venv/bin
source activate
pip install -r requirements.txt
```
2. Update line 5 in database.py to local postgres database url. (Ex. postgresql://postgres:test1234@localhost/PuppleApplicationDatabase)
3. To create the dogs and owners tables in the database, run the following sql:

```
DROP TABLE IF EXISTS owners;

CREATE TABLE owners ( id SERIAL, email varchar(200) DEFAULT NULL, username varchar(45) DEFAULT NULL, first_name varchar(45) DEFAULT NULL, last_name varchar(45) DEFAULT NULL, hashed_password varchar(200) DEFAULT NULL, is_active boolean DEFAULT NULL, role varchar(45) DEFAULT NULL, PRIMARY KEY (id) );

DROP TABLE IF EXISTS dogs;

CREATE TABLE dogs ( id SERIAL, dog_name varchar(200) DEFAULT NULL, temperament varchar(200) DEFAULT NULL, description varchar(200) DEFAULT NULL, breed varchar(200) DEFAULT NULL, age integer DEFAULT NULL, owner_id integer DEFAULT NULL, PRIMARY KEY (id), FOREIGN KEY (owner_id) REFERENCES owners(id) );
```

Execution 
------------
1. While in the PuppleAPI directory run:
```
uvicorn main:app
```
2. In browser, navigate to http://127.0.0.1:8000/docs