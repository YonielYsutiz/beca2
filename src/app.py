from flask import Flask, jsonify, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_session import Session
from config import config
from db_config import db
from models.entities.User import User 

app = Flask (__name__)

app.config['SESSION_TYPE'] = 'sqlalchemy'  # Usa SQLAlchemy para las sesiones
app.config['SESSION_USE_SIGNER'] = True    # Asegurar la firma de las cookies
app.config['SESSION_SQLALCHEMY_TABLE'] = 'flask_sessions'
app.config['SESSION_SQLALCHEMY'] = db      # Define la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/beca2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

Session(app)

@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET','POST', 'PUT', 'DELETE'])
def register():
    if request.method == 'POST':  
        data = request.get_json()

        if not data or 'username' not in data or "password" not in data:
            return jsonify({"error": "faltan campos obligatorios"}), 400
        
        username = data.get('username')
        password = generate_password_hash(data.get('password'))
        number_phone = data.get('number_phone')
        email = data.get('email')
        fullname = data.get('fullname')
        age = data.get('age')
        
        existing_user  = User.query.filter_by(username = username).first()

        if existing_user: 
            return jsonify({"Error": "Usuario ya registrado"}),400
            
        user = User(username=username, password=password, number_phone=number_phone, email=email, fullname=fullname, age=age)
        
        try: 
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "Usuario registrado correctamente"})
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar el usuario: {e}")
            return jsonify({"error": "Error al registrar usuario"}), 500
    
    elif request.method == 'GET':
        user = User.query.all()
        result = []
        for user in user: 
            user_data = {
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname,
                'number_phone': user.number_phone,
                'email': user.email,
                'age': user.age
            }
            result.append(user_data)
        return jsonify(result)
    
    elif request.method == 'PUT':
        data = request.get_json()
        user_id = data.get('id')
        
        user = User.query.get(user_id)

        if not user: 
            return jsonify({"Error": "Usuario no encontrado"}), 400
        
        user.username = data.get('username', user.username)
        user.password = generate_password_hash(data.get('password', user.password))
        user.number_phone = data.get('number_phone', user.number_phone)
        user.email = data.get('email', user.email)
        user.fullname = data.get('fullname', user.fullname)
        user.age = data.get('age', user.age)

        try: 
            db.session.commit()
            return jsonify({"message": "Usuario actualizado correctamente"})
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar el usuario: {e}")
            return jsonify({"Error": "Error al actualizar usuario"}), 400
    
    elif request.method == 'DELETE':
        data = request.get_json()
        user_id = data.get('id')

        user = User.query.get(user_id)

        if not user: 
            return jsonify({"Error": "Usuario no encontrado"}), 400
        
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "Usuario eliminado correctamente"})
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar el usuario: {e}")
            return jsonify({"error": "Error al eliminar usuario"}), 400
        


if __name__ == '__main__': 
    app.config.from_object(config['development'])
    with app.app_context():
        db.create_all()
    app.run()