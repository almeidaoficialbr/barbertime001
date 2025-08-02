from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Time
from sqlalchemy.orm import relationship
from . import db

class Staff(db.Model):
    """Modelo para funcionários das barbearias"""
    __tablename__ = 'staff'
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('platform_users.id'), nullable=True)  # Opcional, para funcionários com login
    
    # Informações pessoais
    name = Column(String(100), nullable=False)
    email = Column(String(120))
    phone = Column(String(20))
    photo_url = Column(String(255))
    bio = Column(Text)
    
    # Informações profissionais
    position = Column(String(50))  # barbeiro, recepcionista, gerente
    specialties = Column(Text)  # JSON string com especialidades
    experience_years = Column(Integer)
    is_active = Column(Boolean, default=True)
    
    # Horários de trabalho (JSON string)
    work_schedule = Column(Text)  # {"monday": {"start": "08:00", "end": "18:00"}, ...}
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tenant = relationship('Tenant', back_populates='staff')
    user = relationship('PlatformUser', backref='staff_profile')
    appointments = relationship('Appointment', back_populates='staff_member')
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'photo_url': self.photo_url,
            'bio': self.bio,
            'position': self.position,
            'specialties': self.specialties,
            'experience_years': self.experience_years,
            'is_active': self.is_active,
            'work_schedule': self.work_schedule,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Staff {self.name} - {self.position}>'

