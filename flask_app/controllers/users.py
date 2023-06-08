from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app.models.address import Address
from flask_app.models.pet import Pet

bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument
@app.route('/')
def index():
    return render_template("landing.html")


@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template('register.html')

#   CREATE A USER WITH ADDRESS

@app.route('/users/create',methods=['POST'])
def create_user():
    print(request.form)
    
    if(User.validate(request.form)):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data1 = {
            **request.form
        }
        address_id = Address.create_address(data1)
        data2 = {
            **request.form,
            'password': pw_hash,
            'address_id' : address_id
        }
        user_id = User.create_user(data2)
        session['user_id'] = user_id
        return redirect('/dashboard')
    return redirect('/register')

#   SHOW FORM ADD PET

@app.route('/users/pet/show')
def show_add_pet():
    return render_template('petcreation.html')

#  CREATE A PET IN THE DB

@app.route('/users/pet/create', methods=['POST'])
def add_pet():
    data = {
        **request.form,
        "user_id" : session['user_id']
    }
    pet_id = Pet.create_pet(data)
    session['pet_id'] = pet_id
    return redirect('/dashboard')

@app.route('/users/pet/update', methods=['POST'])
def edit_pet():
    data = {
        **request.form,
        'id' : session['pet_id']
    }
    Pet.delete_pet(data)
    return redirect('/users/profile')

#  DELETE PET 

@app.route('/users/pet/destroy', methods=['POST'])
def remove_pet():
    data = {
        "id" : session['pet_id']
    }
    Pet.delete_pet(data)
    return redirect('/users/profile')

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    # user = User.get_by_id({'id':session['user_id']})
    return render_template("dashboard.html")


@app.route('/users/login', methods=['POST'])
def login():
    user_from_db = User.get_by_email({'email':request.form['email']})
    if(user_from_db):
        # check password
        if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        # if we get False after checking the password
            flash("Invalid Password")
            return redirect('/')
        session['user_id'] = user_from_db.id
        return redirect('/dashboard')
    flash("Invalid Email")
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')