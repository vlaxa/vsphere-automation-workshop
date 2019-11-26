# Product: vCenter server/vCenter Server High Availability (VCHA)
# Description: Script to initiate vCenter Server High Availability failover

from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl

# For VC 6.5/6.0
#s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# For VC 6.7
s = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
s.verify_mode = ssl.CERT_NONE
c= SmartConnect(host="10.188.140.24", user="administrator@vsphere.local", pwd="VMware1!",sslContext=s)

vcha=c.content.failoverClusterManager
task = vcha.initiateFailover_Task(True)

while(task.info.state != "success"):
        continue
print("Initiate Failover task is completed")
