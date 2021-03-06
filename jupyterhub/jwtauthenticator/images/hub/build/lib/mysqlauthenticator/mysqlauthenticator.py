# coding:utf-8

from jupyterhub.auth import Authenticator
from tornado import gen

from mysqlauthenticator.DAO.base import init
from mysqlauthenticator.DAO.user import User


class MysqlAuthenticator(Authenticator):

	"""JupyterHub Authenticator Based on Mysql"""

	def __init__(self, **kwargs):
		super(MysqlAuthenticator, self).__init__(**kwargs)

	@gen.coroutine
	def authenticate(self, handler, data):

		db_url = "mysql+mysqlconnector://root:jKYDZi53lD@52.131.217.1:31306/user"
		session = init(db_url)

		username = data['username']
		passwd = data['password']

		try:
			user = session.query(User).filter(User.username == username).one()
			if user and user.check_password(passwd):
				return user.username
			else:
				return None
		except:
			return None


