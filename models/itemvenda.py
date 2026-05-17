from database.database import db

class ItemVenda(db.Model):
    __tablename__ = 'itens_venda'

    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Numeric(10,2), nullable=False)

    venda = db.relationship('Venda', back_populates='itens')
    produto = db.relationship('Produto', back_populates='itens_venda')

    def __repr__(self):
        return f'<ItemVenda {self.quantidade}x Produto {self.produto_id}>'

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario