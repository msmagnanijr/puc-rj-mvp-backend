from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid

app = Flask(__name__)
app.config['DEBUG'] = False

# Initializes the Swagger object for generating and serving the API documentation. 
swagger = Swagger(app, template_file='swagger.yaml')

# Initializes Cross-Origin Resource Sharing (CORS) for the Flask app by allowing all origins to access all routes. 
CORS(app, resources={r'/*': {'origins': '*'}})

class Subject:
    """
    A class that represents a subject.

    :param id: The ID of the subject.
    :param name: The name of the subject.
    :param teacher: The teacher of the subject.
    :param inprogress: Whether the subject is in progress or not.
    :param description: The description of the subject.
    """
    def __init__(self, id, name, teacher, inprogress, description):
        self.id = id
        self.name = name
        self.teacher = teacher
        self.inprogress = inprogress
        self.description = description

class SubjectController:
    """
    A class that manages subjects in the database.
    """
    def __init__(self):
        """
        Initializes the SubjectController.
        """
        self.connection = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="senha"
        )
        self.cursor = self.connection.cursor()
        self.create_table()
        
    def create_table(self):
        """
        Creates the "subjects" table in the database if it doesn't exist.

        Returns:
        --------
            None
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
                            id VARCHAR(255) PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            teacher VARCHAR(255) NOT NULL,
                            inprogress BOOLEAN NOT NULL,
                            description TEXT NOT NULL
                            )''')
        self.connection.commit()
        
    def add_subject(self, subject):
        """
        Adds a new subject to the database.
        
        Parameters:
        -----------
        subject : Subject
            A Subject object containing the information about the subject to be added.
            
        Returns:
        --------
        None
        """
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        subject.id = str(uuid.uuid4())
        cur.execute("INSERT INTO subjects (id, name, teacher, inprogress, description) VALUES (%s, %s, %s, %s, %s)",
                    (subject.id, subject.name, subject.teacher, subject.inprogress, subject.description))
        self.connection.commit()
        cur.close()
        
    def remove_subject(self, subject_id):
        """
        Deletes a subject from the database based on the provided `subject_id`.
        
        Parameters:
        -----------
        subject_id (str): The id of the subject to be deleted.
        
        Returns:
        --------
        bool: True if the subject was deleted successfully, False otherwise.
        """
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM subjects WHERE id=%s", (subject_id,))
        rows_deleted = cur.rowcount
        self.connection.commit()
        cur.close()
        return rows_deleted > 0
    
    def update_subject(self, subject_id, name, teacher, inprogress, description):
        """
        Update a subject with the given subject_id with the new data.

        Parameters:
        -----------
            subject_id (str): The ID of the subject to update.
            name (str): The new name of the subject.
            teacher (str): The new teacher of the subject.
            inprogress (bool): The new status of whether the subject is in progress or not.
            description (str): The new description of the subject.

        Returns:
        --------
            bool: True if the subject was successfully updated, False otherwise.
        """
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("UPDATE subjects SET name=%s, teacher=%s, inprogress=%s, description=%s WHERE id=%s",
                    (name, teacher, inprogress, description, subject_id))
        rows_updated = cur.rowcount
        self.connection.commit()
        cur.close()
        return rows_updated > 0

    def get_all_subjects(self):
        """
        Retrieves all subjects from the subjects table in the database and returns a list of serialized subjects.
        
        Returns:
        --------
        - list of serialized subjects: A list containing all subjects in the subjects table, serialized as Python dictionaries.
        """
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM subjects")
        rows = cur.fetchall()
        cur.close()
        return [self._serialize_subject(row) for row in rows]
    
    def _serialize_subject(self, subject):
        """
        Private method that takes a subject dictionary returned from the database and returns a new dictionary with the keys renamed to match the expected format.

        Parameters:
        -----------
            subject (dict): A dictionary representing a subject returned from the database.

        Returns:
        --------
            dict: A new dictionary with the keys renamed to match the expected format.
        """
        return {
            'id': subject['id'],
            'name': subject['name'],
            'teacher': subject['teacher'],
            'inprogress': subject['inprogress'],
            'description': subject['description']
        }

subject_controller = SubjectController()

@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    """
    GET: Retrieves all the subjects from the database and returns them as a JSON object.
    POST: Adds a new subject to the database using the information from the POST request's body.

    Returns:
    --------
        A JSON object with either the status and a list of subjects, or the status and a success message.
    """
    if request.method == 'GET':
        return jsonify({'status': 'success', 'subjects': subject_controller.get_all_subjects()})
    elif request.method == 'POST':
        data = request.get_json()
        subject = Subject(None, data['name'], data['teacher'], data['inprogress'], data['description'])
        subject_controller.add_subject(subject)
        return jsonify({'status': 'success', 'message': 'Disciplina Adicionada!'})

@app.route('/subjects/<subject_id>', methods=['PUT', 'DELETE'])
def subject(subject_id):
    """
    This function handles the HTTP PUT and DELETE requests for a specific subject.

    Parameters:
    -----------
        subject_id (str): The ID of the subject to update or delete.

    Returns:
    --------
        A JSON response indicating the status of the request and, in some cases, a message.
    """
    if request.method == 'PUT':
        data = request.get_json()
        subject_controller.update_subject(subject_id, data['name'], data['teacher'], data['inprogress'], data['description'])
        return jsonify({'status': 'success', 'message': 'Disciplina Atualizada!'})
    elif request.method == 'DELETE':
        success = subject_controller.remove_subject(subject_id)
        if success:
            return jsonify({'status': 'success', 'message': 'Disciplina Removida!'})
        else:
            return jsonify({'status': 'fail', 'message': 'Disciplina não encontrada!'})
        
if __name__ == '__main__':
    app.run()
