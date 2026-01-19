# OPNsense Configuration (Firewall)
<h4> This guide describes how to create and configure the **Firewall** for University Network, which serves simultaneously as a firewall and a router. </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by clicking on the End Devices tab on the left → New Template → Install from the GNS3 server (recommended) → Firewalls → OPNsense → Install → choose where to run the container → OPNsense 24.7 → OPNsense-24.7-nano-amd64.img → Next → follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project and connect it to the Gi0/1 port of Cisco Router R1 with "em0" port.</li>
            <li>Connect to the Cisco Switch L2  with "em1" port</li>
            <li>To setup the firewall with a Graphic User Interface GUI, connect to "em2" port a VM with a GUI.</li>
        </ol>
    </li>
    <li>Start and open the container's console.</li>
</ol>

## Step 2: Interfaces port Configuration
<li> OPNSense will guide the user through the configuration process. The default user and password are : root/opnsense. Choose “Assign interfaces” and answer:
<ol>
    <li>"Do you want to configure LAGGs now?" -> **n**</li>
    <li>"Do you want to configure VLANs now?" -> **n**</li>
</ol>
</li>

<li>After answer to the questions like this:
<ol>      
<li>Enter the WAN interface name or 'a' for auto-detection: **vtnet0** </li>

<li>Enter the LAN interface name or 'a' for auto-detection
NOTE: this enables full Firewalling/NAT mode.
(or nothing if finished): **vtnet2** </li>

<li>Enter the Optional interface 1 name or 'a' for auto-detection
(or nothing if finished): **vtnet1**</li>

<li>The interfaces will be assigned as follows: </li>

<li>WAN  -> vtnet0 </li>
<li>LAN  -> vtnet2 </li>
<li>OPT1 → vtnet1 </li>

<li>Do you want to proceed? [y/N]:**y**</li>
</ol>
This setup is ready to be configured with a VM with a GUI.
</li>

## Step 3: Firewall GUI configuration
<li>Now start the console for the VM that is connetted through "vtnet2" alias "em2" port. Open the browser and navigate to 192.168.1.1 address. It appears firewall page and put in the credentials. Skip initial configuration process clicking th OPNsense logo </li>

<li>**Gateway**: open the panel on the left → System → Gateway → Click on + and assign these values:
<ol>
    <li>Interface: WAN</li>
    <li>Name: WAN_GW</li>
    <li>Gateway Address: 203.0.213.1/30</li>
    <li>Upstream Gateway: check it</li>
</ol>
Save and Apply</li>

<li>**Ip Assignment**: open the panel on the left → Interfaces → WAN → assign these values :
<ol>
    <li>IPv4 Configuration Type: Static IPv4</li>
    <li>IPv4 Address: 203.0.213.2/29</li>
    <li>Block bogon networks: check it</li>
    <li>Gateway Rule: WAN_GW</li>
    <li>Save and apply</li>
</ol>
</li>

<li>**Assign OPT1 as LAN Trunk Interface**: open the panel on the left → Interfaces → Assignments → assign these values :
<ol>
    <li>Add OPT1 and enable it</li>
    <li>Name: Trunk-LAN</li>
</ol>
Save and apply </li>

<li>**VLANs Creation**: open the panel on the left → Interfaces → Other Types → VLAN →  assign each VLANs to a tag:
<ol>
    <li>VLAN 2 → parent interface: OPT1 → tag: 2</li>
    <li>VLAN 10 → parent interface: OPT1 → tag: 10</li>
    <li>VLAN 20 → parent interface: OPT1 → tag: 20</li>
    <li>VLAN 30 → parent interface: OPT1 → tag: 30</li>
    <li>VLAN 40 → parent interface: OPT1 → tag: 40</li>
    <li>VLAN 50 → parent interface: OPT1 → tag: 50</li>
    <li>VLAN 60 → parent interface: OPT1 → tag: 60</li>
    <li>VLAN 70 → parent interface: OPT1 → tag: 70</li>
    <li>VLAN 99 → parent interface: OPT1 → tag: 99</li>
</ol>
Return in Interfaces  → Assignments  → and assign each VLAN to a new interface: 
<ol>
    <li>VLAN 2 → DMZ</li>
    <li>VLAN 10 → Classroom1</li>
    <li>VLAN 20 → Classroom2</li>
    <li>VLAN 30 → Guest</li>
    <li>VLAN 40 → Secretary</li>
    <li>VLAN 50 → Laboratory</li>
    <li>VLAN 60 → Management</li>
    <li>VLAN 70 → DC</li>
    <li>VLAN 99 → Security</li>
</ol>
Return in Interfaces → Other Types → VLAN →  configure the VLANs:
<ol>
    <li>DMZ: enable it and assign static IP: 10.0.2.1/24</li>
    <li>Classroom1: enable it and assign static IP: 10.0.10.1/24 </li>
    <li>Classroom2: enable itand assign static IP: 10.0.20.1/24</li>
    <li>Guest: enable it and assign static IP: 10.0.30.1/24</li>
    <li>Secretary: enable it and assign static IP: 10.0.40.1/24</li>
    <li>Laboratory: enable it and assign static IP: 10.0.50.1/24</li>
    <li>Management: enable it and assign static IP: 10.0.60.1/24</li>
    <li>DomainController: enable it and assign static IP: 10.0.70.1/24</li>
    <li>Security: enable it and assign static IP: 10.0.99.1/24</li>
</ol>
Save and Apply.
</li>

 
<li>**Configure DNS**: open the left panel → System → Settings → General : set DNS servers to 193.205.160.3 193.205.160.139 and uncheck "Allow DNS server list to be overwritten …".
Open the left panel → Services → Unbound DNS → Query Forwarding: check "Use System Nameservers"   
</li>

<li>**Access list**: open the panel on the left → Services → DHCPv4 → click on + :
<ol>
    <li>Enabled → enable it</li>
    <li>Access List Name → Allowed_VLANs</li>
    <li>Action → Allow</li>
    <li>Networks → 10.0.2.0/24 10.0.10.0/24 10.0.20.0/24 10.0.30.0/24 10.0.40.0/24 10.0.50.0/24 10.0.60.0/24 10.0.70.0/24 10.0.99.0/24 </li>
    <li>Description → ACL for all VLANs</li>
</ol>
Save and apply </li>

<li>**Overrides**: open the panel on the left → Services → Unbound DNS → Overrides → click on + :
<ol>
    <li>Host → leave it blank</li>
    <li>Domain → uni.local</li>
    <li>Type → A IPV4 address</li>
    <li>Value → 10.0.2.10</li>
    <li>Description → WebServer</li>
</ol>
Save and apply </li>

<li>**DHCP for each VLAN**: open the panel on the left → Services → DHCPv4 → click on the VLAN name :
<ol>
    <li>DMZ → enable it, set IP range: 10.0.2.50 - 10.0.2.200 and set DNS Server:10.0.2.1</li>
    <li>Classroom1 → enable it, set IP range: 10.0.10.50 - 10.0.10.200 and set DNS Server:10.0.10.1 </li>
    <li>Classroom2 → enable it, set IP range: 10.0.20.50 - 10.0.20.200 and set DNS Server:10.0.20.1</li>
    <li>Guest → enable it, set IP range: 10.0.30.50 - 10.0.30.200 and set DNS Server:10.0.30.1</li>
    <li>Secretary → enable it, set IP range: 10.0.40.50 - 10.0.40.200 and set DNS Server:10.0.40.1</li>
    <li>Laboratory → enable it, set IP range: 10.0.50.50 - 10.0.50.200 and set DNS Server:10.0.50.1</li>
    <li>Management → enable it, set IP range: 10.0.60.50 - 10.0.60.200 and set DNS Server:10.0.60.1</li>
    <li>DomainController → enable it, set IP range: 10.0.70.50 - 10.0.70.200 and set DNS Server:10.0.70.1</li>
    <li>Security → enable it, set IP range: 10.0.99.50 - 10.0.99.200 and set DNS Server:10.0.99.1</li>
</ol>
Save and apply </li>

<li>**Configure NAT**: open the left panel → Firewall → NAT → Outbound : "check Manual Outbound NAT". Save and apply changes.
</li>

<li>**Set Aliases**: open the left panel → Firewall → Aliases → + : 
<ol>
    <li>DMZ → Name: WebServer, Type: Host, Content: 10.0.2.10</li>
    <li>DMZ → Name: VipWebServer, Type: Host, Content: 203.0.213.3</li>
    <li>DMZ → Name: DNS, Type: Host, Content: 10.0.2.30</li>
    <li>Security → Name: Wazuh, Type: Host, Content: 10.0.99.14</li>
    <li>Management → Name: JumpServer, Type: Host, Content: 10.0.60.12</li>
    <li>Management → Name: Workstation, Type: Host, Content: 10.0.60.11</li>
    <li>DomainController → Name: DC, Type: Host, Content: 10.0.70.100</li>
    
</ol>
Save and apply </li>
</li>

<li>**Configure VIP**: open the panel on the left → Interfaces → Virtual IPs → Settings →  Click on + and assign these values:
<ol>
    <li>Type: IP Alias</li>
    <li>Interface: WAN</li>
    <li>Address: 203.0.213.3/32</li>
</ol>
Save and Apply</li>

<li>**Port Forward NAT**: open the panel on the left → Firewall → NAT → Port Forward →  Click on + and assign these values:
<ol>
    <li>Interface: WAN</li>
    <li>Destination: Single host or Alias - VIPWebServer(203.0.213.3) </li>
    <li>Destinantion Port Range: HTTPS (443)</li>
    <li>Redirect target IP: WebServer(10.0.2.10)</li>
    <li>Redirect target port: 443</li>
    <li>Filter rule association: Add associated filter rule</li>
    <li>NAT Reflection: enabled</li>
    <li>Save and apply</li>
</ol>
</li>

<li>**Firewall Rules**: open the panel on the left → Firewall → Rules → click on the VLAN name (the order of the rules is important): </li>

<li> WAN:
<ol> 
    <li>WebServer → Action:Pass | Interface: WAN | Direction: In | Protocol: TCP | Source: any | Destination: WebServer(10.0.2.10)| Destination Port Range: HTTPS(443) </li>
</ol>
</li>

<li> DMZ: 
<ol> 
    <li>Block Class1 → Action:Block | Interface: DMZ | Direction: In | Protocol: any | Source: DMZ net | Destination: Classroom1 net | Destination Port Range: any </li>
    <li>Block Class2 → Action:Block | Interface: DMZ | Direction: In | Protocol: any | Source: DMZ net | Destination: Classroom2 net | Destination Port Range: any </li>
    <li>Block Guest → Action:Block | Interface: DMZ | Direction: In | Protocol: any | Source: DMZ net | Destination: Guest net | Destination Port Range: any </li>
    <li>Block Secretary → Action:Block | Interface: DMZ | Direction: In | Protocol: any | Source: DMZ net | Destination: Secretary net | Destination Port Range: any </li>
    <li>Block Laboratory → Action:Block | Interface: DMZ | Direction: In | Protocol: any | Source: DMZ net | Destination: Laboratory net | Destination Port Range: any</li>
    <li>Block Management → Action:Block | Interface: DMZ | Direction: In | Protocol: any | Source: DMZ net | Destination: Management net | Destination Port Range: any</li>
    <li>Block Security → Action:Block | Interface: DMZ | Direction: In | Protocol: any | Source: DMZ net | Destination: Security net | Destination Port Range: any</li>
    <li>Block DomainController → Action:Block | Interface: DMZ | Direction: In | Protocol: any | Source: DMZ net | Destination: DomainController net | Destination Port Range: any </li>
    <li>Allow DNS → Action:Pass | Interface: DMZ | Direction: In | Protocol:TCP/UDP | Source: DMZ net | Destination: This Firewall | Destination Port Range: DNS (53)</li>
    <li>Send Wazuh Logs → Action:Pass | Interface: DMZ | Direction: In | Protocol:TCP | Source: DMZ net | Destination: Wazuh (10.0.99.14) | Destination Port Range: 1514-1515</li>
    <li>Allow ping → Action:Pass | Interface: DMZ | Direction: In | Protocol:ICMP | Source: DMZ net | Destination: any | Destination Port Range: any</li>
</ol>
</li>


<li> Classroom1:
<ol>
    <li>Access to DNS → Action:Pass | Interface: Classroom1 | Direction: In | Protocol:TCP/UDP | Source: Classroom1 net | Destination: This Firewall | Destination Port Range: DNS (53)</li>
    <li>Send Wazuh Logs → Action:Pass | Interface: Classroom1 | Direction: In | Protocol:TCP | Source: Classroom1 net | Destination: Wazuh (10.0.99.14) | Destination Port Range: 1514-1515</li>
    <li>Access to WebServer → Action:Pass | Interface: Classroom1 | Direction: In | Protocol:TCP | Source: Classroom1 net | Destination: WebServer (10.0.2.10) | Destination Port Range: HTTPS(443)</li>
    <li>Block DMZ → Action:Block | Interface: Classroom1 | Direction: In | Protocol: any | Source: Classroom1 net | Destination: DMZ net | Destination Port Range: any </li>
    <li>Block Class2 → Action:Block | Interface: Classroom1 | Direction: In | Protocol: any | Source: Classroom1 net | Destination: Classroom2 net | Destination Port Range: any </li>
    <li>Block Guest → Action:Block | Interface: Classroom1 | Direction: In | Protocol: any | Source: Classroom1 net | Destination: Guest net | Destination Port Range: any </li>
    <li>Block Secretary → Action:Block | Interface: Classroom1 | Direction: In | Protocol: any | Source: Classroom1 net | Destination: Secretary net | Destination Port Range: any </li>
    <li>Block Laboratory → Action:Block | Interface: Classroom1 | Direction: In | Protocol: any | Source: Classroom1 net | Destination: Laboratory net | Destination Port Range: any</li>
    <li>Block DomainController → Action:Block | Interface: Classroom1 | Direction: In | Protocol: any | Source: Classroom1 net | Destination: DomainController net | Destination Port Range: any </li>
    <li>Block Management → Action:Block | Interface: Classroom1 | Direction: In | Protocol: any | Source: Classroom1 net | Destination: Management net | Destination Port Range: any</li>
    <li>Block Security → Action:Block | Interface: Classroom1 | Direction: In | Protocol: any | Source: Classroom1 net | Destination: Security net | Destination Port Range: any</li>
    <li>Allow ping → Action:Pass | Interface: Classroom1 | Direction: In | Protocol:ICMP | Source: Classroom1 net | Destination: any | Destination Port Range: any</li>
    <li>Access to Web(HTTPS) → Action:Pass | Interface: Classroom1 | Direction: In | Protocol:TCP | Source: Classroom1 net | Destination: any | Destination Port Range: HTTPS (443)</li>
    <li>Access to Web(HTTP) → Action:Pass | Interface: Classroom1 | Direction: In | Protocol:TCP | Source: Classroom1 net | Destination: any | Destination Port Range: HTTP (80)</li>
</ol>
</li>

<li> Classroom2:
<ol>
    <li>Access to DNS → Action:Pass | Interface: Classroom2 | Direction: In |Protocol:TCP/UDP | Source: Classroom2 net | Destination: This Firewall | Destination Port Range: DNS (53)</li>
    <li>Send Wazuh Logs → Action:Pass | Interface: Classroom2 | Direction: In | Protocol:TCP | Source: Classroom2 net | Destination: Wazuh (10.0.99.14) | Destination Port Range: 1514-1515</li>
    <li>Access to WebServer → Action:Pass | Interface: Classroom2 | Direction: In | Protocol:TCP | Source: Classroom2 net | Destination: WebServer (10.0.2.10) | Destination Port Range: HTTPS(443)</li>
    <li>Block DMZ → Action:Block | Interface: Classroom2 | Direction: In | Protocol: any | Source: Classroom2 net | Destination: DMZ net | Destination Port Range: any </li>
    <li>Block Class1 → Action:Block | Interface: Classroom2 | Direction: In | Protocol: any | Source: Classroom2 net | Destination: Classroom1 net | Destination Port Range: any </li>
    <li>Block Guest → Action:Block | Interface: Classroom2 | Direction: In | Protocol: any | Source: Classroom2 net | Destination: Guest net | Destination Port Range: any </li>
    <li>Block Secretary → Action:Block | Interface: Classroom2 | Direction: In | Protocol: any | Source: Classroom2 net | Destination: Secretary net | Destination Port Range: any </li>
    <li>Block Laboratory → Action:Block | Interface: Classroom2 | Direction: In | Protocol: any | Source: Classroom2 net | Destination: Laboratory net | Destination Port Range: any</li>
    <li>Block DomainController → Action:Block | Interface: Classroom2 | Direction: In | Protocol: any | Source: Classroom2 net | Destination: DomainController net | Destination Port Range: any </li>
    <li>Block Management → Action:Block | Interface: Classroom2 | Direction: In | Protocol: any | Source: Classroom2 net | Destination: Management net | Destination Port Range: any</li>
    <li>Block Security → Action:Block | Interface: Classroom2 | Direction: In | Protocol: any | Source: Classroom2 net | Destination: Security net | Destination Port Range: any</li>
    <li>Allow ping → Action:Pass | Interface: Classroom2 | Direction: In | Protocol:ICMP | Source: Classroom2 net | Destination: any | Destination Port Range: any</li>
    <li>Access to Web(HTTPS) → Action:Pass | Interface: Classroom2 | Direction: In | Protocol:TCP | Source: Classroom2 net | Destination: any | Destination Port Range: HTTPS (443)</li>
    <li>Access to Web(HTTP) → Action:Pass | Interface: Classroom2 | Direction: In | Protocol:TCP | Source: Classroom2 net | Destination: any | Destination Port Range: HTTP (80)</li>
</ol>
</li>

<li> Guest:
<ol>
    <li>Access to DNS → Action:Pass | Interface: Guest | Direction: In |Protocol:TCP/UDP | Source: Guest net | Destination: This Firewall | Destination Port Range: DNS (53)</li>
    <li>Send Wazuh Logs → Action:Pass | Interface: Guest | Direction: In | Protocol:TCP | Source: Guest net | Destination: Wazuh (10.0.99.14) | Destination Port Range: 1514-1515</li>
    <li>Access to WebServer → Action:Pass | Interface: Guest | Direction: In | Protocol:TCP | Source: Guest net | Destination: WebServer (10.0.2.10) | Destination Port Range: HTTPS(443)</li>
    <li>Block DMZ → Action:Block | Interface: Guest | Direction: In | Protocol: any | Source: Guest net | Destination: DMZ net | Destination Port Range: any </li>
    <li>Block Class1 → Action:Block | Interface: Guest | Direction: In | Protocol: any | Source: Guest net | Destination: Classroom1 net | Destination Port Range: any </li>
    <li>Block Class2 → Action:Block | Interface: Guest | Direction: In | Protocol: any | Source: Guest net | Destination: Classroom2 net | Destination Port Range: any </li>
    <li>Block Secretary → Action:Block | Interface: Guest | Direction: In | Protocol: any | Source: Guest net | Destination: Secretary net | Destination Port Range: any </li>
    <li>Block Laboratory → Action:Block | Interface: Guest | Direction: In | Protocol: any | Source: Guest net | Destination: Laboratory net | Destination Port Range: any</li>
    <li>Block DomainController → Action:Block | Interface: Guest | Direction: In | Protocol: any | Source: Guest net | Destination: DomainController net | Destination Port Range: any </li>
    <li>Block Management → Action:Block | Interface: Guest | Direction: In | Protocol: any | Source: Guest net | Destination: Management net | Destination Port Range: any</li>
    <li>Block Security → Action:Block | Interface: Guest | Direction: In | Protocol: any | Source: Guest net | Destination: Security net | Destination Port Range: any</li>
    <li>Access to Web(HTTPS) → Action:Pass | Interface: Guest | Direction: In | Protocol:TCP | Source: Guest net | Destination: any | Destination Port Range: HTTPS (443)</li>
    <li>Access to Web(HTTP) → Action:Pass | Interface: Guest | Direction: In | Protocol:TCP | Source: Guest net | Destination: any | Destination Port Range: HTTP (80)</li>
</ol>
</li>

<li> Secretary:
<ol>
    <li>Access to DNS → Action:Pass | Interface: Secretary | Direction: In |Protocol:TCP/UDP | Source: Secretary net | Destination: This Firewall | Destination Port Range: DNS (53)</li>
    <li>Send Wazuh Logs → Action:Pass | Interface: Secretary | Direction: In | Protocol:TCP | Source: Secretary net | Destination: Wazuh (10.0.99.14) | Destination Port Range: 1514-1515</li>
    <li>Access to WebServer → Action:Pass | Interface: Secretary | Direction: In | Protocol:TCP | Source: Secretary net | Destination: WebServer (10.0.2.10) | Destination Port Range: HTTPS(443)</li>
    <li>Block DMZ → Action:Block | Interface: Secretary | Direction: In | Protocol: any | Source: Secretary net | Destination: DMZ net | Destination Port Range: any </li>
    <li>Block Class1 → Action:Block | Interface: Secretary | Direction: In | Protocol: any | Source: Secretary net | Destination: Classroom1 net | Destination Port Range: any </li>
    <li>Block Class2 → Action:Block | Interface: Secretary | Direction: In | Protocol: any | Source: Secretary net | Destination: Classroom2 net | Destination Port Range: any </li>
    <li>Block Guest → Action:Block | Interface: Secretary | Direction: In | Protocol: any | Source: Secretary net | Destination: Guest net | Destination Port Range: any </li>
    <li>Block Laboratory → Action:Block | Interface: Secretary | Direction: In | Protocol: any | Source: Secretary net | Destination: Laboratory net | Destination Port Range: any</li>
    <li>Block DomainController → Action:Block | Interface: Secretary | Direction: In | Protocol: any | Source: Secretary net | Destination: DomainController net | Destination Port Range: any </li>
    <li>Block Management → Action:Block | Interface: Secretary | Direction: In | Protocol: any | Source: Secretary net | Destination: Management net | Destination Port Range: any</li>
    <li>Block Security → Action:Block | Interface: Secretary | Direction: In | Protocol: any | Source: Secretary net | Destination: Security net | Destination Port Range: any</li>
    <li>Allow ping → Action:Pass | Interface: Secretary | Direction: In | Protocol:ICMP | Source: Secretary net | Destination: any | Destination Port Range: any</li>
    <li>Access to Web(HTTPS) → Action:Pass | Interface: Secretary | Direction: In | Protocol:TCP | Source: Secretary net | Destination: any | Destination Port Range: HTTPS (443)</li>
    <li>Access to Web(HTTP) → Action:Pass | Interface: Secretary | Direction: In | Protocol:TCP | Source: Secretary net | Destination: any | Destination Port Range: HTTP (80)</li>
</ol>
</li>

<li> Laboratory:
<ol>
    <li>Access to AD → Action:Pass | Interface: Laboratory | Direction: In | Protocol:TCP/UDP | Source: Laboratory net | Destination: DomainController (10.0.70.100) | Destination Port Range: any</li>
    <li>Access to DNS → Action:Pass | Interface: Laboratory | Direction: In |Protocol:TCP/UDP | Source: Laboratory net | Destination: This Firewall | Destination Port Range: DNS (53)</li>
    <li>Send Wazuh Logs → Action:Pass | Interface: Laboratory | Direction: In | Protocol:TCP | Source: Laboratory net | Destination: Wazuh (10.0.99.14) | Destination Port Range: 1514-1515</li>
    <li>Access to WebServer → Action:Pass | Interface: Laboratory | Direction: In | Protocol:TCP | Source: Laboratory net | Destination: WebServer (10.0.2.10) | Destination Port Range: HTTPS(443)</li>
    <li>Block DMZ → Action:Block | Interface: Laboratory | Direction: In | Protocol: any | Source:Laboratory net | Destination: DMZ net | Destination Port Range: any </li>
    <li>Block Class1 → Action:Block | Interface: Laboratory | Direction: In | Protocol: any | Source: Laboratory net | Destination: Classroom1 net | Destination Port Range: any </li>
    <li>Block Class2 → Action:Block | Interface: Laboratory | Direction: In | Protocol: any | Source: Laboratory net | Destination: Classroom2 net | Destination Port Range: any </li>
    <li>Block Guest → Action:Block | Interface: Laboratory | Direction: In | Protocol: any | Source: Laboratory net | Destination: Guest net | Destination Port Range: any </li>
    <li>Block Secretary → Action:Block | Interface: Laboratory | Direction: In | Protocol: any | Source: Laboratory net | Destination: Secretary net | Destination Port Range: any </li>
    <li>Block Management → Action:Block | Interface: Laboratory | Direction: In | Protocol: any | Source: Laboratory net | Destination: Management net | Destination Port Range: any </li>
    <li>Block Security → Action:Block | Interface: Laboratory | Direction: In | Protocol: any | Source: Laboratory net | Destination: Security net | Destination Port Range: any </li>
    <li>Allow ping → Action:Pass | Interface: Laboratory | Direction: In | Protocol:ICMP | Source: Laboratory net | Destination: any | Destination Port Range: any</li>
    <li>Access to Web(HTTPS) → Action:Pass | Interface: Laboratory | Direction: In | Protocol:TCP | Source: Laboratory net | Destination: any | Destination Port Range: HTTPS (443)</li>
    <li>Access to Web(HTTP) → Action:Pass | Interface: Laboratory | Direction: In | Protocol:TCP | Source: Laboratory net | Destination: any | Destination Port Range: HTTP (80)</li>
</ol>
</li>


<li> DomainController:
<ol>
    <li>Allow AD → Action:Pass | Interface: DomainController | Direction: In | Protocol:TCP/UDP | Source: DomainController net | Destination: Laboratory net | Destination Port Range: any</li>
    <li>Access to DNS → Action:Pass | Interface: DomainController | Direction: In |Protocol:TCP/UDP | Source: DomainController net | This firewall | Destination Port Range: DNS (53)</li>
    <li>Send Wazuh Logs → Action:Pass | Interface: DomainController | Direction: In | Protocol:TCP | Source: DomainController net | Destination: Wazuh (10.0.99.14) | Destination Port Range: 1514-1515</li>
    <li>Access to WebServer → Action:Pass | Interface: DomainController | Direction: In | Protocol:TCP | Source: DomainController net | Destination: WebServer (10.0.2.10) | Destination Port Range: HTTPS(443)</li>
    <li>Block DMZ → Action:Block | Interface: DomainController | Direction: In | Protocol: any | Source: DomainController net | Destination: DMZ net | Destination Port Range: any </li>
    <li>Block Class1 → Action:Block | Interface: DomainController | Direction: In | Protocol: any | Source: DomainController net | Destination: Classroom1 net | Destination Port Range: any </li>
    <li>Block Class2 → Action:Block | Interface: DomainController | Direction: In | Protocol: any | Source: DomainController net | Destination: Classroom2 net | Destination Port Range: any </li>
    <li>Block Guest → Action:Block | Interface: DomainController | Direction: In | Protocol: any | Source: DomainController net | Destination: Guest net | Destination Port Range: any </li>
    <li>Block Secretary → Action:Block | Interface: DomainController  | Direction: In | Protocol: any | Source: DomainController net | Destination: Secretary net | Destination Port Range: any </li>
    <li>Block Management → Action:Block | Interface: DomainController | Direction: In | Protocol: any | Source: DomainController net | Destination: Management net | Destination Port Range: any </li>
    <li>Block Security → Action:Block | Interface: DomainController | Direction: In | Protocol: any | Source: DomainController net | Destination: Security net | Destination Port Range: any </li>
    <li>Allow ping → Action:Pass | Interface: DomainController | Direction: In | Protocol:ICMP | Source: DomainController net | Destination: any | Destination Port Range: any</li>
    <li>Access to Web(HTTPS) → Action:Pass | Interface: DomainController | Direction: In | Protocol:TCP | Source: DomainController net | Destination: any | Destination Port Range: HTTPS (443)</li>
    <li>Access to Web(HTTP) → Action:Pass | Interface: DomainController | Direction: In | Protocol:TCP | Source: DomainController net | Destination: any | Destination Port Range: HTTP (80)</li>
</ol>
</li>

<li> Management:
<ol>
    <li>Ansible for Classroom1 → Action:Pass | Interface: Management | Direction: In |Protocol:TCP | Source: Workstation (10.0.60.11) | Destination: Classroom1 net| Destination Port Range: ssh (22)</li>
    <li>Ansible for Classroom2 → Action:Pass | Interface: Management | Direction: In |Protocol:TCP | Source: Workstation (10.0.60.11) | Destination: Classroom2 net | Destination Port Range: ssh (22)</li>
    <li>Ansible for Secretary → Action:Pass | Interface: Management | Direction: In |Protocol:TCP | Source: Workstation (10.0.60.11) | Destination: Secretary net | Destination Port Range: ssh (22)</li>
    <li>Ansible for Laboratory → Action:Pass | Interface: Management | Direction: In |Protocol:TCP | Source: Workstation (10.0.60.11) | Destination: Laboratory net | Destination Port Range: ssh (22)</li>
    <li>Allow Gateway to DNS → Action:Pass | Interface: Management | Direction: In |Protocol:TCP/UDP | Source: Management net | Destination: This Firewall | Destination Port Range: DNS (53)</li>
    <li>Access to Firewall → Action:Pass | Interface: Management | Direction: In | Protocol:TCP | Source: JumpServer (10.0.60.12)| Destination: This Firewall | Destination Port Range: HTTPS (443)</li>
    <li>Access to Wazuh → Action:Pass | Interface: Management | Direction: In | Protocol:TCP | Source: JumpServer (10.0.60.12)| Destination: Wazuh (10.0.99.14) | Destination Port Range: HTTPS (443)</li>
    <li>Send Wazuh Logs → Action:Pass | Interface: Management | Direction: In | Protocol:TCP | Source: Management net | Destination: Wazuh (10.0.99.14) | Destination Port Range: 1514-1515</li>
    <li>Access to WebServer → Action:Pass | Interface: Laboratory | Direction: In | Protocol:TCP | Source: Laboratory net | Destination: WebServer (10.0.2.10) | Destination Port Range: HTTPS(443)</li>
    <li>Block DMZ → Action:Block | Interface: Management | Direction: In | Protocol: any | Source: Management net | Destination: DMZ net | Destination Port Range: any </li>
    <li>Block Class1 → Action:Block | Interface: Management| Direction: In | Protocol: any | Source: Management net | Destination: Classroom1 net | Destination Port Range: any </li>
    <li>Block Class2 → Action:Block | Interface: Management | Direction: In | Protocol: any | Source: Management net | Destination: Classroom2 net | Destination Port Range: any </li>
    <li>Block Guest → Action:Block | Interface: Management | Direction: In | Protocol: any | Source: Management net | Destination: Guest net | Destination Port Range: any </li>
    <li>Block Laboratory → Action:Block | Interface: Management | Direction: In | Protocol: any | Source: Management net | Destination: Laboratory net | Destination Port Range: any</li>
    <li>Block DomainController → Action:Block | Interface: Management| Direction: In | Protocol: any | Source: Management net | Destination: DomainController net | Destination Port Range: any </li>
    <li>Block Security → Action:Block | Interface: Management | Direction: In | Protocol: any | Source: Management net | Destination: Security net | Destination Port Range: any </li>
    <li>Allow ping → Action:Pass | Interface: Management | Direction: In | Protocol:ICMP | Source: Management net | Destination: any | Destination Port Range: any</li>
    <li>Access to Web(HTTPS) → Action:Pass | Interface: Management | Direction: In | Protocol:TCP | Source: Management net | Destination: any | Destination Port Range: HTTPS (443)</li>
    <li>Access to Web(HTTP) → Action:Pass | Interface: Management | Direction: In | Protocol:TCP | Source: Management net | Destination: any | Destination Port Range: HTTP (80)</li>
</ol>
</li>

<li> Security:
<ol>
    <li>Allow Gateway to DNS → Action:Pass | Interface: Security | Direction: In |Protocol:TCP/UDP | Source: Security net | Destination: This Firewall | Destination Port Range: DNS (53)</li> 
    <li>Block DMZ → Action:Block | Interface: Security | Direction: In | Protocol: any | Source: Security net | Destination: DMZ net | Destination Port Range: any </li>
    <li>Block Class1 → Action:Block | Interface: Security | Direction: In | Protocol: any | Source: Security net | Destination: Classroom1 net | Destination Port Range: any </li>
    <li>Block Class2 → Action:Block | Interface: Security | Direction: In | Protocol: any | Source: Security net | Destination: Classroom2 net | Destination Port Range: any </li>
    <li>Block Guest → Action:Block | Interface: Security | Direction: In | Protocol: any | Source: Security net | Destination: Guest net | Destination Port Range: any </li>
    <li>Block Laboratory → Action:Block | Interface: Security | Direction: In | Protocol: any | Source: Security net | Destination: Laboratory net | Destination Port Range: any</li>
    <li>Block Management → Action:Block | Interface: Security | Direction: In | Protocol: any | Source: Security net | Destination: Security net | Destination Port Range: any</li>
    <li>Block DomainController → Action:Block | Interface: Security | Direction: In | Protocol: any | Source: Security net | Destination: DomainController net | Destination Port Range: any </li>
    <li>Access to Web(HTTPS) → Action:Pass | Interface: Security | Direction: In | Protocol:TCP | Source: Security net | Destination: any | Destination Port Range: HTTPS (443)</li>
    <li>Access to Web(HTTP) → Action:Pass | Interface: Security | Direction: In | Protocol:TCP | Source: Security net | Destination: any | Destination Port Range: HTTP (80)</li>
    <li>Allow ping → Action:Pass | Interface: Security | Direction: In | Protocol:ICMP | Source: Security net | Destination: any | Destination Port Range: any</li>
</ol>
</li>


<li>**Wazuh Agent**: Now we can update the firmware and install the wazuh agent. Go to System → Firmware → Status : click Check for updates and run the installation. After the installation, go to System → Firmware → Plugins: search os-wazuh-agent and install it . After you have to reload the gui. Now go to Services → Wazuh Agent → Settings→ enable it and put in Manager hostname: 10.0.99.14, Wazuh ip. Finally you can see in the Wazuh dashboard that OPNSense agent is working. 
</li>


<li>**End Configuration**: Now it is the time to delete the LAN interface and enable access to the firewall throw Management VLAN. Go to System → Settings → Administration : Listen Interfaces →  select Management. Now open the GUI from the workstation in Management . Connect via SSH to Jumpserver and access to the GUI on the browser. Now you can delete the LAN Interfaces and disable it.
Only the Jumpserver acan access to GUI of the firewall.
</li>



