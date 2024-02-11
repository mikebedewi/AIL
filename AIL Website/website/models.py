import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ail2024",
  database="mydb"
)

mycursor = mydb.cursor()

