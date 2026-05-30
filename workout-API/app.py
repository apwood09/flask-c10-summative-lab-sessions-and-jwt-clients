# app.py
# application's RESTful route definitions, logic for user state handling (Flask sessions) and paginated CRUD resources 

from flask import request, session
from flask_restful import Resource 
from config import app, db, api 
from models import User, Workout, user_schema, workout_schema, workouts_schema

# AUTHENTICATION CONTROLLERS 
class Register(Resource): 
    def post(self): 
        data = request.get_json()
        if not data: 
            return {"error": "Missing JSON body"}, 400
        
        try: 
            new_user = User(username=data.get('username'))
            new_user.password_hash = data.get('password')

            db.session.add(new_user)
            db.session.commit()

            # auto-login after registration 
            session['user_id'] = new_user.id
            return user_schema.dump(new_user), 201
        except ValueError as e: 
            return {"error": str(e)}, 422
        except Exception: 
            db.session.rollback()
            return {"error": "Username already exist or database conflict."}, 400

class Login(Resource): 
    def post(self): 
        data = request.get_json()
        if not data: 
            return {"error": "Missing login credentials"}, 400

        user = User.query.filter_by(username=data.get('username')).first()

        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id
            return user_schema.dump(user), 200
        
        return {"error": "Invalid username or password"}, 401

class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id', None)
            return {}, 204
        return {"error": "No active session found"}, 401   

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user_schema.dump(user), 200
        return {"error": "Unauthorized. Please log in."}, 401    

# CRUD CONTROLLS 
class WorkoutIndex(Resource): 
    def get(self): 
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized access"}, 401
        
        # pagination logic 
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 5))
        except ValueError:
            return {"error": "Page query parameters must be integers"}, 400
        
        # query: logged-in user's records
        query = Workout.query.filter_by(user_id=user_id)
        paginated_workouts = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "workouts": workouts_schema.dump(paginated_workouts.items),
            "total_items": paginated_workouts.total,
            "current_page": paginated_workouts.page,
            "total_pages": paginated_workouts.pages,
            "has_next": paginated_workouts.has_next,
            "has_prev": paginated_workouts.has_prev
        }, 200

    def post(self): 
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized access"}, 401
        
        data = request.get_json()
        if not data:
            return {"error": "Missing payload data"}, 400

        try:
            new_workout = Workout(
                title=data.get('title'),
                description=data.get('description'),
                duration_minutes=data.get('duration_minutes'),
                user_id=user_id
            )
            db.session.add(new_workout)
            db.session.commit()
            return workout_schema.dump(new_workout), 201
        except ValueError as e:
            return {"error": str(e)}, 422

class WorkoutById(Resource): 
    def patch(self, id): 
        user_id = session.get('user_id')
        if not user_id: 
            return {"error": "Unauthorized access"}, 401

        # fetch: ensures record belongs to user context
        workout = Workout.query,filter_by(id=id, user_id=user_id).first()
        if not workout: 
            return {"error": "Workout record not found or access denied"}, 404
        
        data = request.get_json()
        try: 
            if 'title' in data: 
                workout.title = data.get('title')
            if 'description' in data: 
                workout.description = data.get('description')
            if 'duration_minutes' in data: 
                workout.duration_minutes = data.get('duratrion_minutes')
            
            db.session.commit()
            return workout_schema.dump(Workout), 200
        except ValueError as e: 
            db.session.rollback()
            return {"error": str(e)}, 422
    
    def delete(self, id): 
        user_id = session.get('user_id')
        if not user_id: 
            return {"error": "Unauthorized access"}, 401
        
        workout = Workout.query.filter_by(id=id, user_id=user_id).first()
        if not workout: 
            return {"error": "Workout record not found or access denied"}, 404
        
        db.session.delete(workout)
        db.session.commit()
        return {}, 204

# ROUTE REGISTRATION 
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(WorkoutIndex, '/workouts')
api.add_resource(WorkoutById, '/workouts/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)