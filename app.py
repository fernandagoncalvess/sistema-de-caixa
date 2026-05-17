from flask import Flask
from database.database import init_db
from routes.produto_routes import produto_bp
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

init_db(app)

app.register_blueprint(produto_bp)

if __name__ == '__main__':
    app.run(debug=True)