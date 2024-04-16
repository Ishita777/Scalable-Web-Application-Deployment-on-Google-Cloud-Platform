import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage

app = Flask(__name__)

# Get database credentials from environment variables
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')

# Set SQLAlchemy database URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}/{db_name}'
db = SQLAlchemy(app)

# Define your SQLAlchemy model
class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@app.route('/')
def index():
    # Retrieve data from the database and pass it to the template
    data = ExampleModel.query.all()
    return render_template('index.html', data=data)

@app.route('/upload', methods=['POST'])
def upload():
    # Handle file uploads to Cloud Storage
    file = request.files['file']
    if file:
        client = storage.Client()
        bucket_name = os.environ.get('BUCKET_NAME')
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file.filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)
        return 'File uploaded successfully!'
    else:
        return 'No file selected.'

if __name__ == '__main__':
    app.run(debug=True)
