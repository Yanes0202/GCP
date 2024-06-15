import sqlalchemy
from sql.sql_connection import engine
from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    person_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(30))
    last_name = sqlalchemy.Column(sqlalchemy.String(30))


@app.route('/')
def hello_world():
    return 'Hello, World!'


# Endpoint do dodawania osób
@app.route('/add_person', methods=['POST'])
def add_person():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not first_name or not last_name:
        return jsonify({'error': 'Wymagane imię i nazwisko.'}), 400

    Session = sessionmaker(bind=engine)
    session = Session()
    new_person = Person(first_name=first_name, last_name=last_name)
    try:
        session.add(new_person)
        session.commit()
        return jsonify({'message': 'Osoba została dodana do bazy danych!'}), 201
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# Endpoint do pobierania wszystkich osób
@app.route('/persons', methods=['GET'])
def get_persons():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        persons = session.query(Person).all()
        persons_list = [{'person_id': person.person_id, 'first_name': person.first_name, 'last_name': person.last_name} for person in persons]
        return jsonify(persons_list)
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
