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
- Create the VMs of your choice for the Internal/DMZ zone and install the pfsense from https://www.pfsense.org/download/ 

- Now in Virtual Machine Settings according to the network interfaces assign the Network adapter for Internal&DMZ VMs to Host only network interfaces. 
Network Adapter --> Custom Specific virtual network --> Select any Host only interface

![ALT](../src/vmimg3.png)

- For pfsense assign one Network adapter to the Bridge network interface which will act as WAN interface. Than add another new Network adapter assign it to any of the Host only network interfaces, similarly add new adapters and assign the remaining host only interfaces to them.
![alt](../src/vmimg4.png)
- Now start the pfsense first as we need to setup the routing first for isolated network.
---
### pfsense setup




