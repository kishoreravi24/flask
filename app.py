from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:P@ssword1@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zkxepbedjsaejn:53af53290a947781e47e7d6ed67f9efe32758c859db26aa9a88eb20b7d577b0d@ec2-54-87-112-29.compute-1.amazonaws.com:5432/d55sg0k06hrv3s'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#create model
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer,primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self,customer,dealer,rating,comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer,dealer,rating,comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message = 'Please enter the required fields')
        
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer,dealer,rating,comments)
            db.session.add(data)
            db.session.commit()
        else:
            return render_template('index.html', message = 'You are already submitted the feedback')


        return render_template('success.html')

if __name__ == '__main__':
    app.run()