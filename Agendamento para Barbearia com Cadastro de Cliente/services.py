from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from src.models import db, Service
from src.middleware.tenant import get_current_tenant

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
@jwt_required()
def list_services():
    """Listar todos os serviços do tenant"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Parâmetros de filtro
        category = request.args.get('category')
        is_active = request.args.get('is_active', 'true').lower() == 'true'
        
        # Query base
        query = Service.query.filter_by(tenant_id=tenant.id)
        
        # Aplicar filtros
        if category:
            query = query.filter_by(category=category)
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        # Ordenar por nome
        services = query.order_by(Service.name).all()
        
        return jsonify({
            'services': [service.to_dict() for service in services],
            'total': len(services)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@services_bp.route('/', methods=['POST'])
@jwt_required()
def create_service():
    """Criar novo serviço"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['name', 'price', 'duration_minutes']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Criar novo serviço
        service = Service(
            tenant_id=tenant.id,
            name=data['name'],
            description=data.get('description'),
            price=float(data['price']),
            duration_minutes=int(data['duration_minutes']),
            category=data.get('category'),
            image_url=data.get('image_url'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({
            'message': 'Serviço criado com sucesso',
            'service': service.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Dados inválidos: ' + str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Erro de integridade dos dados'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@services_bp.route('/<int:service_id>', methods=['GET'])
@jwt_required()
def get_service(service_id):
    """Obter detalhes de um serviço específico"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        service = Service.query.filter_by(
            id=service_id,
            tenant_id=tenant.id
        ).first()
        
        if not service:
            return jsonify({'error': 'Serviço não encontrado'}), 404
        
        return jsonify({'service': service.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@services_bp.route('/<int:service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    """Atualizar serviço existente"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        service = Service.query.filter_by(
            id=service_id,
            tenant_id=tenant.id
        ).first()
        
        if not service:
            return jsonify({'error': 'Serviço não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'name' in data:
            service.name = data['name']
        if 'description' in data:
            service.description = data['description']
        if 'price' in data:
            service.price = float(data['price'])
        if 'duration_minutes' in data:
            service.duration_minutes = int(data['duration_minutes'])
        if 'category' in data:
            service.category = data['category']
        if 'image_url' in data:
            service.image_url = data['image_url']
        if 'is_active' in data:
            service.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Serviço atualizado com sucesso',
            'service': service.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': 'Dados inválidos: ' + str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@services_bp.route('/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    """Excluir serviço"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        service = Service.query.filter_by(
            id=service_id,
            tenant_id=tenant.id
        ).first()
        
        if not service:
            return jsonify({'error': 'Serviço não encontrado'}), 404
        
        # Verificar se há agendamentos associados
        if service.appointments:
            return jsonify({
                'error': 'Não é possível excluir serviço com agendamentos associados'
            }), 400
        
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({'message': 'Serviço excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@services_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Listar categorias de serviços disponíveis"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Obter categorias únicas dos serviços do tenant
        categories = db.session.query(Service.category).filter_by(
            tenant_id=tenant.id
        ).distinct().all()
        
        categories_list = [cat[0] for cat in categories if cat[0]]
        
        # Adicionar categorias padrão se não existirem
        default_categories = ['corte', 'barba', 'tratamento', 'pacote']
        for cat in default_categories:
            if cat not in categories_list:
                categories_list.append(cat)
        
        return jsonify({'categories': sorted(categories_list)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

