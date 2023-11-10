from dotenv import load_dotenv
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_mail import Mail, Message
import io
import psycopg2
import os
import base64
import re
from datetime import datetime
import matplotlib
matplotlib.use('Agg')

load_dotenv('.env')
fig, ax = plt.subplots(figsize=(6, 6))
x1 = []
y1 = []
uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class FeedBack_form(db.Model):
    __tablename__ = 'feedback_forms'
    id = db.Column(db.Integer, primary_key=True)
    firtsname = db.Column(db.String, nullable=False, unique=False)
    lastname = db.Column(db.String, nullable=False, unique=False)
    Feedback = db.Column(db.String, nullable=False, unique=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"


app.secret_key = os.environ["SECRET"]
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ["EMAIL"]
app.config['MAIL_PASSWORD'] = os.environ["PASSWORD"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/Contact', methods=['GET', 'POST'])
def Contact():
    if request.method == 'POST':
        try:
            email = request.form['email']
            msg = request.form['msg']
            mo = Message("Message From Graph_Maker", sender=email,
                         recipients=[os.environ["EMAIL"]])
            mo.body = msg
            mail.send(mo)
            flash('Thanks For Contacting.')
            return redirect(url_for('Contact'))
        except Exception as e:
            print('--->>> ', e)
            flash('Some Error occurred')
            return redirect(url_for('Contact'))
    else:
        return render_template('Contact.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    try:
        if request.method == 'POST':
            num = int(request.form['value_1'])
            session["gname"] = request.form['gname']
            session["xname"] = request.form['xname']
            session["yname"] = request.form['yname']
        return render_template('Jinja2_ForLoop.html', value_to=num)
    except Exception as e:
        print('-->>', e)
        return redirect(url_for('home'))


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        try:
            First_Name = request.form['First_Name']
            Last_Name = request.form['Last_Name']
            Feed_Back = request.form['Feed_Back']
            just1 = FeedBack_form(firtsname=First_Name,
                                  lastname=Last_Name, Feedback=Feed_Back)
            db.session.add(just1)
            db.session.commit()
            flash('we really appreciate your feedback')
            return render_template('feedback.html')
        except Exception as e:
            print(e)
            flash('Some Error occurred')
            return render_template('feedback.html')
    else:
        return render_template('feedback.html')


@app.route('/plotagraph', methods=['GET', 'POST'])
def plotagraph():
    try:
        if request.method == 'POST':
            for i in range((len(request.form.to_dict())//2)):
                x1.append(float(request.form['x'+str(i)]))
                y1.append(float(request.form['y'+str(i)]))
        img = io.BytesIO()
        plt.figure()
        for x, y in zip(x1, y1):
            plt.text(x, y, '({}, {})'.format(x, y))
        plt.title(session.get("gname"), fontdict={
                  'fontname': 'Comic Sans MS', 'fontsize': 20})
        plt.xlabel(session.get("xname"), fontdict={
                   'fontname': 'Comic Sans MS'})
        plt.ylabel(session.get("yname"), fontdict={
                   'fontname': 'Comic Sans MS'})
        plt.plot(x1, y1)
        x1.clear()
        y1.clear()
        plt.savefig(img)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return render_template('graph.html', plot_url=plot_url)
    except Exception as e:
        print(e)
        return redirect(url_for('submit'))


@app.route('/pie_chart', methods=['GET', 'POST'])
def pie_chart():
    if request.method == 'POST':
        try:
            label = []
            size = []
            for i in range((len(request.form.to_dict())//2)):
                label.append((request.form['x'+str(i)]))
                size.append((request.form['y'+str(i)]))

            size = [float(i) for i in size]

            # Generate the pie chart
            plt.figure(figsize=(8, 6))
            plt.pie(size, labels=label, autopct='%1.1f%%', startangle=140)
            # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.axis('equal')
            plt.title('Pie Chart', fontdict={
                      'fontname': 'Comic Sans MS', 'fontsize': 20})

            img = io.BytesIO()
            plt.savefig(img)
            img.seek(0)
            pie_chart_url = base64.b64encode(img.getvalue()).decode()
            return render_template('plot_pie.html', pie_chart_url=pie_chart_url)
        except Exception as e:
            print(e)
            return redirect(url_for('home'))
    else:
        return render_template('pie_chart.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/upcoming_features')
def upcoming_features():
    return render_template('Upcoming_Features.html')

# ROSPL


@app.route('/bar_start', methods=['GET', 'POST'])
def bar_start():
    return render_template('bar_start.html')

@app.route('/hist_start', methods=['GET', 'POST'])
def hist_start():
    return render_template('hist_start.html')


@app.route('/pie_start', methods=['GET', 'POST'])
def pie_start():
    return render_template('pie_start.html')


@app.route('/bar_chart', methods=['GET', 'POST'])
def bar_chart():
    if request.method == 'POST':
        try:
            x_labels = []
            y_values = []
            for i in range((len(request.form.to_dict())//2)):
                x_labels.append((request.form['x'+str(i)]))
                y_values.append(float(request.form['y'+str(i)]))

            print(x_labels, y_values)

            # Generate the bar chart
            plt.figure(figsize=(8, 6))
            plt.bar(x_labels, y_values)
            plt.xlabel('X-axis Label', fontdict={'fontname': 'Comic Sans MS'})
            plt.ylabel('Y-axis Label', fontdict={'fontname': 'Comic Sans MS'})
            plt.title('Bar Chart', fontdict={
                      'fontname': 'Comic Sans MS', 'fontsize': 20})

            img = io.BytesIO()
            plt.savefig(img)
            img.seek(0)
            bar_chart_url = base64.b64encode(img.getvalue()).decode()
            # print(bar_chart_url)
            return render_template('plot_bar.html', bar_chart_url=bar_chart_url)

        except Exception as e:
            print(e)
            return redirect(url_for('home'))
    else:
        return render_template('bar_start.html')


@app.route('/bar_inputs_all', methods=['POST'])
def bar_inputs_all():
    if request.method == 'POST':
        val = int(request.form['bar_input'])
        return render_template("bar_for_loop.html", value_to=val)


@app.route('/pie_inputs_all', methods=['POST'])
def pie_inputs_all():
    if request.method == 'POST':
        val = int(request.form['pie_input'])
        return render_template("pie_for_loop.html", value_to=val)

@app.route('/hist_inputs_all', methods=['POST'])
def hist_inputs_all():
    if request.method == 'POST':
        val = int(request.form['hist_input'])
        return render_template("hist_for_loop.html", value_to=val)


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    if request.method == 'POST':
        try:
            x_labels = []
            y_values = []
            for i in range((len(request.form.to_dict())//2)):
                x_labels.append((request.form['x_label_'+str(i)]))
                y_values.append((request.form['y_value_'+str(i)]))

            # Convert y_values to floats
            y_values = [float(y) for y in y_values]
            x_labels = [float(y) for y in x_labels]

            print(x_labels, y_values)

            # Generate the bar chart
            plt.figure(figsize=(8, 6))
            plt.hist([x_labels, y_values])
            plt.xlabel('X-axis Label', fontdict={'fontname': 'Comic Sans MS'})
            plt.ylabel('Y-axis Label', fontdict={'fontname': 'Comic Sans MS'})
            plt.title('Histogram', fontdict={
                      'fontname': 'Comic Sans MS', 'fontsize': 20})

            img = io.BytesIO()
            plt.savefig(img)
            img.seek(0)
            histogram_url = base64.b64encode(img.getvalue()).decode()
            return render_template('plot_hist.html', histogram_url=histogram_url)

        except Exception as e:
            print(e)
            return redirect(url_for('home'))
    else:
        return render_template('histogram.html')


if __name__ == '__main__':
    app.run(debug=True)
