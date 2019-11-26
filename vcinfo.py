from pyVim.connect import SmartConnect, Disconnect
import ssl

# For VC 6.5/6.0
#s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# For VC 6.7
s = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
s.verify_mode = ssl.CERT_NONE
 
try:
    c = SmartConnect(host="10.188.140.24", user="administrator@vsphere.local", pwd='VMware1!')
    print('Valid certificate')
except:
    c = SmartConnect(host="10.188.140.24", user="administrator@vsphere.local", pwd='VMware1!', sslContext=s)
    print('Invalid or untrusted certificate')
 
aboutInfo=c.content.about
 
print("Product Name:",aboutInfo.fullName)
print("Product Build:",aboutInfo.build)
print("Product Unique Id:",aboutInfo.instanceUuid)
print("Product Version:",aboutInfo.version)
print("Product Base OS:",aboutInfo.osType)
print("Product vendor:",aboutInfo.vendor)
 
Disconnect(c)