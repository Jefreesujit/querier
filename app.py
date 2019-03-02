# imports
from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

#create instances
app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'querier'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#conn = mysql.connect()
#cursor = conn.cursor()

#routing
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/api/getQueriesList',methods=['GET'])
def fetchQueryList():
    #fetch query list, send it as response
    return json.dumps({'queries': [] })

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
    app.run()

