import pyodbc
server = 'localhost'
bd = 'FerreteriaDB'
user = 'oliver'
password = '12345'

try:
    conexion = pyodbc.connect('DRIVER={SQL Server}; SERVER=' +
                              server + ';DATABASE=' + bd + ';UID=' + user+';PWD=' + password)
    print('conexion exitosa')
except:
    print('Error al intentar conectarse')
    