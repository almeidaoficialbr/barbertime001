from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from src.models import db, TenantConfig
from src.middleware.tenant import get_current_tenant
import json
import re

customization_bp = Blueprint('customization', __name__)

def validate_color(color):
    """Validar formato de cor hexadecimal"""
    if not color:
        return False
    
    # Remover # se presente
    color = color.lstrip('#')
    
    # Verificar se é um hex válido de 6 caracteres
    if len(color) != 6:
        return False
    
    try:
        int(color, 16)
        return True
    except ValueError:
        return False

def validate_url(url):
    """Validar formato de URL"""
    if not url:
        return True  # URLs vazias são permitidas
    
    url_pattern = re.compile(
        r'^https?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domínio
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # porta opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def validate_phone(phone):
    """Validar formato de telefone brasileiro"""
    if not phone:
        return True  # Telefones vazios são permitidos
    
    # Remover caracteres não numéricos
    phone_digits = re.sub(r'\D', '', phone)
    
    # Verificar se tem 10 ou 11 dígitos (telefone brasileiro)
    return len(phone_digits) in [10, 11]

@customization_bp.route('/theme', methods=['GET'])
@jwt_required()
def get_theme():
    """Obter configurações de tema do tenant"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        
        if not config:
            # Retornar configurações padrão
            return jsonify({
                'theme': {
                    'primary_color': '#1A1A1A',
                    'secondary_color': '#B8860B',
                    'accent_color': '#8B0000',
                    'logo_url': None
                }
            }), 200
        
        return jsonify({
            'theme': {
                'primary_color': config.primary_color,
                'secondary_color': config.secondary_color,
                'accent_color': config.accent_color,
                'logo_url': config.logo_url
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customization_bp.route('/theme', methods=['PUT'])
@jwt_required()
def update_theme():
    """Atualizar configurações de tema do tenant"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        data = request.get_json()
        
        # Validar cores se fornecidas
        if 'primary_color' in data and not validate_color(data['primary_color']):
            return jsonify({'error': 'Cor primária inválida'}), 400
        
        if 'secondary_color' in data and not validate_color(data['secondary_color']):
            return jsonify({'error': 'Cor secundária inválida'}), 400
        
        if 'accent_color' in data and not validate_color(data['accent_color']):
            return jsonify({'error': 'Cor de destaque inválida'}), 400
        
        # Obter ou criar configuração
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        if not config:
            config = TenantConfig(tenant_id=tenant.id)
            db.session.add(config)
        
        # Atualizar campos fornecidos
        if 'primary_color' in data:
            config.primary_color = f"#{data['primary_color'].lstrip('#')}"
        
        if 'secondary_color' in data:
            config.secondary_color = f"#{data['secondary_color'].lstrip('#')}"
        
        if 'accent_color' in data:
            config.accent_color = f"#{data['accent_color'].lstrip('#')}"
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tema atualizado com sucesso',
            'theme': {
                'primary_color': config.primary_color,
                'secondary_color': config.secondary_color,
                'accent_color': config.accent_color,
                'logo_url': config.logo_url
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customization_bp.route('/business-info', methods=['GET'])
@jwt_required()
def get_business_info():
    """Obter informações do negócio"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        
        business_info = {
            'business_name': config.business_name if config else None,
            'description': config.description if config else None,
            'address': config.address if config else None,
            'city': config.city if config else 'Brejo',
            'state': config.state if config else 'MA',
            'zip_code': config.zip_code if config else None,
            'phone': config.phone if config else None,
            'email': config.email if config else None,
            'website': config.website if config else None,
            'instagram': config.instagram if config else None,
            'facebook': config.facebook if config else None,
            'whatsapp': config.whatsapp if config else None
        }
        
        return jsonify({'business_info': business_info}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customization_bp.route('/business-info', methods=['PUT'])
@jwt_required()
def update_business_info():
    """Atualizar informações do negócio"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        data = request.get_json()
        
        # Validações
        if 'website' in data and data['website'] and not validate_url(data['website']):
            return jsonify({'error': 'URL do website inválida'}), 400
        
        if 'phone' in data and not validate_phone(data['phone']):
            return jsonify({'error': 'Formato de telefone inválido'}), 400
        
        if 'whatsapp' in data and not validate_phone(data['whatsapp']):
            return jsonify({'error': 'Formato de WhatsApp inválido'}), 400
        
        if 'email' in data and data['email']:
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(data['email']):
                return jsonify({'error': 'Formato de email inválido'}), 400
        
        # Obter ou criar configuração
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        if not config:
            config = TenantConfig(tenant_id=tenant.id)
            db.session.add(config)
        
        # Atualizar campos fornecidos
        allowed_fields = [
            'business_name', 'description', 'address', 'city', 'state', 
            'zip_code', 'phone', 'email', 'website', 'instagram', 
            'facebook', 'whatsapp'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(config, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Informações atualizadas com sucesso',
            'business_info': {
                'business_name': config.business_name,
                'description': config.description,
                'address': config.address,
                'city': config.city,
                'state': config.state,
                'zip_code': config.zip_code,
                'phone': config.phone,
                'email': config.email,
                'website': config.website,
                'instagram': config.instagram,
                'facebook': config.facebook,
                'whatsapp': config.whatsapp
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customization_bp.route('/opening-hours', methods=['GET'])
@jwt_required()
def get_opening_hours():
    """Obter horários de funcionamento"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        
        # Horários padrão
        default_hours = {
            'monday': {'open': '08:00', 'close': '18:00', 'closed': False},
            'tuesday': {'open': '08:00', 'close': '18:00', 'closed': False},
            'wednesday': {'open': '08:00', 'close': '18:00', 'closed': False},
            'thursday': {'open': '08:00', 'close': '18:00', 'closed': False},
            'friday': {'open': '08:00', 'close': '18:00', 'closed': False},
            'saturday': {'open': '08:00', 'close': '16:00', 'closed': False},
            'sunday': {'open': '08:00', 'close': '16:00', 'closed': True}
        }
        
        opening_hours = default_hours
        if config and config.opening_hours:
            try:
                saved_hours = json.loads(config.opening_hours)
                opening_hours.update(saved_hours)
            except json.JSONDecodeError:
                pass  # Usar horários padrão se JSON inválido
        
        return jsonify({'opening_hours': opening_hours}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customization_bp.route('/opening-hours', methods=['PUT'])
@jwt_required()
def update_opening_hours():
    """Atualizar horários de funcionamento"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        data = request.get_json()
        opening_hours = data.get('opening_hours', {})
        
        # Validar formato dos horários
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
        
        for day, hours in opening_hours.items():
            if day not in valid_days:
                return jsonify({'error': f'Dia inválido: {day}'}), 400
            
            if not isinstance(hours, dict):
                return jsonify({'error': f'Formato inválido para {day}'}), 400
            
            if not hours.get('closed', False):
                if 'open' not in hours or 'close' not in hours:
                    return jsonify({'error': f'Horários de abertura e fechamento obrigatórios para {day}'}), 400
                
                if not time_pattern.match(hours['open']) or not time_pattern.match(hours['close']):
                    return jsonify({'error': f'Formato de horário inválido para {day}'}), 400
                
                # Verificar se horário de abertura é antes do fechamento
                open_time = hours['open'].split(':')
                close_time = hours['close'].split(':')
                open_minutes = int(open_time[0]) * 60 + int(open_time[1])
                close_minutes = int(close_time[0]) * 60 + int(close_time[1])
                
                if open_minutes >= close_minutes:
                    return jsonify({'error': f'Horário de abertura deve ser antes do fechamento para {day}'}), 400
        
        # Obter ou criar configuração
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        if not config:
            config = TenantConfig(tenant_id=tenant.id)
            db.session.add(config)
        
        config.opening_hours = json.dumps(opening_hours)
        db.session.commit()
        
        return jsonify({
            'message': 'Horários atualizados com sucesso',
            'opening_hours': opening_hours
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customization_bp.route('/policies', methods=['GET'])
@jwt_required()
def get_policies():
    """Obter políticas e termos"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        
        policies = {}
        if config and config.policies:
            try:
                policies = json.loads(config.policies)
            except json.JSONDecodeError:
                policies = {}
        
        return jsonify({'policies': policies}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customization_bp.route('/policies', methods=['PUT'])
@jwt_required()
def update_policies():
    """Atualizar políticas e termos"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        data = request.get_json()
        policies = data.get('policies', {})
        
        # Validar que policies é um objeto
        if not isinstance(policies, dict):
            return jsonify({'error': 'Políticas devem ser um objeto'}), 400
        
        # Obter ou criar configuração
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        if not config:
            config = TenantConfig(tenant_id=tenant.id)
            db.session.add(config)
        
        config.policies = json.dumps(policies)
        db.session.commit()
        
        return jsonify({
            'message': 'Políticas atualizadas com sucesso',
            'policies': policies
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@customization_bp.route('/preview', methods=['GET'])
@jwt_required()
def get_preview_config():
    """Obter todas as configurações para preview"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        config = TenantConfig.query.filter_by(tenant_id=tenant.id).first()
        
        if not config:
            return jsonify({
                'tenant_name': tenant.name,
                'theme': {
                    'primary_color': '#1A1A1A',
                    'secondary_color': '#B8860B',
                    'accent_color': '#8B0000',
                    'logo_url': None
                },
                'business_info': {
                    'business_name': None,
                    'description': None,
                    'address': None,
                    'city': 'Brejo',
                    'state': 'MA',
                    'phone': None,
                    'email': None,
                    'website': None,
                    'instagram': None,
                    'facebook': None,
                    'whatsapp': None
                },
                'opening_hours': {},
                'policies': {}
            }), 200
        
        # Processar horários de funcionamento
        opening_hours = {}
        if config.opening_hours:
            try:
                opening_hours = json.loads(config.opening_hours)
            except json.JSONDecodeError:
                pass
        
        # Processar políticas
        policies = {}
        if config.policies:
            try:
                policies = json.loads(config.policies)
            except json.JSONDecodeError:
                pass
        
        return jsonify({
            'tenant_name': tenant.name,
            'theme': {
                'primary_color': config.primary_color,
                'secondary_color': config.secondary_color,
                'accent_color': config.accent_color,
                'logo_url': config.logo_url
            },
            'business_info': {
                'business_name': config.business_name,
                'description': config.description,
                'address': config.address,
                'city': config.city,
                'state': config.state,
                'zip_code': config.zip_code,
                'phone': config.phone,
                'email': config.email,
                'website': config.website,
                'instagram': config.instagram,
                'facebook': config.facebook,
                'whatsapp': config.whatsapp
            },
            'opening_hours': opening_hours,
            'policies': policies
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

