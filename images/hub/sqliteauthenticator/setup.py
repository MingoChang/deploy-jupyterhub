from setuptools import setup

setup(name='sqliteauthenticator',
      version='0.11',
      description='SQLite Authenticator for Jupyterhub',
      author='sparkingarthur',
      license='MIT',
      author_email='sparkingarthur@163.com',
      url='https://github.com/sparkingarthur/jupyterhub-localsqliteauthenticator',
      packages=['sqliteauthenticator'],
      install_requires=[
          'jupyterhub',
          'pycrypto'
      ]
      )
