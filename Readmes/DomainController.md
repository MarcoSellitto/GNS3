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

## Step 2: Installation GUI
Windows will guide the user through the installation process. Choose “Custom: Install Windows only (advanced)” as the installation type, and set the administrator password to “DomainController/70.”

----- Indirizzo IP statico ------

----- Installare direttamente prima DC e poi fare la roba della CA ------