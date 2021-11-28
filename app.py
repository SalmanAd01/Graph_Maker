from flask import Flask,render_template,request,url_for,redirect,flash,session
from flask_mail import Mail, Message
import io
import psycopg2
import os
import base64
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
fig,ax=plt.subplots(figsize=(6,6))
x1=[]
y1=[]
app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class FeedBack_form(db.Model):
    __tablename__ = 'feedback_form'
    id = db.Column(db.Integer, primary_key=True)
    firtsname = db.Column(db.String, unique=True)
    lastname = db.Column(db.String, unique=True)
    Feedback = db.Column(db.String,default="NOT_SET")

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"
app.secret_key = os.environ["SECRET"]
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=os.environ["EMAIL"]
app.config['MAIL_PASSWORD']=os.environ["PASSWORD"]
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/ma',methods=['GET','POST'])
def ma():
    try:
        if request.method == 'POST':
            email=request.form['email']
            msg=request.form['msg']
            mo=Message("Message From Graph_Maker",sender=email,recipients=[os.environ["EMAIL"]])
            mo.body=msg
            mail.send(mo)
            flash('Thanks For Contacting.')
            return redirect(url_for('Contact'))
    except Exception as e:
        print('--->>> ',e)
        flash('Some Error occurred')
        return redirect(url_for('Contact'))
@app.route('/submit',methods=['POST','GET'])
def submit():
    try:
        if request.method=='POST':
            num=int(request.form['value_1'])
            session["gname"]=request.form['gname']
            session["xname"]=request.form['xname']
            session["yname"]=request.form['yname']
        return render_template('Jinja2_ForLoop.html',value_to=num)
    except Exception as e:
        print('-->>',e)
        return redirect(url_for('home'))
@app.route('/feed',methods=['GET','POST'])
def feedback():
    if request.method == 'POST':
        try:
            First_Name=request.form['First_Name']
            Last_Name=request.form['Last_Name']
            Feed_Back=request.form['Feed_Back']
            just1 = FeedBack_form(firtsname=First_Name, lastname=Last_Name, Feedback=Feed_Back)
            db.session.add(just1)
            db.session.commit()
            flash('we really appreciate your feedback')
            return render_template('feedback.html')
        except:
            flash('Some Error occurred')
            return render_template('feedback.html')
    else:
        return render_template('feedback.html')

@app.route('/plotagraph',methods=['GET','POST'])
def plotagraph():
    try:
        if request.method == 'POST':
            for i in range((len(request.form.to_dict())//2)):
                x1.append(float(request.form['x'+str(i)]))
                y1.append(float(request.form['y'+str(i)]))
        img=io.BytesIO()
        plt.figure()
        for x,y in zip(x1,y1):
            plt.text(x,y,'({}, {})'.format(x,y))
        plt.title(session.get("gname"), fontdict={'fontname': 'Comic Sans MS', 'fontsize': 20})
        plt.xlabel(session.get("xname"), fontdict={'fontname': 'Comic Sans MS'})
        plt.ylabel(session.get("yname"), fontdict={'fontname': 'Comic Sans MS'})
        plt.plot(x1,y1)
        x1.clear()
        y1.clear()
        plt.savefig(img)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return render_template('graph.html',plot_url=plot_url)    
    except Exception as e:
        print(e)
        return redirect(url_for('submit'))
@app.route('/about')
def about():
    return render_template('About.html')
@app.route('/feedba')
def feedb():
    return render_template('feedback.html')
@app.route('/upcoming_features')
def upcoming_features():
    return render_template('Upcoming_Features.html')
@app.route('/Contact')
def Contact():
    return render_template('Contact.html')
if __name__ == '__main__':
    app.run(debug=True)
