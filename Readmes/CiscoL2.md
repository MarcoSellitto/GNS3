# NOTA: Manca la Gi2/2 nella configurazione!!
# Cisco L2 Configuration
<h4> This guide describes how to create and configure the **Cisco L2** switch (level 2 switch to connect all the VLANs). </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by clicking on the Switches tab on the left → New Template → choose where to run the container → Switches → Cisco IOSvL2 → Install → choose where to run the container → IOSvL2 version 15.2(20200924:215240) → vios_l2-adventerprisek9-m.ssa.high_iron_20200929.qcow2 → Next → follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project and connect "Gi0/0" port to the OpnSense's "em1" port.</li>
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

    end
    wr

```