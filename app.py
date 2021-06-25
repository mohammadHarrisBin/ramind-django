from datetime import datetime
import os
from flask import Flask,render_template,request,redirect,flash,Response,session
from flask_login.utils import logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, form
from wtforms.fields.core import BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired
import random
from flask_login import LoginManager,login_user, UserMixin, login_required



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskapp3?charset=utf8'
app.config['SQLACCHEMY_TRACK_MODIFICATION'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['UPLOAD_FOLDER'] = 'static/img/uploads/'
app.config['MAX_CONTENT_PATH'] = 200000

app.config.update(
    SECRET_KEY="My_Family_Is_Awesome"
)

csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)



#models
class People(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.Text,nullable=False)
    age = db.Column(db.Integer, nullable=False)
    race = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    gender = db.Column(db.String(100),nullable=False, default="Unavailable to specify")
    task = db.relationship('Task', backref='people', lazy=True)
    account_id_from = db.Column(db.Integer, nullable=False)
    help_requsted = db.Column(db.Boolean(), nullable=False, default=True)
    banner_img = db.Column(db.Text, nullable=True, default='rand1.jpg')
    def __repr__(self):
        return 'People '  + str(self.id)

def generate_code(users):
    users = users.query.all()
    char = [1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
    current_len = 0
    code = 'Ramind-'
    while current_len < 6:
        number = random.randrange(0,len(char) - 1)
        code += str(char[number])
        current_len += 1
    
    for user in users:
        if user.access_code == code:
            generate_code()
    return code


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.Text,nullable=False)
    description = db.Column(db.Text,nullable=True)
    people_jobs_id = db.Column(db.Integer,db.ForeignKey('people.id'),nullable=False)
    status= db.Column(db.Text, default='Incompleted')
    assigned_by = db.Column(db.Integer, nullable=False)
    needHelp = db.Column(db.Boolean(),nullable=False,default=False)
    reasonForHelp = db.Column(db.Text,nullable=True,default='')


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=False)
    password = db.Column(db.Text,nullable=False)
    AccountType = db.Column(db.Text,nullable=False,default='user')
    access_code = db.Column(db.Text,nullable=False)


    

def empty(string):
    if string == '':
        return True
    else:
        return False

#forms
class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired()],render_kw={'placeholder':'email...'})
    password = PasswordField('password',validators=[DataRequired()],render_kw={'placeholder':'password...'})

class RegisterForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()],render_kw={'placeholder':'name...'})
    email = StringField('email',validators=[DataRequired()],render_kw={'placeholder':'email...'})
    password = PasswordField('password',validators=[DataRequired()],render_kw={'placeholder':'password...'})
    r_password = PasswordField('password',validators=[DataRequired()],render_kw={'placeholder':'repeat password...'})
    tau = BooleanField('',validators=[DataRequired()],render_kw={})

class AccessCodeForm(FlaskForm):
    code = StringField('code',validators=[DataRequired()],render_kw={'placeholder':'code...', 'value' : 'Ramind-'})


#routes

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    """
     Status-> Empty, wrong 
    """
    status = ''
    if form.validate_on_submit():
      name = form.name.data
      email = form.email.data
      password = form.password.data
      r_password = form.r_password.data
      tau = form.tau.data
      accessCode = generate_code(Users)
    # if request.method == 'POST':
    #   name = request.form['name']
    #   email = request.form['email']
    #   password = request.form['password']
    #   r_password = request.form['r_password']
      if empty(name) or empty(email) or empty(password) or empty(r_password):
          status = "empty"
          return render_template('register.html',form=form,status=status)
      elif tau == False:
          errorMessage = "Please accept our terms and coniditons"
          return render_template('register.html',form=form,error=errorMessage)
      else:
          for user in Users.query.all():
              if user.email == email:
                  errorMessage = 'Sorry, the email is used already'
                  return render_template('register.html',form=form, error=errorMessage)

          if password == r_password:
                db.session.add(Users(name=name, email=email, password=generate_password_hash(password),access_code=accessCode))
                db.session.commit()
                successMessage = 'Account has been created for you!, Please Login'
                flash(successMessage)
                return redirect('/leader/login')
               
          elif password != r_password:
                errorMessage = "Sorry, the password does not match"
          return render_template('register.html',form=form,error=errorMessage)
    
    return render_template('register.html',form=form)



@app.route('/ask',methods=['GET','POST'])
def normPass():
    if request.method == 'POST':
        decision = request.form['decision']
        if decision == 'Leader🤴🏻':
            return redirect('/leader/login')
        elif decision == 'Follower👨‍👨‍👦‍👦':
            return redirect('/follower/login')
    return render_template('ask.html')


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_follower(follower_id):
    return People.query.get(int(follower_id))

@app.route('/follower/login',methods=['GET','POST'])
def follower_login():


    if session.get('CURRENT_USER_CODE'):
        return redirect('/follower/already_login')


    form=AccessCodeForm()
    
    if form.validate_on_submit():
        # follower = request.form['choose']
        code = form.code.data
        user = ''
        people = []
        
        for user in Users.query.all():
            if user.access_code == code:
                login_user(user)
                user = user
                people = People.query.filter(People.account_id_from == user.id)
                session['CURRENT_USER_CODE'] = code
                return render_template('loginFollower.html',form=form,code=code,peoples=people)
                

        if people == []:
            return render_template('wrongCode.html')

    else:
        return render_template('loginFollower.html', form=form)




login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_follower(follower_id):
    return Users.query.get(int(follower_id))


@app.route('/leader/login',methods=['POST','GET'])
def loginf():
    decision = 'leader'
    errorMessage = ''
    form = LoginForm()

    if form.validate_on_submit():
    
        email = form.email.data
        password = form.password.data
                
        for user in Users.query.all():
            if user.email == email and check_password_hash(user.password, password) == False:
                errorMessage = 'Your Email or Password is incorrect'
                return render_template('login.html',form=form,error=errorMessage,decision=decision)
            
            if user.email == email and check_password_hash(user.password, password):

                login_user(user)

                session['CURRENT_USER_EMAIL'] = str(user.email)
                session['CURRENT_USER_ID'] = str(user.id)
                session['CURRENT_USER_CODE'] = str(user.access_code)
                session['ACCOUNT_TYPE'] = 'leader'
        
        
                return redirect('/welcome')

    else:
       if session.get('CURRENT_USER_EMAIL'):
           return redirect('/already_login')
       else:
           return render_template('login.html',form=form,error=errorMessage,decision=decision)



@app.route('/welcome')
@login_required
def index():

    if session.get('CURRENT_USER_EMAIL'):        
        people = People.query.filter(People.account_id_from == session['CURRENT_USER_ID'])
        return render_template('index.html', everyone=people, Current_user_code = session['CURRENT_USER_CODE'])
        
    return redirect('/ask')
    





@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('CURRENT_USER_EMAIL',None)
    session.pop('CURRENT_USER_ID',None)
    session.pop('CURRENT_USER_CODE',None)
    session.pop('ACCOUNT_TYPE',None)
    logout_user()
    # if request.form['logout']:
    #     Current_user.pop()
    return redirect('/')


@app.route('/already_login')
@login_required
def logged_in_leader():
    typeA = 'leader'
    return render_template('already_logged.html', type=typeA)

@app.route('/follower/already_login')
@login_required
def logged_in_follower():
     typeA = 'follower'
     return render_template('already_logged.html',type=typeA)




app.config['IMAGE_UPLOADS'] = "C:/Users/65883/Desktop/flaskapp3 - Copy/static/img/uploads"
app.config['ALLOWED_IMG_EXTENSIONS'] = ['PNG','JPG','JPEG','GIF']

@app.route('/people/new',methods=['GET','POST'])
def new():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        race = request.form['race']
        occ = request.form['occ']
        status = request.form['status']
        category = request.form['category']
        other_category = request.form['others']
        gender = request.form['gender']

        # pic = request.files['avatar']
        account = session['CURRENT_USER_ID']
        if other_category == '':
            people = People(name=name, age=int(age), race=race,occupation=occ, status=status, category=category, gender=gender, account_id_from=account)
            db.session.add(people)
            db.session.commit()

        elif other_category != '':
            people = People(name=name, age=int(age), race=race,occupation=occ, status=status, category=other_category, gender=gender,account_id_from=account)
            db.session.add(people)
            db.session.commit()


        return redirect('/welcome')
    else:
         if session.get('CURRENT_USER_ID'):
            return render_template('new.html')
         else:
            return redirect('/leader/login')

# @app.route('/check_pic/<int:id>')
# def checkImage(id):
#     code = PeopleImages.query.get(id).img
    

@app.route('/people/delete/<int:id>',methods=['GET','POST'])
def delete(id):
    # return redirect('/welcome')
    if request.method == 'POST':
        if request.form['verify'] == 'YES':
            #people_jobs_id is related to the id of the follower
            tasks = Task.query.filter(Task.people_jobs_id == id)
            for task in tasks:
                db.session.delete(task)
            db.session.delete(People.query.get(id))
            # db.session.delete(opleImages.query.get(id))
            db.session.commit()
            return redirect('/welcome')
        elif request.form['verify'] == 'NO':
            return redirect('/welcome')
    else:
         people = People.query.get(id)
         return render_template('delete.html',people=people)

@app.route('/people/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    people = People.query.get(id)
    if request.method == 'POST':
        if request.form.get('name'):
            people.name = request.form['name']
            db.session.commit()
            return redirect(f'/people/edit/{id}')
            
        elif request.form.get('age'):
            people.age = request.form['age']
            db.session.commit()
            return redirect(f'/people/edit/{id}')
        
        elif request.form.get('occ'):
            people.occupation = request.form['occ']
            db.session.commit()
            return redirect(f'/people/edit/{id}')
        
        elif request.form.get('status'):
            people.status = request.form['status']
            db.session.commit()
            return redirect(f'/people/edit/{id}')
        
        elif request.form.get('category'):
            if request.form['others'] == '':
                people.category = request.form['category']
                db.session.commit()
                return redirect(f'/people/edit/{id}')
            elif request.form['others'] != '':
                people.category = request.form['others']
                db.session.commit()
                return redirect(f'/people/edit/{id}')


        elif request.form.get('gender'):
            people.gender = request.form['gender']
            db.session.commit()
            return redirect(f'/people/edit/{id}')

        elif request.form.get('race'):
            people.race = request.form['race']
            db.session.commit()
            return redirect(f'/people/edit/{id}')


        elif request.files['file']:
            file = request.files['file']
            fileName = secure_filename(file.filename)
            file.save( os.path.join( app.config['UPLOAD_FOLDER'] ,secure_filename(file.filename)))
            people.banner_img = fileName
            db.session.commit()
            return redirect(f'/people/edit/{id}')

        
        
    else:
        if session.get('CURRENT_USER_ID'):
            return render_template('edit.html',people=people, image=people.banner_img)
        else:
            return redirect('/leader/login')

        


@app.route('/task/new',methods=['POST','GET'])
def newtask():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        who = request.form['choose']
        assigned_by = session['CURRENT_USER_ID']
        
        if who == 'everyone':
            for follower in People.query.all():
                newTask = Task(title=title,description=desc,people_jobs_id=follower.id, assigned_by=assigned_by)
                db.session.add(newTask)
                db.session.commit()
            return redirect('/welcome')
                
        newTask = Task(title=title,description=desc,people_jobs_id=who, assigned_by=assigned_by)
        db.session.add(newTask)
        db.session.commit()
        return redirect('/welcome')
    else:
        if session.get('CURRENT_USER_ID'):
           people = People.query.filter(People.account_id_from == session['CURRENT_USER_ID'])
           return render_template('newTask.html',peoples=people)
        else:
            return redirect('/leader/login')

@app.route('/people/<int:id>/tasks/incompleted')
def getPost(id):
    icons = ['']
    typeTask = 'incompleted'
    className = ['button is-primary','button']
    people = People.query.get(id)
    currentUser = session['CURRENT_USER_ID']
    task = Task.query.filter(Task.people_jobs_id == id, Task.status=='incompleted', Task.assigned_by == currentUser)
    if session.get('CURRENT_USER_ID'):
        return render_template('getPost.html',currentUser = currentUser, Users=Users, typeTask=typeTask,className=className, people=people,tasks=task)
    else:
        return redirect('/leader/login')

# @app.route('/people/<int:id>/tasks/warning')
# def warning(id):
#     return str(id)

@app.route('/follower/tasks',methods=['POST','GET'])
def getfollowersAccount():
    if request.method == 'POST':
       follower_id = request.form['choose']# id of the follower

       if follower_id == "none":
           flash('Sorry, please select your account')
           session.pop('CURRENT_USER_CODE')
           return redirect('/follower/login')

       session['CURRENT_USER_ID'] = follower_id
       session['ACCOUNT_TYPE'] = 'follower'
       return redirect(f'/follower/tasks/{follower_id}')
    
    
    else:
        return redirect('/follower/login')
    



@app.route('/follower/tasks/<int:id>',methods=['POST','GET'])
def getfollowersProfileCompleted(id):
    if id:
        typeTask = 'completed'
        className = ['button is-primary','button']
        #get the people id to get the task via the people_jobs_id
        follower_id = id # id of the follower chosen
        followerTask = Task.query.filter(Task.people_jobs_id == follower_id, Task.status == 'Completed')
        follower = People.query.get(follower_id)
        # return followerTask[0].title
        return render_template('followerProfile.html', tasks=followerTask, people=follower, Users=Users,typeTask=typeTask,className=className)

    else:
        typeTask = 'completed'
        className = ['button is-primary','button']
        follower_id = id # id of the follower chosen
        followerTask = Task.query.filter(Task.people_jobs_id == follower_id, Task.status == 'Completed')
        follower = People.query.get(follower_id)        
        return render_template('followerProfile.html', tasks=followerTask, people=follower, Users=Users,typeTask=typeTask,className=className)


@app.route('/follower/tasks/<int:id>/incompleted',methods=['POST','GET'])
def getfollowersProfileInompleted(id):
        typeTask = 'incompleted'
        className = ['button is-primary','button']
        #get the people id to get the task via the people_jobs_id
        followerTask = Task.query.filter(Task.people_jobs_id == id, Task.status == 'Incompleted')
        follower = People.query.get(id)
        # return followerTask[0].title
        return render_template('followerProfile.html', tasks=followerTask, people=follower, Users=Users,typeTask=typeTask,className=className)


@app.route('/people/<int:id>/tasks/completed')
def getPostCompleted(id):
    icons = ['']
    typeTask = 'completed'
    className = ['button is-primary','button']
    people = People.query.get(id)
    currentUser = session['CURRENT_USER_ID']
    task = Task.query.filter(Task.people_jobs_id == id, Task.status=='completed', Task.assigned_by == currentUser)
    if session.get('CURRENT_USER_ID'):
        return render_template('getPost.html',Users=Users, typeTask=typeTask,className=className, people=people,tasks=task)
    else:
        return redirect('/leader/login')
    
@app.route('/people/<int:id>/tasks/finished',methods=['POST','GET'])
def finish(id):
    task = Task.query.get(id)
    task.status = "Completed"
    db.session.commit()
    return redirect(f'/people/{task.people_jobs_id}/tasks/completed')

@app.route('/follower/<int:id>/tasks/finished',methods=['POST','GET'])
def followers_finish_task(id):
    task = Task.query.get(id)
    task.status = "Completed"
    db.session.commit()
    return redirect(f'/follower/tasks/{task.people_jobs_id}')

@app.route('/people/<int:id>/tasks/restore',methods=['POST','GET'])
def restore(id):
    if not session.get('CURRENT_USER_ID'):
        return redirect('/ask')
    task = Task.query.get(id)
    task.status = "Incompleted"
    db.session.commit()
    return redirect(f'/people/{task.people_jobs_id}/tasks/incompleted')

@app.route('/follower/<int:id>/tasks/restore',methods=['POST','GET'])
def followers_restore_task(id):
    if not session.get('CURRENT_USER_ID'):
        return redirect('/ask')
    task = Task.query.get(id)
    task.status = "Incompleted"
    db.session.commit()
    return redirect(f'/follower/tasks/{task.people_jobs_id}/incompleted')

@app.route('/people/<int:id>/tasks/delete',methods=['POST','GET'])
def deleteTask(id):
    if not session.get('CURRENT_USER_ID'):
        return redirect('/ask')
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(f'/people/{task.people_jobs_id}/tasks/completed')

@app.route('/follower/<int:id>/tasks/help',methods=['GET','POST'])
def helpTask(id):
    if not session.get('CURRENT_USER_ID'):
        return redirect('/ask')
    task = Task.query.get(id)
    help = task.needHelp
    follower = task.people_jobs_id
    if help == False:
        task.needHelp = True
        db.session.commit()
        return redirect(f'/follower/tasks/{follower}/incompleted')
    elif help == True:
        task.needHelp = False
        task.reasonForHelp = ''
        db.session.commit()
        return redirect(f'/follower/tasks/{follower}/incompleted')

    # return redirect(f'/follower/tasks/{id}/incompleted')
    #  task = Task.query.get(id)
    #  db.session.delete(task)
    #  db.session.commit()
    #  return redirect(f'/people/{task.people_jobs_id}/tasks/completed')

@app.route('/reason/<int:id>',methods=['GET','POST'])
def reason(id):
    if not session.get('CURRENT_USER_ID'):
        return redirect('/ask')
    task = Task.query.get(id)
    reason = request.form['reason']
    task.reasonForHelp  = str(reason)
    db.session.commit()
    follower = task.people_jobs_id
    return redirect(f'/follower/tasks/{follower}/incompleted')



@app.route('/Terms&Conditions')
def tos():
    return render_template('tos.html')


@app.route('/people/family')
def familyPage():
    pass


@app.route('/profile/<int:id>',methods=['POST','GET'])
def profile_page(id):
    user = Users.query.get(int(session['CURRENT_USER_ID']))
    followers = People.query.filter(People.account_id_from == id).count()
    tasks = Task.query.filter(Task.assigned_by == id).count()

    if request.method == 'POST':
        if request.form.get('name'):
            user.name = request.form.get('name')
        elif request.form.get('email'):
            user.email = request.form.get('email')
        db.session.commit()
        return redirect(f"/profile/{int(session['CURRENT_USER_ID'])}")


    return render_template('profile.html',people=user, followers=str(followers), tasks=tasks )


if __name__ == "__main__":
    app.run(debug=True)







