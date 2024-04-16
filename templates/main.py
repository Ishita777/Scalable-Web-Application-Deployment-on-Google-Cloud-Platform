from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://[USERNAME]:[PASSWORD]@[DB_HOST]/[DB_NAME]'
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
        bucket = client.bucket('[BUCKET_NAME]')
        blob = bucket.blob(file.filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)
        return 'File uploaded successfully!'
    else:
        return 'No file selected.'

if __name__ == '__main__':
    app.run(debug=True)
