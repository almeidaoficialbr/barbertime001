from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
from src.models import db, Appointment, Client, Service, Staff
from src.models.appointment import AppointmentStatus
from src.middleware.tenant import get_current_tenant
from datetime import datetime, timedelta
import json

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/', methods=['GET'])
@jwt_required()
def list_appointments():
    """Listar agendamentos do tenant"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Parâmetros de filtro
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        status = request.args.get('status')
        staff_id = request.args.get('staff_id')
        client_id = request.args.get('client_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Query base
        query = Appointment.query.filter_by(tenant_id=tenant.id)
        
        # Aplicar filtros
        if status:
            query = query.filter_by(status=AppointmentStatus(status))
        
        if staff_id:
            query = query.filter_by(staff_id=int(staff_id))
        
        if client_id:
            query = query.filter_by(client_id=int(client_id))
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                query = query.filter(Appointment.appointment_date >= date_from_obj)
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para date_from. Use YYYY-MM-DD'}), 400
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Appointment.appointment_date < date_to_obj)
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para date_to. Use YYYY-MM-DD'}), 400
        
        # Ordenar por data do agendamento
        query = query.order_by(Appointment.appointment_date.desc())
        
        # Paginação
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'appointments': [appointment.to_dict() for appointment in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointments_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment():
    """Criar novo agendamento"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['client_id', 'service_id', 'staff_id', 'appointment_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Validar se cliente, serviço e funcionário pertencem ao tenant
        client = Client.query.filter_by(id=data['client_id'], tenant_id=tenant.id).first()
        if not client:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        service = Service.query.filter_by(id=data['service_id'], tenant_id=tenant.id).first()
        if not service:
            return jsonify({'error': 'Serviço não encontrado'}), 404
        
        staff = Staff.query.filter_by(id=data['staff_id'], tenant_id=tenant.id).first()
        if not staff:
            return jsonify({'error': 'Funcionário não encontrado'}), 404
        
        # Validar data do agendamento
        try:
            appointment_date = datetime.fromisoformat(data['appointment_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Formato de data inválido'}), 400
        
        # Verificar se a data não é no passado
        if appointment_date < datetime.utcnow():
            return jsonify({'error': 'Não é possível agendar para datas passadas'}), 400
        
        # Verificar disponibilidade do funcionário
        duration = data.get('duration_minutes', service.duration_minutes)
        end_time = appointment_date + timedelta(minutes=duration)
        
        conflicting_appointments = Appointment.query.filter(
            and_(
                Appointment.staff_id == staff.id,
                Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED, AppointmentStatus.IN_PROGRESS]),
                or_(
                    and_(
                        Appointment.appointment_date <= appointment_date,
                        Appointment.appointment_date + timedelta(minutes=Appointment.duration_minutes) > appointment_date
                    ),
                    and_(
                        Appointment.appointment_date < end_time,
                        Appointment.appointment_date >= appointment_date
                    )
                )
            )
        ).first()
        
        if conflicting_appointments:
            return jsonify({'error': 'Funcionário não disponível neste horário'}), 400
        
        # Calcular preços
        price = data.get('price', service.price)
        discount = data.get('discount', 0.0)
        final_price = price - discount
        
        # Criar novo agendamento
        appointment = Appointment(
            tenant_id=tenant.id,
            client_id=client.id,
            service_id=service.id,
            staff_id=staff.id,
            appointment_date=appointment_date,
            duration_minutes=duration,
            price=price,
            discount=discount,
            final_price=final_price,
            payment_status=data.get('payment_status', 'pending'),
            payment_method=data.get('payment_method'),
            notes=data.get('notes'),
            client_notes=data.get('client_notes'),
            status=AppointmentStatus(data.get('status', 'scheduled'))
        )
        
        db.session.add(appointment)
        
        # Atualizar estatísticas do cliente
        client.total_appointments += 1
        client.total_spent += final_price
        client.last_visit = appointment_date
        
        db.session.commit()
        
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'appointment': appointment.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Dados inválidos: ' + str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Erro de integridade dos dados'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    """Obter detalhes de um agendamento específico"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        appointment = Appointment.query.filter_by(
            id=appointment_id,
            tenant_id=tenant.id
        ).first()
        
        if not appointment:
            return jsonify({'error': 'Agendamento não encontrado'}), 404
        
        return jsonify({'appointment': appointment.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointments_bp.route('/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    """Atualizar agendamento existente"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        appointment = Appointment.query.filter_by(
            id=appointment_id,
            tenant_id=tenant.id
        ).first()
        
        if not appointment:
            return jsonify({'error': 'Agendamento não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'appointment_date' in data:
            try:
                new_date = datetime.fromisoformat(data['appointment_date'].replace('Z', '+00:00'))
                if new_date < datetime.utcnow():
                    return jsonify({'error': 'Não é possível agendar para datas passadas'}), 400
                appointment.appointment_date = new_date
            except ValueError:
                return jsonify({'error': 'Formato de data inválido'}), 400
        
        if 'duration_minutes' in data:
            appointment.duration_minutes = int(data['duration_minutes'])
        
        if 'status' in data:
            appointment.status = AppointmentStatus(data['status'])
        
        if 'price' in data:
            appointment.price = float(data['price'])
            appointment.final_price = appointment.price - appointment.discount
        
        if 'discount' in data:
            appointment.discount = float(data['discount'])
            appointment.final_price = appointment.price - appointment.discount
        
        if 'payment_status' in data:
            appointment.payment_status = data['payment_status']
        
        if 'payment_method' in data:
            appointment.payment_method = data['payment_method']
        
        if 'notes' in data:
            appointment.notes = data['notes']
        
        if 'client_notes' in data:
            appointment.client_notes = data['client_notes']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Agendamento atualizado com sucesso',
            'appointment': appointment.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': 'Dados inválidos: ' + str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    """Cancelar/excluir agendamento"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        appointment = Appointment.query.filter_by(
            id=appointment_id,
            tenant_id=tenant.id
        ).first()
        
        if not appointment:
            return jsonify({'error': 'Agendamento não encontrado'}), 404
        
        # Se o agendamento já foi realizado, apenas marcar como cancelado
        if appointment.status in [AppointmentStatus.COMPLETED, AppointmentStatus.IN_PROGRESS]:
            appointment.status = AppointmentStatus.CANCELLED
            db.session.commit()
            return jsonify({'message': 'Agendamento cancelado com sucesso'}), 200
        
        # Caso contrário, excluir completamente
        db.session.delete(appointment)
        db.session.commit()
        
        return jsonify({'message': 'Agendamento excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@appointments_bp.route('/calendar', methods=['GET'])
@jwt_required()
def get_calendar():
    """Obter agendamentos para visualização em calendário"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Parâmetros de data
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        staff_id = request.args.get('staff_id')
        
        if not date_from or not date_to:
            return jsonify({'error': 'Parâmetros date_from e date_to são obrigatórios'}), 400
        
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        # Query base
        query = Appointment.query.filter(
            and_(
                Appointment.tenant_id == tenant.id,
                Appointment.appointment_date >= date_from_obj,
                Appointment.appointment_date < date_to_obj
            )
        )
        
        # Filtrar por funcionário se especificado
        if staff_id:
            query = query.filter_by(staff_id=int(staff_id))
        
        appointments = query.order_by(Appointment.appointment_date).all()
        
        # Formatar para calendário
        calendar_events = []
        for appointment in appointments:
            end_time = appointment.appointment_date + timedelta(minutes=appointment.duration_minutes)
            
            calendar_events.append({
                'id': appointment.id,
                'title': f"{appointment.client.name} - {appointment.service.name}",
                'start': appointment.appointment_date.isoformat(),
                'end': end_time.isoformat(),
                'status': appointment.status.value,
                'client_name': appointment.client.name,
                'service_name': appointment.service.name,
                'staff_name': appointment.staff_member.name,
                'price': appointment.final_price,
                'payment_status': appointment.payment_status
            })
        
        return jsonify({
            'events': calendar_events,
            'total': len(calendar_events)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@appointments_bp.route('/availability', methods=['GET'])
@jwt_required()
def check_availability():
    """Verificar disponibilidade de horários"""
    try:
        tenant = get_current_tenant()
        if not tenant:
            return jsonify({'error': 'Tenant não encontrado'}), 404
        
        # Parâmetros obrigatórios
        staff_id = request.args.get('staff_id')
        date = request.args.get('date')
        service_id = request.args.get('service_id')
        
        if not all([staff_id, date, service_id]):
            return jsonify({'error': 'Parâmetros staff_id, date e service_id são obrigatórios'}), 400
        
        # Validar funcionário e serviço
        staff = Staff.query.filter_by(id=int(staff_id), tenant_id=tenant.id).first()
        if not staff:
            return jsonify({'error': 'Funcionário não encontrado'}), 404
        
        service = Service.query.filter_by(id=int(service_id), tenant_id=tenant.id).first()
        if not service:
            return jsonify({'error': 'Serviço não encontrado'}), 404
        
        try:
            target_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        # Obter horário de trabalho do funcionário
        work_schedule = {}
        if staff.work_schedule:
            try:
                work_schedule = json.loads(staff.work_schedule)
            except json.JSONDecodeError:
                work_schedule = {}
        
        # Obter dia da semana
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday = weekdays[target_date.weekday()]
        
        if weekday not in work_schedule or not work_schedule[weekday]:
            return jsonify({
                'available_slots': [],
                'message': 'Funcionário não trabalha neste dia'
            }), 200
        
        # Horários de trabalho
        work_start = work_schedule[weekday]['start']
        work_end = work_schedule[weekday]['end']
        
        # Obter agendamentos existentes para o dia
        start_of_day = datetime.combine(target_date, datetime.min.time())
        end_of_day = start_of_day + timedelta(days=1)
        
        existing_appointments = Appointment.query.filter(
            and_(
                Appointment.staff_id == staff.id,
                Appointment.appointment_date >= start_of_day,
                Appointment.appointment_date < end_of_day,
                Appointment.status.in_([
                    AppointmentStatus.SCHEDULED,
                    AppointmentStatus.CONFIRMED,
                    AppointmentStatus.IN_PROGRESS
                ])
            )
        ).all()
        
        # Gerar slots disponíveis (intervalos de 30 minutos)
        available_slots = []
        current_time = datetime.strptime(work_start, '%H:%M').time()
        end_time = datetime.strptime(work_end, '%H:%M').time()
        
        while current_time < end_time:
            slot_datetime = datetime.combine(target_date, current_time)
            slot_end = slot_datetime + timedelta(minutes=service.duration_minutes)
            
            # Verificar se o slot não conflita com agendamentos existentes
            is_available = True
            for appointment in existing_appointments:
                apt_end = appointment.appointment_date + timedelta(minutes=appointment.duration_minutes)
                
                if (slot_datetime < apt_end and slot_end > appointment.appointment_date):
                    is_available = False
                    break
            
            # Verificar se o slot termina dentro do horário de trabalho
            if slot_end.time() > end_time:
                is_available = False
            
            if is_available:
                available_slots.append({
                    'time': current_time.strftime('%H:%M'),
                    'datetime': slot_datetime.isoformat(),
                    'duration': service.duration_minutes
                })
            
            # Próximo slot (30 minutos depois)
            current_time = (datetime.combine(target_date, current_time) + timedelta(minutes=30)).time()
        
        return jsonify({
            'date': date,
            'staff_name': staff.name,
            'service_name': service.name,
            'available_slots': available_slots,
            'total_slots': len(available_slots)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

