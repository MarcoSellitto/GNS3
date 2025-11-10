# WebServer (Apache2) Configuration in the DMZ
<h4> This guide describes how to create and configure the **Apache WebServer** (an open-source HTTP server for modern operating systems) within a Debian machine. </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by going to Edit → Preferences → Qemu VMs → New → choose where to run the container → enter the image debian-12.6.qcow2 → choose a name and follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project and connect it to the switch in the DMZ subnet
        </ol>
    </li>
    <li>Start and open the container's console.</li>
</ol>

## Step 2: Set static IP
<li>Open the file</li>

``` shell
    $ sudo nano /etc/network/interfaces
```
<li>Uncomment the relevant lines and modify the settings as shown below</li>

```
    # Static config for ens4
    auto ens4
    iface ens4 inet static
        address 10.0.2.10
        netmask 255.255.255.0
        gateway 10.0.2.1
        dns-nameservers 10.0.2.30
```

## Step 3: Apache2 Installation
<li>Update repositories and install Apache2</li>

``` shell
    $ sudo apt update && apt upgrade -y
    $ sudo apt install apache2 -y
```
<li>Start the Apache service</li>

``` shell
    $ service apache2 start
```

## Step 4: Update the homepage
At this stage, accessing the web server will display the default Apache page. The personalized homepage must be uploaded to replace it.

<li>Open the directory and remove the default index</li>

``` shell
    $ cd /var/www/html
    $ sudo rm index.html
```
<li>Create the new index and import all the content of the file "uniMockup.html" (the entire content of the file must be copied here!)</li>

``` shell
    $ sudo nano index.html
```

<li>Update the file permissions and restart the Apache service</li>

``` shell
    $ sudo chown www-data:www-data index.html
    $ sudo chmod 644 index.html
    $ sudo systemctl restart apache2
```

At this stage, provided the DNS is properly configured, the custom web page can be accessed through the “uni.loc” domain.