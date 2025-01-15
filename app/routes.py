from flask import Blueprint, request, make_response
from . import bcrypt, logger, jwt
from .validators import LoginForm, UserRegistrationForm, LogoutForm
from datetime import datetime
from wtforms.validators import ValidationError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt

auth_bp = Blueprint('auth', __name__)

# In-memory storages and ID counter
data_store = []
token_blacklist = set()
next_id = 1000 

@auth_bp.route('/create_user', methods=['POST'])
def create_user():
    try:
        global next_id  
        data = request.get_json()
        form = UserRegistrationForm(data=data, data_store=data_store)
        
        logger.info(f"create_user request received: {data}")
        
        if form.validate():
            time = datetime.now()
            password = bcrypt.generate_password_hash(password=data.get('password')).decode('utf-8')
            
            if any(user['username'] == data.get('username') for user in data_store):
                logger.error({
                    "message": "Validations errors",
                    "errors": {
                        "username": [
                            "Username already being used!"
                        ]
                    }
                })
                return make_response({
                    "success": False,
                    "message": "Validations errors",
                    "errors": {
                        "username": [
                            "Username already being used!"
                        ]
                    }
                }, 409)
            
            
            new_user = {
                "id": next_id,
                "username": data.get('username'),
                "password": password,
                "date_created": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            response_data = {
                "id": new_user["id"],
                "username": new_user["username"],
                "date_created": new_user["date_created"]
            }

            next_id += 1
            data_store.append(new_user)
            
            logger.info("register_client request {}".format(
                {
                    "message": "User registered successfully!",
                    "data": {
                        new_user['id'],
                        new_user['username'],   
                        new_user['date_created'],
                    }
                }
            ))
            
            
            return make_response({
                "success": True,
                "message": "User registered successfully!",
                "data": response_data
            }, 201)
            
        else:
            logger.error({
                "message": "Validations errors",
                "errors": form.errors,
            })
            return make_response({
                "success": False,
                "message": "Validations errors",
                "errors": form.errors
            }, 400)
        
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"error {e} occured on create_user api")
        return make_response({
            "message": "An unexpected error occurred. Please try again later!",
            "code": 500
        }, 500)


@auth_bp.route('/user_login', methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        
        logger.info(f'user_login request {data.get('username')}')
        
        form = LoginForm(data=data)

        if form.validate():
            user = next((u for u in data_store if u['username'] == data.get('username')), None)
            if not user:
                logger.error(f"user_login response: Username '{data.get('username')}' not found!")
                return make_response({
                    "success": False,
                    "message": "Invalid username or password!"
                }, 401)

            if not bcrypt.check_password_hash(user['password'], data.get('password')):
                logger.error(f"user_login response: Invalid password for user '{data.get('username')}'")
                return make_response({
                    "success": False,
                    "message": "Invalid username or password!"
                }, 401)
                
            access_token = create_access_token(identity=data.get('username'))
            
            logger.info(f"user_login response: User {data.get('username')} logged in successfully!")
            return make_response({
                "success": True,
                "message": "Login successful!",
                "access_token": access_token
                }, 200)

        
        logger.info("user_login response: {}".format(
            {
                "message": "Validation errors",
                "errors": form.errors
            }
        ))
        
        return make_response({
            "success": False,
            "message": "Validation errors",
            "errors": form.errors,
            "code": 400}, 400)
        
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"error {e} occured on user_login api")
        return make_response({
            "message": "An unexpected error occurred. Please try again later!",
            "code": 500
        }, 500)
        

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in token_blacklist



@auth_bp.route('/user_logout', methods=['POST'])
@jwt_required()
def user_logout():
    try:
        data = request.get_json()
        
        logger.info(f'user_logout request {data.get('username')}')
        form = LogoutForm(data=data)
        
        if form.validate():  
            user = next((u for u in data_store if u['username'] == data.get('username')), None)
            if not user:
                logger.error(f"user_login response: Username '{data.get('username')}' not found!")
                return make_response({
                    "success": False,
                    "message": "User not found!"
                }, 401)
                  
            jti = get_jwt()["jti"]
            token_blacklist.add(jti)

            logger.info(f"user_logout response: Token revoked {jti}")
            return make_response({
                "success": True,
                "message": "User logged out successfully!"
            }, 200)
        else:
            logger.info("user_login response: {}".format(
            {
                "message": "Validation errors",
                "errors": form.errors
            }
        ))
        return make_response({
            "success": False,
            "message": "Validation errors",
            "errors": form.errors,
            "code": 400}, 400)

    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"Error {e} occurred on user_logout api")
        return make_response({
            "message": "An unexpected error occurred. Please try again later!",
            "code": 500
        }, 500)