from macpath import split
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import sqlite3
import os
currentdirectory =os.path.dirname(os.path.abspath(__file__))
 


app = Flask(__name__)


# stores the uploaded file in static folder
app.config["UPLOADS_FOLDER"] = "templates/"

# after Starting the apllications render the index.html page 
@app.route('/')
def upload_file():
    return render_template('home.html')

#  renders to annoting.html page  
@app.route('/display', methods = ['GET', 'POST'])
def display_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOADS_FOLDER'] + filename)
        file = open(app.config['UPLOADS_FOLDER'] + filename,"r")
        content = file.read()          
    return render_template('process.html', content=content)    

@app.route('/savedata', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        cdata = request.form['contentvalue']     
        adata = request.form['anotatedata']  
        anotateary = adata.split(";");    
        index = 0
        listarray = []
        for data in anotateary:
            if(data != ""):
                valueary =  data.split(",")
                for value in valueary:
                    listarray.append(value)

                type = listarray[index]
                word = listarray[index + 1]
                indices = listarray[index + 2]

                connection = sqlite3.connect(currentdirectory +"\demo.db")
                cursor = connection.cursor()
                query2 ="INSERT INTO Document(content) VALUES(""'{content}'"")".format(content = cdata)
                query3 = "INSERT INTO Annot VALUES('{typ}',""'{text}'"",'{stidx}')".format(typ = type,text =word,stidx = indices )
                cursor.execute(query2)
                cursor.execute(query3)

                connection.commit()
                index += 3
 
        return render_template('home.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug = True)
