from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.debug = True
app.secret_key = 'djhfjdhfdkfheirweuryeuryei'

# Configurações do Banco de Dads SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogoslivros.db'
  
#Criando Instância SQLAlchemy
db = SQLAlchemy(app)
 
# Modelos da tabela catalogoslivros
class Catalogoslivros(db.Model):
    # id: Identificado Único na tabela catalogoslivros
    # titulo: Usado para definir o campo Titulo do Livro
    # autor: Usado para definir o campo Autor do Livro
    # exemplares: Usado para definir o número de Exemplares disponíveis
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), unique=False, nullable=False)
    autor = db.Column(db.String(255), unique=False, nullable=False)
    exemplares = db.Column(db.Integer, nullable=False)

    #Método repr que representa a aparência de um objeto da Tabela catalogoslivros
    def __repr__(self):
        return f"Titulo do Livro : {self.titulo}, Autor do Livro: {self.autor}, Exemplares: {self.exemplares}"

#Pagina inicial do aplicativo
@app.route("/")
def index():
    return render_template("index.html")

#Pagina para acesso ao aplicativo
@app.route("/acesso")
def acesso():
    return render_template("acesso.html")

#Pagina para informações do aplicativo
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

#Página para informação de operação realizada com sucesso
@app.route("/sucesso")
def sucesso():
    return render_template("sucesso.html")

#Classe para criação do formulário de cadastro de livros
class LivroForm(FlaskForm):
    titulo = StringField(label='Titulo do Livro', validators=[DataRequired()])
    autor = StringField('Nome do Autor', validators=[DataRequired()])
    exemplares = IntegerField('Exemplares')
    submit = SubmitField('Enviar')

# Função para cadstrar um novo Livro
@app.route("/cadastrar", methods=['GET','POST'])
def cadastrar():
    #Cria uma nova intância da clase LivroForm
    form = LivroForm()
    if request.method == 'POST':
        titulo = request.form.get("titulo")
        autor = request.form.get("autor")
        exemplares = request.form.get("exemplares")

        #Verifica se o número de exemplares é igual ou menos que 0
        if int(exemplares) <= 0:
            return render_template('erro.html', form=form)
    
    if form.validate_on_submit():
        if titulo != '' and autor != '' or exemplares is not None:
            p = Catalogoslivros(titulo=titulo, autor=autor, exemplares=exemplares)
            db.session.add(p)
            db.session.commit()
            db.session.close()
            return render_template('sucesso.html', form=form)
        else:
            return render_template('erro.html', form=form)
   
    return render_template('cadastrar.html', form=form)

# Função para listar tidos os livros cadastrado na base de daods e sua disponibilidade
@app.route('/disponibilidade')
def disponibilidade():
    page = request.args.get('page', 1, type=int)
    pagination = Catalogoslivros.query.order_by(Catalogoslivros.titulo).paginate(page=page, per_page=4)
    return render_template('disponibilidade.html', pagination=pagination)

# Função para deletar um Livro cadastrado na base de dados   
@app.route('/delete/<int:id>')
def erase(id):    
    data = Catalogoslivros.query.get(id)
    db.session.delete(data)
    db.session.commit()
    db.session.close()
    return redirect('/disponibilidade')

#Funçaõ utilizada para pesquisar Titulo ou Nome do Autor do Livro 
@app.route("/pesquisar", methods=['GET','POST'])
def pesquisar():
    form = LivroForm()
    select = request.form.get('opcoes')
    if request.method == 'POST':
        #Pesquisa por Titulo do Livro
        if select == 'titulo':
            titulo_pesq = request.form.get("titulo_pesq")
            search = "%{}%".format(titulo_pesq)
            if titulo_pesq is not None:
                data = Catalogoslivros.query.filter(Catalogoslivros.titulo.like(search)).all()
                page = request.args.get('page', 1, type=int)
                pagination = Catalogoslivros.query.filter(Catalogoslivros.titulo.like(search)).paginate(page=page, per_page=5)
                return render_template("resultado.html", data=data, pagination=pagination)
            else:
                return render_template("pesquisar.html", form=form, select=select)    
        #Pesquisa por Autor do Livro
        if select == 'autor':
            autor_pesq = request.form.get("autor_pesq")
            search = "%{}%".format(autor_pesq)
            if autor_pesq is not None:
                data = Catalogoslivros.query.filter(Catalogoslivros.autor.like(search)).all()
                page = request.args.get('page', 1, type=int)
                pagination = Catalogoslivros.query.filter(Catalogoslivros.autor.like(search)).paginate(page=page, per_page=5)
                return render_template("resultado.html", data=data, pagination=pagination)
            else:
                    return render_template("pesquisar.html", form=form, select=select)    

    return render_template("pesquisar.html", form=form, select=select)

if __name__ == '__main__':
    app.run()