from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from src.models import db, Tenant, TenantConfig

public_bp = Blueprint('public', __name__)

@public_bp.route('/barbershops', methods=['GET'])
def list_barbershops():
    """Listar barbearias disponíveis em Brejo-MA"""
    try:
        # Parâmetros de busca
        search = request.args.get('search', '').strip()
        city = request.args.get('city', 'Brejo').strip()
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 10)), 50)  # Máximo 50 por página
        
        # Query base - apenas tenants ativos
        query = db.session.query(Tenant, TenantConfig).join(
            TenantConfig, Tenant.id == TenantConfig.tenant_id, isouter=True
        ).filter(Tenant.status == 'active')
        
        # Filtrar por cidade
        if city:
            query = query.filter(
                or_(
                    TenantConfig.city.ilike(f'%{city}%'),
                    TenantConfig.city.is_(None)  # Incluir sem cidade definida
                )
            )
        
        # Filtrar por busca (nome da barbearia ou descrição)
        if search:
            query = query.filter(
                or_(
                    Tenant.name.ilike(f'%{search}%'),
                    TenantConfig.business_name.ilike(f'%{search}%'),
                    TenantConfig.description.ilike(f'%{search}%')
                )
            )
        
        # Ordenar por nome
        query = query.order_by(Tenant.name)
        
        # Paginação
        total = query.count()
        results = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Formatar resultados
        barbershops = []
        for tenant, config in results:
            barbershop_data = {
                'id': tenant.id,
                'name': tenant.name,
                'slug': tenant.slug,
                'business_name': config.business_name if config else tenant.name,
                'description': config.description if config else None,
                'address': config.address if config else None,
                'city': config.city if config else 'Brejo',
                'state': config.state if config else 'MA',
                'phone': config.phone if config else None,
                'email': config.email if config else None,
                'website': config.website if config else None,
                'instagram': config.instagram if config else None,
                'facebook': config.facebook if config else None,
                'whatsapp': config.whatsapp if config else None,
                'logo_url': config.logo_url if config else None,
                'primary_color': config.primary_color if config else '#1A1A1A',
                'secondary_color': config.secondary_color if config else '#B8860B',
                'opening_hours': config.opening_hours if config else None,
                'status': 'open',  # Implementar lógica de horário de funcionamento
                'rating': 4.5,  # Implementar sistema de avaliações
                'total_reviews': 0  # Implementar sistema de avaliações
            }
            barbershops.append(barbershop_data)
        
        return jsonify({
            'barbershops': barbershops,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            },
            'filters': {
                'search': search,
                'city': city
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@public_bp.route('/barbershops/<slug>', methods=['GET'])
def get_barbershop_details(slug):
    """Obter detalhes de uma barbearia específica"""
    try:
        # Buscar tenant pelo slug
        tenant = Tenant.query.filter_by(slug=slug, status='active').first()
        
        if not tenant:
            return jsonify({'error': 'Barbearia não encontrada'}), 404
        
        # Obter configuração
        config = tenant.config
        
        # Dados da barbearia
        barbershop_data = {
            'id': tenant.id,
            'name': tenant.name,
            'slug': tenant.slug,
            'business_name': config.business_name if config else tenant.name,
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
            'whatsapp': config.whatsapp if config else None,
            'logo_url': config.logo_url if config else None,
            'primary_color': config.primary_color if config else '#1A1A1A',
            'secondary_color': config.secondary_color if config else '#B8860B',
            'accent_color': config.accent_color if config else '#8B0000',
            'opening_hours': config.opening_hours if config else {
                'monday': {'open': '08:00', 'close': '18:00'},
                'tuesday': {'open': '08:00', 'close': '18:00'},
                'wednesday': {'open': '08:00', 'close': '18:00'},
                'thursday': {'open': '08:00', 'close': '18:00'},
                'friday': {'open': '08:00', 'close': '18:00'},
                'saturday': {'open': '08:00', 'close': '17:00'},
                'sunday': {'closed': True}
            },
            'policies': config.policies if config else None,
            'status': 'open',  # Implementar lógica de horário de funcionamento
            'rating': 4.5,  # Implementar sistema de avaliações
            'total_reviews': 0,  # Implementar sistema de avaliações
            'services': [],  # Implementar quando tiver modelo de serviços
            'staff': [],  # Implementar quando tiver modelo de funcionários
            'gallery': []  # Implementar galeria de fotos
        }
        
        return jsonify({'barbershop': barbershop_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@public_bp.route('/barbershops/<slug>/services', methods=['GET'])
def get_barbershop_services(slug):
    """Obter serviços de uma barbearia"""
    try:
        tenant = Tenant.query.filter_by(slug=slug, status='active').first()
        
        if not tenant:
            return jsonify({'error': 'Barbearia não encontrada'}), 404
        
        # Implementar quando tiver modelo de serviços
        services = [
            {
                'id': 1,
                'name': 'Corte Masculino',
                'description': 'Corte tradicional masculino',
                'duration': 30,
                'price': 25.00,
                'category': 'Corte'
            },
            {
                'id': 2,
                'name': 'Barba',
                'description': 'Aparar e modelar barba',
                'duration': 20,
                'price': 15.00,
                'category': 'Barba'
            },
            {
                'id': 3,
                'name': 'Corte + Barba',
                'description': 'Combo completo',
                'duration': 45,
                'price': 35.00,
                'category': 'Combo'
            }
        ]
        
        return jsonify({'services': services}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@public_bp.route('/barbershops/<slug>/staff', methods=['GET'])
def get_barbershop_staff(slug):
    """Obter funcionários de uma barbearia"""
    try:
        tenant = Tenant.query.filter_by(slug=slug, status='active').first()
        
        if not tenant:
            return jsonify({'error': 'Barbearia não encontrada'}), 404
        
        # Buscar funcionários ativos
        from src.models import PlatformUser
        staff_members = PlatformUser.query.filter_by(
            tenant_id=tenant.id,
            role='tenant_user',
            status='active'
        ).all()
        
        staff_data = []
        for staff in staff_members:
            staff_info = {
                'id': staff.id,
                'name': staff.full_name,
                'first_name': staff.first_name,
                'specialties': [],  # Implementar quando tiver modelo de especialidades
                'rating': 4.5,  # Implementar sistema de avaliações
                'total_reviews': 0,  # Implementar sistema de avaliações
                'photo_url': None,  # Implementar upload de fotos
                'bio': None  # Implementar biografia
            }
            staff_data.append(staff_info)
        
        return jsonify({'staff': staff_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@public_bp.route('/barbershops/<slug>/available-slots', methods=['GET'])
def get_available_slots(slug):
    """Obter horários disponíveis para agendamento"""
    try:
        tenant = Tenant.query.filter_by(slug=slug, status='active').first()
        
        if not tenant:
            return jsonify({'error': 'Barbearia não encontrada'}), 404
        
        date = request.args.get('date')  # Formato: YYYY-MM-DD
        service_id = request.args.get('service_id')
        staff_id = request.args.get('staff_id')
        
        if not date:
            return jsonify({'error': 'Data é obrigatória'}), 400
        
        # Implementar lógica de horários disponíveis
        # Por enquanto, retornar horários fixos
        available_slots = [
            {'time': '08:00', 'available': True},
            {'time': '08:30', 'available': True},
            {'time': '09:00', 'available': False},
            {'time': '09:30', 'available': True},
            {'time': '10:00', 'available': True},
            {'time': '10:30', 'available': True},
            {'time': '11:00', 'available': True},
            {'time': '11:30', 'available': False},
            {'time': '14:00', 'available': True},
            {'time': '14:30', 'available': True},
            {'time': '15:00', 'available': True},
            {'time': '15:30', 'available': True},
            {'time': '16:00', 'available': True},
            {'time': '16:30', 'available': True},
            {'time': '17:00', 'available': True},
            {'time': '17:30', 'available': True}
        ]
        
        return jsonify({
            'date': date,
            'slots': available_slots
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@public_bp.route('/cities', methods=['GET'])
def get_cities():
    """Listar cidades disponíveis"""
    try:
        # Por enquanto, retornar apenas Brejo-MA
        cities = [
            {
                'name': 'Brejo',
                'state': 'MA',
                'full_name': 'Brejo - MA',
                'barbershops_count': Tenant.query.filter_by(status='active').count()
            }
        ]
        
        return jsonify({'cities': cities}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

