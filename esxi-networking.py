#! /usr/bin/env python
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import json

vsphere_hosts = ['10.188.140.23']
vsphere_password = 'VMware1!'
vsphere_username = 'root'


def main():
    esxi_hosts = []
    for vsphere_host in vsphere_hosts:
        serviceInstance = SmartConnectNoSSL(host=vsphere_host, user=vsphere_username, pwd=vsphere_password)
        content = serviceInstance.RetrieveContent()

        host_view = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.HostSystem], True)

        hosts = [host for host in host_view.view]
        for host in hosts:
            host_info = dict()
            host_pnics = capture_host_pnics(host)
            host_vnics = capture_host_vnics(host)
            host_vswitches = capture_host_vswitches(host)
            host_portgroups = capture_host_portgroups(host)
            host_info.update(
                {'host': vsphere_host, 'hostname': host.name,
                 'pnics': host_pnics, 'vswitches': host_vswitches,
                 'portgroups': host_portgroups, 'vnics': host_vnics})
            esxi_hosts.append(host_info)

        Disconnect(serviceInstance)

    print(json.dumps(esxi_hosts, indent=4))


# Capture ESXi host physical nics
def capture_host_pnics(host):
    host_pnics = []
    for pnic in host.config.network.pnic:
        pnic_info = dict()
        pnic_info.update(
            {'device': pnic.device, 'driver': pnic.driver, 'mac': pnic.mac})
        host_pnics.append(pnic_info)

    return host_pnics


# Capture ESXi host virtual nics
def capture_host_vnics(host):
    host_vnics = []
    for vnic in host.config.network.vnic:
        vnic_info = dict()
        vnic_info.update(
            {'device': vnic.device, 'portgroup': vnic.portgroup,
             'dhcp': vnic.spec.ip.dhcp, 'ipAddress': vnic.spec.ip.ipAddress,
             'subnetMask': vnic.spec.ip.subnetMask,
             'mac': vnic.spec.mac, 'mtu': vnic.spec.mtu})
        host_vnics.append(vnic_info)
    return host_vnics


# Capture ESXi host virtual switches
def capture_host_vswitches(host):
    host_vswitches = []
    for vswitch in host.config.network.vswitch:
        vswitch_info = dict()
        vswitch_pnics = []
        vswitch_portgroups = []
        for pnic in vswitch.pnic:
            pnic = pnic.replace('key-vim.host.PhysicalNic-', '')
            vswitch_pnics.append(pnic)
        for pg in vswitch.portgroup:
            pg = pg.replace('key-vim.host.PortGroup-', '')
            vswitch_portgroups.append(pg)
        vswitch_info.update(
            {'name': vswitch.name, 'pnics': vswitch_pnics,
             'portgroups': vswitch_portgroups, 'mtu': vswitch.mtu})
        host_vswitches.append(vswitch_info)

    return host_vswitches


def capture_host_portgroups(host):
    host_portgroups = []
    for portgroup in host.config.network.portgroup:
        portgroup_info = dict()
        portgroup_info.update(
            {'name': portgroup.spec.name, 'vlanId': portgroup.spec.vlanId,
             'vswitchName': portgroup.spec.vswitchName,
             'nicTeamingPolicy': portgroup.spec.policy.nicTeaming.policy,
             'allowPromiscuous': portgroup.spec.policy.security.allowPromiscuous,
             'macChanges': portgroup.spec.policy.security.macChanges,
             'forgedTransmits': portgroup.spec.policy.security.forgedTransmits})
        host_portgroups.append(portgroup_info)

    return host_portgroups


if __name__ == "__main__":
    main()