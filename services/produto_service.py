from models.produto import Produto
from database.database import db
from sqlalchemy.exc import SQLAlchemyError

class ProdutoService:
    @staticmethod
    def listar_todos():
        return Produto.query.all()
    
    @staticmethod
    def buscar_por_id(id):
        return Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    
    @staticmethod
    def buscar_por_nome(nome):
        """Busca produtos por nome (parcial)"""
        return Produto.query.filter(Produto.nome.ilike(f'%{nome}%')).all()
    
    @staticmethod
    def salvar(data, imagem_file=None):
        try:
            imagem_blob = None
            if imagem_file and imagem_file.filename != '':
                #validar extensão
                formato = imagem_file.filename.rsplit('.', 1)[-1].lower()
                if formato not in ['png', 'jpg', 'jpeg', 'webp']:
                    raise ValueError("Formato de imagem não permitido.")
                
            imagem_blob = imagem_file.read()
            novo_produto = Produto(
                nome=data['nome'],
                descricao=data.get('descricao', ''),
                preco=float(data['preco']),
                imagem=imagem_blob,
                quantidade_estoque=int(data.get('quantidade_estoque', 0)),
                ativo=data.get('ativo', 'on') == 'on',
            )

            db.session.add(novo_produto)
            db.session.commit()

            return novo_produto

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erro ao salvar produto no banco: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao processar produto: {str(e)}")
    
    @staticmethod
    def atualizar(id, data, imagem_file=None):
        try:
            produto = ProdutoService.buscar_por_id(id)
            produto.nome = data.get('nome', produto.nome)
            produto.preco = float(data.get('preco', produto.preco))
            produto.quantidade_estoque = int(data.get('quantidade_estoque', produto.quantidade_estoque))
            produto.ativo = data.get('ativo', 'on') == 'on'

            if imagem_file and imagem_file.filename != '':
                    produto.imagem = imagem_file.read()
            
            db.session.commit()
            return produto

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erro ao atualizar produto: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro inesperado: {str(e)}")
    
    @staticmethod
    def deletar(id):
        try:
            produto = ProdutoService.buscar_por_id(id)
            db.session.delete(produto)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erro ao deletar produto: {str(e)}")
    
    @staticmethod
    def reduzir_estoque(produto_id, quantidade):
        try:
            produto = ProdutoService.buscar_por_id(produto_id)
            if produto.reduzir_estoque(quantidade):
                db.session.commit()
                return True
            else:
                raise Exception(f"Estoque insuficiente para o produto {produto.nome}")
        except Exception as e:
            db.session.rollback()
            raise e