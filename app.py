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

# conn = mysql.connect()
# cursor = conn.cursor()

#routing
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/api/getQueriesList',methods=['GET'])
def fetchQueryList():
    #fetch query list, send it as response
    ''' cursor.execute("select querySeqID,queryName,inputParams from query;")
    result = cursor.fetchall()
    k=[]
    print(len(result))
    return len(result)
    for i in range(0,len(result)-1):
        print i
        j={"id":result[i][0],"name":result[i][1],"params":result[i][2]}
        k.append(j)
        print(k)
    ''' 
    return json.dumps({'queries': [{
            'id': 1,
            'name': 'Query 1',
            'params': 'Params1;Params2;Params3'
        }, {
            'id': 2,
            'name': 'Query 2',
            'params': 'Params1'
        }, {
            'id': 3,
            'name': 'Query 3',
            'params': 'Params1;Params2'
        }]
    })


@app.route('/api/executeQuery',methods=['POST'])
def executeQuery():
    #fetch query list, send it as response
    ''' cursor.execute("select querySeqID,query,displayTitle from query;")
    result = cursor.fetchall() '''

    # read the posted values from the UI
    print request.form

    # substitute and execute queries
    query = 'Select empCode, empName, empSalary from EmpTab where empSalary > Params1 and DateOfJoin > Params2'
    for key, value in request.form.iteritems():
        print key+' : '+value
        query = re.sub(key, value, query)
    
    print query
    ''' cursor.execute(query)
    result = cursor.fetchall()
    return result '''

    # validate the received values
    success = True
    if success:
        return json.dumps({'success': True, 'result': {
            'displayTitle': 'Title1;Title2;Title3',
            'data': [[1, 'Emp1', 5000], [2, 'Emp2', 15000], [3, 'Emp3', 10000]]
        }})
    else:
        return json.dumps({'success': False, 'error': 'Query execution failed, please check the parameters'})

#start
if __name__ == "__main__":
    # cursor.execute("select * from employee")
    # result = cursor.fetchall()
    app.run()

