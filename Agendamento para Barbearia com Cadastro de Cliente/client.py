from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from . import db

class Client(db.Model):
    """Modelo para clientes das barbearias"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    
    # Informações pessoais
    name = Column(String(100), nullable=False)
    email = Column(String(120))
    phone = Column(String(20), nullable=False)
    birth_date = Column(Date)
    
    # Informações adicionais
    notes = Column(Text)  # Observações sobre o cliente
    preferences = Column(Text)  # JSON string com preferências
    is_active = Column(Boolean, default=True)
    
    # Estatísticas
    total_appointments = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    last_visit = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship('Tenant', back_populates='clients')
    appointments = relationship('Appointment', back_populates='client')
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'notes': self.notes,
            'preferences': self.preferences,
            'is_active': self.is_active,
            'total_appointments': self.total_appointments,
            'total_spent': self.total_spent,
            'last_visit': self.last_visit.isoformat() if self.last_visit else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Client {self.name} - {self.phone}>'

