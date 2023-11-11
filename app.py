from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.debug = True
app.secret_key = 'djhfjdhfdkfheirweuryeuryei'

#messages = [{'titulo': 'Mensagem Titulo',
#             'autor': 'Mensagem Autor',
#             'exemplares': 'Mensagem Exemplares'}
#            ] 

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogoslivros.db'
  
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
 
# Settings for migrations
#migrate = Migrate(app, db)

# Models
class Catalogoslivros(db.Model):
    # Id : Field which stores unique id for every row in 
    # database table.
    # first_name: Used to store the first name if the user
    # last_name: Used to store last name of the user
    # Age: Used to store the age of the user
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), unique=False, nullable=False)
    autor = db.Column(db.String(255), unique=False, nullable=False)
    exemplares = db.Column(db.Integer, nullable=False)
  
    # repr method repersents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Titulo do Livro : {self.titulo}, Autor do Livro: {self.autor}, Exemplares: {self.exemplares}"

#Pagina inicial do aplicativo
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

#Pagina para acesso ao aplicativo
@app.route("/acesso")
def acesso():
    return render_template("acesso.html")

#Pagina para informações do aplicativo
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/sucesso")
def sucesso():
    return render_template("sucesso.html")

#Classe para criação do formulário de cadastro de livros
class LivroForm(FlaskForm):
    titulo = StringField(label='Titulo do Livro', validators=[DataRequired()])
    autor = StringField('Nome do Autor', validators=[DataRequired()])
    exemplares = IntegerField('Exemplares')
    submit = SubmitField('Enviar')

# function to add profiles
@app.route("/cadastrar", methods=['GET','POST'])
def cadastrar():
    form = LivroForm()

    #titulo = request.form.get("titulo")
    #autor = request.form.get("autor")
    #exemplares = request.form.get("exemplares")
    titulo = form.titulo.data
    autor  = form.autor.data
    exemplares = form.exemplares.data
  
    # create an object of the Profile class of models
    # and store data as a row in our datatable
    if request.method == 'POST':
        if form.validate_on_submit():
            if titulo != '' and autor != '' and exemplares is not None:
                p = Catalogoslivros(titulo=titulo, autor=autor, exemplares=exemplares)
                db.session.add(p)
                db.session.commit()
                #messages.append({'titulo': titulo, 'autor': autor, 'exemplares': exemplares})
                return render_template('sucesso.html', form=form)
            #else:
            #    return redirect('cadastrar.html', form=form)
   
    return render_template('cadastrar.html', form=form)

# function to render index page
@app.route('/disponibilidade')
def disponibilidade():
    page = request.args.get('page', 1, type=int)
    pagination = Catalogoslivros.query.order_by(Catalogoslivros.titulo).paginate(page=page, per_page=4)
    #catalogoslivros = Catalogoslivros.query.all()
    #return render_template('index.html', catalagoslivros=catalogoslivros,posts=posts.items, next_url=next_url, prev_url=prev_url)
    return render_template('disponibilidade.html', pagination=pagination)

#@app.route('/add_data')
#def add_data():
#    return render_template('cadastrar.html')
   
@app.route('/delete/<int:id>')
def erase(id):    
    # letes the data on the basis of unique id and 
    # directs to hoem page
    data = Catalogoslivros.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/disponibilidade')

#Pagina para informações do aplicativo
@app.route("/pesquisar", methods=['GET','POST'])
def pesquisar():
    form = LivroForm()
    select = request.form.get('opcoes')
    return render_template("pesquisar.html", form=form, select=select)

if __name__ == '__main__':
    app.run()