
from flask import Flask, jsonify, request, abort

# Initialize the Flask app
app = Flask(__name__)


students = [
    {"id": 1, "name": "Alice", "grade": "B+", "email": "sdaasd@laskflask"},
]

# Define route to handle requests to the root URL ('/')
@app.route('/')
def index():
    return "Welcome to Flask REST API Demo! Try accessing /students to see all users."


# This endpoint returns a 200 OK status and a JSON response to confirm that the service is running.
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200  # Return HTTP status 200 OK


# It is used to map a specific URL (route) to a function in your Flask application.
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200  # 200 is the HTTP status code for 'OK'

# When the client sends a GET request to /users/<id>, this function will return the user with the specified ID.
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    # Using a list comprehension to find the user by ID
    student = next((student for student in students if student['id'] == student_id), None)
    if student is None:
        abort(404)  # If the user is not found, return a 404 error (Not Found)
    return jsonify(student), 200  # Return the user as a JSON object with a 200 status code (OK)

# Route to create a new user (POST request)
# When the client sends a POST request to /users with user data, this function will add the new user to the list.
@app.route('/students', methods=['POST'])
def create_student():
    # If the request body is not in JSON format or if the 'name' field is missing, return a 400 error (Bad Request)
    if not request.json or not 'name' in request.json:
        abort(400)
    
    # Create a new user dictionary. Assign the next available ID by incrementing the highest current ID.
    # If no users exist, the new ID will be 1.
    new_student = {
        'id': students[-1]['id'] + 1 if students else 1,
        'name': request.json['name'],  # The name is provided in the POST request body
        'grade': request.json['grade'],  # The name is provided in the POST request body
        'email': request.json['email'],  # The email is provided in the POST request body
    }
    # Add the new user to the users list
    students.append(new_student)
    return jsonify(new_student), 201  # 201 is the HTTP status code for 'Created'

# Route to update an existing user (PUT request)
# When the client sends a PUT request to /users/<id> with updated user data, this function will update the user.
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    # Find the user by their ID
    student = next((student for student in students if student['id'] == student_id), None)
    if student is None:
        abort(404)  # If the user is not found, return a 404 error (Not Found)
    
    # If the request body is missing or not in JSON format, return a 400 error (Bad Request)
    if not request.json:
        abort(400)
    
    # Update the user's data based on the request body
    # If a field is not provided in the request, keep the existing value
    student['name'] = request.json.get('name', student['name'])
    student['grade'] = request.json.get('grade', student['grade'])
    student['email'] = request.json.get('email', student['email'])

    return jsonify(student), 200  # Return the updated user data with a 200 status code (OK)

# Route to delete a user (DELETE request)
# When the client sends a DELETE request to /users/<id>, this function will remove the user with that ID.
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students  # Reference the global users list
    # Rebuild the users list, excluding the user with the specified ID
    students = [student for student in students if student['id'] != student_id]
    return '', 204  # 204 is the HTTP status code for 'No Content', indicating the deletion was successful

# Debug mode is disabled (set to False).
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)