from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from . import db
import enum

class AppointmentStatus(enum.Enum):
    """Status dos agendamentos"""
    SCHEDULED = "scheduled"      # Agendado
    CONFIRMED = "confirmed"      # Confirmado
    IN_PROGRESS = "in_progress"  # Em andamento
    COMPLETED = "completed"      # Concluído
    CANCELLED = "cancelled"      # Cancelado
    NO_SHOW = "no_show"         # Não compareceu

class Appointment(db.Model):
    """Modelo para agendamentos"""
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False)
    
    # Informações do agendamento
    appointment_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    
    # Informações financeiras
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    final_price = Column(Float, nullable=False)
    payment_status = Column(String(20), default='pending')  # pending, paid, cancelled
    payment_method = Column(String(20))  # cash, card, pix
    
    # Observações
    notes = Column(Text)
    client_notes = Column(Text)  # Observações do cliente
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship('Tenant', back_populates='appointments')
    client = relationship('Client', back_populates='appointments')
    service = relationship('Service', back_populates='appointments')
    staff_member = relationship('Staff', back_populates='appointments')
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'client_id': self.client_id,
            'service_id': self.service_id,
            'staff_id': self.staff_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'duration_minutes': self.duration_minutes,
            'status': self.status.value if self.status else None,
            'price': self.price,
            'discount': self.discount,
            'final_price': self.final_price,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'notes': self.notes,
            'client_notes': self.client_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Dados relacionados
            'client': self.client.to_dict() if self.client else None,
            'service': self.service.to_dict() if self.service else None,
            'staff_member': self.staff_member.to_dict() if self.staff_member else None
        }
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date} - {self.status.value}>'

