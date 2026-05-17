from app import app
from database.database import db
from models.produto import Produto
from models.usuario import Usuario
from models.venda import Venda
from models.itemvenda import ItemVenda

with app.app_context():
    db.create_all()
    print("Todas as tabelas foram criadas com sucesso!")