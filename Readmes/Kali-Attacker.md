# Attacker VM Configuration
<h4> This guide describes how to create and configure the virtual machine VM for the Attacker. This Vm is directly connected through Switch to NAT Node to simulate a host coming from the WAN  </h4>

## Step 1: VM Installation, Placement, and Configuration
<ol>
    <li>Add QEMU VM
        <ol>
            <li>In GNS3, instantiate the VM by going to Edit → Preferences → Qemu VMs → New → choose where to run the VM → enter the image kali-linux-2025.2-qemu-amd64.qcow2 → choose a name and follow the on-screen instructions.</li>
            <li>Drag the VM to the GNS3 project and connect it to the Switch1 on eth1, the NAT Node is conneted to eth0</li>
        </ol>
    </li>
    <li>Start and open the VM's console.</li>
</ol>


## Step 2: Network Configuration
<li> Set Network Manager configuration. To add the route for router R1 (ip: 192.168.122.38), to visualize the WebServer page of the university ( ip: 203.0.213.3) </li>

``` shell
    $ sudo nmcli connection modify "Wired Connection 1" +ipv4.routes  "203.0.213.0/29 192.168.122.38" 
```
To add the name of the web server
<li>Open the file</li>

``` shell
    $ sudo nano /etc/hosts
```

<li>Add the line:</li>

```
   203.0.213.3  uni.local

```
<li>Update the repositories and install the upgrades</li>

``` shell
    $ sudo apt update
    $ sudo apt upgrade 
```

## Step 3: Certificate Installation
<li> Install the Web Server Certificate.</li>
The first step is to download the rootCA.cer for Domain Controller.
Now install the certificate. Move into directory that contains the file rootCA.cer and launch on console:
``` shell
    $  sudo cp rootCa.cer /usr/local/share/ca-certificates/rootCA.crt
    $  sudo update-ca-certificates
```
Import the certificate into browser. For Mozilla:
<li> Preferences → Privacy & Security → View Certificates → Authorities → Import</li>
select /usr/local/share/ca-certificates/rootCA.crt → select “Trust this CA to identify websites” → OK.
<li>Close and reload the browser</li>


At this point, the Attacker Machine is ready and connected to the Internet. 