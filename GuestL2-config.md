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
	ovs-ofctl del-flows br0
	ovs-ofctl add-flow br0 "priority=200, dl_type=0x0806, actions=NORMAL"
	ovs-ofctl add-flow br0 "priority=200, dl_type=0x0800, nw_proto=17, tp_src=68, tp_dst=67, actions=NORMAL"
	ovs-ofctl add-flow br0 "priority=200, dl_type=0x0800, nw_proto=17, tp_src=67, tp_dst=68, actions=NORMAL"
	ovs-ofctl add-flow br0 "priority=150, dl_type=0x0800, nw_proto=1, actions=NORMAL"
	ovs-ofctl add-flow br0 "priority=100, in_port=eth0, actions=NORMAL"
	ovs-ofctl add-flow br0 "priority=100, in_port=eth1, actions=learn(table=0,idle_timeout=300,priority=200,NXM_OF_ETH_DST[]=NXM_OF_ETH_SRC[],load:NXM_OF_IN_PORT[]->NXM_OF_OUTPUT[]),output:eth0"
	ovs-ofctl add-flow br0 "priority=100, in_port=eth2, actions=learn(table=0,idle_timeout=300,priority=200,NXM_OF_ETH_DST[]=NXM_OF_ETH_SRC[],load:NXM_OF_IN_PORT[]->NXM_OF_OUTPUT[]),output:eth0"
	ovs-ofctl add-flow br0 "priority=100, in_port=eth3, actions=learn(table=0,idle_timeout=300,priority=200,NXM_OF_ETH_DST[]=NXM_OF_ETH_SRC[],load:NXM_OF_IN_PORT[]->NXM_OF_OUTPUT[]),output:eth0"
```