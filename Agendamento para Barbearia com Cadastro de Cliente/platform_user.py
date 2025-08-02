from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.models import db

class PlatformUser(db.Model):
    """Usuários que têm acesso à plataforma (admins, proprietários, funcionários)"""
    __tablename__ = 'platform_users'
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, db.ForeignKey('tenants.id'), nullable=True)  # Null para super admins
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    role = Column(String(50), nullable=False)  # super_admin, tenant_admin, tenant_user
    status = Column(String(20), default='active')
    last_login_at = Column(DateTime, nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    tenant = db.relationship('Tenant', backref='users')
    
    def __repr__(self):
        return f'<PlatformUser {self.email}>'
    
    def set_password(self, password):
        """Define a senha do usuário"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Retorna o nome completo do usuário"""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    def has_role(self, role):
        """Verifica se o usuário tem uma role específica"""
        return self.role == role
    
    def can_access_tenant(self, tenant_id):
        """Verifica se o usuário pode acessar um tenant específico"""
        if self.role == 'super_admin':
            return True
        return self.tenant_id == tenant_id
    
    def to_dict(self, include_sensitive=False):
        """Converte o usuário para dicionário"""
        data = {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'role': self.role,
            'status': self.status,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'email_verified_at': self.email_verified_at.isoformat() if self.email_verified_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
            
        return data
    
    @staticmethod
    def create_super_admin(email, password, first_name, last_name=None):
        """Cria um super administrador"""
        user = PlatformUser(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='super_admin',
            tenant_id=None,
            email_verified_at=datetime.utcnow()
        )
        user.set_password(password)
        return user
    
    @staticmethod
    def create_tenant_admin(tenant_id, email, password, first_name, last_name=None):
        """Cria um administrador de tenant"""
        user = PlatformUser(
            tenant_id=tenant_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='tenant_admin'
        )
        user.set_password(password)
        return user
    
    @staticmethod
    def create_tenant_user(tenant_id, email, password, first_name, last_name=None):
        """Cria um usuário de tenant (funcionário)"""
        user = PlatformUser(
            tenant_id=tenant_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='tenant_user'
        )
        user.set_password(password)
        return user

