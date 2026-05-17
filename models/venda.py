from database.database import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total = db.Column(db.Numeric(10,2), nullable=False, default=0.0)
    status = db.Column(db.String(20), default='finalizada', nullable=False)
    forma_pagamento = db.Column(db.String(20), default='dinheiro')
    
    itens = db.relationship('ItemVenda', back_populates='venda', lazy=True, cascade='all, delete-orphan')
    usuario = db.relationship('Usuario', backref='vendas')

    def __repr__(self):
        return f'<Venda #{self.id}>'

    def calcular_total(self):
        self.total = sum(item.subtotal for item in self.itens)
        return self.total