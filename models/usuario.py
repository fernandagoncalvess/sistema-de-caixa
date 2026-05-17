from database.database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), default='cliente')
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    vendas = db.relationship('Venda', back_populates='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.username} - {self.tipo}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.tipo == 'admin'
    
    def is_caixa(self):
        return self.tipo in ['caixa', 'admin']
    
    def is_cliente(self):
        return self.tipo == 'cliente'