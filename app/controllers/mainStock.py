# Bibliotecas
from datetime import datetime, date
from json import load, dump, loads, dumps
from uuid import uuid4

# carregando os dicionarios e listas #

global estoqueData, estoque_DATA 
global clientesData, clientes_DATA
global carroData, carro_DATA
global ForadoEscritorioData, ForadoEscritorio_DATA

def runLists(data_path):
    global estoqueData, estoque_DATA 
    global clientesData, clientes_DATA
    global carroData, carro_DATA
    global ForadoEscritorioData, ForadoEscritorio_DATA

    estoque_DATA = f"{data_path}/Escritorio.json"
    clientes_DATA = f"{data_path}/Clientes.json"
    carro_DATA = f"{data_path}/Carro.json"
    ForadoEscritorio_DATA = f"{data_path}/ForadoEscritorio.json"

    with open(estoque_DATA, "r") as arquivo:
        estoqueData = load(arquivo)

    with open(clientes_DATA, "r") as arquivo:
        clientesData = load(arquivo)

    with open(carro_DATA, "r") as arquivo:
        carroData = load(arquivo)

    with open(ForadoEscritorio_DATA, "r") as arquivo:
        ForadoEscritorioData = load(arquivo)

#region - Funções e Class:
def CheckData(Data: str, Return = 'int'): # Data = DDMMAA or DDMMAAAA, Return = 'int', 'bool', 'str' 'formatada', 'dia', 'mes', 'ano' Função responsavel apenar por formatar datas

#    Esta função é responsavel por analizar e formatar uma data.
#    formatando ela para o padrão dia-mes-ano, dando um retorno deste valor em um número inteiro.
#    alem disso sera analizado:
#    - Se a data esta no futuro.
#    - Se o Valor possui o número de caracteres de uma data.
#    - Se o ano, mes, dia é válido

# region Pré declaração das variaveis
    DataCheck = True
    Error = str
    Dia, DiaAA = int, int
    Mes, MesAA = int, int
    Ano, AnoAA = int, int
# endregion


# region Main

    data_obj = datetime.strptime(Data, "%Y-%m-%d")
    Data = data_obj.strftime("%d%m%Y")

    if len(Data) == 8 or len(Data) == 6: # checa se a quantidade de números na data esta correta
        if len(Data) == 6: # Converte a data de 6 digitos xx/xx/xx para a de 8 xx/xx/xxxx
            Seculo = date.today().strftime("%Y")
            Data = f'{Data[:4]}{Seculo[:2]}{Data[4:]}'
        # Separação da data inserida em Dia Mes e Ano
        Dia = int(Data[:2])
        Mes = int(Data[2:4])
        Ano = int(Data[4:])
        Data = int(Data)
        # Separação da data Atual em Dia Mes e Ano
        DiaAA = int(date.today().strftime("%d"))
        MesAA = int(date.today().strftime("%m"))
        AnoAA = int(date.today().strftime("%Y"))
        if Ano > AnoAA or Ano == AnoAA and Mes > MesAA or Ano == AnoAA and Mes == MesAA and Dia > DiaAA :# Checa se a data inserida é maior do que a data atual
            DataCheck = False
            Error = f'A data inserida - {Dia}/{Mes}/{Ano} - é maior doque a data atual - {DiaAA}/{MesAA}/{AnoAA} -'
        if Ano > AnoAA:# Checa se o ano é válido
            DataCheck = False
            Error = f'O ano inserido - {Ano} - está no futuro'
        if Mes > 12 or Mes < 1:# Checa se o mês é válido
            DataCheck = False
            Error = f'O mês inserido - {Mes} - é invalido'
        if Data < 1:# Checa se o dia é maior do que 1
            DataCheck = False
            Error = f'O dia inserido - {Dia} - não pode ser menor do que '
        else:# Checa os dias levando em consideração os meses
            if Mes == 2 and Ano % 4 == 0 and Dia > 29 or Dia < 1:# Valida os dias no mês de fevereiro com 29 dias
                DataCheck = False
                Error = f'O dia inserido - {Dia} - é invalido'
            elif Mes == 2 and Ano % 4 != 0 and Dia > 28 or Dia < 1:# Valida os dias no mês de fevereiro com 28 dias
                DataCheck = False
                Error = f'O dia inserido - {Dia} - é invalido'
            elif Mes == 1 and Dia > 31 or Mes == 3 and Dia > 31 or Mes == 5 and Dia > 31 or Mes == 7 and Dia > 31 or Mes == 8 and Dia > 31 or Mes == 10 and Dia > 31 or Mes == 12 and Dia > 31:# Valida os dias dos meses com 31 dias
                DataCheck = False
                Error = f'O dia inserido - {Dia} - é invalido'
            elif Mes == 4 and Dia > 30 or Mes == 6 and Dia > 30 or  Mes == 9 and Dia > 30 or Mes == 11 and Dia > 30:# Valida os dias dos meses com 30 dias
                DataCheck = False
                Error = f'O dia inserido - {Dia} - é invalido'
    else:
        DataCheck = False
        Error = f'O valor inserido - {Data} - não é uma data'
# endregion

# region Retorno Da função
    if Return == 'bool':
        return DataCheck
    elif DataCheck == False:
        return False, f'{Error}'
    elif Return == 'int':
        return Data # retorna o Valor da Data em DDMMAAAA
    elif Return == 'str':
        return str(Data)
    elif Return == 'formatada':
        if Dia < 10:
            return f'0{Dia}/{Mes}/{Ano}'
        if Mes < 10:
            return f'{Dia}/0{Mes}/{Ano}'
        if Dia < 10 and Mes < 10:
            return f'0{Dia}/0{Mes}/{Ano}'
        return f'{Dia}/{Mes}/{Ano}'
    elif Return == 'dia':
        return Dia
    elif Return == 'mes':
        return Mes
    elif Return == 'ano':
        return Ano

# endregion

def serializeEquipamento(equipamento): # recebe o objeto "equipamento" e retorna uma lista com os atibutos do mesmo
    historico = eval(str(equipamento.historico))
    return {
            "marca": equipamento.marca,
            "modelo": equipamento.modelo,
            "id": equipamento.id,
            "empresa": equipamento.empresa,
            "localizacao_atual": equipamento.localizacaoAtual,
            "UltimaMov_Data": equipamento.UltimaMov_Data,
            "historico": historico,
        }

def deserializeEquipamento(equipamentoDic): # recebe uma lista com as informações de um objeto e retorna o objeto
    historico = eval(str(equipamentoDic['historico'])) # caso o o historico do equipamento esteja no formato de str o covertera para um dict
    temp = f"_{equipamentoDic['id']}"
    exec(f"{temp} = equipamento(equipamentoDic['marca'], equipamentoDic['modelo'], equipamentoDic['id'], equipamentoDic['empresa'], equipamentoDic['localizacao_atual'], equipamentoDic['UltimaMov_Data'], historico)")
    return eval(temp)

def searsh(wanted): # rebe qual equipamento deseja encontrar (_70A56A497CB7) e retorna o objeto

    for key, i in estoqueData.items():
        if key == wanted:
            return deserializeEquipamento(i)
        
    for key, e in clientesData.items():
        for key, i in e.items():
            if key == wanted:
                return deserializeEquipamento(i)
            
    for key, e in carroData.items():
        for key, i in e.items():
            if key == wanted:
                return deserializeEquipamento(i)
    
    for key, e in ForadoEscritorioData.items():
        for key, i in e.items():
            if key == wanted:
                return deserializeEquipamento(i)
            
    return False

def Entrada(Entrada: str, subEntrada: str,Motivo:str, data: str, manuseador: str, MARCA: str, MODELO: str, ID: str, EMPRESA: str, obs= '' ):# executa a criação de um equipamento (obj) dentro de uma lista
    movement_id = uuid4()
    movement_id = str(movement_id)
    historico = {movement_id: {"saida": "", "entrada": f"{Entrada}:{subEntrada}", "motivo": f"{Motivo}:{obs}", "data": data, "manuseador": manuseador, "dataMovimentacao": datetime.now().strftime('%d/%m/%Y %H:%M')}}# montando um historico de movimentação
    localizacaoAtual = f"{Entrada}:{subEntrada}"
    exec(f'_{ID} = equipamento("{MARCA}", "{MODELO}", "{ID}", "{EMPRESA}", "{localizacaoAtual}", "{data}", "{historico}")')

    if Entrada.upper() == 'ESCRITORIO':
        exec(f'estoqueData["_{ID}"] = serializeEquipamento(_{ID})')
        with open(estoque_DATA, "w") as arquivo:
            dump(estoqueData, arquivo)

    elif Entrada.upper() == 'CLIENTE':
        if subEntrada not in clientesData:
            clientesData[subEntrada] = {}
        exec(f'clientesData[subEntrada]["_{ID}"] = serializeEquipamento(_{ID})')
        with open(clientes_DATA, "w") as arquivo:
            dump(clientesData, arquivo)

    elif Entrada.upper() == 'CARRO':
        if subEntrada.capitalize() not in carroData:
            carroData[subEntrada.capitalize()] = {}
        exec(f'carroData[subEntrada]["_{ID}"] = serializeEquipamento(_{ID})')
        with open(carro_DATA, "w") as arquivo:
            dump(carroData, arquivo)

    elif Entrada.upper() == 'FORA':
        if subEntrada.capitalize() not in ForadoEscritorioData:
            ForadoEscritorioData[subEntrada.capitalize()] = {}
        exec(f'ForadoEscritorioData[subEntrada]["_{ID}"] = serializeEquipamento(_{ID})')
        with open(ForadoEscritorio_DATA, "w") as arquivo:
            dump(ForadoEscritorioData, arquivo)

def Movimentacao(ID: str, Saida: str, subSaida: str, Entrada: str, subEntrada: str, Motivo: str, observacao: str, data: str, manuseador: str):# faz a movimentação do equipamento(obj) de uma lista para outra
    # encontrar o equipamento
    equipamento = searsh(f'_{ID}')
    if not equipamento:
        return False, "Erro na busca pelo equipamento - o equipamento não existe no sistema de stoque - "
    # checagens de segurança
    if equipamento.localizacaoAtual != f'{Saida}:{subSaida}':
        return False, f"Erro na checagem da localização - atualmente o equipamento esta em {equipamento.localizacaoAtual} e não em {Saida}:{subSaida} - "
    Data_Split = data.split('/')# ['DD', 'MM', 'AAAA']
    DataAA_Split = equipamento.UltimaMov_Data.split("/")# ['DD', 'MM', 'AAAA']
    if int(DataAA_Split[2]) > int(Data_Split[2]) or int(DataAA_Split[2]) == int(Data_Split[2]) and int(DataAA_Split[1]) > int(Data_Split[1]) or int(DataAA_Split[2]) == int(Data_Split[2]) and int(DataAA_Split[1]) == int(Data_Split[1]) and int(DataAA_Split[0]) > int(Data_Split[0]) :# Checa se a data inserida é menor do que a data da ultima movimentação
        return False, f'A data inserida - {Data_Split[0]}/{Data_Split[1]}/{Data_Split[2]} - é menor doque a data da ultima movimentação - {DataAA_Split[0]}/{DataAA_Split[1]}/{DataAA_Split[2]} -'
    # atuliazar os valores dele
    movement_id = uuid4()
    movement_id = str(movement_id)
    historicoMovimentacao = {"saida":f"{Saida}:{subSaida}", "entrada": f"{Entrada}:{subEntrada}", "motivo": f"{Motivo}:{observacao}", "data": data, "manuseador": manuseador, "dataMovimentacao": datetime.now().strftime('%d/%m/%Y %H:%M')}
    equipamento.historico[movement_id] = historicoMovimentacao
    equipamento.localizacaoAtual = f"{Entrada}:{subEntrada}"
    equipamento.UltimaMov_Data = data

    # retirar ele da lista em que ele esta
    if Saida.lower() == 'escritorio':
        try:
            estoqueData.pop(f'_{ID}')
            with open(estoque_DATA, "w") as arquivo:
                dump(estoqueData, arquivo)
        except IndexError:
            print(f'O elemento _{ID} não esta presente na lista')

    elif Saida.lower() == 'cliente':
        try:
            clientesData[subSaida].pop(f'_{ID}')
            with open(clientes_DATA, "w") as arquivo:
                dump(clientesData, arquivo)
        except IndexError:
            print(f'O elemento _{ID} não esta presente na lista')

    elif Saida.lower() == 'carro':
        try:
            carroData[subSaida].pop(f'_{ID}')
            with open(carro_DATA, "w") as arquivo:
                dump(carroData, arquivo)
        except IndexError:
            print(f'O elemento _{ID} não esta presente na lista')

    elif Saida.lower() == 'fora':
        try:
            ForadoEscritorioData[subSaida].pop(f'_{ID}')
            with open(ForadoEscritorio_DATA, "w") as arquivo:
                dump(ForadoEscritorioData, arquivo)
        except IndexError:
            print(f'O elemento _{ID} não esta presente na lista')     

    # adicionar a nova lista
    if Entrada.lower() == 'escritorio':
        try:
            estoqueData[f'_{ID}'] = serializeEquipamento(equipamento)
            with open(estoque_DATA, "w") as arquivo:
                dump(estoqueData, arquivo)
        except IndexError:
            print(f'Não foi possível adicionar o objeto _{ID} na lista {Entrada}')
    
    elif Entrada.lower() == 'cliente':
        try:
            if subEntrada not in clientesData:
                clientesData[subEntrada] = {}
            clientesData[subEntrada][f'_{ID}'] = serializeEquipamento(equipamento)
            with open(clientes_DATA, "w") as arquivo:
                dump(clientesData, arquivo)
        except IndexError:
            print(f'Não foi possível adicionar o objeto _{ID} na lista {Entrada}')
    
    elif Entrada.lower() == 'carro':
        try:
            if subEntrada.lower() not in [se.lower() for se in carroData]:
                carroData[subEntrada] = {}
            carroData[subEntrada][f'_{ID}'] = serializeEquipamento(equipamento)
            with open(carro_DATA, "w") as arquivo:
                dump(carroData, arquivo)
        except IndexError:
            print(f'Não foi possível adicionar o objeto _{ID} na lista {Entrada}')

    elif Entrada.lower() == 'fora':
        try:
            if subEntrada.lower() not in [se.lower() for se in carroData]:
                ForadoEscritorioData[subEntrada] = {}
            ForadoEscritorioData[subEntrada][f'_{ID}'] = serializeEquipamento(equipamento)
            with open(ForadoEscritorio_DATA, "w") as arquivo:
                dump(ForadoEscritorioData, arquivo)
        except IndexError:
            print(f'Não foi possível adicionar o objeto _{ID} na lista {Entrada}')
 
    return True, "Movimentação realizada com sucesso"

#def MovimentacaoQt(Entrada: str, subEntrada: str,Motivo:str, qtd: int, data: str, manuseador: str, MARCA: str, MODELO: str, EMPRESA: str, obs= '' ):# Faz a movimentação de itens quantitativos os quais não possuem ID


class equipamento:
    def __init__(self, MARCA: str, MODELO: str, ID: str, EMPRESA: str, LOCALIZACAOATUAL: str, ULTIMAMOV_DATA: str, HISTORICO: dict ):
        self.marca = MARCA
        self.modelo = MODELO
        self.id = ID
        self.historico = HISTORICO
        self.empresa = EMPRESA
        self.localizacaoAtual = LOCALIZACAOATUAL
        self.UltimaMov_Data = ULTIMAMOV_DATA

    def ShowObject(self): # da um Print em todos os atributos do objeto
        print(f'Marca:{self.marca}\nModelo:{self.modelo}\nId:{self.id}\nEmpresa:{self.empresa}\nLocalização Atual:{self.localizacaoAtual}\nHistórico:{self.historico}')

#endregion
