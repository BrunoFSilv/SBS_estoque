from json import load


def Check(user, pwd, USER_DATA):
    with open(USER_DATA, "r") as arquivo:
        userData = load(arquivo)
    for key, content in userData.items():
        if key == user.upper().replace(" ","") and content['password'] == pwd.replace(" ",""):
            return True
    return False