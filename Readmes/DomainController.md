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

## Step 4: Active Directory Services Installation
<li>Server Manager → Add Roles and Features → click "Next" until the "Server Roles" window → Check "Active Directory Domain Services" → always click "Next" → Install </li>

<li>A notification will appear indicating that the machine can be promoted to a Domain Controller. Continue with the post-deployment configuration as follows:
<ol>
    <li>Add new forest "uni.local" → Next </li>
    <li>Windows Server 2016 → Password restore: "DomainController/70" </li>
    <li>Next → Next → Next </li>
    <li>Wait until the system completes the prerequisite verification process → Install </li>
</ol>
</li>

## Step 5: Certification Authority Services Installation and configuration
<li>Server Manager → Add Roles and Features → click "Next" until the "Server Roles" window → Check "Active Directory Certificate Services" → always click "Next" → Install </li>
<li>Server Manager → Click the flag with the notification → Configure Active Directory Services on this server → Do as follows:
<ol>
    <li>Crentials: keep "Administrator (local)" </li>
    <li>Role Services: Certification Authority </li>
    <li>Setup Type: Standalone CA </li>
    <li>CA Type: Root CA </li>
    <li>Private Key: Create a new private key </li>
    <li>Cryptography: </li>
    <ol>
        <li>Key length: 2048 or 4096 bit </li>
        <li>Hash: SHA256 </li>
    </ol>
    <li>CA Name: CA-SERVER-CA </li>
    <li>Validity Period: 10 years </li>
    <li>Database Locations: keep "Default" </li>
    <li>Click "Configure" </li>
</ol>
</li>

## Step 6: Export Root CA Certificate
<li>Open the search bar → search "certsrv.msc" → press enter or clic on the result → right click on the machine name in the left tab → Properties → General → View Certificate → Details → Copy to File → Do as follows:
<ol>
    <li>Format: Base-64 encoded X.509 (.CER) </li>
    <li>Save as: rootCA.cer </li>
</ol>
</li>

## Step 7: WebServer Certificate Creation
The commands in this step must be executed on the Debian machine hosting the webserver. The machine must remain active during step 8 as the certificate will be generated within the /tmp directory of the Linux environment.
<li>Create a temporary file</li>

``` shell
    $ sudo nano /tmp/web_openssl.cnf
```
<li>Copy and paste this content inside:</li>

```
    [req]
    default_bits        = 2048
    prompt              = no
    default_md          = sha256
    distinguished_name  = dn
    req_extensions      = v3_req

    [dn]
    C=IT
    ST=Campania
    L=Salerno
    O=Uni
    OU=IT
    CN=uni.loc

    [v3_req]
    subjectAltName = @alt_names

    [alt_names]
    DNS.1 = uni.loc
    DNS.2 = uni
    IP.1  = 10.0.2.10
    IP.2  = 203.0.213.3

```
<li>Generate the key and the Certificate Signing Request (CSR), and configure the appropriate permissions </li>

``` shell
    $ sudo openssl req -new -nodes -newkey rsa:2048 -keyout /etc/ssl/private/webserver.key -out /tmp/webserver.csr -config /tmp/web_openssl.cnf
    $ sudo chmod 600 /etc/ssl/private/webserver.key
    $ sudo chown root:root /etc/ssl/private/webserver.key
```

## Step 8: Update And Copy The Certificates To The WebServer
<li>Open a cmd while the webserver is still running from the previous step </li>

``` bat
    C:\> scp debian@10.0.2.10:/tmp/webserver.csr .
```

<li>Type "yes" when asked and then insert the debian's password. Now copy the rootCA on the debian machine </li>

``` bat
    C:\> scp "C:\Users\Administrator\Desktop\rootCA.cer" debian@10.0.2.10:/home/debian
```

<li>Insert the debian's password. The webserver’s certificate now needs to be imported into the Certification Authority </li>
<li>Open the search bar → search "certsrv.msc" → press enter or clic on the result → right click on the machine name in the left tab → All Tasks → Submit new request → Select the file "webserver.csr" → right click on "Pending Requests" → All Tasks → Issue → Go on "Issued Certificates" → right click on the certificate → Open → Details → Copy to File → Export in Base-64 (.CER) → Save as "uni.loc.cer" </li>

<li>Now copy this certificate on the webserver </li>

``` bat
    C:\> scp "C:\Users\Administrator\Desktop\uni.loc.cer" debian@10.0.2.10:/home/debian
```

<li>Insert the debian's password </li>

## Step 9: Convert The Certificates And Create The Full Chain.
<li>Rename the certificates from .cer to .crt (renaming is sufficient since they are in base64 PEM format) </li>

``` shell
    $ sudo cp /home/you/web_lab_local.cer /etc/ssl/certs/webserver.crt
    $ sudo cp /home/you/rootCA.cer /etc/ssl/certs/rootCA.crt
```
<li>Create the fullchain and update it's permissions </li>

``` shell
    $ sudo sh -c 'cat /etc/ssl/certs/webserver.crt /etc/ssl/certs/rootCA.crt > /etc/ssl/certs/web_fullchain.crt'
    $ sudo chmod 644 /etc/ssl/certs/web_fullchain.crt
```
<li>Update system's certificates </li>

``` shell
    $ sudo cp /etc/ssl/certs/rootCA.crt /usr/local/share/ca-certificates/
    $ sudo update-ca-certificates
```
The RootCA certificate should be installed on all trusted network devices; however, it is not necessary for machines that will be joined to the Active Directory domain (the Laboratory workstations). Furthermore, the RootCA certificate must be installed on browsers that will connect to the “uni.loc” portal over HTTPS.

## Step 10: Setup VirtualHost On The WebServer
This step must be executed on the Debian machine hosting the web server. With the certificates and full chain now available, the Virtual Host can be configured.
<li>Create the file</li>

``` shell
    $ sudo nano /etc/apache2/sites-available/web-ssl.conf
```
<li>Copy and paste this content inside:</li>

```
    <IfModule mod_ssl.c>
    <VirtualHost *:443>
        ServerName web.lab.local
        ServerAlias web
        DocumentRoot /var/www/html

        SSLEngine on
        SSLCertificateFile /etc/ssl/certs/web_fullchain.crt
        SSLCertificateKeyFile /etc/ssl/private/webserver.key

        <Directory /var/www/html>
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/web_ssl_error.log
        CustomLog ${APACHE_LOG_DIR}/web_ssl_access.log combined

        Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    </VirtualHost>
    </IfModule>

```
<li>Enable the modules </li>

``` shell
    $ sudo a2enmod ssl headers
    $ sudo a2ensite web-ssl
    $ sudo systemctl reload apache2
```

## Step 11: -------
<li> Open the search bar → search "Active Directory Users and Computers" → right click "uni.local" → New → Organization Unit → Name it "Laboratory" → right click "Laboratory" → New → Organization Unit → Name it "Computers" → right click "Laboratory" → New → Organization Unit → Name it "Users" → right click "uni.local" → New → Group → Name it "GRP_Segreteria" → right click "uni.local" → New → Group → Name it "GRP_Laboratorio" </li>
As machines are added to the domain, ensure that users and computers are assigned to their correct organizational units.

