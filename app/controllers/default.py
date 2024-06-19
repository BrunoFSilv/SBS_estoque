from flask.views import MethodView
from flask import request, render_template, redirect, current_app, flash, url_for 
from app.controllers import userController, mainStock
from json import load
from random import randrange

logged = False
using = ""


class LoginController(MethodView):
    def get(self):
        if logged:
          return redirect('/')
        return render_template('login.html')
    
    def post(self):
        
        global logged, using

        USER_DATA = f"{current_app.root_path}/static/models/users.json"

        user = request.form['user']
        pwd = request.form['password']

        if userController.Check(user, pwd, USER_DATA):
            logged = True
            using = user.upper().replace(" ","")
            return redirect('/')
        else:
            flash('Senha incorreta. Por favor, tente novamente.')
            return redirect('/login')

class IndexControoler(MethodView):
   def get(self):
      if not logged:
         return redirect('/login')
      user = str(using).capitalize()
      return render_template('index.html', user=user)
   
   def post(self):
      if 'entry' in request.form:
         return redirect('/entrada')
      if 'movement' in request.form:
         return redirect('/movimentacao')
      if 'search' in request.form:
         return redirect('/procura')

class EntryController(MethodView):
    def get(self):
      if not logged:
        return redirect('/login')
      return render_template('entry.html')
    
    def post(self):
      print(request.form)
      error = ''
      global using
      mainStock.runLists(f"{current_app.root_path}/static/models/stockJsons")
      

      CONFIG_DATA = f"{current_app.root_path}/static/models/dados.json"
      with open(CONFIG_DATA, "r") as arquivo:
        configData = load(arquivo)

      estoque_DATA = f"{current_app.root_path}/static/models/stockJsons/Escritorio.json"

      clientes_DATA = f"{current_app.root_path}/static/models/stockJsons/Clientes.json"
      carro_DATA = f"{current_app.root_path}/static/models/stockJsons/Carro.json"
      ForadoEscritorio_DATA = f"{current_app.root_path}/static/models/stockJsons/ForadoEscritorio.json"

      with open(estoque_DATA, "r") as arquivo:
          estoqueData = load(arquivo)

      with open(clientes_DATA, "r") as arquivo:
          clientesData = load(arquivo)

      with open(carro_DATA, "r") as arquivo:
          carroData = load(arquivo)

      with open(ForadoEscritorio_DATA, "r") as arquivo:
          ForadoEscritorioData = load(arquivo)       

      # pegando os valores entregues pelo formulario
      entry = request.form['entry'].strip()
      sub_entry = request.form['sub-entry'].strip()
      motive = request.form['motive'].strip()
      date = request.form['date']
      user = using
      brand = request.form['brand'].strip()
      model = request.form['model'].strip()
      id_mac = request.form['id_mac'].strip()
      company = request.form['company'].strip()

      # verificando se os campos foram preenchidos
      if company.replace(' ', '') == '':
         error = f'Por favor preencha o campo Empresa'
      elif entry.replace(' ', '') == '':
         error = f'Por favor preencha o campo Entrada'
      elif entry.capitalize() != 'Escritorio' and sub_entry.replace(' ', '') == '':
         error = f'Por favor preencha o campo Subentrada'
      elif motive.replace(' ', '') == '':
         error = f'Por favor preencha o campo Motivo'
      elif date.replace(' ', '') == '':
         error = f'Por favor preencha o campo Data'
      elif brand.replace(' ', '') == '':
         error = f'Por favor preencha o campo Marca'
      elif model.replace(' ', '') == '':
         error = f'Por favor preencha o campo Modelo'
      elif id_mac.replace(' ', '') == '':
         error = f'Por favor preencha o campo ID'
      
      # Verificando se os campos foram preenchidos corretamente
      elif company.lower() not in [c.lower() for c in configData['empresas']]:
         error = f'{company} não é um valor de empresa válida'
      elif entry.lower() not in [e.lower() for e in configData['entradas']]:
         error = f'{entry} não é um valor de entrada válida'
      elif sub_entry.lower() not in [se.lower() for se in configData['subentradas']] and entry.lower() == 'carro':
         error = f'{sub_entry} não é um valor de subentrada válida'
      elif sub_entry.replace(' ', '') != '' and entry.lower() == 'escritorio':
         error = f'Escritorio não possui subentradas - subentrada inserida: {sub_entry} não é válida'
      elif motive.lower() not in [m.lower() for m in configData['motivos_e']]:
         error = f'{motive} não é um valor de motivo válido'
      elif type(mainStock.CheckData(date, 'formatada')) == tuple:
         error = mainStock.CheckData(date, 'formatada')[1]
      elif brand.lower() not in [b.lower() for b in configData['marcas']]:
         error = f'{brand} não é um valor de marca válido'
      elif model.lower() not in [m.lower() for m in configData['modelos']]:
         error = f'{model} não é um valor de modelo válido'

      
      # verifica se o equipamento já esta inserido em algum lugar
      equipamento_Name = str(f'_{id_mac}').upper()
      if equipamento_Name in estoqueData:
        error = f'o equipamento com o ID: {id_mac} já esta presente no Escritorio'
      for key, v in clientesData.items():
         if equipamento_Name in v:
            error = f'O equipamento com o ID: {id_mac} já esta presente no Cliente {key}'
      for key, v in carroData.items():
         if equipamento_Name in v:
            error = f'O equipamento com o ID: {id_mac} já esta presente no Carro do {key}'
      for key, v in ForadoEscritorioData.items():
         if equipamento_Name in v:
            error = f'O equipamento com o ID: {id_mac} já esta presente na lista de equipamentos fora, mais especificamente {key}'

      # retornando o erro caso aja
      if error != '':
         print(f'\033[1;31;40m{error}\033[0m')
         return render_template('entry.html', error=error, company=company, date=date, entry=entry, sub_entry=sub_entry, brand=brand, model=model, motive=motive)
      
      # configurando as variaveis para realizar o lançamento no banco de dados
      entry = entry.upper()
      sub_entry = sub_entry.capitalize()
      motive = motive.capitalize()
      dateF = mainStock.CheckData(date, 'formatada')
      user = user.capitalize()
      id_mac = id_mac.upper()

      # executando a função para lanção os valores no banco de dados
      mainStock.Entrada(Entrada = entry, subEntrada= sub_entry, Motivo= motive, data= dateF, manuseador= user, MARCA= brand, MODELO= model, ID= id_mac, EMPRESA= company)

      return render_template('entry.html', status=f'Entrada Efetuada com sucesso: {id_mac}', company=company, date=date, entry=entry, sub_entry=sub_entry, brand=brand, model=model, motive=motive)
    
class MovementController(MethodView):
    def get(self):
      if not logged:
        return redirect('/login')
      return render_template('movement.html')
    
    def post(self):
      error = ''
      global using
      mainStock.runLists(f"{current_app.root_path}/static/models/stockJsons")

      # carrega as listas json
      CONFIG_DATA = f"{current_app.root_path}/static/models/dados.json"
      with open(CONFIG_DATA, "r") as arquivo:
        configData = load(arquivo)

      if 'btnauto_preencher' in request.form: # realiza o auto preenchimento
         id_mac = request.form['id_mac']
         id_mac = id_mac.upper()
         equipamento = mainStock.searsh(f'_{id_mac}')


         if not equipamento: # checa se o equipamento existe no sistema
            error = f'O equipamento não existe no sistema de estoque'

         if error != '':
            print(f'\033[1;31;40m{error}\033[0m')
            return render_template('movement.html', error=error)
         
         # validação das variaveis
         partes = equipamento.localizacaoAtual.split(":")

         return render_template('movement.html', id_mac=equipamento.id, brand=equipamento.marca, model=equipamento.modelo, exit=partes[0], sub_exit=partes[1])

      if 'btn_executar' in request.form: # Executando a movimentação
         # pegando os valores do form
         id_mac = request.form['id_mac']
         equipamento = mainStock.searsh(f'_{id_mac}')
         if not equipamento: # checa se o equipamento existe no sistema
            error = f'O equipamento {id_mac} não existe no sistema de estoque'
            print(f'\033[1;31;40m{error}\033[0m')

         

         partes = equipamento.localizacaoAtual.split(":") # partes["exit", "sub_exit"]
         entry = request.form['entry'].strip()
         sub_entry = request.form['sub-entry'].strip()
         motive = request.form['motive']
         date = request.form['date']
         obs = request.form['obs']
         user = using.capitalize()
         

         # validações de segurança

         # verificando se os campos foram preenchidos
         if entry.replace(' ', '') == '':
            error = f'Por favor preencha o campo Entrada'
         elif entry.capitalize() != 'Escritorio' and sub_entry.replace(' ', '') == '':
            error = f'Por favor preencha o campo Subentrada'
         elif motive.replace(' ', '') == '':
            error = f'Por favor preencha o campo Motivo'
         elif date.replace(' ', '') == '':
            error = f'Por favor preencha o campo Data'

         # verificando se os campos foram preenchidos corretamente
         elif entry.lower() not in [e.lower() for e in configData['entradas']]:
            error = f'{entry} não é um valor de entrada válida'
         elif sub_entry.lower() not in [se.lower() for se in configData['subentradas']] and entry.lower() == 'carro':
            error = f'{sub_entry} não é um valor de subentrada válida'
         elif sub_entry.replace(' ', '') != '' and entry == 'Escritorio':
            error = f'Escritorio não possui subentradas - subentrada inserida: {sub_entry} não é válida'
         elif motive.lower() not in [m.lower() for m in configData['motivos_m']]:
            error = f'{motive} não é um valor de motivo válido'
         elif type(mainStock.CheckData(date, 'formatada')) == tuple:
            error = mainStock.CheckData(date, 'formatada')[1]
         elif partes[0].lower() == entry.lower() and partes[1].lower() == sub_entry.lower():
            error = f'o equipamento {equipamento.id} já esta presente em {equipamento.localizacaoAtual}'

         # para evitar conversão de data sendo ela igual a uma str vazia
         if error == '':
            dateF = mainStock.CheckData(date, 'formatada')

         # caso aja algum erro
         if error != '':
            print(f'\033[1;31;40m{error}\033[0m')
            return render_template('movement.html', error=error, date=date, entry=entry, sub_entry=sub_entry, id_mac=equipamento.id, brand=equipamento.marca, model=equipamento.modelo, exit=partes[0], sub_exit=partes[1], motive=motive)
         
         # executando a movimentação
         mov = mainStock.Movimentacao(ID= equipamento.id, Saida= partes[0], subSaida= partes[1], Entrada= entry, subEntrada= sub_entry, Motivo= motive, observacao= obs, data= dateF, manuseador= user)
         if type(mov) == tuple:
            print(f'\033[1;31;40m{mov[1]}\033[0m')
            return render_template('movement.html', error=mov[1], date=date, entry=entry, sub_entry=sub_entry, id_mac=equipamento.id, brand=equipamento.marca, model=equipamento.modelo, exit=partes[0], sub_exit=partes[1], motive=motive)

         return render_template('movement.html', status='Movimentação realizada com sucesso', date=date)

class SearchController(MethodView):
    def get(self):
      if not logged:
        return redirect('/login')
      return render_template('searsh.html')
      
    def post(self):
      error = ""
      mainStock.runLists(f"{current_app.root_path}/static/models/stockJsons")

      # carrega o banco de dados
      clientes_DATA = f"{current_app.root_path}/static/models/stockJsons/Clientes.json"

      with open(clientes_DATA, "r") as arquivo:
          clientesData = load(arquivo)

      CONFIG_DATA = f"{current_app.root_path}/static/models/dados.json"
      with open(CONFIG_DATA, "r") as arquivo:
        configData = load(arquivo)

      if 'Searsh_ID' in request.form:
         mac_id = request.form["mac_id"]
         if mac_id.replace(" ","") == "":
            error = "Porfavor preencha o campo Mac/ID"
            return render_template('searsh.html', error=error)
         else:
            mac_id = mac_id.upper()
            equipamento = mainStock.searsh(f"_{mac_id}")
         if not equipamento:
            error = "Equipamento não encontrado"
            return render_template('searsh.html', error=error)
         
         return redirect(f'/procura/{mac_id}')
      
      if 'Searsh_ProcuraLista' in request.form:
         locate = request.form["locate"].strip()
         sub_locate = request.form["sub-locate"].strip()

         # verifica se os campos estão vazios
         if locate.replace(" ", "") == "":
            error = 'Porfavor preencha o campo Local'

         # Verifica se os campos foram preenchidos corretamente
         elif locate.lower == 'cliente' and sub_locate != "" and sub_locate.isdigit() == False:
            error = f'{sub_locate} não é um valor válido para Clientes'
         elif locate.lower() not in [l.lower() for l in configData['entradas']]:
            error = f'{locate} não é um valor de local válido'
         elif locate.lower() == 'carro' and sub_locate != "" and sub_locate.lower() not in [sl.lower() for sl in configData['subentradas']]:
            error = f'{sub_locate} não é um valor de sub-Local válido'
         elif locate.lower() == 'cliente' and sub_locate != "" and sub_locate not in clientesData:
            error = f"O cliente {sub_locate} não esta presente no sistema de estoque"

         # retorna o erro
         if error != "":
            return render_template('searsh.html', error=error)
         
         # redireciona para a procura
         return redirect(f'/procura/{locate}:{sub_locate}')

class FoundController(MethodView):
   def get(self, movement_id):
      if not logged:
        return redirect('/login')
      error = ""

      mainStock.runLists(f"{current_app.root_path}/static/models/stockJsons")

      # carrega o banco de dados
      estoque_DATA = f"{current_app.root_path}/static/models/stockJsons/Escritorio.json"
      clientes_DATA = f"{current_app.root_path}/static/models/stockJsons/Clientes.json"
      carro_DATA = f"{current_app.root_path}/static/models/stockJsons/Carro.json"
      ForadoEscritorio_Data = f"{current_app.root_path}/static/models/stockJsons/ForadoEscritorio.json"


      with open(estoque_DATA, "r") as arquivo:
          estoqueData = load(arquivo)

      with open(clientes_DATA, "r") as arquivo:
          clientesData = load(arquivo)

      with open(carro_DATA, "r") as arquivo:
          carroData = load(arquivo)

      with open(ForadoEscritorio_Data, "r") as arquivo:
          ForadoEscritorioData = load(arquivo)


      if ":" in movement_id: # verifica se o movement_id tem o valor : ou seja se ele esta no formato local:sub-local
         local_sub_local = movement_id.split(":")
         local = str(local_sub_local[0]).strip()
         sub_local = str(local_sub_local[1]).strip()
         local_list = {}
         rnumber = int

         if sub_local == '':
            SLocalValue = False
         else:
            SLocalValue = True

         if local.lower() == 'cliente':
            rnumber = randrange(1,6)
            img = f'image/found/user-found/user_{rnumber}.svg'
            local_list = clientesData

         elif local.lower() == 'escritorio':
            img = f'image/found/server-found/server_1.svg'
            local_list = estoqueData
            organizedDict = {}

            for key, v in local_list.items():
               marca = v['marca']
               modelo = v['modelo']
               if marca not in organizedDict:
                  organizedDict[marca] = {}
               if modelo not in organizedDict[marca]:
                  organizedDict[marca][modelo] = {}
               organizedDict[marca][modelo][key] = v

            local_list = organizedDict

         elif local.lower() == 'carro':
            rnumber = randrange(1,6)
            img = f'image/found/user-found/user_{rnumber}.svg'
            local_list = carroData

         elif local.lower() == 'fora':
            rnumber = randrange(1,6)
            img = f'image/found/user-found/user_{rnumber}.svg'
            local_list = ForadoEscritorioData

         else:
            error = 'Problema ao buscar o banco de dados'
            return f'{error}'

         return render_template('found_locate.html',img=img, SLocalValue=SLocalValue, local=local, sub_local=sub_local, local_list=local_list, )

      else: 
         equipamento = mainStock.searsh(f"_{movement_id}")
         if not equipamento:
            return 'equipamento não encontrado'
         return render_template('found_id.html', company=equipamento.empresa, movement_id=movement_id, brand=equipamento.marca, model=equipamento.modelo, mac_id=equipamento.id, Current_locate=equipamento.localizacaoAtual, movimentacao=equipamento.historico)

   def post(self, movement_id): #
      if ":" in movement_id: # verifica se o movement_id tem o valor : ou seja se ele esta no formato local:sub-local
         if 'Searsh_return' in request.form:
            newMovement = request.form['Searsh_return']
            return redirect(f'/procura/{newMovement}')
      else:
         if 'movimentacao' in request.form:
            movement_uuid = request.form['movimentacao']
            return redirect(f'/procura/{movement_id}/{movement_uuid}')




class MovementSearshController(MethodView):
   def get(self, movement_id, movement_uuid):
      if not logged:
        return redirect('/login')
      error = ""
      
      mainStock.runLists(f"{current_app.root_path}/static/models/stockJsons")

      equipamento = mainStock.searsh(f"_{movement_id}") # caso encontre retornara o equipamento como objeto | caso não encontre retornara false

      if not equipamento:
         error = f'Equipamento não encontrado no banco de dados'
         return error
      
      movement = equipamento.historico[movement_uuid]

      if movement['saida'] != "":
         exit = str(movement['saida']).split(':')
         exit = (f"{str(exit[0]).capitalize()} : {str(exit[1]).capitalize()}")
      else:
         exit = ""
         

      if movement['entrada'] != "":
         entry = str(movement['entrada']).split(':')
         if entry[1] == '':
            entry = str(entry[0]).capitalize()
         else:
            entry = (f"{str(entry[0]).capitalize()} : {str(entry[1]).capitalize()}")

      motivo = str((str(movement["motivo"]).split(':'))[0]).capitalize().strip()
      obs = str((str(movement["motivo"]).split(':'))[1]).capitalize().strip()

      manuseador = str(movement['manuseador']).capitalize()
      dataMovimentacao = str(movement['dataMovimentacao']).replace(":", "h")
      data = movement['data']

      if error != "":
         return error
      
      return render_template('found_movement.html', data=data, mac_id=equipamento.id, brand=equipamento.marca, model=equipamento.modelo, Current_locate=equipamento.localizacaoAtual, UltimaMov_Data=equipamento.UltimaMov_Data, exit=exit, entry=entry, motivo=motivo, manuseador=manuseador, obs=obs, dataMovimentacao=dataMovimentacao)

      

      