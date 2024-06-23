from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/khush'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)
class BusFeedback(db.Model):
    __tablename__ = 'bus_feedback'
    id_feedback = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    subject = db.Column(db.String(10), nullable=False)
    message = db.Column(db.String(50), nullable=False)

# Create
@app.route('/insert', methods=['POST'])
def insert_feedback():
    request_data = request.get_json()
    namep = request_data['namek']
    emailp = request_data['emailk']
    subjectp = request_data['subk']
    messagep = request_data['messk']
    print(namep)
    feedback = BusFeedback(name=namep, email=emailp, subject=subjectp, message=messagep)
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"status": "success"})

# Read

@app.route('/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = BusFeedback.query.all()
    feedback_list = []
    for feedback in feedbacks:
        feedback_data = {
            'id': feedback.id_feedback,
            'Name': feedback.name,
            'Email': feedback.email,
            'Subject': feedback.subject,
            'Message': feedback.message
        }
        feedback_list.append(feedback_data)
    return jsonify({"status": 200, "msg": "success", "data": feedback_list})
    
# Update
@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    data = request.get_json()
    print(data)
    user = BusFeedback.query.get(id)
    if user:
        user.name = data['namek']
        user.email = data['emailk']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User not found'}), 404

# Delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedback = BusFeedback.query.get(id)
    print(feedback)
    if feedback:
        db.session.delete(feedback)
        db.session.commit()
        return jsonify({"status": "success"})
    else:
        return jsonify({"error": "Feedback not found"})

if __name__ == '__main__':
    app.run(debug=True)


# import pandas as pd
# from sqlalchemy import create_engine

# # Create a SQLAlchemy engine
# engine = create_engine('mysql+pymysql://root:@localhost:3306/khush')

# @app.route('/feedback_stats', methods=['GET'])
# def feedback_stats():
#     # Read the data into a pandas DataFrame
#     feedbacks = "SELECT * FROM bus_feedback"
#     df = pd.read_sql(feedbacks, engine)
#     feedback_list = []
#     for feedback in feedbacks:
#         feedback_data = {
#             'id': feedback.id_feedback,
#             'Name': feedback.name,
#             'Email': feedback.email,
#             'Subject': feedback.subject,
#             'Message': feedback.message
#         }
#         feedback_list.append(feedback_data)
#     return jsonify({"status": 200, "msg": "success", "data": feedback_list})
   
#     # Perform some data analysis
#     feedback_count = df.shape[0]
#     unique_users = df['email'].nunique()

#     stats = {
#         'total_feedbacks': feedback_count,
#         'unique_users': unique_users
#     }

#     return jsonify({"status": 200, "msg": "success", "data": stats})

