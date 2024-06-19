from app import app

HOST = 'localhost'
PORT = 4000
DEBUG = True

if __name__ == "__main__":# conferindo se o usuario esta ativando a instancia principal
    app.run(HOST, PORT, DEBUG)