from flask import Flask, render_template
from routes.admin import admin_route
from routes.comum import comum_route
from models import Usuarios, Objetos,Sala
from flask_sqlalchemy import SQLAlchemy
from database.db import db
from flask_login import LoginManager

app = Flask(__name__)

#chave de segurança do projeto
app.secret_key = '12345678'
lm = LoginManager(app)
lm.login_view = 'login'

#cirando conexão com o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)   

@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuarios).filter_by(id=id).first()
    
    return usuario

app.register_blueprint(admin_route, url_prefix = '/lista')

app.register_blueprint(comum_route, url_prefix = '/comum')

@app.route('/')
def index():
    #apagar 
    #Cadeira.__table__.drop(db.engine)
    #print("Tabela Objetos deletada com sucesso!")
    
    nomes= ['','Informática 1', 'Informática 2', 'Informática 3']

    for i in range(1,4):
        nc = Sala(id = i, nome = nomes[i])
        db.session.add(nc)
    db.session.commit()

    
    return render_template('index.html')

   
    
#criando o banco de dados
with app.app_context():
    db.create_all()
app.run(debug=True)