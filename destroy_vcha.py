# Product: vCenter server/vCenter Server High Availability (VCHA)
# Description: Python script to destroy vCenter server HA 

from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
#Destroy vCenter server HA
# For VC 6.5/6.0
#s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# For VC 6.7
s = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
s.verify_mode = ssl.CERT_NONE
si= SmartConnect(host="10.188.140.24", user="administrator@vsphere.local", pwd="VMware1!",sslContext=s)
content=si.content

#Getting VCHA configurator managed object
vcha=si.content.failoverClusterConfigurator

#Getting VCHA cluster manager
vcha_cluster_manager=si.content.failoverClusterManager

# Setting vCenter HA to "disabled" mode.
task = vcha_cluster_manager.setClusterMode_Task("disabled")
while(task.info.state != "success"):
        continue

#Getting VCHA cluster mode
VCHA_mode=vcha_cluster_manager.getClusterMode()
if (VCHA_mode == "disabled"):
        vcha.destroyVcha_Task() #Destroing it
else:
        print("VCHA must be in disabled mode before destrying it")
