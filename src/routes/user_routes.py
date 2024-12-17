from flask import  Blueprint, jsonify, request, redirect, url_for, session 
from schemas.user_schemas import UserCreate , UserResponse, DeleteResponse, LoginResponse
from werkzeug.security import generate_password_hash, check_password_hash
from models.entities.User import User
from db_config import db
from pydantic import ValidationError

user_routes = Blueprint('user_routes', __name__, url_prefix='/users')

@user_routes.route('/')
def index():
    return redirect(url_for('register'))


@user_routes.post('/register')
def register():  
    
    # data = request.get_json()

    try:
        user_data = UserCreate(**request.json)

    except ValidationError as e:
        return jsonify ({"error": e.errors()}),400

    existing_user  = User.query.filter_by(username = user_data.username).first()

    if existing_user: 
        return jsonify({"Error": "Usuario ya registrado"}),400
    
    hashed_password = generate_password_hash(user_data.password)
    user = User(
        username=user_data.username, 
        password=hashed_password, 
        number_phone=user_data.number_phone, 
        email=user_data.email, 
        fullname=user_data.fullname, 
        date=user_data.date
    )
    
    try: 
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario registrado correctamente"})
    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar el usuario: {e}")
        return jsonify({"error": "Error al registrar usuario"}), 500
    
    
@user_routes.get('/find-user/<int:user_id>')    

def FindUser(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'Error': 'Usuario no encontrado'}), 400
    
    try: 
        user_data = UserResponse.model_validate(user)
        return jsonify(user_data.model_dump())
    except Exception as e: 
        print(f"Error al serializarel usuario: {e}")
        return jsonify({'error': 'error al procesar datos del usuario'}), 500
    

@user_routes.get('/all-user')
def AllUser():
    users = User.query.all()
    result =[UserResponse.from_orm(user) for user in users]
    return jsonify([user.dict() for user in result])


@user_routes.put('/user-update/<int:user_id>')

def userUpdate(user_id):
    data = request.get_json()
    
    user = User.query.get(user_id)

    if not user: 
        return jsonify({"Error": "Usuario no encontrado"}), 400
        
    # Verifica y actualiza solo si el campo está en los datos entrantes
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    if 'number_phone' in data:
        user.number_phone = data['number_phone']
    if 'email' in data:
        user.email = data['email']
    if 'fullname' in data:
        user.fullname = data['fullname']
    if 'date' in data:
        user.date = data['date']

    try: 
        db.session.commit()
        return jsonify({"message": "Usuario actualizado correctamente", "updated_fields": {key: data[key] for key in data if key in ["username", "number_phone", "email", "fullname", "date"]}})
    
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar el usuario: {e}")
        return jsonify({"Error": "Error al actualizar usuario"}), 400

@user_routes.delete('/user-delete/<int:user_id>')
def userDelete(user_id):
        
        user = User.query.get(user_id)

        if not user: 
            return jsonify({"Error": "Usuario no encontrado"}), 400
        
        try: 
            db.session.delete(user)
            db.session.commit()

            response = DeleteResponse(
                message = "Usuario eliminado correctamente",
                deleted_user_id = user.id
            )
            return jsonify(response.model_dump()), 200
        except Exception as e: 
            db.session.rollback()
            print(f"Error al eliminar el usuario: {e}")
            return jsonify({"error": "Error al eliminar usuario"}), 400
        
@user_routes.post('/login')
def login():
    data = request.get_json()

    login_data = LoginResponse(**data)

    user = User.query.filter_by(email=login_data.email).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    if not check_password_hash(user.password, login_data.password):
        return jsonify({"error": "Clave incorrecta"}),401
    
    session['user_id'] = user.id
    return jsonify({
        'message': "Inicio de session exitoso",
        "user_id" : user.id,
        "username": user.username,
        "email": user.email,

    }), 200

