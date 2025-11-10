# Cisco L2 Configuration
<h4> This guide describes how to create and configure the **Cisco L2** switch (level 2 switch to connect all the VLANs). </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by clicking on the Switches tab on the left → New Template → choose where to run the container → Switches → Cisco IOSvL2 → Install → choose where to run the container → IOSvL2 version 15.2(20200924:215240) → vios_l2-adventerprisek9-m.ssa.high_iron_20200929.qcow2 → Next → follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project
                <ol>
                    <li>Connect "Gi0/0" port to the OpnSense's "em1" port.</li>
                    <li>Add 9 Ethernet switches (one for each VLAN). Rename them as follows.</li>
                    <li>Connect the "Gi0/1" port to the DMZ switch.</li>
                    <li>Connect the "Gi0/2" port to the Management switch.</li>
                    <li>Connect the "Gi0/3" port to the Classroom1 switch.</li>
                    <li>Connect the "Gi1/0" port to the Classroom2 switch.</li>
                    <li>Connect the "Gi1/1" port to the Guests switch.</li>
                    <li>Connect the "Gi1/2" port to the Segreteria switch.</li>
                    <li>Connect the "Gi1/3" port to the Laboratorio switch.</li>
                    <li>Connect the "Gi2/0" port to the Wazuh switch.</li>
                    <li>Connect the "Gi2/1" port to the DC (Domain Controller) switch.</li>
                </ol>
            </li>
        </ol>
    </li>
    <li>Start and open the container's console.</li>
</ol>

## Step 2: Import setting
<li>Copy and paste all the settings in the console</li>

``` shell
    enable
    conf t

    vlan 2
        name DMZ
    exit
    vlan 99
        name MANAGMENT
    exit
    vlan 10
        name CLASSROOM1
    exit
    vlan 20
    name CLASSROOM2
    exit

    vlan 30
    name GUEST
    exit

    vlan 40
    name SECRETARY
    exit

    vlan 50
    name LABORATORY
    exit

    vlan 60
    name ZABBIX
    exit

    vlan 70
    name DC
    exit

    interface GigabitEthernet0/0
    switchport trunk allowed vlan 2,10,20,30,40,50,60,70,99
    switchport trunk encapsulation dot1q
    switchport mode trunk
    spanning-tree portfast edge trunk
    description Trunk
    no shutdown
    exit

    interface GigabitEthernet0/1
    switchport access vlan 2
    switchport mode access
    description DMZ
    no shutdown
    exit

    interface GigabitEthernet0/2
    switchport access vlan 99
    switchport mode access
    description Management
    no shutdown
    exit

    interface GigabitEthernet0/3
    switchport access vlan 10
    switchport mode access
    description Classroom1
    no shutdown
    exit

    interface GigabitEthernet1/0
    switchport access vlan 20
    switchport mode access
    description Classroom2
    no shutdown
    exit

    interface GigabitEthernet1/1
    switchport access vlan 30
    switchport mode access
    description Guest
    no shutdown
    exit

    interface GigabitEthernet1/2
    switchport access vlan 40
    switchport mode access
    description Secretary
    no shutdown
    exit

    interface GigabitEthernet1/3
    switchport access vlan 50
    switchport mode access
    description Laboratory
    no shutdown
    exit

    interface GigabitEthernet2/0
    switchport access vlan 60
    switchport mode access
    description Zabbix
    no shutdown
    exit

    interface GigabitEthernet2/1
    switchport access vlan 70
    switchport mode access
    description DC
    no shutdown
    exit

    interface GigabitEthernet2/2
    description IDS
    shutdown
    exit

    monitor session 1 source interface GigabitEthernet0/0 both
    monitor session 1 source interface GigabitEthernet0/1 both
    monitor session 1 source interface GigabitEthernet0/2 both
    monitor session 1 source interface GigabitEthernet0/3 both
    monitor session 1 source interface GigabitEthernet1/0 both
    monitor session 1 source interface GigabitEthernet1/1 both
    monitor session 1 source interface GigabitEthernet1/2 both
    monitor session 1 source interface GigabitEthernet1/3 both
    monitor session 1 source interface GigabitEthernet2/0 both
    monitor session 1 source interface GigabitEthernet2/1 both
    monitor session 1 destination interface GigabitEthernet2/2

    interface GigabitEthernet2/2
    no shutdown
    exit

    end
    wr

```