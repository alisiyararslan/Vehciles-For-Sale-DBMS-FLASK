from email import message
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
#from models import Img
from werkzeug.utils import secure_filename
import os

# User Login Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "logged_in" in session:
            return f(*args,**kwargs)
        else:
            flash("Please login to view this page.","danger")
            return redirect(url_for("login")) 
        
    return decorated_function

#user registration form
class RegisterForm(Form):
    name=StringField("Name: ",validators=[validators.DataRequired(message="Please set a name"),validators.Length(min=3,max=35)])#
    username=StringField("Username: ",validators=[validators.DataRequired(message="Please set a username"),validators.Length(min=3,max=35)])
    phone_number=StringField("Phone number: ",validators=[validators.DataRequired(message="Please set a phone number"),validators.Length(min=3,max=35)])#
    email=StringField("Email: ",validators=[validators.DataRequired(message="Please set a email"),validators.Email(message="Please enter a valid email address...")])#
    password=PasswordField("Password: ",validators=[
        validators.DataRequired(message="Please set a password"),
        validators.EqualTo(fieldname="confirm",message="Your Password Doesn't Match..."),
    ])
    confirm=PasswordField("Confirm the password: ",validators=[validators.DataRequired(message="Please set a confirm")])

class LoginForm(Form):
    username=StringField("Username: ",validators=[validators.DataRequired()])
    password=PasswordField("Password: ",validators=[validators.DataRequired(message='dfds')])



class OtomobileForm(Form):#makes form handling easy and structured and ensures the effective handling of form rendering, validation, and security. 
    title=StringField("Title: ",validators=[validators.DataRequired()])
    price=StringField("Price: ",validators=[validators.DataRequired()])
    brand=StringField("Brand: ",validators=[validators.DataRequired()])
    series=StringField("Series: ",validators=[validators.DataRequired()])
    model=StringField("Model: ",validators=[validators.DataRequired()])
    year=StringField("Year: ",validators=[validators.DataRequired()])
    fuel=StringField("Fuel: ",validators=[validators.DataRequired()])
    gear=StringField("Gear: ",validators=[validators.DataRequired()])
    color=StringField("Color: ",validators=[validators.DataRequired()])
    km=StringField("Km: ",validators=[validators.DataRequired()])
    body_type=StringField("Body Type: ",validators=[validators.DataRequired()])
    engine_power=StringField("Engine Power: ",validators=[validators.DataRequired()])
    engine_volume=StringField("Engine Volume: ",validators=[validators.DataRequired()])
    traction=StringField("Traction: ",validators=[validators.DataRequired()])
    city=StringField("City: ",validators=[validators.DataRequired()])
    district=StringField("District: ",validators=[validators.DataRequired()])
    description=TextAreaField("Advert Description: ",validators=[validators.DataRequired()])


class MotorcycleForm(Form):#makes form handling easy and structured and ensures the effective handling of form rendering, validation, and security.
    title=StringField("Title: ",validators=[validators.DataRequired()])
    price=StringField("Price: ",validators=[validators.DataRequired()])
    brand=StringField("Brand: ",validators=[validators.DataRequired()])
    type=StringField("Type: ",validators=[validators.DataRequired()])
    model=StringField("Model: ",validators=[validators.DataRequired()])
    year=StringField("Year: ",validators=[validators.DataRequired()])
    gear=StringField("Gear: ",validators=[validators.DataRequired()])
    color=StringField("Color: ",validators=[validators.DataRequired()])
    km=StringField("Km: ",validators=[validators.DataRequired()])
    engine_power=StringField("Engine Power: ",validators=[validators.DataRequired()])
    engine_volume=StringField("Engine Volume: ",validators=[validators.DataRequired()])
    city=StringField("City: ",validators=[validators.DataRequired()])
    district=StringField("District: ",validators=[validators.DataRequired()])
    description=TextAreaField("Advert Description: ",validators=[validators.DataRequired()])

class WatercraftForm(Form):#makes form handling easy and structured and ensures the effective handling of form rendering, validation, and security.
    title=StringField("Title: ",validators=[validators.DataRequired()])
    price=StringField("Price: ",validators=[validators.DataRequired()])
    type=StringField("Type: ",validators=[validators.DataRequired()])
    length=StringField("Length: ",validators=[validators.DataRequired()])
    width=StringField("Width: ",validators=[validators.DataRequired()])
    year=StringField("Year: ",validators=[validators.DataRequired()])
    color=StringField("Color: ",validators=[validators.DataRequired()])
    city=StringField("City: ",validators=[validators.DataRequired()])
    district=StringField("District: ",validators=[validators.DataRequired()])
    description=TextAreaField("Advert Description: ",validators=[validators.DataRequired()])

class AircraftForm(Form):#makes form handling easy and structured and ensures the effective handling of form rendering, validation, and security.
    title=StringField("Title: ",validators=[validators.DataRequired()])
    price=StringField("Price: ",validators=[validators.DataRequired()])
    type=StringField("Type: ",validators=[validators.DataRequired()])
    width=StringField("Width: ",validators=[validators.DataRequired()])
    year=StringField("Year: ",validators=[validators.DataRequired()])
    color=StringField("Color: ",validators=[validators.DataRequired()])
    max_altitude=StringField("Max Altitude: ",validators=[validators.DataRequired()])
    city=StringField("City: ",validators=[validators.DataRequired()])
    district=StringField("District: ",validators=[validators.DataRequired()])
    description=TextAreaField("Advert Description: ",validators=[validators.DataRequired()])


app=Flask(__name__,static_folder='C:/Users/siyar/OneDrive/Masaüstü/DBMSPROJECT/templates')#

app.secret_key= "dbmsproject"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'Images'

#Mysql Configuration with Flask
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="dbmsproject"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
app.config['UPLOAD_FOLDER'] = "templates\Images"

mysql=MySQL(app)

@app.route("/about")
def about():#about us page of website
    return render_template("about.html")

@app.route("/")
def index():#main page of website
    cursor=mysql.connection.cursor()
    query="""
    CREATE PROCEDURE IF NOT EXISTS getUserInfo(IN user_name VARCHAR(255))
    BEGIN
        SELECT * FROM users WHERE username = user_name;
    END"""
    cursor.execute(query)

    return render_template("index.html")


#Register
@app.route("/register",methods=["GET","POST"])
def register():#register page of website. The user registers in the system by entering the necessary information.
    form=RegisterForm(request.form)

    if request.method=="POST" and form.validate():
        name=form.name.data
        username=form.username.data
        email=form.email.data
        phone_number=form.phone_number.data
        password=sha256_crypt.encrypt(form.password.data)

        cursor=mysql.connection.cursor()
        query="INSERT INTO users(name,email,username,password,phone_number) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(query,(name,email,username,password,phone_number))
        mysql.connection.commit()
        cursor.close()
        flash("You Have Successfully Registered","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():#login page of website. The user logins in the system by entering the necessary information.
    form=LoginForm(request.form)
    if request.method=="POST":
        username=form.username.data
        password_entered=form.password.data
        
        cursor =mysql.connection.cursor()
        result=cursor.execute(" call getUserInfo(%s)",(username,))

        if result >0:
            data=cursor.fetchone()
            real_password=data["password"]
            if sha256_crypt.verify(password_entered,real_password): 
                flash("You have successfully logged in...","success")
                #
                cursor=mysql.connection.cursor()
                query="INSERT INTO logs(type,user_id) VALUES(%s,%s)"
                cursor.execute(query,("login",data["id"]))
                mysql.connection.commit()
                # #
                session["logged_in"]=True
                session["username"]=username
                query="""SELECT * FROM admins WHERE user_id=%s"""
                result=cursor.execute(query,(data["id"],))

                if result>0:
                    session["isAdmin"]=True
                else:
                    session["isAdmin"]=False
                return redirect(url_for("index"))
                
            else:
                flash("You Entered Your Password Wrong...","danger")
                return redirect(url_for("login"))
        else:
            flash("There is no such user...","danger")
            return redirect(url_for("login"))

    return render_template("login.html",form=form)


@app.route("/logout")
def logout():#logout page of website. The user logs out of the system
    cursor=mysql.connection.cursor()

    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    id=data["id"]

    query="INSERT INTO logs(type,user_id) VALUES(%s,%s)"
    cursor.execute(query,("logout",id))
    mysql.connection.commit()
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():#dashboard page of website.The page where the user can add and manage the ads he/she added.

    cursor=mysql.connection.cursor()

    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    id=data["id"]

    getAdvertsQuery="SELECT * FROM otomobiles WHERE seller_id = %s"
    result=cursor.execute(getAdvertsQuery,(id,))

    otomobiles=cursor.fetchall()
    getAdvertsQuery="SELECT * FROM motorcycles WHERE seller_id = %s"
    result=cursor.execute(getAdvertsQuery,(id,))
    motorcycles=cursor.fetchall()

    getAdvertsQuery="SELECT * FROM watercrafts WHERE seller_id = %s"
    result=cursor.execute(getAdvertsQuery,(id,))
    watercrafts=cursor.fetchall()

    getAdvertsQuery="SELECT * FROM aircrafts WHERE seller_id = %s"
    result=cursor.execute(getAdvertsQuery,(id,))
    aircrafts=cursor.fetchall()
    return render_template("dashboard.html",otomobiles=otomobiles,motorcycles=motorcycles,watercrafts=watercrafts,aircrafts=aircrafts)

@app.route("/admin")
def admin():#admin page of website.Only users with admin authority can access this page. can access and manage all log records, all users and all advertisements.
    cursor=mysql.connection.cursor()
    query="""
    CREATE VIEW IF NOT EXISTS AllAdmins AS
    SELECT logs.id ,logs.type,logs.date,logs.user_id,users.username   FROM logs
    INNER JOIN users
    ON logs.user_id=users.id
    ORDER BY logs.date DESC;
    """
    cursor.execute(query)
    query="""SELECT *   FROM AllAdmins;"""
    result=cursor.execute(query)
    
    if result>0 :
        logs=cursor.fetchall()
        return render_template("admin.html",logs=logs)
    else:
        return render_template("admin.html")

@app.route("/manageUsers")
def manageUsers():#manage users page. Only admins can access this page. has the authority to delete any user and give admin authority.
    cursor=mysql.connection.cursor()
    query="""SELECT users.id,users.username,users.email,admins.user_id   FROM users
    LEFT JOIN admins
    ON admins.user_id=users.id;"""
    result=cursor.execute(query)
    
    if result>0 :
        users=cursor.fetchall()
        return render_template("manageusers.html",users=users)
    else:
        return render_template("manageusers.html")


@app.route("/manageAdverts")
def manageAdverts():#manage adverts page. Only admins can access this page. has the authority to delete and manage any advert .
    cursor=mysql.connection.cursor()
    

    getAdvertsQuery="SELECT * FROM otomobiles"
    result=cursor.execute(getAdvertsQuery)
    otomobiles=cursor.fetchall()

    getAdvertsQuery="SELECT * FROM motorcycles"
    result=cursor.execute(getAdvertsQuery)
    motorcycles=cursor.fetchall()

    getAdvertsQuery="SELECT * FROM watercrafts"
    result=cursor.execute(getAdvertsQuery)
    watercrafts=cursor.fetchall()

    getAdvertsQuery="SELECT * FROM aircrafts"
    result=cursor.execute(getAdvertsQuery)
    aircrafts=cursor.fetchall()
    return render_template("manageAdverts.html",otomobiles=otomobiles,motorcycles=motorcycles,watercrafts=watercrafts,aircrafts=aircrafts)

    
@app.route("/giveAdminAuthority/<string:id>")
def giveAdminAuthority(id):#The user with the received id value is given admin authority.
    cursor=mysql.connection.cursor()
    query="""INSERT INTO admins(user_id) VALUES(%s);"""
    cursor.execute(query,(id,))
    mysql.connection.commit()
    
    return redirect(url_for("manageUsers"))

@app.route("/deleteUser/<string:id>")
def deleteUser(id):#The user with the received id value is deleted.
    cursor=mysql.connection.cursor()
    query="""DELETE FROM users WHERE id=%s;"""
    cursor.execute(query,(id,))
    mysql.connection.commit()
    
    return redirect(url_for("manageUsers"))

@app.route("/addotomobile",methods=["GET","POST"])
def addotomobile():#add otomobile advert page of website. The user adds advert in the system by entering the necessary information.
    form=OtomobileForm(request.form)

    if request.method=="POST" and form.validate():

        title=form.title.data
        price=form.price.data
        brand=form.brand.data
        series=form.series.data
        model=form.model.data
        year=form.year.data
        fuel=form.fuel.data
        gear=form.gear.data
        color=form.color.data
        km=form.km.data
        body_type=form.body_type.data
        engine_power=form.engine_power.data
        engine_volume=form.engine_volume.data
        traction=form.traction.data
        city=form.city.data
        district=form.district.data
        description=form.description.data

        cursor=mysql.connection.cursor()
        result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
        data=cursor.fetchone()
        id=data["id"]
        
        addQuery="""INSERT INTO otomobiles(seller_id,title,price,brand,series,model,year,fuel,gear,color,km,body_type,engine_power,engine_volume,traction,city,district,description) 
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        cursor.execute(addQuery,(int(id),title,int(price),brand,series,model,int(year),fuel,gear,color,int(km),body_type,int(engine_power),int(engine_volume),traction,city,district,description))
        mysql.connection.commit()

        getAdvertId="SELECT  * FROM otomobiles WHERE seller_id = %s ORDER BY created_date DESC LIMIT 1"
        result=cursor.execute(getAdvertId,(id,))
        data=cursor.fetchone()
        advert_id=data["id"]

        isFirstImg=True
        
        uploaded_files = request.files.getlist("file")
        for f in uploaded_files:
            if isFirstImg:
                updateCoverImgQuery="UPDATE otomobiles SET cover_image =%s WHERE id=%s"
                cursor.execute(updateCoverImgQuery,(f.filename,advert_id))
                mysql.connection.commit()
                isFirstImg=False
            
            addImgQuery="INSERT INTO otomobile_images(seller_id,otomobile_advert_id,img) VALUES(%s,%s,%s)"
            cursor.execute(addImgQuery,(id,advert_id,f.filename))

            mysql.connection.commit()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

        cursor.close()
        
        flash("Advert Added Successfully","success")
        return redirect(url_for("dashboard"))

    return render_template("addotomobile.html",form=form)



@app.route("/otomobiles")
def otomobiles():#page listing all otomobile ads 
    cursor=mysql.connection.cursor()
    query="SELECT * FROM otomobiles"
    result=cursor.execute(query)
    
    if result>0 :
        otomobiles=cursor.fetchall()
        return render_template("otomobiles.html",otomobiles=otomobiles)
    else:
        return render_template("otomobiles.html")

#otomobile detail page
@app.route("/otomobileDetail?<id>")
def otomobileDetail(id):#The otomobile in the received id is shown in detail, together with its picture.
    cursor=mysql.connection.cursor()
    query="SELECT * FROM otomobiles where id =%s"
    result=cursor.execute(query,(id,))
    
    if result>0:
        otomobile=cursor.fetchone()
        imageQuery="SELECT * FROM otomobile_images WHERE otomobile_advert_id=%s"
        image_result=cursor.execute(imageQuery,(id,))
        images=cursor.fetchall()

        getSellerInfoQuery="SELECT * FROM users WHERE id=%s"
        seller_result=cursor.execute(getSellerInfoQuery,(otomobile["seller_id"],))
        seller=cursor.fetchone()
        
        return render_template("otomobile.html",otomobile=otomobile,images=images,seller=seller)
        
    else:
        return render_template("otomobile.html")

#otomobile intermediary func
@app.route("/otomobile/<string:id>")
def otomobile(id):
    return redirect(url_for("otomobileDetail",id=id))

#Search otombile url
@app.route("/searchotomobile",methods=["GET","POST"])
def searchotomobile():#Returns otomobiles that contain the given keyword in brand,series,color,model attributes
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword=request.form.get("keyword")

        cursor=mysql.connection.cursor()

        query="Select * from otomobiles where brand like '%" + keyword +"%' OR series like '%"+ keyword+"%' OR color like '%"+ keyword +"%' OR model like '%"+ keyword +"%'"

        result=cursor.execute(query)

        if result==0:
            flash("No advert found matching the search term.","warning")
            return redirect(url_for("otomobiles"))
        else:
            otomobiles= cursor.fetchall()

            return render_template("otomobiles.html",otomobiles=otomobiles)

#sort otombile adverts
@app.route("/sortOtomobile/<string:by>",methods=["GET","POST"])
def sortOtomobile(by):#Sorts the otomobile ads according to the given keyword

    direction=""
    index=""

    if by=="highestFirstPrice":
        index="price" 
        direction="DESC"
    elif by=="lowestFirstPrice":
        index="price" 
        direction="ASC"
    elif by=="newestFirstDate":
        index="created_date" 
        direction="DESC"
    elif by=="oldestFirstDate":
        index="created_date" 
        direction="ASC"
    elif by=="highestFirstKm":
        index="km" 
        direction="DESC"
    elif by=="lowestFirstKm":
        index="km" 
        direction="ASC"
    elif by=="oldFirstYear":
        index="year" 
        direction="ASC"
    elif by=="newFirstYear":
        index="year" 
        direction="DESC"

    cursor=mysql.connection.cursor()

    query="SELECT * FROM otomobiles ORDER BY "+index+" "+direction+";"

    result=cursor.execute(query)

    if result==0:
        flash("No advert found matching the list term.","warning")
        return redirect(url_for("otomobiles"))
    else:
        otomobiles= cursor.fetchall()
        return render_template("otomobiles.html",otomobiles=otomobiles)

#delete otomobile advert
@app.route("/deleteotomobile/<string:id>")
@login_required
def deleteotomobile(id):#deletes the otomobile advert with the given id
    cursor=mysql.connection.cursor()
    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    isAdmin=False
    query="SELECT * FROM admins where user_id=%s "
    result=cursor.execute(query,(int(seller_id),))
    if result>0:
        isAdmin=True

    query="SELECT * FROM otomobiles where seller_id=%s AND id=%s"
    result=cursor.execute(query,(seller_id,int(id)))

    

    if result >0 or isAdmin:
        query2="DELETE FROM otomobiles where id =%s"
        cursor.execute(query2,(int(id),))

        mysql.connection.commit()

        return redirect(url_for("dashboard"))
    else:
        flash("There is no such advert or you are not authorized to do so","danger")
        return redirect(url_for("index"))

#update otomobile advert
@app.route("/editotomobile/<string:id>",methods=["GET","POST"])
@login_required
def updateotomobile(id):#update page of the otomobile ad on the given id
    cursor=mysql.connection.cursor()
    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    if request.method=="GET":
        
        query="SELECT * FROM otomobiles where seller_id=%s AND id=%s"
        result=cursor.execute(query,(seller_id,int(id)))

        if result >0 :
            otomobile=cursor.fetchone()
            form=OtomobileForm()

            form.title.data=otomobile["title"]
            form.price.data=otomobile["price"]
            form.brand.data=otomobile["brand"]
            form.series.data=otomobile["series"]
            form.model.data=otomobile["model"]
            form.year.data=otomobile["year"]
            form.fuel.data=otomobile["fuel"]
            form.gear.data=otomobile["gear"]
            form.color.data=otomobile["color"]
            form.km.data=otomobile["km"]
            form.body_type.data=otomobile["body_type"]
            form.engine_power.data=otomobile["engine_power"]
            form.engine_volume.data=otomobile["engine_volume"]
            form.traction.data=otomobile["traction"]
            form.city.data=otomobile["city"]
            form.district.data=otomobile["district"]
            form.description.data=otomobile["description"]

            return render_template("updateOtomobile.html",form=form)
        else:
            flash("There is no such advert or you are not authorized to do so","danger")
            return redirect(url_for("index"))
    else:
        form=OtomobileForm(request.form)

        new_title=form.title.data
        new_price=form.price.data
        new_brand=form.brand.data
        new_series=form.series.data
        new_model=form.model.data
        new_year=form.year.data
        new_fuel=form.fuel.data
        new_gear=form.gear.data
        new_color=form.color.data
        new_km=form.km.data
        new_body_type=form.body_type.data
        new_engine_power=form.engine_power.data
        new_engine_volume=form.engine_volume.data
        new_traction=form.traction.data
        new_city=form.city.data
        new_district=form.district.data
        new_description=form.description.data

        updateQuery="""UPDATE otomobiles SET title =%s ,  price=%s ,  brand=%s ,  series=%s ,  model=%s ,  year=%s ,  fuel=%s ,  gear=%s ,
          color=%s ,  km=%s ,  body_type=%s ,  engine_power=%s ,  engine_volume=%s ,  traction=%s ,  city=%s ,  district=%s ,  description=%s  
         WHERE id =%s
         """

        cursor = mysql.connection.cursor()

        cursor.execute(updateQuery,(new_title,int(new_price),new_brand,new_series,new_model,int(new_year),new_fuel,new_gear,new_color,int(new_km),
        new_body_type,int(new_engine_power),int(new_engine_volume),new_traction,new_city,new_district,new_description,int(id)))

        mysql.connection.commit()

        flash("The advert has been successfully updated.","success")

        return redirect(url_for("dashboard"))

@app.route("/addmotorcycle",methods=["GET","POST"])
def addmotorcycles():#add motorcycle advert page of website. The user adds advert in the system by entering the necessary information.
    form=MotorcycleForm(request.form)

    if request.method=="POST" and form.validate():

        title=form.title.data
        price=form.price.data
        brand=form.brand.data
        model=form.model.data
        type=form.type.data
        year=form.year.data
        gear=form.gear.data
        color=form.color.data
        km=form.km.data
        engine_power=form.engine_power.data
        engine_volume=form.engine_volume.data
        city=form.city.data
        district=form.district.data
        description=form.description.data

        cursor=mysql.connection.cursor()

        result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
        data=cursor.fetchone()
        id=data["id"]
        
        addQuery="""INSERT INTO motorcycles(seller_id,title,price,brand,type,model,year,gear,color,km,engine_power,engine_volume,city,district,description) 
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        cursor.execute(addQuery,(int(id),title,int(price),brand,type,model,int(year),gear,color,int(km),int(engine_power),int(engine_volume),city,district,description))
        mysql.connection.commit()

        getAdvertId="SELECT  * FROM motorcycles WHERE seller_id = %s ORDER BY created_date DESC LIMIT 1"
        result=cursor.execute(getAdvertId,(id,))
        data=cursor.fetchone()
        advert_id=data["id"]

        isFirstImg=True
        
        uploaded_files = request.files.getlist("file")
        for f in uploaded_files:
            if isFirstImg:
                updateCoverImgQuery="UPDATE motorcycles SET cover_image =%s WHERE id=%s"
                cursor.execute(updateCoverImgQuery,(f.filename,advert_id))
                mysql.connection.commit()
                isFirstImg=False
            
            addImgQuery="INSERT INTO motorcycle_images(seller_id,motorcycle_advert_id,image) VALUES(%s,%s,%s)"
            cursor.execute(addImgQuery,(id,advert_id,f.filename))

            mysql.connection.commit()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

        cursor.close()
        
        flash("Advert Added Successfully","success")
        return redirect(url_for("dashboard"))

    return render_template("addmotorcycle.html",form=form)


@app.route("/motorcycles")
def motorcycles():#page listing all motorcycle ads
    cursor=mysql.connection.cursor()
    query="SELECT * FROM motorcycles"
    result=cursor.execute(query)
    
    if result>0 :
        motorcycles=cursor.fetchall()
        return render_template("motorcycles.html",motorcycles=motorcycles)
    else:
        return render_template("motorcycles.html")

#motorcycle detail page
@app.route("/motorcycleDetail?<id>")
def motorcycleDetail(id):#The motorcycle in the received id is shown in detail, together with its picture.
    cursor=mysql.connection.cursor()
    query="SELECT * FROM motorcycles where id =%s"
    result=cursor.execute(query,(id,))
    
    if result>0:
        motorcycle=cursor.fetchone()
        imageQuery="SELECT * FROM motorcycle_images WHERE motorcycle_advert_id=%s"
        image_result=cursor.execute(imageQuery,(id,))
        images=cursor.fetchall()

        getSellerInfoQuery="SELECT * FROM users WHERE id=%s"
        seller_result=cursor.execute(getSellerInfoQuery,(motorcycle["seller_id"],))
        seller=cursor.fetchone()
        
        return render_template("motorcycle.html",motorcycle=motorcycle,images=images,seller=seller)
        
    else:
        return render_template("motorcycle.html")  


#motorcycle intermediary func
@app.route("/motorcycle/<string:id>")
def motorcycle(id):
    return redirect(url_for("motorcycleDetail",id=id)) 


#update motorcycle advert
@app.route("/editmotorcycle/<string:id>",methods=["GET","POST"])
@login_required
def updatemotorcycle(id):#update page of the motorcycle ad on the given id
    cursor=mysql.connection.cursor()
    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    if request.method=="GET":
        
        query="SELECT * FROM motorcycles where seller_id=%s AND id=%s"
        result=cursor.execute(query,(seller_id,int(id)))

        if result >0 :
            motorcycle=cursor.fetchone()
            form=MotorcycleForm()

            form.title.data=motorcycle["title"]
            form.price.data=motorcycle["price"]
            form.brand.data=motorcycle["brand"]
            form.type.data=motorcycle["type"]
            form.model.data=motorcycle["model"]
            form.year.data=motorcycle["year"]
            form.gear.data=motorcycle["gear"]
            form.color.data=motorcycle["color"]
            form.km.data=motorcycle["km"]
            form.engine_power.data=motorcycle["engine_power"]
            form.engine_volume.data=motorcycle["engine_volume"]
            form.city.data=motorcycle["city"]
            form.district.data=motorcycle["district"]
            form.description.data=motorcycle["description"]

            return render_template("updateMotorcycle.html",form=form)
        else:
            flash("There is no such advert or you are not authorized to do so","danger")
            return redirect(url_for("index"))
    else:
        form=MotorcycleForm(request.form)

        new_title=form.title.data
        new_price=form.price.data
        new_brand=form.brand.data
        new_type=form.type.data
        new_model=form.model.data
        new_year=form.year.data
        new_gear=form.gear.data
        new_color=form.color.data
        new_km=form.km.data
        new_engine_power=form.engine_power.data
        new_engine_volume=form.engine_volume.data
        new_city=form.city.data
        new_district=form.district.data
        new_description=form.description.data

        updateQuery="""UPDATE motorcycles SET title =%s ,  price=%s ,  brand=%s ,  type=%s ,  model=%s ,  year=%s ,    gear=%s ,
          color=%s ,  km=%s  ,  engine_power=%s ,  engine_volume=%s ,    city=%s ,  district=%s ,  description=%s  
         WHERE id =%s
         """

        cursor = mysql.connection.cursor()

        cursor.execute(updateQuery,(new_title,int(new_price),new_brand,new_type,new_model,int(new_year),new_gear,new_color,int(new_km)
        ,int(new_engine_power),int(new_engine_volume),new_city,new_district,new_description,int(id)))

        mysql.connection.commit()

        flash("The advert has been successfully updated.","success")

        return redirect(url_for("dashboard"))

#delete motorcycle advert
@app.route("/deletemotorcycle/<string:id>")
@login_required
def deletemotorcycle(id):#deletes the motorcycle advert with the given id
    cursor=mysql.connection.cursor()
    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    isAdmin=False
    query="SELECT * FROM admins where user_id=%s "
    result=cursor.execute(query,(int(seller_id),))
    if result>0:
        isAdmin=True

    query="SELECT * FROM motorcycles where seller_id=%s AND id=%s"
    result=cursor.execute(query,(seller_id,int(id)))

    if result >0 or isAdmin:
        query2="DELETE FROM motorcycles where id =%s"
        cursor.execute(query2,(int(id),))

        mysql.connection.commit()

        return redirect(url_for("dashboard"))
    else:
        flash("There is no such advert or you are not authorized to do so","danger")
        return redirect(url_for("index"))

#Search motorcycle url
@app.route("/searchmotorcycle",methods=["GET","POST"])
def searchmotorcycle():#Returns motorcycle that contain the given keyword in brand,color,model attributes
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword=request.form.get("keyword")

        cursor=mysql.connection.cursor()

        query="Select * from motorcycles where brand like '%" + keyword +"%' OR model like '%"+ keyword +"%' OR color like '%"+ keyword +"%'"

        result=cursor.execute(query)

        if result==0:
            flash("No advert found matching the search term.","warning")
            return redirect(url_for("motorcycles"))
        else:
            motorcycles= cursor.fetchall()

            return render_template("motorcycles.html",motorcycles=motorcycles)

#sort motorcycle adverts
@app.route("/sortmotorcycle/<string:by>",methods=["GET","POST"])
def sortmotorcycle(by):#Sorts the motorcyle ads according to the given keyword

    direction=""
    index=""

    if by=="highestFirstPrice":
        index="price" 
        direction="DESC"
    elif by=="lowestFirstPrice":
        index="price" 
        direction="ASC"
    elif by=="newestFirstDate":
        index="created_date" 
        direction="DESC"
    elif by=="oldestFirstDate":
        index="created_date" 
        direction="ASC"
    elif by=="highestFirstKm":
        index="km" 
        direction="DESC"
    elif by=="lowestFirstKm":
        index="km" 
        direction="ASC"
    elif by=="oldFirstYear":
        index="year" 
        direction="ASC"
    elif by=="newFirstYear":
        index="year" 
        direction="DESC"

    cursor=mysql.connection.cursor()

    query="SELECT * FROM motorcycles ORDER BY "+index+" "+direction+";"

    result=cursor.execute(query)

    if result==0:
        flash("No advert found matching the list term.","warning")
        return redirect(url_for("motorcycles"))
    else:
        motorcycles= cursor.fetchall()
        return render_template("motorcycles.html",motorcycles=motorcycles)

#watercraft
@app.route("/addwatercraft",methods=["GET","POST"])
def addwatercrafts():#add watercraft advert page of website. The user adds advert in the system by entering the necessary information.
    form=WatercraftForm(request.form)

    if request.method=="POST" and form.validate():

        title=form.title.data
        price=form.price.data
        type=form.type.data
        year=form.year.data
        color=form.color.data
        width=form.width.data
        length=form.length.data
        city=form.city.data
        district=form.district.data
        description=form.description.data

        cursor=mysql.connection.cursor()
        result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
        data=cursor.fetchone()
        id=data["id"]
        
        addQuery="""INSERT INTO watercrafts(seller_id,title,price,type,year,color,width,length,city,district,description) 
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        cursor.execute(addQuery,(int(id),title,int(price),type,int(year),color,int(width),int(length),city,district,description))
        mysql.connection.commit()

        getAdvertId="SELECT  * FROM watercrafts WHERE seller_id = %s ORDER BY created_date DESC LIMIT 1"
        result=cursor.execute(getAdvertId,(id,))
        data=cursor.fetchone()
        advert_id=data["id"]

        isFirstImg=True
        
        uploaded_files = request.files.getlist("file")
        for f in uploaded_files:
            if isFirstImg:
                updateCoverImgQuery="UPDATE watercrafts SET cover_image =%s WHERE id=%s"
                cursor.execute(updateCoverImgQuery,(f.filename,advert_id))
                mysql.connection.commit()
                isFirstImg=False
            
            addImgQuery="INSERT INTO watercraft_images(seller_id,watercraft_advert_id,image) VALUES(%s,%s,%s)"
            cursor.execute(addImgQuery,(id,advert_id,f.filename))

            mysql.connection.commit()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

        cursor.close()
        
        flash("Advert Added Successfully","success")
        return redirect(url_for("dashboard"))

    return render_template("addwatercraft.html",form=form)

@app.route("/watercrafts")
def watercrafts():#page listing all watercraft ads
    cursor=mysql.connection.cursor()
    query="SELECT * FROM watercrafts"
    result=cursor.execute(query)
    
    if result>0 :
        watercrafts=cursor.fetchall()
        return render_template("watercrafts.html",watercrafts=watercrafts)
    else:
        return render_template("watercrafts.html")

#watercraft detail page
@app.route("/watercraftDetail?<id>")
def watercraftDetail(id):#The watercraft in the received id is shown in detail, together with its picture.
    cursor=mysql.connection.cursor()
    query="SELECT * FROM watercrafts where id =%s"
    result=cursor.execute(query,(id,))
    
    if result>0:
        watercraft=cursor.fetchone()
        imageQuery="SELECT * FROM watercraft_images WHERE watercraft_advert_id=%s"
        image_result=cursor.execute(imageQuery,(id,))
        images=cursor.fetchall()

        getSellerInfoQuery="SELECT * FROM users WHERE id=%s"
        seller_result=cursor.execute(getSellerInfoQuery,(watercraft["seller_id"],))
        seller=cursor.fetchone()
        
        return render_template("watercraft.html",watercraft=watercraft,images=images,seller=seller)
        
    else:
        return render_template("watercraft.html")  


#watercraft intermediary func
@app.route("/watercraft/<string:id>")
def watercraft(id):
    return redirect(url_for("watercraftDetail",id=id)) 


#update watercraft advert
@app.route("/editwatercraft/<string:id>",methods=["GET","POST"])
@login_required
def updatewatercraft(id):#update page of the watercraft ad on the given id
    cursor=mysql.connection.cursor()
    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    if request.method=="GET":
        
        query="SELECT * FROM watercrafts where seller_id=%s AND id=%s"
        result=cursor.execute(query,(seller_id,int(id)))

        if result >0 :
            watercraft=cursor.fetchone()
            form=WatercraftForm()

            form.title.data=watercraft["title"]
            form.price.data=watercraft["price"]

            form.type.data=watercraft["type"]
            form.length.data=watercraft["length"]
            form.width.data=watercraft["width"]

            form.year.data=watercraft["year"]

            form.color.data=watercraft["color"]

            form.city.data=watercraft["city"]
            form.district.data=watercraft["district"]
            form.description.data=watercraft["description"]

            return render_template("updatewatercraft.html",form=form)
        else:
            flash("There is no such advert or you are not authorized to do so","danger")
            return redirect(url_for("index"))
    else:
        form=WatercraftForm(request.form)
        new_title=form.title.data
        new_price=form.price.data
        new_type=form.type.data
        new_year=form.year.data
        new_color=form.color.data
        new_length=form.length.data
        new_width=form.width.data
        new_city=form.city.data
        new_district=form.district.data
        new_description=form.description.data

        updateQuery="""UPDATE watercrafts SET title =%s ,  price=%s ,   type=%s ,    year=%s ,    
          color=%s ,    width=%s ,  length=%s ,    city=%s ,  district=%s ,  description=%s  
         WHERE id =%s
         """

        cursor = mysql.connection.cursor()

        cursor.execute(updateQuery,(new_title,int(new_price),new_type,int(new_year),new_color
        ,int(new_width),int(new_length),new_city,new_district,new_description,int(id)))

        mysql.connection.commit()

        flash("The advert has been successfully updated.","success")

        return redirect(url_for("dashboard"))

#delete watercraft advert
@app.route("/deletewatercraft/<string:id>")
@login_required
def deletewatercraft(id):#deletes the watercraft advert with the given id
    cursor=mysql.connection.cursor()
    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]
    isAdmin=False
    query="SELECT * FROM admins where user_id=%s "
    result=cursor.execute(query,(int(seller_id),))
    if result>0:
        isAdmin=True

    query="SELECT * FROM watercrafts where seller_id=%s AND id=%s"
    result=cursor.execute(query,(seller_id,int(id)))

    if result >0 or isAdmin:
        query2="DELETE FROM watercrafts where id =%s"
        cursor.execute(query2,(int(id),))

        mysql.connection.commit()

        return redirect(url_for("dashboard"))
    else:
        flash("There is no such advert or you are not authorized to do so","danger")
        return redirect(url_for("index"))

#Search watercraft url
@app.route("/searchwatercraft",methods=["GET","POST"])
def searchwatercraft():#Returns otomobiles that contain the given keyword in ,color,year attributes
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword=request.form.get("keyword")
        cursor=mysql.connection.cursor()
        query="Select * from watercrafts where year like '%" + keyword +"%' OR color like '%"+ keyword +"%'"
        result=cursor.execute(query)
        if result==0:
            flash("No advert found matching the search term.","warning")
            return redirect(url_for("watercrafts"))
        else:
            watercrafts= cursor.fetchall()

            return render_template("watercrafts.html",watercrafts=watercrafts)

#sort watercraft adverts
@app.route("/sortwatercraft/<string:by>",methods=["GET","POST"])
def sortwatercraft(by):#Sorts the watercraft ads according to the given keyword

    direction=""
    index=""

    if by=="highestFirstPrice":
        index="price" 
        direction="DESC"
    elif by=="lowestFirstPrice":
        index="price" 
        direction="ASC"
    elif by=="newestFirstDate":
        index="created_date" 
        direction="DESC"
    elif by=="oldestFirstDate":
        index="created_date" 
        direction="ASC"
    elif by=="oldFirstYear":
        index="year" 
        direction="ASC"
    elif by=="newFirstYear":
        index="year" 
        direction="DESC"

    cursor=mysql.connection.cursor()

    query="SELECT * FROM watercrafts ORDER BY "+index+" "+direction+";"

    result=cursor.execute(query)

    if result==0:
        flash("No advert found matching the list term.","warning")
        return redirect(url_for("watercrafts"))
    else:
        watercrafts= cursor.fetchall()
        return render_template("watercrafts.html",watercrafts=watercrafts)

#aircraft
@app.route("/addaircraft",methods=["GET","POST"])
def addaircrafts():#add aircraft advert page of website. The user adds advert in the system by entering the necessary information.
    form=AircraftForm(request.form)

    if request.method=="POST" and form.validate():

        title=form.title.data
        price=form.price.data
        type=form.type.data
        year=form.year.data
        color=form.color.data
        width=form.width.data
        max_altitude=form.max_altitude.data
        city=form.city.data
        district=form.district.data
        description=form.description.data

        cursor=mysql.connection.cursor()
        result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
        data=cursor.fetchone()
        id=data["id"]
        
        addQuery="""INSERT INTO aircrafts(seller_id,title,price,type,year,color,width,max_altitude,city,district,description) 
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        cursor.execute(addQuery,(int(id),title,int(price),type,int(year),color,int(width),int(max_altitude),city,district,description))
        mysql.connection.commit()

        getAdvertId="SELECT  * FROM aircrafts WHERE seller_id = %s ORDER BY created_date DESC LIMIT 1"
        result=cursor.execute(getAdvertId,(id,))
        data=cursor.fetchone()
        advert_id=data["id"]

        isFirstImg=True
        
        uploaded_files = request.files.getlist("file")
        for f in uploaded_files:
            if isFirstImg:
                updateCoverImgQuery="UPDATE aircrafts SET cover_image =%s WHERE id=%s"
                cursor.execute(updateCoverImgQuery,(f.filename,advert_id))
                mysql.connection.commit()
                isFirstImg=False
            
            addImgQuery="INSERT INTO aircraft_images(seller_id,aircraft_advert_id,image) VALUES(%s,%s,%s)"
            cursor.execute(addImgQuery,(id,advert_id,f.filename))

            mysql.connection.commit()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

        cursor.close()
        
        flash("Advert Added Successfully","success")
        return redirect(url_for("dashboard"))

    return render_template("addaircraft.html",form=form)

@app.route("/aircrafts")
def aircrafts():#page listing all aircraft ads
    cursor=mysql.connection.cursor()
    query="SELECT * FROM aircrafts"
    result=cursor.execute(query)
    
    if result>0 :
        aircrafts=cursor.fetchall()
        return render_template("aircrafts.html",aircrafts=aircrafts)
    else:
        return render_template("aircrafts.html")

#aircraft detail page
@app.route("/aircraftDetail?<id>")
def aircraftDetail(id):#The aircraft in the received id is shown in detail, together with its picture.
    cursor=mysql.connection.cursor()
    query="SELECT * FROM aircrafts where id =%s"
    result=cursor.execute(query,(id,))
    
    if result>0:
        aircraft=cursor.fetchone()
        imageQuery="SELECT * FROM aircraft_images WHERE aircraft_advert_id=%s"
        image_result=cursor.execute(imageQuery,(id,))
        images=cursor.fetchall()

        getSellerInfoQuery="SELECT * FROM users WHERE id=%s"
        seller_result=cursor.execute(getSellerInfoQuery,(aircraft["seller_id"],))
        seller=cursor.fetchone()
        
        return render_template("aircraft.html",aircraft=aircraft,images=images,seller=seller)
        
    else:
        return render_template("aircraft.html")  


#aircraft intermediary func
@app.route("/aircraft/<string:id>")
def aircraft(id):
    return redirect(url_for("aircraftDetail",id=id)) 

#update aircraft advert
@app.route("/editaircraft/<string:id>",methods=["GET","POST"])
@login_required
def updateaircraft(id):#update page of the aircraft ad on the given id
    cursor=mysql.connection.cursor()
    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    if request.method=="GET":
        
        query="SELECT * FROM aircrafts where seller_id=%s AND id=%s"
        result=cursor.execute(query,(seller_id,int(id)))

        if result >0 :
            aircraft=cursor.fetchone()
            form=AircraftForm()
            form.title.data=aircraft["title"]
            form.price.data=aircraft["price"]
            form.type.data=aircraft["type"]
            form.max_altitude.data=aircraft["max_altitude"]
            form.width.data=aircraft["width"]
            form.year.data=aircraft["year"]
            form.color.data=aircraft["color"]
            form.city.data=aircraft["city"]
            form.district.data=aircraft["district"]
            form.description.data=aircraft["description"]

            return render_template("updateaircraft.html",form=form)
        else:
            flash("There is no such advert or you are not authorized to do so","danger")
            return redirect(url_for("index"))
    else:
        form=AircraftForm(request.form)

        new_title=form.title.data
        new_price=form.price.data
        new_type=form.type.data
        new_year=form.year.data
        new_color=form.color.data
        new_max_altitude=form.max_altitude.data
        new_width=form.width.data
        new_city=form.city.data
        new_district=form.district.data
        new_description=form.description.data

        updateQuery="""UPDATE aircrafts SET title =%s ,  price=%s ,   type=%s ,    year=%s ,    
          color=%s ,    width=%s ,  max_altitude=%s ,    city=%s ,  district=%s ,  description=%s  
         WHERE id =%s
         """

        cursor = mysql.connection.cursor()

        cursor.execute(updateQuery,(new_title,int(new_price),new_type,int(new_year),new_color
        ,int(new_width),int(new_max_altitude),new_city,new_district,new_description,int(id)))

        mysql.connection.commit()

        flash("The advert has been successfully updated.","success")

        return redirect(url_for("dashboard"))

#delete aircraft advert
@app.route("/deleteaircraft/<string:id>")
@login_required
def deleteaircraft(id):#deletes the aircraft advert with the given id
    cursor=mysql.connection.cursor()
    result=cursor.execute(" call getUserInfo(%s)",(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    isAdmin=False
    query="SELECT * FROM admins where user_id=%s "
    result=cursor.execute(query,(int(seller_id),))
    if result>0:
        isAdmin=True

    query="SELECT * FROM aircrafts where seller_id=%s AND id=%s"
    result=cursor.execute(query,(seller_id,int(id)))

    if result >0 or isAdmin:
        query2="DELETE FROM aircrafts where id =%s"
        cursor.execute(query2,(int(id),))

        mysql.connection.commit()

        return redirect(url_for("dashboard"))
    else:
        flash("There is no such advert or you are not authorized to do so","danger")
        return redirect(url_for("index"))

#Search aircraft url
@app.route("/searchaircraft",methods=["GET","POST"])
def searchaircraft():#Returns aircraft that contain the given keyword in color,year attributes
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword=request.form.get("keyword")

        cursor=mysql.connection.cursor()

        query="Select * from aircrafts where year like '%" + keyword +"%' OR color like '%"+ keyword +"%'"

        result=cursor.execute(query)

        if result==0:
            flash("No advert found matching the search term.","warning")
            return redirect(url_for("aircrafts"))
        else:
            aircrafts= cursor.fetchall()

            return render_template("aircrafts.html",aircrafts=aircrafts)

#sort aircraft adverts
@app.route("/sortaircraft/<string:by>",methods=["GET","POST"])
def sortaircraft(by):#Sorts the aircraft ads according to the given keyword

    direction=""
    index=""

    if by=="highestFirstPrice":
        index="price" 
        direction="DESC"
    elif by=="lowestFirstPrice":
        index="price" 
        direction="ASC"
    elif by=="newestFirstDate":
        index="created_date" 
        direction="DESC"
    elif by=="oldestFirstDate":
        index="created_date" 
        direction="ASC"
    elif by=="oldFirstYear":
        index="year" 
        direction="ASC"
    elif by=="newFirstYear":
        index="year" 
        direction="DESC"

    cursor=mysql.connection.cursor()

    query="SELECT * FROM aircrafts ORDER BY "+index+" "+direction+";"

    result=cursor.execute(query)

    if result==0:
        flash("No advert found matching the list term.","warning")
        return redirect(url_for("aircrafts"))
    else:
        aircrafts= cursor.fetchall()
        return render_template("aircrafts.html",aircrafts=aircrafts)

if __name__=="__main__":
    app.run(debug=True)