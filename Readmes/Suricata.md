# IDS (Suricata) Configuration in Management
<h4> This guide describes how to create and configure the **Suricata IDS** (a high performance, open-source network analysis and threat detection software) within a Debian machine with a mirroring port. </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by going to Edit → Preferences → Qemu VMs → New → choose where to run the container → enter the image debian-12.6.qcow2 → choose a name and follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project
                <ol>
                    <li>Right-click on it → Configure → Network → increase the adapters to 2.</li>
                    <li>Connect the "ens4" port to the Management switch.</li>
                    <li>Connect the "ens5" port to the CiscoL2 "Gi2/2" port.</li>
                </ol>
            </li>
        </ol>
    </li>
    <li>Start and open the container's console.</li>
</ol>

## Step 2: Update packets and install Suricata
<li>Create directory if it doesn't exist and write file as root</li>

``` shell
    $ sudo mkdir -p /etc/apt/sources.list.d
    $ echo "deb http://deb.debian.org/debian bookworm-backports main" | sudo tee /etc/apt/sources.list.d/backports.list
```
<li> Update repositories and install Suricata</li>

``` shell
    $ apt update
    $ sudo apt -t bookworm-backports install suricata
```

## Step 3: Enable ens4 and setup mirroring on ens5
Configure the machine so that it obtains its IP address from the Management VLAN and can capture all network traffic via a mirroring interface on ens5.
<li> Open the file </li>

``` shell
    $ sudo nano /etc/network/interfaces
```
<li>Remove the comments for DHCP on ens4 and have something like this:</li>

```
    # DHCP config for ens4
    auto ens4
    iface ens4 inet dhcp
```
<li> In the same file, add these lines:</li>

```
    auto ens5
    iface ens5 inet manual
        up ip link set $IFACE up
        down ip link set $IFACE down
```

<li> Open Suricata's configuration file </li>

``` shell
    $ sudo nano /etc/suricata/suricata.yaml
```

<li> Find the “af-packet” section (approximately between lines 200 and 300) and uncomment the necessary lines as shown below.</li>

```
    af-packet:
        - interface: ens5
        threads: auto
        cluster-id: 99
        cluster-type: cluster_flow
        defrag: yes
```
<li> Restart Suricata </li>

``` shell
    $ sudo systemctl restart suricata
```

## Step 4: Download the ET Open (Emerging Threats) rules
<li>Use this command to</li>
<ol>
    <li>Download the “Emerging Threats Open” rules</li>
    <li>Put them in "/var/lib/suricata/rules/"</li>
    <li>Update the file "suricata.rules"</li>
</ol>

``` shell
    $ sudo suricata-update
    $ sudo systemctl restart suricata
```
<li> Restart Suricata </li>

``` shell
    $ sudo systemctl restart suricata
```