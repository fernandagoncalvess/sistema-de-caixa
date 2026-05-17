from flask import Blueprint, render_template, request, redirect, url_for, flash

produto_bp = Blueprint('produto', __name__, url_prefix='/produtos')

@produto_bp.route('/')
def listar():
    print('TesteProduto')