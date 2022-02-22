FROM jupyterhub/k8s-hub:1.1.3

USER root
COPY logo.png /usr/local/share/jupyterhub/static/images/jupyterhub-80.png
COPY favicon.ico /usr/local/share/jupyterhub/static/favicon.ico
COPY template /usr/local/share/jupyterhub/templates
COPY css /usr/local/share/jupyterhub/static/css
COPY images /usr/local/share/jupyterhub/static/images
COPY api_client.py /usr/local/lib/python3.8/dist-packages/kubernetes/client/api_client.py
COPY mysqlauthenticator /srv/mysqlauthenticator
RUN python3 -m pip install --no-cache /srv/mysqlauthenticator -i https://mirrors.aliyun.com/pypi/simple/

USER jovyan