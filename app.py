from flask import Flask,render_template,request
import sqlite3
import os 

name=''
email=''
currentdirectory = os.path.dirname(os.path.abspath(__file__))
foodz=[
    ('Paratha and Egg Curry','50','../static/images/food/paratha.jpg'),
    ('Fried Rice','70','../static/images/food/fried_rice.jpg'),
    ('Idli','30','../static/images/food/idli.jpg'),
    ('Masala dosa','40','../static/images/food/masala_dosa.jpg'),
    ('Veg fried maggi','12.99','../static/images/food/maggie.jpg')  
]

juicesz=[
     ('Strawberry','40','../static/images/juices/straw.jpg'),
    ('Watermelon','30','../static/images/juices/watermelon.png'),
    ('Mango','50','../static/images/juices/man.jpg'),
    ('Raspberry','35','../static/images/juices/rasp.png'),
    ('Mosambi','30','../static/images/juices/mosam.jpg')  
]

icez=[
     ('Strawberry','22','../static/images/icecream/strawbe.png'),
    ('Chocolate','22','../static/images/icecream/choco.png'),
    ('Butterscotch','22','../static/images/icecream/butter.jpg'),
    ('Blackcurrant','22','../static/images/icecream/bcurrant.jpg'),
    ('Vanilla','22','../static/images/icecream/vanilla.jpg')  
]


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("sign_up.html")

@app.route("/", methods=["POST"])
def show_index():
    connection=sqlite3.connect(currentdirectory+"\database.db")
    c=connection.cursor()
    t=[]
    global name
    name=request.form["name"]
    global email
    email=request.form["email"]
    print(name,email)
    command= "INSERT INTO datas(name,email,current_orders,past_orders) VALUES ('{name}','{email}','NULL','NULL')".format(name=name,email=email)
    c.execute(command)
    connection.commit()
    c.close()
    connection.close()
    return render_template("index.html", name=name, orders=t)
@app.route("/food")
def show_food():
    return render_template("food.html",food=foodz)


@app.route("/juices",  methods=["POST"])
def proces_food():
    toAdd = request.form["submit"]
    print('toadd', toAdd)
    connection=sqlite3.connect(currentdirectory+"\database.db")
    c=connection.cursor()
    print(email)
    c.execute("""SELECT current_orders from datas WHERE email=?""", (email,))
    
    curOrder=c.fetchone()[0]
    if curOrder=='NULL':
        curOrder= toAdd
    else:
        curOrder = curOrder+','+toAdd

    t=curOrder.split(',')
    print(t)
    c.execute("UPDATE datas SET current_orders=? WHERE email=?",(curOrder,email))
    connection.commit()
    return render_template("index.html",name=name,orders=t)


@app.route("/juices")
def show_juices():
    return render_template("juice.html",food=juicesz, name=name)


@app.route("/icecream")
def show_icecream():
    return render_template("ice.html",food=icez)



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')