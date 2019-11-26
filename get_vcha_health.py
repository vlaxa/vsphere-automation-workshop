# Product: vCenter server/vCenter Server High Availability (VCHA)
# Description: Python script to Get vCenter server HA health information

from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl

# For VC 6.5/6.0
#s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# For VC 6.7
s = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
s.verify_mode = ssl.CERT_NONE
c= SmartConnect(host="10.188.140.24", user="administrator@vsphere.local", pwd="VMware1!",sslContext=s)

vcha = c.content.failoverClusterManager

VchaClusterHealth = vcha.GetVchaClusterHealth()

vcha_health_Messages = VchaClusterHealth.healthMessages
print("VCHA Health messages:")
for health_data in vcha_health_Messages:
        print(health_data.message)

print("\nAdditional Information:",VchaClusterHealth.additionalInformation)

vcha_runtime_info = VchaClusterHealth.runtimeInfo
print("\nVCHA Cluster Mode:",vcha_runtime_info.clusterMode)
print("\nVCHA Cluster State:",vcha_runtime_info.clusterState)

vcha_node_info = vcha_runtime_info.nodeInfo

print("\nVCHA Node information:")
for node in vcha_node_info:
        print(node.nodeRole+":"+node.nodeIp+":"+node.nodeState)
