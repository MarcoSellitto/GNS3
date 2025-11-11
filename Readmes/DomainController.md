# Windows Server Configuration in DC (Domain Controller)
<h4> This guide describes how to create and configure the **Windows Server**, which serves simultaneously as a Domain Controller and a Certification Authority. </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by clicking on the End Devices tab on the left → New Template → Install from the GNS3 server (recommended) → Guests → Windows Server → Install → choose where to run the container → Windows Server version 2022 → SERVER_EVAL_x64FRE_en-us.iso → Next → follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project and connect it to the switch in the DC subnet.</li>
        </ol>
    </li>
    <li>Start and open the container's console.</li>
</ol>

## Step 2: Installation and DNS Server
<li>Windows will guide the user through the installation process. Choose “Custom: Install Windows only (advanced)” as the installation type, and set the administrator password to “DomainController/70.” </li>

<li>After the reboot, the “Server Manager” window will appear automatically → Add Roles and Features → click "Next" until the "Server Roles" window → Check "DNS Server" -> always click "Next" → Install </li>

## Step 3: DNS and Static IP configuration
<li>To set a static IP: open the search bar → search "ncpa.cpl" → press enter or clic on the result → right click "Ethernet" → Uncheck "Internet Protocol Version 6 (TCP/IPv6)" → left click on "Internet Protocol Version 4 (TCP/IPv4)" → Properties → Check "Use the following IP address:" → put these values:
<ol>
    <li>IP address: 10.0.70.100</li>
    <li>Subnet mask: 255.255.255.0</li>
    <li>Default gateway: 10.0.70.1</li>
</ol>
Check "Use the following DNS server addresses: → put these values:
<ol>
    <li>Preferred DNS server: 127.0.0.1</li>
    <li>Leave "Alternate DNS server" empty</li>
</ol>
Click Ok → Restart the machine. </li>

<li> Open the search bar → search "DNS" → press enter or clic on the result → right click on the machine name in the left tab → Properties → Forwarders → Edit → Insert "10.0.2.30" → Ok → Apply → Restart the machine. </li>

## Step 4: Active Directory Installation
<li>Server Manager → Add Roles and Features → click "Next" until the "Server Roles" window → Check "Active Directory Domain Services" → always click "Next" → Install </li>

<li>A notification will appear indicating that the machine can be promoted to a Domain Controller. Continue with the post-deployment configuration as follows:
<ol>
    <li>Add new forest "uni.local" → Next </li>
    <li>Windows Server 2016 → Password restore: "DomainController/70" </li>
    <li>Next → Next → Next </li>
    <li>Wait until the system completes the prerequisite verification process → Install </li>
</ol>
</li>