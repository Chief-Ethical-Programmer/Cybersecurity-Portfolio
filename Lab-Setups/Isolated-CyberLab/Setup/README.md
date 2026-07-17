# Isolated CyberLab

A dual-perspective (red team + blue team) security operations homelab combining on premises virtualized infrastructure with a cloud-hosted virtual private server. Built for hands-on SOC analysis and offensive security practice, with an emphasis on realistic network segmentation and detection engineering.

---
## Architecture

The architecture is designed to simulate a real-world SOC environment, supporting both defensive analysis and offensive practice.

![Architecture](../src/architecture.png)

---
## Technologies Used

- **VMware** - Hypervisor for deploying and isolating multiple VMs.
- **pfSense** - Router, firewall, and DHCP server providing network segmentation (LAN/DMZ) for the lab.
- **Suricata (IDS)** - Running in alert-only mode on the DMZ interface to monitor and detect malicious traffic.
- **AWS EC2 (VPS)** - Cloud-hosted instance running honeypots (Cowrie, OpenCanary) and a Wazuh agent, connected back to the home lab via WireGuard.
- **Wazuh (SIEM)** - Manager, indexer, and dashboard hosted on-prem (Parrot OS), serving as the central hub for alerts and activity from both DMZ and cloud honeypots.
- **WireGuard (VPN)** - Encrypted tunnel connecting the EC2 instance to the home lab, used to transfer Wazuh agent logs securely.
- **Honeypots** - Cowrie, OpenCanary T-Pot

---

### VMware Setup

**1. Configuring the Network Interfaces** 
- Go to the Edit --> Virtual Network Editor 

![Alt](../src/vmimg1.png)

- Add Network interfaces where one interface should be in Bridged mode which will act as the router (WAN) and rest all Host only for isolated (LAN) network. Also turn off the (Use local DHCP services to distribute IP address to VMs) as pfsense will handle it.

    ***Note:***- For ease edit the subnet address to consecutive addresses shown below.
![ALt](../src/vmimg2.png)


**2. VM Setup**
- Create the VMs of your choice for the Internal/DMZ zone ref: [link](https://www.youtube.com/watch?v=3cK8YHO0fWo) and install the pfsense from https://www.pfsense.org/download/ 

- Now in Virtual Machine Settings according to the network interfaces assign the Network adapter for Internal&DMZ VMs to Host only network interfaces. 
Network Adapter --> Custom Specific virtual network --> Select any Host only interface

![ALT](../src/vmimg3.png)

- For pfsense assign one Network adapter to the Bridge network interface which will act as WAN interface. Than add another new Network adapter assign it to any of the Host only network interfaces, similarly add new adapters and assign the remaining host only interfaces to them.
![alt](../src/vmimg4.png)
- Now start the pfsense first as we need to setup the routing first for isolated network.
---
### pfsense setup

**1. Installing the pfsense**

- After starting the pfsense VM will prompted the screen below hit enter. 
![alt](../src/pfsense1.png)
- Now select the WAN interface MAC address. 
![alt](../src/pfimg2.png)
To identify the mac address referrer to pfsense VMware menu --> Edit virtual machine settings --> Network Adapter with the Bridged mode --> Select Advance where the MAC address is located.
![alt](../src/pfimg3.png)
- Similarly identify the LAN/Host-only MAC addresses and press enter.
- Install the CE edition. 
![alt](../src/pfimg4.png)
- Continue with the default file system type and disk partition scheme.
- Hit enter with the default disk selection.
- Select the current stable version and let it install, than after installation hit reboot.
- After reboot will land in pfsense console.
![alt](../src/pfimg6.png)

**2. Web GUI**
- From the pfsense console note down anyone of the LAN IP address.
- Than in the attacker VM go to the browser and enter the noted IP address which will land to pfsense web pannel.
**Default** **Username - admin** and **Password - pfsense**

![alt](../src/pfimg7.png)

- On the pfSense Setup you can change the Hostname, Domain, Primary DNS Server of your own I have kept it default.

![alt](../src/pfimg8.png) 

- On the **Time Server Information** page either keep it default or select accordingly.
- On the Configure WAN interface page change the **SelectedType** to DHCP and rest default.
- On the **Configure LAN interface** page keep it default.
- On the **Set Admin WebGUI Password** set the new admin password.
- Click on finish and will land into pfsense dashboard.

**3. WAN & DMZ Interfaces Setup**
- Go to **Interfaces** --> **WAN** verify if **Enable the interface** is checked,the **IPv4 Configuration Type** is in **DHCP**, **IPv6 Configuration Type** in **DHCP6**, rest keep it to default and save it.
![alt](../src/pfimg9.png)
- Now for LAN **Interfaces** --> **LAN** --> change **IPv4 Configuration Type** to Static IPv4 for **IPv6 Configuration Type** to None. In **Static IPv4 Configuration IPv4 address** enter the LAN IP of the attacker/internal network machine with subnet mask /24,uncheck the **Reserved Networks** and save it. 
![alt](../src/pfimg10.png)

- Now go to Interfaces --> Assignments --> OPT1 --> Enable the interface than change **Description** from OPT1 to DMZ with **IPv4 COnfiguration Type** to Static IPv4 and **IPv6 Configuration Type** to None, assign the DMZ Vm LAN IP with subnet mask /24 on the **Static IPv4 Configuration**, Uncheck the **Reserved Networks** and save it. 
![alt](../src/pfimg11.png)

**4. DHCP Server**
- **Services** --> **DHCP Server** --> **LAN** --> Enable DHCP server on LAN interface, in the **Primary Address Pool** set the address pool range from the assigned subnet xxx.xxx.xx.100 to xxx.xxx.xx.200 and save it.
![alt](../src/pfimg12.png)
- Similarly for DMZ set the address pool range with respect to the assigned subnet xxx.xxx.xx.100 to xxx.xxx.xx.200 and save it.
![alt](../src/pfimg13.png)

**5. Firewall Rules**
- Go to the **Firewall** --> **DMZ** leave the default rule as it is.
- Click **Add** --> **Action**: Block, **Protocol**: Any, **Source:** DMZnet, **Destination:** LANnet add a **Description:** Block DMZ to LAN and save it
![alt](../src/pfimg15.png)
- Similarly add another rule for allowing DMZ wazuh agent to send logs to LAN wazuh manager 
**Action:** Pass, **Protocol:** TCP, **Source:**  DMZ subnet, **Destination:** Address or Alias also asign the IP of the LAN VMs IP address, **Destination Port Range**: 1514 to 1515, add the description  and save it. 
***Note:*** Drag this rule to the top.
![alt](../src/pfimg16.png)
- Similarly add another rule for internet access where **Action:** Pass, **Protocol:**Any, **Source:** DMZnet, **Destination:** Any, **Description:** Allow internet access and save it.
- Final firewall rules for DMZ should looks like the img below
![alt](../src/pfimg17.png)
- Now for LAN rules keep the default rules.
- Add a new rule **Action:** Pass, **Protocol:** TCP, **Source:** LAN subnets, **Destination:** DMZ subnets, **Description:** Allow LAN to DMZ, **Destination Port range** : Any to Any and save it.
![alt](../src/pfimg18.png)
---
### Suricata Setup
**1. DMZ Interface settings**
- Go to **System** --> **Package Manager** --> **Availabe Packages** --> Search for Suricata. Click Install, confirm and wait for it to finish.
- Go to **Services → Suricata**, click **Add**.
- **Enable** Suricata inspection on the interface, then configure:
  - **Interface:** DMZ
  - **Description:** DMZ-IDS
  - **EVE JSON Log:** checked
  - **EVE Log Alert Payload Data Formats:** BOTH
  - **EVE Logged Traffic:** DNS, FTP, HTTP, HTTP2, IKE, Kerberos, NFS, QUICv1, RFB, SMB, SMTP, TFTP all checked
  - **EVE Logged Info:** DHCP Messages, MQTT, SNMP, SSH Handshakes, TLS Handshakes, Tracked Files all checked
  - **EVE Logged Extended:** Extended HTTP Info, Extended TLS Info, Extended SMTP Info checked
- Leave all other settings at their default values.
![alt](../src/surimg1.png)
![alt](../src/surimg2.png)
- CLick **Save.**

**2. Threat Detection**
- Go to **Global Settings** --> Check the **Install ETOpen EMerging Threats rules** --> **Save**
- Go to DMZ row --> Edit --> **DMZ Categories**
- Check these rules 
    - emerging-scan.rules
    - emerging-exploit.rules
    - emerging-malware.rules
    - emerging-web_server.rules
- **Save** it.

**3. Start the instance**
- Go back to **Services** --> **Suricata** --> Click the play button on the DMZ which will start capturing the alerts.
![alt](../src/surimg3.png)
---
### AWS (VPS) Setup
**1. Create the EC2 instance**
- Create an EC2 instance. Ref: [link](https://www.youtube.com/watch?v=ismLPGjdzhk)
- Now in the **Security groups** --> **Inbound** --> **Edit inbound rules** --> **Add rule** 
    - Add the below rules
    - ![alt](../src/aws.png)
    - Where the 51820 port will be used for wireguard tunnel, port 22 for SSH, port 80/443 for HTTP/HTTPS and 21 for telnet.
    
    ***Note:*** Don't create unecessary open ports.
---

### WireGuard Setup






### Honeypot Setup
For this lab I have used the cowrie and opencanary but their are more open source options available like T-Pot, Dionaea, etc.

