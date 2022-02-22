import jwt
import time

def create_url():
    jupyterhub_host = "192.168.133.220"
    jupyterhub_port = "30002"
    username = '18960863892'
    SECRET_KEY = "5020408408b8984b2e25b47e544f3f3943b9f86ddd15d501287ed32a70e3f168"

    timenow = int(time.time())
    payload = {"username": username, "timestamp":str(timenow)}
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')
    url = "http://" + jupyterhub_host + ":" + jupyterhub_port + "/login?auth_token=" + token
    print(url)

if __name__ == "__main__":
    create_url()
