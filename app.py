from flask import Flask,render_template,request,redirect,session
from pymongo import MongoClient
from flask_cors import CORS
import smtplib
import boto3

cluster = MongoClient('mongodb+srv://bodlapatikavya041:kavya1901@kavya.0xncc1w.mongodb.net/?retryWrites=true&w=majority&appName=kavya')
bucketName ="ecommerce.app" #ecom.appp

db = cluster['prada']
users = db['users']
admins = db['admins']
products = db['products']
reviews = db['reviews']

s3 = boto3.client('s3')


app = Flask(__name__)
app.secret_key='344gfjkl'
CORS(app)

@app.route('/',methods=['get'])
def home():
    return render_template('home.html')

@app.route('/signup',methods=['get'])
def homes():
    return render_template('/index.html')
@app.route('/signup',methods=['post'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']
    user = users.find_one({"email":email})
    if user:
        return render_template('index.html',status="User already exist with same email")
    if password != cpassword:
        return render_template('index.html',status="Passwords miss match")
    users.insert_one({"name":name,"email":email,"password":password})
    return render_template('index.html',status="Success")

@app.route('/dashboard',methods=['get'])
def dash():
    try:
        session['user']
        return render_template('prada.html')
    except:
        return render_template('err.html')

@app.route('/login',methods=['post'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = users.find_one({"email":email,"password":password})
    if user:
        session['user'] = email
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/forget',methods=['get'])
def forget():
    return render_template('forgot.html')

@app.route('/women',methods=['get'])
def women():
    data = products.find({'category':"womens"})
    return render_template('women.html',wdata=data)

@app.route('/men',methods=['get'])
def men():
    data = products.find({'category':"mens"})
    return render_template('men.html',mdata=data)

@app.route('/forget',methods=['post'])
def f():
    email = request.form['email']
    user = users.find_one({'email':email})
    if not user:
        return render_template('forgot.html',ack='User not found with this email')
    
    server= smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('kavyabodlapati19@gmail.com','xmkvbfccqpntkrpy')
    server.sendmail('kavyabodlapati19@gmail.com',email,'click on the following link to update password \n http://localhost:5000/updatepass/'+email)
    return render_template('change.html',ack="Mail sent")

@app.route('/updatepass/<email>',methods=['get'])
def loadc(email):
    return render_template('change.html',data = email)

@app.route('/updatepass/<email>',methods=['post'])
def ch(email):
    npass = request.form['npass']
    cpass = request.form['cpass']
    if npass!=cpass:
        return render_template('change.html',ack="passwords miss match")
    users.update_one({"email":email},{'$set':{"password":npass}})
    return render_template('change.html',ack="password changed")

@app.route('/beauty',methods=['get'])
def be():
    data = products.find({'category':"beauty"})
    return render_template('/beauty.html',bdata=data)

@app.route('/admindash')
def admindash():
    try:
        session['admin']
        return render_template('admindash.html')
    except:
        return render_template('err.html')
    
@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/adminlogin',methods=['post'])
def doadminlogin():
    email = request.form['email']
    password = request.form['password']
    admin = admins.find_one({'email':email,'password':password})
    if admin:
        session['admin'] = email
        return redirect('/admindash')
    return render_template('adminlogin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/addproduct',methods=['post'])
def addproduct():
    category = request.form['category']
    product_name = request.form['product_name']
    price = request.form['price']
    description = request.form['description']
    imgfile = request.files['image']
    imguri = imgfile.filename
    s3.upload_fileobj(imgfile,bucketName,imguri)
    products.insert_one({'category':category,'productName':product_name,'price':price,'imguri':"https://s3.us-east-1.amazonaws.com/"+bucketName+"/"+imguri,'description':description})
    return render_template('admindash.html',ack="Product added...")

@app.route('/reviews/<productId>',methods=['get'])
def getProduct(productId):
    user = users.find_one({'email':session['user']})
    allReviews = reviews.find({'productId':productId})
    return render_template('reviews.html',item =productId,revs = allReviews,name=user['name'])

@app.route('/reviews/<productId>',methods=['post'])
def pushcomment(productId):
    name = request.form['name']
    rating = request.form['rating']
    comment = request.form['comment']
    reviews.insert_one({'productId':productId,'name':name,'rating':rating,'comment':comment})
    return redirect('/reviews/'+productId)

@app.route('/analytics/<productId>')
def analytics(productId):
    return render_template('dash.html',id=productId)

@app.route('/getReviews/<id>',methods=['get'])
def getrevies(id):
    revs = reviews.find({'productId':id})
    data = []
    for i in revs:
        i = dict(i)
        i['_id'] = str(i['_id'])
        data.append(i)
    return data

if __name__ == "__main__":
    app.run(host="0.0.0.0")