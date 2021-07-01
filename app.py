from flask import Flask,render_template,request,url_for,redirect,flash
from flask_mail import Mail, Message
import io
import base64
from datetime import datetime
import matplotlib.pyplot as plt
from flask_pymongo import PyMongo
fig,ax=plt.subplots(figsize=(6,6))
x1=[]
y1=[]
app=Flask(__name__)
app.config['MONGO_URI']="mongodb://localhost:27017/test1"
mongo=PyMongo(app)
db=mongo.db
app.secret_key = 'ye ye'
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='salmanad5s3@gmail.com'
app.config['MAIL_PASSWORD']='Salman9021618891'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/ma',methods=['GET','POST'])
def ma():
    if request.method == 'POST':
        email=request.form['email']
        msg=request.form['msg']
        mo=Message("Message From Graph_Maker",sender=email,recipients=['salmanad5s3@gmail.com'])
        mo.body=msg
        mail.send(mo)
        flash('Thanks For Contacting.')
        return redirect(url_for('Contact'))


@app.route('/submit',methods=['POST','GET'])
def submit():
    global num
    global gname
    global xname
    global yname
    try:
        if request.method=='POST':
            num=int(request.form['value_1'])
            gname=request.form['gname']
            xname=request.form['xname']
            yname=request.form['yname']
        return render_template('Jinja2_ForLoop.html',value_to=num)
    except:
        return redirect(url_for('home'))
@app.route('/feed',methods=['GET','POST'])
def feedback():
    if request.method == 'POST':
        First_Name=request.form['First_Name']
        Last_Name=request.form['Last_Name']
        Feed_Back=request.form['Feed_Back']

        db.feedback.insert_one({'firstname':First_Name,'lastname':Last_Name , 'feedbacks':Feed_Back,'datatime':datetime.utcnow()})
        flash('we really appreciate your feedback')
    return render_template('feedback.html')
@app.route('/plotagraph',methods=['GET','POST'])
def plotagraph():
    try:
        if request.method == 'POST':
            for i in range(num):
                x1.append(float(request.form['x'+str(i)]))
                y1.append(float(request.form['y'+str(i)]))
        img=io.BytesIO()
        plt.figure()
        for x,y in zip(x1,y1):
            plt.text(x,y,'({}, {})'.format(x,y))

        plt.title(gname, fontdict={'fontname': 'Comic Sans MS', 'fontsize': 20})
        plt.xlabel(xname, fontdict={'fontname': 'Comic Sans MS'})
        plt.ylabel(yname, fontdict={'fontname': 'Comic Sans MS'})
        plt.plot(x1,y1)
        x1.clear()
        y1.clear()
        plt.savefig(img)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return render_template('graph.html',plot_url=plot_url)    
    except:
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
