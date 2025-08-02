from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime
import os
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DATABASE = 'database.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create clientes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create agendamentos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data_agendamento DATE NOT NULL,
            horario TIME NOT NULL,
            status TEXT DEFAULT 'agendado',
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def validate_email(email):
    """Validate email format"""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone format"""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it has 10 or 11 digits (Brazilian phone format)
    return len(digits_only) in [10, 11]

def send_confirmation_email(cliente_data, agendamento_data):
    """Send confirmation email to client and notification to owner"""
    try:
        # Email configuration (you would need to set up SMTP credentials)
        # For demo purposes, we'll just log the email content
        
        email_content = f"""
        Olá {cliente_data['nome']},
        
        Seu agendamento foi confirmado com sucesso!
        
        Detalhes do agendamento:
        - Data: {agendamento_data['data_agendamento']}
        - Horário: {agendamento_data['horario']}
        - Telefone: {cliente_data['telefone']}
        
        Aguardamos você na Barbearia Clássica!
        
        Atenciosamente,
        Equipe Barbearia Clássica
        """
        
        print(f"Email enviado para {cliente_data['email']}:")
        print(email_content)
        
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/agendamento')
def agendamento():
    """Agendamento page"""
    return render_template('agendamento.html')

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    """API endpoint for client registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['nome', 'email', 'telefone']):
            return jsonify({'error': 'Campos obrigatórios: nome, email, telefone'}), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Email inválido'}), 400
        
        # Validate phone format
        if not validate_phone(data['telefone']):
            return jsonify({'error': 'Telefone inválido'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        existing_client = cursor.execute(
            'SELECT id FROM clientes WHERE email = ?', (data['email'],)
        ).fetchone()
        
        if existing_client:
            conn.close()
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Insert new client
        cursor.execute(
            'INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)',
            (data['nome'], data['email'], data['telefone'])
        )
        
        client_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Cliente cadastrado com sucesso',
            'client_id': client_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/agendamento', methods=['POST'])
def criar_agendamento():
    """API endpoint for creating appointments"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['nome', 'email', 'telefone', 'data', 'horario']
        if not all(key in data for key in required_fields):
            return jsonify({'error': 'Campos obrigatórios: nome, email, telefone, data, horario'}), 400
        
        # Validate email and phone
        if not validate_email(data['email']):
            return jsonify({'error': 'Email inválido'}), 400
        
        if not validate_phone(data['telefone']):
            return jsonify({'error': 'Telefone inválido'}), 400
        
        # Validate date format and ensure it's not in the past
        try:
            appointment_date = datetime.datetime.strptime(data['data'], '%Y-%m-%d').date()
            if appointment_date < datetime.date.today():
                return jsonify({'error': 'Data não pode ser no passado'}), 400
        except ValueError:
            return jsonify({'error': 'Formato de data inválido (use YYYY-MM-DD)'}), 400
        
        # Validate time format
        try:
            appointment_time = datetime.datetime.strptime(data['horario'], '%H:%M').time()
        except ValueError:
            return jsonify({'error': 'Formato de horário inválido (use HH:MM)'}), 400
        
        # Check if it's not Sunday
        if appointment_date.weekday() == 6:  # Sunday = 6
            return jsonify({'error': 'Não atendemos aos domingos'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if client exists, if not create
        client = cursor.execute(
            'SELECT id FROM clientes WHERE email = ?', (data['email'],)
        ).fetchone()
        
        if client:
            client_id = client['id']
            # Update client info if needed
            cursor.execute(
                'UPDATE clientes SET nome = ?, telefone = ? WHERE id = ?',
                (data['nome'], data['telefone'], client_id)
            )
        else:
            # Create new client
            cursor.execute(
                'INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)',
                (data['nome'], data['email'], data['telefone'])
            )
            client_id = cursor.lastrowid
        
        # Check if time slot is available
        existing_appointment = cursor.execute(
            'SELECT id FROM agendamentos WHERE data_agendamento = ? AND horario = ? AND status = "agendado"',
            (data['data'], data['horario'])
        ).fetchone()
        
        if existing_appointment:
            conn.close()
            return jsonify({'error': 'Horário já ocupado'}), 400
        
        # Create appointment
        cursor.execute(
            'INSERT INTO agendamentos (cliente_id, data_agendamento, horario) VALUES (?, ?, ?)',
            (client_id, data['data'], data['horario'])
        )
        
        appointment_id = cursor.lastrowid
        conn.commit()
        
        # Get client data for email
        client_data = cursor.execute(
            'SELECT * FROM clientes WHERE id = ?', (client_id,)
        ).fetchone()
        
        conn.close()
        
        # Send confirmation email
        agendamento_data = {
            'data_agendamento': data['data'],
            'horario': data['horario']
        }
        
        send_confirmation_email(dict(client_data), agendamento_data)
        
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'appointment_id': appointment_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/horarios-disponiveis/<data>')
def horarios_disponiveis(data):
    """API endpoint to get available time slots for a specific date"""
    try:
        # Validate date format
        try:
            appointment_date = datetime.datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido (use YYYY-MM-DD)'}), 400
        
        # Check if it's not in the past
        if appointment_date < datetime.date.today():
            return jsonify({'available_times': []}), 200
        
        # Check if it's not Sunday
        if appointment_date.weekday() == 6:  # Sunday = 6
            return jsonify({'available_times': []}), 200
        
        # Define available times based on day of week
        if appointment_date.weekday() == 5:  # Saturday = 5
            all_times = [
                '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
                '11:00', '11:30', '14:00', '14:30', '15:00', '15:30',
                '16:00', '16:30'
            ]
        else:  # Monday to Friday
            all_times = [
                '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
                '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
                '17:00', '17:30', '18:00', '18:30'
            ]
        
        # Get booked times
        conn = get_db_connection()
        cursor = conn.cursor()
        
        booked_times = cursor.execute(
            'SELECT horario FROM agendamentos WHERE data_agendamento = ? AND status = "agendado"',
            (data,)
        ).fetchall()
        
        conn.close()
        
        # Convert booked times to list
        booked_times_list = [row['horario'] for row in booked_times]
        
        # Filter available times
        available_times = [time for time in all_times if time not in booked_times_list]
        
        return jsonify({'available_times': available_times}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/agendamentos')
def listar_agendamentos():
    """API endpoint to list all appointments (for admin use)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        agendamentos = cursor.execute('''
            SELECT a.id, a.data_agendamento, a.horario, a.status, a.data_criacao,
                   c.nome, c.email, c.telefone
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            ORDER BY a.data_agendamento DESC, a.horario DESC
        ''').fetchall()
        
        conn.close()
        
        # Convert to list of dictionaries
        agendamentos_list = []
        for agendamento in agendamentos:
            agendamentos_list.append({
                'id': agendamento['id'],
                'data_agendamento': agendamento['data_agendamento'],
                'horario': agendamento['horario'],
                'status': agendamento['status'],
                'data_criacao': agendamento['data_criacao'],
                'cliente': {
                    'nome': agendamento['nome'],
                    'email': agendamento['email'],
                    'telefone': agendamento['telefone']
                }
            })
        
        return jsonify({'agendamentos': agendamentos_list}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)

