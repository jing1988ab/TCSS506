from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wiki import findBirths
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel


class loginForm(FlaskForm):
    username=StringField(label="Enter username",validators=[DataRequired(), Length(min=6,max=20)])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=8)])
    submit=SubmitField(label="Login")

class registerForm(FlaskForm):
    username=StringField(label="Enter username",validators=[DataRequired(), Length(min=6,max=20)])
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=8)])
    submit=SubmitField(label="Register")

DBUSER= 'lhhung'
DBPASS= 'password'
DBHOST= 'db'
DBPORT= '5432'
DBNAME= 'pglogindb'

app = Flask(__name__)
app.secret_key="a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
    user=DBUSER,
    passwd=DBPASS,
    host=DBHOST,
    port=DBPORT,
    db=DBNAME
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

def addUser(email, username, password):
    #check if email or username exits
    user=UserModel()
    user.set_password(password)
    user.email=email
    user.username=username
    db.session.add(user)
    db.session.commit()


@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email = "lhhung@uw.edu").first()
    if user is None:
        addUser("lhhung@uw.edu","lhhung", "qwerty")    
    
@app.route("/home",methods=['GET','POST'])
@login_required
def findBirthday():
    if request.method == "POST":
        myDate=request.form["date1"]
        form_value_array = myDate.split('-')
        if len(form_value_array)!=3:
            return render_template("home.html")
        monthinput = form_value_array[1]+'/'+form_value_array[2]
        yearinput = form_value_array[0]
        sizeinput=request.form["size"]
        if int(sizeinput)< 1 or int(sizeinput) > 20:
            print("herer")
            return render_template("home.html")
        if monthinput and yearinput and sizeinput:
            return render_template("home.html", myData=findBirths(monthinput,yearinput,sizeinput))
    return render_template("home.html")

@app.route("/")
def redirectToLogin():
    return redirect("/login")

@app.route("/login",methods=['GET','POST'])
def login():
    msg = ""
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username=request.form["username"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(username = username).first()
            if user is not None and user.check_password(pw) :
                login_user(user)
                return redirect('/home')
            else:
                msg = "Please enter correct login details or register"
    return render_template("login.html",form=form,msg=msg)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/register",methods=['GET','POST'])
def register():
    form=registerForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            username=request.form["username"]
            pw=request.form["password"]
            user = UserModel.query.filter_by(email = email).first()
            print(user)
            if user is not None:
                flash("User already exist. Please login!")
                return redirect('/login')
            # elif user is not None and not user.check_password(pw) :
            #     return redirect('/login')
            else:
                pw = str(pw)
                addUser(email, username, pw)
                flash("Register success. Please login!")
                return redirect('/login')
            
    return render_template("register.html",form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
