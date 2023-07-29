from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ajax import handle_uploaded_file


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://ghjk_user:password@localhost/ghjk34'

db = SQLAlchemy(app)


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(49), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)


@app.route('/')
def home():
    """Главная страница"""
    return render_template('home.html')


@app.route('/result/')
def result():
    """Страница записей"""
    records = db.session.query(Record).all()
    return render_template('result.html', records=records)


@app.route('/ajax/upload-file/', methods=['POST'])
def upload_file():
    """Загрузка json файла"""
    if request.method == 'POST':
        records = handle_uploaded_file(request.files['file'])
        if records['status'] == 'ok':
            records = records['records']
            for record in records:
                db.session.add(Record(name=record['name'], date=record['date']))
            db.session.commit()
            return jsonify({'status': 'ok'})
        else:
            return jsonify(records)
    return jsonify({'status': 'error'})


if __name__ == '__main__':
    app.run()
