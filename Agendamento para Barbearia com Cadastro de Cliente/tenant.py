from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models import db, Tenant, TenantConfig, PlatformUser
from src.middleware import get_current_tenant, require_tenant

tenant_bp = Blueprint('tenant', __name__)

def require_tenant_admin():
    """Decorator para verificar se usuário é admin do tenant"""
    def decorator(f):
        from functools import wraps
        
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_data = get_jwt_identity()
            
            if current_user_data['role'] not in ['super_admin', 'tenant_admin']:
                return jsonify({'error': 'Acesso negado'}), 403
            
            # Se não for super admin, verificar se pertence ao tenant
            if current_user_data['role'] != 'super_admin':
                tenant = get_current_tenant()
                if not tenant or current_user_data['tenant_id'] != tenant.id:
                    return jsonify({'error': 'Acesso negado'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

@tenant_bp.route('/config', methods=['GET'])
@require_tenant_admin()
@require_tenant
def get_tenant_config():
    """Obter configurações do tenant atual"""
    try:
        tenant = get_current_tenant()
        
        if not tenant.config:
            # Criar configuração padrão se não existir
            config = TenantConfig(tenant_id=tenant.id)
            db.session.add(config)
            db.session.commit()
            tenant.config = config
        
        return jsonify({
            'tenant': tenant.to_dict(),
            'config': tenant.config.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenant_bp.route('/config', methods=['PUT'])
@require_tenant_admin()
@require_tenant
def update_tenant_config():
    """Atualizar configurações do tenant"""
    try:
        tenant = get_current_tenant()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Obter ou criar configuração
        config = tenant.config
        if not config:
            config = TenantConfig(tenant_id=tenant.id)
            db.session.add(config)
        
        # Atualizar campos permitidos
        allowed_fields = [
            'business_name', 'description', 'address', 'city', 'state', 'zip_code',
            'phone', 'email', 'website', 'instagram', 'facebook', 'whatsapp',
            'primary_color', 'secondary_color', 'accent_color', 'opening_hours', 'policies'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(config, field, data[field])
        
        # Atualizar nome do tenant se fornecido
        if 'business_name' in data:
            tenant.name = data['business_name']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Configurações atualizadas com sucesso',
            'tenant': tenant.to_dict(),
            'config': config.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenant_bp.route('/logo', methods=['POST'])
@require_tenant_admin()
@require_tenant
def upload_logo():
    """Upload do logo do tenant"""
    try:
        tenant = get_current_tenant()
        
        if 'logo' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['logo']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Validar tipo de arquivo
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
        
        # Salvar arquivo (implementação simplificada)
        # Em produção, usar serviço de storage como AWS S3
        import os
        from werkzeug.utils import secure_filename
        
        filename = secure_filename(f"logo_{tenant.slug}_{file.filename}")
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Atualizar configuração
        config = tenant.config
        if not config:
            config = TenantConfig(tenant_id=tenant.id)
            db.session.add(config)
        
        config.logo_url = f'/static/uploads/{filename}'
        db.session.commit()
        
        return jsonify({
            'message': 'Logo atualizado com sucesso',
            'logo_url': config.logo_url
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenant_bp.route('/staff', methods=['GET'])
@require_tenant_admin()
@require_tenant
def get_staff():
    """Listar funcionários do tenant"""
    try:
        tenant = get_current_tenant()
        
        staff = PlatformUser.query.filter_by(
            tenant_id=tenant.id,
            role='tenant_user'
        ).all()
        
        return jsonify({
            'staff': [user.to_dict() for user in staff]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenant_bp.route('/staff', methods=['POST'])
@require_tenant_admin()
@require_tenant
def create_staff():
    """Criar novo funcionário"""
    try:
        tenant = get_current_tenant()
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['email', 'password', 'first_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Verificar se email já existe
        if PlatformUser.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Este email já está cadastrado'}), 400
        
        # Criar funcionário
        staff = PlatformUser.create_tenant_user(
            tenant_id=tenant.id,
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data.get('last_name')
        )
        
        db.session.add(staff)
        db.session.commit()
        
        return jsonify({
            'message': 'Funcionário criado com sucesso',
            'staff': staff.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenant_bp.route('/staff/<int:staff_id>', methods=['PUT'])
@require_tenant_admin()
@require_tenant
def update_staff(staff_id):
    """Atualizar funcionário"""
    try:
        tenant = get_current_tenant()
        data = request.get_json()
        
        staff = PlatformUser.query.filter_by(
            id=staff_id,
            tenant_id=tenant.id,
            role='tenant_user'
        ).first()
        
        if not staff:
            return jsonify({'error': 'Funcionário não encontrado'}), 404
        
        # Atualizar campos permitidos
        allowed_fields = ['first_name', 'last_name', 'status']
        for field in allowed_fields:
            if field in data:
                setattr(staff, field, data[field])
        
        # Atualizar senha se fornecida
        if 'password' in data and data['password']:
            staff.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Funcionário atualizado com sucesso',
            'staff': staff.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenant_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
@require_tenant_admin()
@require_tenant
def delete_staff(staff_id):
    """Remover funcionário"""
    try:
        tenant = get_current_tenant()
        
        staff = PlatformUser.query.filter_by(
            id=staff_id,
            tenant_id=tenant.id,
            role='tenant_user'
        ).first()
        
        if not staff:
            return jsonify({'error': 'Funcionário não encontrado'}), 404
        
        # Soft delete - apenas desativar
        staff.status = 'inactive'
        db.session.commit()
        
        return jsonify({
            'message': 'Funcionário removido com sucesso'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@tenant_bp.route('/dashboard', methods=['GET'])
@require_tenant_admin()
@require_tenant
def get_dashboard():
    """Obter dados do dashboard do tenant"""
    try:
        tenant = get_current_tenant()
        
        # Estatísticas básicas (implementação simplificada)
        total_staff = PlatformUser.query.filter_by(
            tenant_id=tenant.id,
            role='tenant_user',
            status='active'
        ).count()
        
        dashboard_data = {
            'tenant': tenant.to_dict(),
            'stats': {
                'total_staff': total_staff,
                'total_appointments_today': 0,  # Implementar quando tiver modelo de agendamentos
                'total_clients': 0,  # Implementar quando tiver modelo de clientes
                'revenue_today': 0.0  # Implementar quando tiver modelo de pagamentos
            }
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

