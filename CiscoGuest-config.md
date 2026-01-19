# Cisco L2 Configuration
<h4> This guide describes how to create and configure the **GuestL2** switch (level 2 switch configured to prevent communication between devices inside the Guest VLAN). </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add VM
        <ol>
            <li>In GNS3, instantiate the VM by clicking on the Switches tab on the left → New Template → Install from the GNS3 server (recommended) → Switches → Cisco IOSvL2 → Install → choose where to run the VM → IOSvL2 version 15.2(20200924:215240) → vios_l2-adventerprisek9-m.ssa.high_iron_20200929.qcow2 → Next → follow the on-screen instructions.</li>
            <li>Drag the VM into the GNS3 project
                <ol>
                    <li>Connect "Gi0/0" port to the L2's "eth5" port.</li>
                    <li>Connect "Gi0/1" port to the Guest-Android machine.</li>
                    <li>Connect "Gi0/2" port to the Guest-Simulator1 machine.</li>
                    <li>Connect "Gi0/3" port to the Guest-Simulator2 machine.</li>
                </ol>
            </li>
        </ol>
    </li>
    <li>Start and open the VM's console.</li>
</ol>

## Step 2: Import Settings
<li>Copy and paste all the settings in the console</li>

``` shell
    enable
    conf t

    vlan 30
        name GUEST
    exit

    interface GigabitEthernet0/0
        description ToL2
        switchport trunk encapsulation dot1q
        switchport mode trunk
        switchport trunk allowed vlan 30
        no shutdown
    exit

    interface range GigabitEthernet0/1-3
        description GUEST_CLIENTS
        switchport mode access
        switchport access vlan 30
        switchport protected
        spanning-tree portfast
        no shutdown
    exit

    end
    wr

```