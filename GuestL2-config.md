# Guest L2 Configuration
<h4> This guide describes how to create and configure the **Guest L2** switch (level 2 switch configured to prevent communication between devices inside the Guest VLAN). </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add VM
        <ol>
            <li>In GNS3, instantiate the VM by clicking on the Switches tab on the left → New Template → Install from the GNS3 server (recommended) → Switches → Open vSwitch → Install → choose where to run the VM → Finish. </li>
            <li>Drag the VM into the GNS3 project
                <ol>
                    <li>Connect "eth0" port to the L2's "eth5" port.</li>
                    <li>Connect "eth1"/"eth2" ports to the machines in the Guest VLAN.</li>
                </ol>
            </li>
        </ol>
    </li>
    <li>Start and open the VM's console.</li>
</ol>

## Step 2: Import Settings
<li>Copy and paste all the settings in the console</li>

``` shell
    ovs-vsctl del-br br0

    ovs-vsctl add-br br0
    ip link set br0 up

    ovs-vsctl add-port br0 eth0
    ovs-vsctl set port eth0 trunks=30
    ovs-vsctl set port eth0 other_config:isolated=false

    ovs-vsctl add-port br0 eth1 tag=30
    ovs-vsctl set port eth1 other_config:isolated=true
    ovs-vsctl add-port br0 eth2 tag=30
    ovs-vsctl set port eth2 other_config:isolated=true
    ovs-vsctl add-port br0 eth3 tag=30
    ovs-vsctl set port eth3 other_config:isolated=true

    ovs-ofctl del-flows br0
    ovs-ofctl add-flow br0 "priority=100, actions=NORMAL"

```