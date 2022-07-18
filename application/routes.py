# This serves as file that stores every route to each sub link

from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for
from application.forms import LoginForm, RegisterForm
from application.models import User, Course, Enrollment


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
    return render_template("index.html", index=True)

@app.route("/register", methods=['POST','GET'])
def register():
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
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True )


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
    
    courseID = request.form.get("courseID")
    courseTitle = request.form.get("title")
    user_id = 1
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops! You are already registered in this course {courseTitle}!", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")
    classes = None
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

# @app.route("/api")
# @app.route("/api/<idx>")
# def api(idx=None):
#     # If no index provided, returns all data instead
#     if(idx == None):
#         jdata = courseData
#     else:
#         jdata = courseData[int(idx)]

#     return Response(json.dumps(jdata), mimetype="application/json")