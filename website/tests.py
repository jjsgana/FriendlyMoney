from config import CurrenciesChoices
print(CurrenciesChoices())
c = ('NZD')
print(type(c))
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Ve3hffM2DBuJJx9k7DwD'
MYSQL_HOST = 'containers-us-west-189.railway.app'
MYSQL_DB = 'railway'
MYSQL_PORT = '6862'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_PORT + '/' +  MYSQL_DB
print(SQLALCHEMY_DATABASE_URI)