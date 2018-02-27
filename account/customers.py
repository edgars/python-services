import ConfigParser
from flask import Flask, jsonify, request,MySQLdb
from flask_mysqldb import MySQL


mysql = MySQL()
application = Flask(__name__)
application.config['MYSQL_DATABASE_USER'] = 'admin_s4GK3rOB'
application.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
application.config['MYSQL_DATABASE_DB'] = 'mybank_eascorp'
application.config['MYSQL_DATABASE_HOST'] = 'mysql.storage.cloud.wso2.com'
mysql.init_app(application)

# Read config file
config = ConfigParser.ConfigParser()
config.read('bankDB.conf')

@application.route('/')
def users():
    # Open database connection with username= "root", password= "password" and database= "pythonTest"
    db = MySQLdb.connect("localhost", "root", "password", "pythonTest")

    # Prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Execute SQL query using execute() method.
    # Table: rooms with attributes "roomID"
    cursor.execute("SELECT roomID FROM rooms")

    # Fetch a single row using fetchone() method.
    data = cursor.fetchall()
    res = list(sum(data, ()))
    print (data)
    print(res)

    # Disconnect from server
    db.close()
    return res


@application.route('/product', methods=['POST'])
def createProduct():


    # fetch name and rate from the request
    rate = request.get_json()["rate"]
    name = request.get_json()["name"]
