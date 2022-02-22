from setuptools import setup

setup(
    name='jupyterhub-mysqlauthenticator',
    version='0.1.dev0',
    description='mysqlauthenticator for JupyterHub',
    url='https://github.com/tygxy/jupyterhub_localauthenticor',
    author='fangying',
    author_email='fangying@newland.com.cn',
    license='Apache 2.0',
    packages=['mysqlauthenticator'],
    install_requires=[
        'jupyterhub',
        'python-jose',
        'wheel',
        'sqlalchemy',
        'mysql-connector',
        'werkzeug',
    ]
)
