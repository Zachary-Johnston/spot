# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists Users;")
# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists newsupdates;")
# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists ready;")

cursor.execute("drop table if exists visits;")



1. id (autoincrementing primary key -- so each row is unique)
1. session_id  (of the user visiting the route)
2. route_name  (could also be the URL if you prefer)
3. timestamp (when the user visited the route)




# CREATED VISITS TABLE
try:
  cursor.execute("""
    CREATE TABLE visits (
      id integer  AUTO_INCREMENT PRIMARY KEY,
      session_id  VARCHAR(50) NOT NULL,
      route_name   VARCHAR(50) NOT NULL,
      timestamp       VARCHAR(50) NOT NULL
    );
  """)
except:
  print("Table already exists. Not recreating it.")

# Insert Records into visits
query = "insert into visits (session_id, route_name, timestamp) values (%s, %s, %s)"
values = [
  ('session id of user visiting the route','name of route','timestamp'),
]
cursor.executemany(query, values)
db.commit()


# CREATED USERS TABLE
try:
  cursor.execute("""
    CREATE TABLE Users (
      id integer  AUTO_INCREMENT PRIMARY KEY,
      Email  VARCHAR(50) NOT NULL,
      Password   VARCHAR(50) NOT NULL,
      Status       VARCHAR(50) NOT NULL
    );
  """)
except:
  print("Table already exists. Not recreating it.")

# Insert Records into Users
query = "insert into Users (Email, Password, Status) values (%s, %s, %s)"
values = [
  ('jesi@ucsd.edu','Jesi','Valid'),
  ('jesus@ucsd.edu','Jesus','Pending'),
  ('zack@ucsd.edu','Zack','Pending'),
  ('john@ucsd.edu','John','Pending'),
]
cursor.executemany(query, values)
db.commit()


#NEWS UPDATES TABLE
try:
 cursor.execute("""
   CREATE TABLE newsupdates (
     id integer  AUTO_INCREMENT PRIMARY KEY,
     title VARCHAR(100) NOT NULL,
     release_time VARCHAR(100) NOT NULL,
     description    VARCHAR(100) NOT NULL
   );
 """)
except:
 print("Table already exists. Not recreating it.")
 
# Insert Records into newsupdates
query = "insert into newsupdates (title, release_time, description) values (%s, %s, %s)"
values = [
 ('Prototype Completed', 'May 15, 2020', 'All hardware is functional.'),
 ('Taste Quality Improvements','May 20, 2020','Taste is 100% safe and neutral!'),
]
cursor.executemany(query, values)
db.commit()




try:
 cursor.execute("""
   CREATE TABLE cofset (
     id integer  AUTO_INCREMENT PRIMARY KEY,
     coffeeid VARCHAR(50) NOT NULL,
     temperature VARCHAR(50) NOT NULL,
     time    VARCHAR(50) NOT NULL
   );
 """)
except:
 print("Table already exists. Not recreating it.")
 
# Insert Records into cofset
query = "insert into cofset (coffeeid, temperature, time) values (%s, %s, %s)"
values = [
 ('someid', 'sometemp', 'sometime'),
]
cursor.executemany(query, values)
db.commit()


#readiness metric
try:
 cursor.execute("""
   CREATE TABLE ready (
     id integer  AUTO_INCREMENT PRIMARY KEY,
     days VARCHAR(50) NOT NULL,
     howsoon VARCHAR(50) NOT NULL
   );
 """)
except:
 print("Table already exists. Not recreating it.")
 
# Insert days into readiness
query = "insert into ready (days, howsoon) values (%s, %s)"
values = [
 ('24', 'soon'),
 ('23', 'soon'),
 ('22', 'soon'),
 ('21', 'soon'),
 ('20', 'soon'),
 ('19', 'soon'),
 ('18', 'soon'),
 ('17', 'soon'),
 ('16', 'soon'),
 ('15', 'soon'),
 ('14', 'soon'),
 ('13', 'soon'),
 ('12', 'soon'),
 ('11', 'soon'),
 ('10', 'soon'),
 ('9', 'very soon'),
 ('8', 'very soon'),
 ('7', 'very soon'),
 ('6', 'very soon'),
 ('5', 'very soon'),
 ('4', 'very soon'),
 ('3', 'very soon'),
 ('2', 'very soon'),
 ('1', 'very soon'),
]
cursor.executemany(query, values)
db.commit()



# Selecting Records
cursor.execute("select * from Users;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from cofset;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from newsupdates;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from ready;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

db.close()
