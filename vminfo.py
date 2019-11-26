from pyVim.connect import SmartConnect, Disconnect
import ssl
 
# For VC 6.5/6.0
#s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# For VC 6.7
s = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
s.verify_mode = ssl.CERT_NONE
 
try:
    c = SmartConnect(host="10.188.140.23", user="root", pwd='VMware1!')
    print('Valid certificate')
except:
    c = SmartConnect(host="10.188.140.23", user="root", pwd='VMware1!', sslContext=s)
    print('Invalid or untrusted certificate')
 
datacenter = c.content.rootFolder.childEntity[0]
vms = datacenter.vmFolder.childEntity
 
for i in vms:
    print(i.name)
 
Disconnect(c)