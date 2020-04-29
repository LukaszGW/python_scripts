from mysql.connector import (connection)

'''
Script connect to SQL database. Required parametres. User Name, User Password, host ip, database name, query in SQL
'''

base = {'website_name': {
            'host': 'host_ip',
            'user': 'Enter_USER_NAME',
            'pass':'Enter_USER_PASSWORD',
            'database': 'Enter_Database_Name'},
        'wordpress_site': {
            'host': 'host_ip',
            'user': 'Enter_USER_NAME',
            'pass':'Enter_USER_PASSWORD',
            'database': 'Enter_Database_Name'
        }
    }
	
def connection_website(base):
    cnx = connection.MySQLConnection(user=base['website_name']['user'], password=base['website_name']['pass'],
                                 host=base['website_name']['host'],
                                 database=base['website_name']['database'])
    return cnx

def connection_wordpress(base):
    cnx = connection.MySQLConnection(user=base['wordpress_site']['user'], password=base['wordpress_site']['pass'],
                                 host=base['wordpress_site']['host'],
                                 database=base['wordpress_site']['database'])
    return cnx

def dane_bazy(query, cnx):
    curs = cnx.cursor()
    curs.execute(query)
    dane_bazy = [curs.fetchall(), curs.column_names]
    print(dane_bazy)
    curs.close()
    return dane_bazy

