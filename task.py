from flask import Flask, app, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an engine
engine = create_engine('sqlite:///user.db', echo=True)

app = Flask(__name__)
#define base
Base = declarative_base()

# Define table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    subject = Column(String(50))
    message = Column(String(50))



# Create all tables
Base.metadata.create_all(engine)

#create session
Session = sessionmaker(bind=engine)
session = Session()

#api for insert
@app.route('/insert', methods=['POST'])
def insert_feedback():
    request_data = request.get_json()
    namep = request_data['name']
    emailp = request_data['email']
    subjectp = request_data['subject']
    messagep = request_data['message']

    data = User(name=namep, email=emailp, subject=subjectp, message=messagep)
    session.add(data)
    session.commit()
    return jsonify({"status": "success"})

# api for update
@app.route('/update', methods=['POST'])
def update_feedback():
    request_data = request.get_json()
    name = request_data['name']
    email = request_data['email']
    session.query(User).filter(User.name==name).update({'email':email})
    session.commit()
    return jsonify({"status": "success"})

#api for delete
@app.route('/delete', methods=['POST'])
def delete_feedback():
    request_data = request.get_json()
    name = request_data['name']
    session.query(User).filter(User.name==name).delete()
    session.commit()
    return jsonify({"status": 200, "msg": "success", "data": ""})

#api for get all data
@app.route('/get_data', methods=['GET'])
def get_data():
    user_data = session.query(User).all()
    user_list = []
    for user in user_data:
        user_data1 = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'subject': user.subject,
            'message': user.message
        }
        user_list.append(user_data1)
    return jsonify({"status": 200, "msg": "success", "data": user_list})
    

if __name__ == '__main__':
    app.run(debug=True)
