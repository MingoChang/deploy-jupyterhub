FROM jupyterhub/k8s-hub:1.1.3

USER root
COPY jwtauthenticator /srv/jwtauthenticator
COPY sqliteauthenticator /srv/sqliteauthenticator
COPY logo.png /usr/local/share/jupyterhub/static/images/jupyterhub-80.png
COPY css /usr/local/share/jupyterhub/static/css
COPY images /usr/local/share/jupyterhub/static/images
COPY templates /usr/local/share/jupyterhub/templates
RUN python3 -m pip install --no-cache /srv/jwtauthenticator -i https://mirrors.aliyun.com/pypi/simple/
RUN python3 -m pip install --no-cache /srv/sqliteauthenticator -i https://mirrors.aliyun.com/pypi/simple/
USER jovyan
