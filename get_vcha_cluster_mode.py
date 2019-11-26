# Product: vCenter server/vCenter Server High Availability (VCHA)
# Description: Python Script to get vCenter Server High Availability (VCHA) mode

from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl

# Script to get vCenter Server High Availability (VCHA) mode
# Below is Python 2.7.x code, which can be easily converted to python 3.x version

# For VC 6.5/6.0
#s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# For VC 6.7
s = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
s.verify_mode = ssl.CERT_NONE
c= SmartConnect(host="10.188.140.24", user="administrator@vsphere.local", pwd="VMware1!",sslContext=s)
vcha=c.content.failoverClusterManager

VCHA_mode=vcha.getClusterMode()
print("VCHA Cluster mode:", VCHA_mode)
