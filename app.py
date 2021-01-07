import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)

# Config
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Question

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'question', 'create_at')

# Init schema
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)

# Create a Question
@app.route('/question', methods=['POST'])
def add_question():
    question = request.json['question']

    new_question = Question(question)

    db.session.add(new_question)
    db.session.commit()

    return question_schema.jsonify(new_question)

# Get all Questions
@app.route('/question', methods=['GET'])
def get_questions():
    all_questions = Question.query.all()
    result = questions_schema.dump(all_questions)

    return jsonify(result)

# Get single Question
@app.route('/question/<id>', methods=['GET'])
def get_question(id):
    question = Question.query.get(id)

    return question_schema.jsonify(question)

# Update a Question
@app.route('/question/<id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get(id)

    new_question = request.json['question']

    question.question = new_question

    db.session.commit()

    return question_schema.jsonify(question)

# Delete Question
@app.route('/question/<id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)

    db.session.delete(question)
    db.session.commit()

    return question_schema.jsonify(question)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)