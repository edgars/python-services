from flask import Flask, jsonify, request
import MySQLdb,json


app = Flask(__name__)

db = MySQLdb.connect(host="mysql.storage.cloud.wso2.com",  # your host
                     user="admin_s4GK3rOB",  # username
                     passwd="mysql",  # password
                     db="mybank_eascorp")  # name of the database

@app.route('/')
def home():
    # Create a Cursor object to execute queries.
    cur = db.cursor()

    cur.execute("SELECT * FROM mybank_eascorp.account")

    db.commit()

    print "Done"

    data = cur.fetchall()

    cur.close()

    return json.dumps(data)

@app.route('/accounts')
def accountsHome():
  # Create a Cursor object to execute queries.
    cur = db.cursor()

    result = cur.execute("SELECT account_ID,accountNumber,agency,customer_ID FROM mybank_eascorp.account")

    if (result<=0):
        response = app.response_class(
            response=json.dumps('not accounts found'),
            status=405,
            mimetype='application/json'
        )

    if (result > 0):
        accounts = cur.fetchall();
        accountsArray = []

        for account in accounts :
            context={}
            context['id']=           account[0]
            context['number'] =     account[1]
            context['agency'] =      account[2]
            context[ 'customerID'] = account[3]
            accountsArray.append(context)

    response = app.response_class(
        response=json.dumps(accountsArray),
        status=200,
        mimetype='application/json'
    )
    cur.close()

    return response

@app.route('/accounts/<accountId>')
def accountsHomeById(accountId):
  # Create a Cursor object to execute queries.
    cur = db.cursor()

    result = cur.execute("SELECT account_ID,accountNumber,agency,customer_ID FROM mybank_eascorp.account where account_ID="+ accountId)

    if (result<=0):
        response = app.response_class(
            response=json.dumps('not accounts found'),
            status=405,
            mimetype='application/json'
        )

    if (result > 0):
        accounts = cur.fetchall();
        accountsArray = []

        for account in accounts :
            context={}
            context['id']=           account[0]
            context['number'] =     account[1]
            context['agency'] =      account[2]
            context[ 'customerID'] = account[3]
            accountsArray.append(context)

    response = app.response_class(
        response=json.dumps(accountsArray),
        status=200,
        mimetype='application/json'
    )
    cur.close()

    return response


@app.route('/accounts', methods=['POST'])
def createAccount():

    # fetch name and rate from the request
    number = request.get_json()['number']
    agency = request.get_json()['agency']
    customerId = request.get_json()['customerID']

    cur = db.cursor()


    result = cur.execute('INSERT INTO account (accountNumber, agency, customer_ID) VALUES (%s,%s,%s)', (number,agency,customerId))

    if (result > 0):
        response = app.response_class(
            response=json.dumps('Inserted with sucessful '),
            status=200,
            mimetype='application/json'
        )

    db.commit()
    cur.close()

    return response

@app.route('/accounts/<accountId>', methods=['DELETE'])
def deleteAccount(accountId):

    payload = {};
    payload['msg'] = 'No response'
    payload[ 'method'] = "DELETE HTTP deleteAccount Account Microservice - ID " + accountId

    try:
        cur = db.cursor()
        result = cur.execute('DELETE from account where account_ID='+accountId )
        if (result > 0):
            payload['msg'] = 'Record % removed with sucessful',(accountId)
            payload['method'] = "DELETE HTTP deleteAccount Account Microservice - ID " + accountId
            db.commit()
    except:
        payload['msg'] = 'Error trying to remove the record ... '
        payload['method'] = "DELETE HTTP deleteAccount Account Microservice - ID " + accountId
    finally:
        cur.close()

    response = app.response_class(
        response=json.dumps(payload),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)