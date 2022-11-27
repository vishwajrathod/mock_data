
from flask import Flask,jsonify,render_template,request
import pickle
import json
import config
import numpy as np
from flaskext.mysql import MySQL

app = Flask(__name__)

# MySQL configuration step
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vishwaj123'
app.config['MYSQL_DB'] = 'IRIS_DATABASE'
mysql = MySQL()
mysql.init_app(app)

with open(config.MODEL_FILE_PATH,'rb') as file:
    model = pickle.load(file)
with open(config.JSON_FILE_PATH,'r') as file:
    json_data = json.load(file)

# home API
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods = ["GET","POST"])
def predict():
    data = request.form
    test_array = np.zeros(4)
    test_array[0] = eval(data['sepal length (cm)'])
    a = test_array[0]
    test_array[1] = eval(data['sepal width (cm)'])
    b = test_array[1]
    test_array[2] = eval(data['petal length (cm)'])
    c = test_array[2]
    test_array[3] = eval(data['petal width (cm)'])
    d = test_array[3]

    z = model.predict([test_array])
    z1 = np.round(z[0])

    cursor = mysql.get_db().cursor()
    query = 'CREATE TABLE IF NOT EXISTS Iris_data(sepal length (cm) VARCHAR(10), sepal width (cm) VARCHAR(10), petal length (cm) VARCHAR(10), petal width (cm) VARCHAR(10), target VARCHAR(10))'
    cursor.execute(query)
    cursor.execute('INSERT INTO Iris_data (sepal length (cm),sepal width (cm),petal length (cm),petal width (cm),target) VALUES (%s,%s,%s,%s,%s)',(a,b,c,d,z1))
    mysql.get_db().commit()
    cursor.close()

    return render_template("index1.html",z1=z1)


if __name__ =="__main__":
    app.run(host="0.0.0.0",port=config.PORT_NUMBER)










# Hot to create cursor in flaskext
# from flaskext.mysql import MySQL
# mysql = MySQL()
# mysql.init_app(app)
# cursor = mysql.get_db().cursor()