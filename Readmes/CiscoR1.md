# Cisco Router R1 Configuration
<h4> This guide describes how to create and configure the **Cisco iOSv15.9** router (perimetral router to connect Attacker Virtual Machine VM with University Network). </h4>

## Step 1: VM Installation, Placement, and Configuration
<ol>
    <li>Add Qemu VM
        <ol>
            <li>In GNS3, instantiate the virtual machine by clicking on the Routers tab on the left → New Template → Install from the GNS3 server (recommended) → Routers → Cisco IOSv → Install → choose where to run the vm → IOSv version 15.9 → vios-adventerprisek9-m.spa.159-3.m6.qcow2 → Next → follow the on-screen instructions.</li>
            <li>Drag the qemu vm into the GNS3 project
                <ol>
                    <li>Connect "Gi0/0" port to the OpnSense's "eth2" port.</li>
                    <li>Connect the "Gi0/1" port to the OPNsense firewall .</li>  
            </li>
        </ol>
    </li>
    <li>Start and open the VM's console.</li>
</ol>

## Step 2: Import setting
<li>Copy and paste all the settings in the console</li>

``` shell
    enable
    conf t
    hostname R1

    interface GigabitEthernet0/0
      description to-Internet
      ip address dhcp
      no shutdown
      ip nat outside
    exit

    interface GigabitEthernet0/1
      description to-University 
      ip address 203.0.213.1 255.255.255.248
      no shutdown
      ip nat inside
    exit
 
    access-list 1 permit 10.0.0.0 0.0.255.255
    ip nat inside source list 1 interface GigabitEthernet0/0 overload
    ip route 10.0.0.0 255.255.0.0 203.0.213.2

    end
    write memory
```