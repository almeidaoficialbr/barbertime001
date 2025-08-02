from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from src.models import db, Client
from src.middleware.tenant import get_current_tenant
from datetime import datetime
import json

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/', methods=['GET'])
@jwt_required()
def list_clients():
    """Listar todos os clientes do tenant"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Parâmetros de filtro e paginação
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        search = request.args.get('search', '').strip()
        is_active = request.args.get('is_active', 'true').lower() == 'true'
        
        # Query base
        query = Client.query.filter_by(tenant_id=tenant.id)
        
        # Aplicar filtros
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        # Busca por nome, email ou telefone
        if search:
            query = query.filter(
                or_(
                    Client.name.ilike(f'%{search}%'),
                    Client.email.ilike(f'%{search}%'),
                    Client.phone.ilike(f'%{search}%')
                )
            )
        
        # Ordenar por nome
        query = query.order_by(Client.name)
        
        # Paginação
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'clients': [client.to_dict() for client in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/', methods=['POST'])
@jwt_required()
def create_client():
    """Criar novo cliente"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['name', 'phone']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se telefone já existe
        existing_client = Client.query.filter_by(
            tenant_id=tenant.id,
            phone=data['phone']
        ).first()
        if existing_client:
            return jsonify({'error': 'Telefone já cadastrado para outro cliente'}), 400
        
        # Verificar se email já existe (se fornecido)
        if data.get('email'):
            existing_email = Client.query.filter_by(
                tenant_id=tenant.id,
                email=data['email']
            ).first()
            if existing_email:
                return jsonify({'error': 'Email já cadastrado para outro cliente'}), 400
        
        # Processar data de nascimento
        birth_date = None
        if data.get('birth_date'):
            try:
                birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        # Processar preferências (JSON)
        preferences = data.get('preferences', {})
        if isinstance(preferences, dict):
            preferences = json.dumps(preferences)
        
        # Criar novo cliente
        client = Client(
            tenant_id=tenant.id,
            name=data['name'],
            email=data.get('email'),
            phone=data['phone'],
            birth_date=birth_date,
            notes=data.get('notes'),
            preferences=preferences,
            is_active=data.get('is_active', True)
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'message': 'Cliente criado com sucesso',
            'client': client.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Dados inválidos: ' + str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Erro de integridade dos dados'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    """Obter detalhes de um cliente específico"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        client = Client.query.filter_by(
            id=client_id,
            tenant_id=tenant.id
        ).first()
        
        if not client:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        # Incluir histórico de agendamentos
        client_data = client.to_dict()
        client_data['appointments_history'] = [
            {
                'id': apt.id,
                'appointment_date': apt.appointment_date.isoformat(),
                'service_name': apt.service.name if apt.service else None,
                'staff_name': apt.staff_member.name if apt.staff_member else None,
                'status': apt.status.value if apt.status else None,
                'final_price': apt.final_price
            }
            for apt in sorted(client.appointments, key=lambda x: x.appointment_date, reverse=True)
        ]
        
        return jsonify({'client': client_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    """Atualizar cliente existente"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        client = Client.query.filter_by(
            id=client_id,
            tenant_id=tenant.id
        ).first()
        
        if not client:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        data = request.get_json()
        
        # Verificar se telefone já existe (se sendo alterado)
        if 'phone' in data and data['phone'] != client.phone:
            existing_client = Client.query.filter_by(
                tenant_id=tenant.id,
                phone=data['phone']
            ).first()
            if existing_client:
                return jsonify({'error': 'Telefone já cadastrado para outro cliente'}), 400
        
        # Verificar se email já existe (se sendo alterado)
        if 'email' in data and data['email'] != client.email:
            existing_email = Client.query.filter_by(
                tenant_id=tenant.id,
                email=data['email']
            ).first()
            if existing_email:
                return jsonify({'error': 'Email já cadastrado para outro cliente'}), 400
        
        # Atualizar campos permitidos
        if 'name' in data:
            client.name = data['name']
        if 'email' in data:
            client.email = data['email']
        if 'phone' in data:
            client.phone = data['phone']
        if 'birth_date' in data:
            if data['birth_date']:
                try:
                    client.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
            else:
                client.birth_date = None
        if 'notes' in data:
            client.notes = data['notes']
        if 'preferences' in data:
            preferences = data['preferences']
            if isinstance(preferences, dict):
                preferences = json.dumps(preferences)
            client.preferences = preferences
        if 'is_active' in data:
            client.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Cliente atualizado com sucesso',
            'client': client.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': 'Dados inválidos: ' + str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    """Excluir cliente"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        client = Client.query.filter_by(
            id=client_id,
            tenant_id=tenant.id
        ).first()
        
        if not client:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        # Verificar se há agendamentos futuros
        future_appointments = [apt for apt in client.appointments 
                             if apt.appointment_date > datetime.utcnow()]
        
        if future_appointments:
            return jsonify({
                'error': 'Não é possível excluir cliente com agendamentos futuros'
            }), 400
        
        db.session.delete(client)
        db.session.commit()
        
        return jsonify({'message': 'Cliente excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/<int:client_id>/appointments', methods=['GET'])
@jwt_required()
def get_client_appointments(client_id):
    """Obter histórico de agendamentos de um cliente"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        client = Client.query.filter_by(
            id=client_id,
            tenant_id=tenant.id
        ).first()
        
        if not client:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        # Parâmetros de filtro
        status = request.args.get('status')
        limit = int(request.args.get('limit', 50))
        
        # Query de agendamentos
        appointments = client.appointments
        
        # Filtrar por status se especificado
        if status:
            appointments = [apt for apt in appointments if apt.status.value == status]
        
        # Ordenar por data (mais recentes primeiro) e limitar
        appointments = sorted(appointments, key=lambda x: x.appointment_date, reverse=True)[:limit]
        
        return jsonify({
            'client_id': client_id,
            'client_name': client.name,
            'appointments': [apt.to_dict() for apt in appointments],
            'total': len(appointments)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clients_bp.route('/search', methods=['GET'])
@jwt_required()
def search_clients():
    """Buscar clientes por termo"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        search_term = request.args.get('q', '').strip()
        limit = int(request.args.get('limit', 10))
        
        if not search_term:
            return jsonify({'clients': []}), 200
        
        # Buscar por nome, email ou telefone
        clients = Client.query.filter_by(
            tenant_id=tenant.id,
            is_active=True
        ).filter(
            or_(
                Client.name.ilike(f'%{search_term}%'),
                Client.email.ilike(f'%{search_term}%'),
                Client.phone.ilike(f'%{search_term}%')
            )
        ).order_by(Client.name).limit(limit).all()
        
        return jsonify({
            'clients': [client.to_dict() for client in clients],
            'total': len(clients)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

