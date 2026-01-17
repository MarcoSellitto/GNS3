# Printer Configuration in Secretary
<h4> This guide describes how to create and configure the printer in the Secretary VLAN using a Debian machine. </h4>

## Step 1: VM Installation, Placement, and Configuration
<ol>
    <li>Add VM
        <ol>
            <li>In GNS3, instantiate the VM by going to Edit → Preferences → Qemu VMs → New → choose where to run the VM → enter the image debian-12.6.qcow2 → choose a name and follow the on-screen instructions.</li>
            <li>Drag the VM into the GNS3 project and connect it to the switch in the Secretary subnet.</li>
        </ol>
    </li>
    <li>Start and open the VM's console.</li>
</ol>

## Step 2: Cups Installation
<li> Update repositories and install Cups</li>

``` shell
    $ sudo apt update
    $ sudo apt install -y cups
    $ sudo apt install printer-driver-cups-pdf
```
By default, CUPS only listens on localhost. It is necessary to enable listening on all interfaces.
<li>Open the file</li>

``` shell
    $ sudo nano /etc/cups/cupsd.conf
```

<li>Replace it's content with:</li>

```
    #
    # Configuration file for the CUPS scheduler.  See "man cupsd.conf" for a complete description of this file.
    #

    # Log general information in error_log - change "warn" to "debug" for troubleshooting...

    LogLevel warn
    PageLogFormat

    # Specifies the maximum size of the log files before they are rotated.  The value "0" disables log rotation.
    MaxLogSize 0

    # Default error policy for printers
    ErrorPolicy retry-job

    # Only listen for connections from the local machine.
    Port 631
    Listen 0.0.0.0:631
    Listen [::]:631

    # Show shared printers on the local network.
    Browsing Yes
    BrowseLocalProtocols dnssd

    # Default authentication type, when authentication is required...
    DefaultAuthType Basic

    # Web interface setting...
    WebInterface Yes

    # Timeout after cupsd exits if idle (applied only if cupsd runs on-demand - with -l)
    IdleExitTimeout 60

    # Restrict access to the server...

    <Location />
       Order allow,deny
       Allow all
    </Location>

    # Restrict access to the admin pages...

    <Location /admin>
       Order allow,deny
       Allow all
    </Location>

    # Restrict access to configuration files...

    <Location /admin/conf>
       AuthType Default
       Require user @SYSTEM
       Order allow,deny
    </Location>

    # Restrict access to log files...
    <Location /admin/log>
       AuthType Default
       Require user @SYSTEM
       Order allow,deny
    </Location>

    # Set the default printer/job policies...
    <Policy default>
       # Job/subscription privacy...
       JobPrivateAccess default
       JobPrivateValues default
       SubscriptionPrivateAccess default
       SubscriptionPrivateValues default

       # Job-related operations must be done by the owner or an administrator...
       <Limit Create-Job Print-Job Print-URI Validate-Job>
           AuthType None
           Order deny,allow
           Allow all
       </Limit>


       <Limit Send-Document Send-URI Hold-Job Release-Job Restart-Job Purge-Jobs Set-Job-Attributes Create-Job-Subscription Renew-Subscription Cancel-Subscription Get-Notifications Reprocess-Job Cancel-Current-Job Suspend-Current-Job Resume-Job Cancel-My-Jobs Close-Job CUPS-Move-Job>

          #Require user @OWNER @SYSTEM
          AuthType None
          Order deny,allow
          Allow all
       </Limit>

       <Limit CUPS-Get-Document>
          AuthType Default
          # Require user @OWNER @SYSTEM
          Order deny,allow
          Allow all
       </Limit>

       # All administration operations require an administrator to authenticate...
       <Limit CUPS-Add-Modify-Printer CUPS-Delete-Printer CUPS-Add-Modify-Class CUPS-Delete-Class CUPS-Set-Default CUPS-Get-Devices>
          AuthType Default
          Require user @SYSTEM
          Order deny,allow
       </Limit>

       # All printer operations require a printer operator to authenticate...
       <Limit Pause-Printer Resume-Printer Enable-Printer Disable-Printer Pause-Printer-After-Current-Job Hold-New-Jobs Release-Held-New-Jobs Deactivate-Printer Activate-Printer Restart-Printer Shutdown-Printer Startup-Printer Promote-Job Schedule-Job-After Cancel-Jobs CUPS-Accept-Jobs CUPS-Reject-Jobs>
          AuthType Default
          Require user @SYSTEM
          Order deny,allow
       </Limit>

       # Only the owner or an administrator can cancel or authenticate a job...

       <Limit Cancel-Job CUPS-Authenticate-Job>
          #Require user @OWNER @SYSTEM
          Order deny,allow
          Allow all
       </Limit>

       <Limit All>
          Order deny,allow
       </Limit>

    </Policy>

       # Set the authenticated printer/job policies...

       <Policy authenticated>
          # Job/subscription privacy...
          JobPrivateAccess default
          JobPrivateValues default
          SubscriptionPrivateAccess default
          SubscriptionPrivateValues default
          # Job-related operations must be done by the owner or an administrator...

       <Limit Create-Job Print-Job Print-URI Validate-Job>
          AuthType Default
          Order deny,allow
          Allow all
       </Limit>

       <Limit Send-Document Send-URI Hold-Job Release-Job Restart-Job Purge-Jobs Set-Job-Attributes Create-Job-Subscription Renew-Subscription Cancel-Subscription Get-Notifications Reprocess-Job Cancel-Current-Job Suspend-Current-Job Resume-Job Cancel-My-Jobs Close-Job CUPS-Move-Job CUPS-Get-Document>
          AuthType Default
          # Require user @OWNER @SYSTEM
          Order deny,allow
          Allow all
       </Limit>

       # All administration operations require an administrator to authenticate...
       <Limit CUPS-Add-Modify-Printer CUPS-Delete-Printer CUPS-Add-Modify-Class CUPS-Delete-Class CUPS-Set-Default>
          AuthType Default
          Require user @SYSTEM
          Order deny,allow
       </Limit>

       # All printer operations require a printer operator to authenticate...
       <Limit Pause-Printer Resume-Printer Enable-Printer Disable-Printer Pause-Printer-After-Current-Job Hold-New-Jobs Release-Held-New-Jobs Deactivate-Printer Activate-Printer Restart-Printer Shutdown-Printer Startup-Printer Promote-Job Schedule-Job-After Cancel-Jobs CUPS-Accept-Jobs CUPS-Reject-Jobs>
          AuthType Default
          Require user @SYSTEM
          Order deny,allow
       </Limit>

       # Only the owner or an administrator can cancel or authenticate a job...
       <Limit Cancel-Job CUPS-Authenticate-Job>
          AuthType Default
          Require user @OWNER @SYSTEM
          Order deny,allow
       </Limit>

       <Limit All>
          Order deny,allow
       </Limit>

    </Policy>

    # Set the kerberized printer/job policies...
    <Policy kerberos>
       # Job/subscription privacy...
       JobPrivateAccess default
       JobPrivateValues default
       SubscriptionPrivateAccess default
       SubscriptionPrivateValues default

       # Job-related operations must be done by the owner or an administrator...

       <Limit Create-Job Print-Job Print-URI Validate-Job>
          AuthType Negotiate
          Order deny,allow
          Allow all
       </Limit>

       <Limit Send-Document Send-URI Hold-Job Release-Job Restart-Job Purge-Jobs Set-Job-Attributes Create-Job-Subscription Renew-Subscription Cancel-Subscription Get-Notifications Reprocess-Job Cancel-Current-Job Suspend-Current-Job Resume-Job Cancel-My-Jobs Close-Job CUPS-Move-Job CUPS-Get-Document>
          AuthType Negotiate
          Require user @OWNER @SYSTEM
          Order deny,allow
          Allow all
       </Limit>

       # All administration operations require an administrator to authenticate...
       <Limit CUPS-Add-Modify-Printer CUPS-Delete-Printer CUPS-Add-Modify-Class CUPS-Delete-Class CUPS-Set-Default>
          AuthType Default
          Require user @SYSTEM
          Order deny,allow
       </Limit>

       # All printer operations require a printer operator to authenticate...

      <Limit Pause-Printer Resume-Printer Enable-Printer Disable-Printer Pause-Printer-After-Current-Job Hold-New-Jobs Release-Held-New-Jobs Deactivate-Printer Activate-Printer Restart-Printer Shutdown-Printer Startup-Printer Promote-Job Schedule-Job-After Cancel-Jobs CUPS-Accept-Jobs CUPS-Reject-Jobs>
         AuthType Default
         Require user @SYSTEM
         Order deny,allow
      </Limit>

      # Only the owner or an administrator can cancel or authenticate a job...
      <Limit Cancel-Job CUPS-Authenticate-Job>
         AuthType Negotiate
         Require user @OWNER @SYSTEM
         Order deny,allow
      </Limit>

     <Limit All>

        Order deny,allow

     </Limit>

   </Policy>

```
<li>Set the printer as shared</li>

``` shell
    $ sudo lpadmin -p PDF -o printer-is-shared=true
```


<li>Enable and start Cups</li>

``` shell
    $ sudo systemctl enable cups
    $ sudo systemctl start cups
```
At this point, the printer is ready to be configured on the Windows 11 workstation within the Secretary VLAN.

## Step 3: Set static IP
<li>Open the file</li>

``` shell
    $ sudo nano /etc/network/interfaces
```
<li>Uncomment the relevant lines and modify the settings as shown below</li>

```
    # Static config for ens4
    auto ens4
    iface ens4 inet static
        address 10.0.40.40
        netmask 255.255.255.0
        gateway 10.0.40.1
        dns-nameservers 10.0.40.1
```
<li>Restart the machine to apply changes</li>