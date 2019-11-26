
# Product: vCenter server/vCenter Server High Availability (VCHA)
# Description: Python Script to set vCenter Server High Availability (VCHA) mode
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

# Set Maintenance Mode (Replication is running, but automatic failover is not enabled)
#task = vcha.setClusterMode_Task("maintenance")
# Disable VCHA Cluster
#task = vcha.setClusterMode_Task("disabled")
# Enable VCHA Cluster
task = vcha.setClusterMode_Task("enabled")

while(task.info.state != "success"):
        continue
print("VCHA mode is set to: ", vcha.getClusterMode())
