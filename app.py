# imports
from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
import pprint
import re

#create instances
app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'querier'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

#routing
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/api/getQueriesList', methods=['GET'])
def fetchQueryList():
    #fetch query list, send it as response
    cursor.execute("select querySeqID,queryName,inputParams from query;")
    result = cursor.fetchall()
    queryList=[]
    print(len(result))
    #return len(result)
    for i in range(len(result)):
        query = {
            "id":result[i][0],
            "name":result[i][1],
            "params":result[i][2]
        }
        queryList.append(query)

    print(queryList)
    return json.dumps({'queries': queryList })


@app.route('/api/executeQuery/<queryId>', methods=['POST'])
def executeQuery(queryId):
    #fetch query list, send it as response
    cursor.execute("select querySeqID,query,displayTitle from query where querySeqID = " + queryId + ";")
    queryResult = cursor.fetchone()
    print queryResult

    # read the posted values from the UI
    print request.form

    # substitute and execute queries
    query = queryResult[1]
    for key, value in request.form.iteritems():
        print key+' : '+value
        query = re.sub(key, value, query)
    
    cursor.execute(query)
    queryResponse = cursor.fetchall()

    # validate the received values
    if len(queryResponse):
        return json.dumps({'success': True, 'result': {
            'displayTitle': queryResult[2],
            'data': queryResponse
        }})
    else:
        return json.dumps({'success': False, 'error': 'Query execution failed, please check the parameters'})

#start
if __name__ == "__main__":
    app.run()
