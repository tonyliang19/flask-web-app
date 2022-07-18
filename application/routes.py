# This serves as file that stores every route to each sub link

from application import app, api, db
from flask import render_template, request, redirect, flash, url_for, session, jsonify
from application.course_list import course_list
from application.forms import LoginForm, RegisterForm
from application.models import User, Course, Enrollment
from flask_restx import Resource
from application.course_list import course_list

# API
#################
@api.route("/api", "/api/")
class GetAndPost(Resource):
    # GET all, fetches all data
    def get(self):
        return jsonify(User.objects.all())

    # POST (create or insert data)
    def post(self):
        data = api.payload
        user = User(user_id=data["user_id"], email=data["email"], 
        first_name=data["first_name"], last_name=data["last_name"])
        user.set_password(data["password"])
        user.save()
        return jsonify(User.objects(user_id=data["user_id"]))

@api.route("/api/<idx>")
class GetUpdateDelete(Resource):
    # GET one, fetches single data by id /<id>
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))
    # PUT
    def put(self, idx):
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))
    
    # DELETE
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted!")


#################


# Making the route for home page
@app.route("/")
@app.route("/index")
@app.route("/home")
# These functions returns html

# Make sure the "xxx.html" is inside the templates folder
# These parameters can be passed to jinja and its html

# eg. {% if param%}
#     // 
#     {% else %}
#     //
#     {% endif %} 

# Use url_for("function_name")
# url_for("index")
# url_for("courses")

# function_name = True to highlight active 
# index = True
def index():
    #ses = session.get("username")
    return render_template("index.html", index=True)

@app.route("/register", methods=['POST','GET'])
def register():
    if session.get("username"):
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id     = User.objects.count()
        user_id     += 1

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data
        # Creates the model User to be store to db
        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form, register=True)


@app.route("/login", methods=['GET','POST'])
def login():
    # When user already loggon, redirect to home page
    if session.get("username"):
        return redirect(url_for("index"))
    form = LoginForm()
    # if form has no errors
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data
        # This user is from the database
        user = User.objects(email=email).first()
        if user and user.get_password(password):
        # These prints to the page
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session["user_id"] = user.user_id
            session["username"] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True )

@app.route("/logout")
def logout():
    #session["user_id"]=False
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/courses/")
# "/base_pattern/<variable>"
# use <variable> as user want to change urls to display different links
# and dont forget to use it in its corresponding html {{ variable }}
# and pass this arg in the function definition
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "Summer 2022"
    
    classes = Course.objects.order_by("+courseID")
    
    return render_template("courses.html", courseData=classes, courses=True, term=term)


@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    # For GET request.args.get or request.args["dict_key"]
    # id = request.args.get("courseID")
    # title = request.args.get("title")
    # term = request.args.get("term")
    
    # For POST request.form.get
    #id = request.form.get("courseID")
    #title = request.form.get("title")
    
    # if not signed in redirect user to login page
    if not session.get("username"):
        return redirect(url_for("login"))

    courseID = request.form.get("courseID")
    courseTitle = request.form.get("title")
    user_id = session.get("user_id")
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops! You are already registered in this course {courseTitle}!", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")
    
    course_list = course_list()
    return render_template("enrollment.html", enrollment=True,  title="Enrollment",
    classes=classes)

# route for user
@app.route("/user")
def user():
    # .save() requires in order to be properly saved
    # User(user_id=1, first_name="Tony", last_name="Liang", email="chunqingliang@gmail.com", 
    # password="1234").save()

    # Get variable back from the db to template
    users = User.objects.all()
    return render_template("user.html", users=users)

