# DNS Configuration in the DMZ
<h4> This guide describes how to create and configure the **DNS** in the DMZ. </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by going to Edit → Preferences → Docker Containers → New → choose where to run the container → enter the image adosztal/dns:latest → choose a name and follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project and connect it to the switch in the DMZ subnet.</li>
        </ol>
    </li>
    <li>Start and open the container's console.</li>
</ol>

## Step 2: Set static IP
<li>Open the file</li>

``` shell
    $ nano /etc/network/interfaces
```
<li>Uncomment the relevant lines and modify the settings as shown below</li>

```
    # Static config for eth0
    auto eth0
    iface eth0 inet static
        address 10.0.2.30
        netmask 255.255.255.0
        gateway 10.0.2.1
        up echo nameserver 127.0.0.1 > /etc/resolv.conf
```

## Step 3: Set the DNS' servers
<li>Open the file</li>

``` shell
    $ nano /etc/dnsmasq.conf
```
For the thesis project, we use the university’s DNS servers.
<li>Add these lines anywhere in the file</li>

```
    no-resolv
    server=193.205.160.3
    server=193.205.160.139
    listen-address=127.0.0.1,10.0.2.30
```

<li>Restart the machine to apply the changes</li>

## Step 4: Map the IP address of the web server.
<li>Open the file</li>

``` shell
    $ nano /etc/hosts
```
<li>Add this line</li>

``` shell
    10.0.2.10   uni.loc
```