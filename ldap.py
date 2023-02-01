# DO NOT RUN THIS THROUGH AN IDE INSTEAD USE A TERMINAL
# An IDE will echo your password!
import ldap3
from getpass import getpass

server = ldap3.Server('ldaps://esss.lu.se')
password = getpass("password >>")
conn = ldap3.Connection(server, user='mattclarke@ESSS.SE',  password=password, auto_bind=True, read_only=True)
conn.search('dc=esss,dc=lu,dc=se', '(&(objectCategory=person)(objectClass=user)(cn=matt*))')

print(conn.entries)