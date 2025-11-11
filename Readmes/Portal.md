# Portal Server (Apache2) Configuration in the Laboratory
<h4> This guide describes how to create and configure the **Apache Portal Server** (an open-source HTTP server for modern operating systems) within a Debian machine. </h4>

## Step 1: Container Installation, Placement, and Configuration
<ol>
    <li>Add Container
        <ol>
            <li>In GNS3, instantiate the container by going to Edit → Preferences → Qemu VMs → New → choose where to run the container → enter the image debian-12.6.qcow2 → choose a name and follow the on-screen instructions.</li>
            <li>Drag the container into the GNS3 project and connect it to the switch in the DMZ subnet.</li>
        </ol>
    </li>
    <li>Start and open the container's console.</li>
</ol>

## Step 2: MariaDB Installation
<li> Update repositories, install packages and MariaDB</li>

``` shell
    $ sudo apt update && sudo apt upgrade -y
    $ sudo apt install -y apache2 php libapache2-mod-php php-mysql php-xml php-mbstring php-json php-cli php-curl php-zip php-fileinfo
    $ sudo apt install -y mariadb-server mariadb-client
```
<li> Secure the installation </li>

``` shell
    $ mysql_secure_installation
```
Perform the following operations when shown on screen:

<ol>
    <li>Enter current password for root (enter for none): Press Enter (there is no password)</li>
    <li>Switch to unix_socket authentication? [Y/n]: Type n and press Enter.</li>
    <li> Change the root password? [Y/n]: Type Y, press Enter, and set a strong password for the database root user</li>
    <li>Remove anonymous users?: Y </li>
    <li>Disallow root login remotely?: Y</li>
    <li>Remove test database and access to it?: Y</li>
    <li> Reload privilege tables now?: Y </li>
</ol>

## Step 3: Create the DB
Create the space and credentials that the web application will use to connect.
<li> Access MariaDB as root using the password set previously </li>

``` shell
    $ mysql -u root -p
```
<li>Execute the SQL commands: </li>

``` sql 
    CREATE DATABASE secure_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    CREATE USER 'portal_user'@'localhost' IDENTIFIED BY 'PasswordMoltoForte!';
    GRANT SELECT, INSERT, UPDATE, DELETE ON secure_portal.* TO 'portal_user'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;
```
<li>Restart the database </li>

``` shell
    $ service mariadb restart
```

## Step 4: Import The Structure
<li>Create the file structure as: </li>
```
    secure_portal/
    ├─ sql/
    │  └─ init.sql
    ├─ www/
    │  ├─ .htaccess
    │  ├─ index.php
    │  ├─ dashboard.php
    │  ├─ login.php
    │  ├─ logout.php
    │  ├─ download.php
    │  ├─ upload.php
    │  ├─ files.php
    │  ├─ templates/
    │  │   ├─ header.php
    │  │   └─ footer.php
    │  └─ assets/
    │      └─ styles.css
    ├─ private_storage/
    │  └─ (files...)
    └─ config.php
```

