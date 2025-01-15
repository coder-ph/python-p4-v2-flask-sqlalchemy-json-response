# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'welcome to the pet directory'}
    return make_response(
        body,
        200
    )


@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    
    if pet:
        response = {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species
        }
        status = 200
        
    else:
        response = {'message': f'pet {id} not found'}
        status = 404
    return make_response(response, status)

@app.route('/species/<string:species>')
def get_by_species(species):
    pets = []
    for pet in Pet.query.filter(Pet.species ==species).all():
        pet_dict = {
            'id':pet.id,
            'name': pet.name,
            'species': pet.species
        }
        pets.append(pet_dict)
    
    body = {
        'count': len(pets),
        'pets': pets
    }
    
    return make_response(body, 200)
if __name__ == '__main__':
    app.run(port=5555, debug=True)
