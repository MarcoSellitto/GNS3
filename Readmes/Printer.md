# Printer Configuration in Segreteria
<h4> This guide describes how to create and configure the printer in the Segreteria VLAN using a Debian machine. </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by going to Edit → Preferences → Qemu VMs → New → choose where to run the container → enter the image debian-12.6.qcow2 → choose a name and follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project and connect it to the switch in the Segreteria subnet.</li>
        </ol>
    </li>
    <li>Start and open the container's console.</li>
</ol>

## Step 2: Cups Installation
<li> Update repositories and install Cups</li>

``` shell
    $ sudo apt update
    $ sudo apt install -y cups
```
By default, CUPS only listens on localhost. It is necessary to enable listening on all interfaces.
<li>Open the file</li>

``` shell
    $ sudo nano /etc/cups/cupsd.conf
```

<li>Replace it's content with:</li>

```
    LogLevel warn
    SystemGroup lpadmin
    Port 631
    Listen 0.0.0.0:631
    Browsing On
    DefaultAuthType Basic
    WebInterface Yes

    <Location />
        Order allow,deny
        Allow from 127.0.0.1
        Allow from 10.0.40.12
        Allow from 10.0.40.0/24
        Deny from all
    </Location>

    <Location /admin>
        AuthType Default
        Require user @SYSTEM
        Order allow,deny
        Allow from 127.0.0.1
        Allow from 10.0.40.12
        Allow from 10.0.40.0/24
        Deny from all
    </Location>

    <Location /admin/conf>
        AuthType Default
        Require user @SYSTEM
        Order allow,deny
        Allow from 127.0.0.1
        Allow from 10.0.40.12
        Allow from 10.0.40.0/24
        Deny from all
    </Location>

```
<li>Enable and start Cups</li>

``` shell
    $ sudo systemctl enable cups
    $ sudo systemctl start cups
```

At this point, the printer is ready to be configured on the Windows 11 workstation within the Segreteria VLAN.