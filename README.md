# async_db_playground

My personal playground to test some python async features and their interaction in a "real" scenario.   

## Use:

If you want to try this examples you need to install:
* Postgresql 9.4 (or later) 
* Python 3.5 (or later)
* Python dependencies listed in /pip_requirements.txt 

Database:
* Creation: To create the database you should use the commands listed in db/create_db.sql
* Model: To deploy the model you should use the script db/adm_deploy_db.sh or manually deploy it in the order listed in db/create_model.sql

### examples / async_notify /

This is a simple Proof of Concept to get real time notifications from the Database and display them on the screen.
I'll use the base of this POC for async_notify_dbsync. 
 
### examples / async_db_sync /

This POC aims to create a replication mechanism between two given tables using:
* python3.5 (asyncio + ThreadPoolExecutor +  psycopg2 + sqlalchemy)
* Postgresql 9.4 (Notifications + json features).py
It's not intended to be used as a replication mechanisms in a production environment. Is just a POC.
Several implementation decisions are based on [this zzzeek blog entry](http://techspot.zzzeek.org/2015/02/15/asynchronous-python-and-databases/) if you are interested I recommend you to read it.
 
## Other references: 

* Psycopg2 
  * [asynchronous-notifications](http://initd.org/psycopg/docs/advanced.html#asynchronous-notifications)
  * [asynchronous-support](http://initd.org/psycopg/docs/advanced.html#asynchronous-support)
  * [connection.fileno](http://initd.org/psycopg/docs/connection.html#connection.fileno)

* SqlAlchemy
  * [zzzeek about async db](http://techspot.zzzeek.org/2015/02/15/asynchronous-python-and-databases/)
  * [contextual session](http://docs.sqlalchemy.org/en/latest/orm/contextual.html)
  * [session pooling](http://docs.sqlalchemy.org/en/latest/core/pooling.html)

* Python Asyncion and threads
  * [executor](https://docs.python.org/3/library/asyncio-eventloop.html#executor)
  * [thread pooling](https://docs.python.org/3/library/concurrent.futures.html)
  * [asyncio and threads example](http://stackoverflow.com/questions/28492103/how-to-combine-python-asyncio-with-threads) 