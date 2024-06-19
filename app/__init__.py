# Modulo principal - Configurações principais
from flask import Flask
from app.routes import routes

app = Flask(__name__)# variavel que controla a aplicação todo o flask esta aqui
app.secret_key = 'mftsbs+@'


app.add_url_rule(routes['index_route'], view_func=routes['index_controller'])

app.add_url_rule(routes['login_route'], view_func=routes['login_controller'])

app.add_url_rule(routes['entry_route'], view_func=routes['entry_controller'])

app.add_url_rule(routes['movement_route'], view_func=routes['movement_controller'])

app.add_url_rule(routes['search_route'], view_func=routes['search_controller'])

app.add_url_rule(routes['found_route'], view_func=routes['found_controller'])

app.add_url_rule(routes['movement_searsh_route'], view_func=routes['movement_searsh_controller'])


@app.errorhandler(404) 
def not_found(e): 
  return f"{e}"