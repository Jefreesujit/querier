# imports
from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
import pprint
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

@app.route('/api/getQueriesList',methods=['GET'])
def fetchQueryList():
    #fetch query list, send it as response
    cursor.execute("select querySeqID,queryName,inputParams from query;")
    result = cursor.fetchall()
    k=[]
    print(len(result))
    return len(result)
'''    for i in range(0,len(result)-1):
        print i
        j={"id":result[i][0],"name":result[i][1],"params":result[i][2]}
        k.append(j)
        print(k)'''
        
 
@app.route('/api/executeQuery',methods=['POST'])
def executeQuery():
    #fetch query list, send it as response
    # read the posted values from the UI
    param1 = request.form['param1']
    param2 = request.form['param2']
 
    # substitute and execute queries
    success = True
    # validate the received values
    if success:
        return json.dumps({'success': True, 'response': []})
    else:
        return json.dumps({'success': False, 'error': 'Query execution failed, please check the parameters'})

#start
if __name__ == "__main__":
    cursor.execute("select * from employee");
    result = cursor.fetchall()
    app.run(host="0.0.0.0",port="12345")

