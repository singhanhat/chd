from typing import Counter
from flask import Flask, render_template, url_for,request, flash, redirect,session

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add_area', methods=["post"])
def add_area():
    length=request.form.get("length", type=int)
    width=request.form.get("width", type=int)
    distance=request.form.get("dis", type=int)
    area=(length)*(width)
    capacity=area//((distance)*(distance))
    session["capacity"]=capacity
    session ["area"]=area
    session["counter"]=0
    print (capacity)
    return render_template("cover.html",show_add=isnext_allowed(session))

def isnext_allowed(session):
    counter=session.get("counter",0)
    show_add=False
    capacity=session.get("capacity",0)
    if counter<capacity:
        show_add=True
    return show_add    

def isprevious_allowed(session):
    counter=session.get("counter",0)
    show_sub=False
    capacity=session.get("capacity",0)
    if counter>0:
        show_sub=True
    return show_sub   

@app.route("/reset")
def reset():
    session.pop("counter", 0)
    return redirect("/home")


@app.route('/social_distancing')
def social_distancing():
    return render_template("social.html")


@app.route('/home', methods=["get", "post"])
def home():
    return render_template("cover.html", show_sub=isprevious_allowed(session), show_add=isnext_allowed(session))

    
        

@app.route('/distancing_add',methods=["GET","POST"])
def distancing():
    print("inside distancing")
    if request.method=="GET":
        return render_template("social.html")
    else:
        print("insode else")
        visitors=request.form.get("more",0)#2
    
        visitors=int(visitors)
        print(visitors,"visitors")
        capacity=session.get("capacity",0)#10 unit in sqm
        counter=session.get("counter",0)
        print("earlier counter",counter)
        counter+=visitors

        if counter<=capacity:
            session["counter"]=counter
            print(counter,6)
            return redirect("/home")

        else:
            return render_template("error.html",message="This operation could not be processed ")

@app.route('/distancing_sub',methods=["GET","POST"])
def distancin():
    print("inside distancing")
    if request.method=="GET":
        return render_template("subtract.html")
    else:
        visitors=request.form.get("more",0)#2
    
        visitors=int(visitors)
        print(visitors,"visitors")
        capacity=session.get("capacity",0)#10 unit in sqm
        counter=session.get("counter",0)
        print("earlier counter",counter)
        counter-=visitors

        if counter<=capacity and counter>0:
            session["counter"]=counter
            print(counter,6)
            return redirect("/home")
            

        elif counter<0:
            return render_template("error.html",message="Minimum capacity exceeded ")        

        else:
            return render_template("error.html",message="This operation could not be processed ")        

def number_of_people_tobe_added(session):
    capacity=session.get('capacity',0)
    counter=session.get("counter",0)
    return capacity-counter

def number_of_people_tobe_removed(session):
    counter=session.get("counter",0)
    return counter




if __name__ == '__main__':
    app.run(debug=True)


