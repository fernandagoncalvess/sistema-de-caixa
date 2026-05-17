from datetime import datetime
from database.database import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0, nullable=False)
    imagem = db.Column(db.LargeBinary, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    itens_venda = db.relationship( 'ItemVenda', back_populates='produto')

    def __repr__(self):
        return f'<Produto {self.nome}>'

    def tem_estoque(self, quantidade):
        return self.quantidade_estoque >= quantidade

    def reduzir_estoque(self, quantidade):
        if self.tem_estoque(quantidade):
            self.quantidade_estoque -= quantidade
            return True
        return False

