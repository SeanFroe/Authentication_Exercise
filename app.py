from flask import Flask, render_template, flash, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized


from models import db, connect_db, User, Feedback
from forms import AddUserForm, Loginform, DeleteForm, FeedbackForm



app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)




# #########################################################################
#----------------------------- Routes -------------------------------------

@app.route("/")
def root():
    """Homepage"""

    return redirect("/register")


#--------------------------- User Registration Routes ------------------------------------


@app.route('/register', methods=['GET', 'POST'])
def add_register():
    """ registers a user: produce form and handle form submission."""
    if "username" in session:
        return redirect(f"users/{session['username']}")

    form = AddUserForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user = User.register(**data)
        #user = User(username-form.username.data, password=password.password.data, ... )
        db.session.add(user)
        db.session.commit()
        flash(f"{user.username} added.")
        session['username'] = user.username
        return redirect(f"/users/{user.username}")

    else:    
        # re-present form for editing
        return render_template("users/register.html", form=form)
    
# ------------------------------- Login Form/logout ------------------------------------
    
@app.route('/login', methods=[ 'GET', 'POST'])
def login_user():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = Loginform()

    if form.validate_on_submit():
        data = {k: v for k,v in form.data.items() if k != "csrf_token"}
        user = User.authenticate(**data)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password/"]
            render_template("users/login.html", form=form)
    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")

# ------------------------------- Show User/ Delete User ------------------------------------

@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """ Remove user and redirect to login."""

    if "username" not in session or username!= session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.add(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")
        
# --------------------- User Feedback _________________________________________________

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """ Show add-feedback form, and process it."""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:
        return render_template("feedback/new.html", form=form)
        
# ----------------- User Feedback Update/Delete -------------------------------------------
    
@app.route("/feedback/<int:feedback_id>/update", methods={"GET","POST"})
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()

        return redirect(f"/user/{feedback.username}")
    
    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")


