# SSH Bruteforce attack

![alt](../src/ssh.png)
# Alert Triage 

### Severity level - High
---

### Incident Summary
 - Multiple SSH login attempts were made to the AWS EC2 instance with agent id: 001 followed by successful login to the machine, at Aug 7, 2026 @ 23:45:55.894 from the src_ip 195.178.110.227, where it ran an automated credential validation script which fingerprints the system and tests for sandbox indicators.     

 ---

### Filters Used 

- data.src_ip: 195.178.110.227
    - 4 previous login sessions found in short spam of time.
- data.input: exsits

    - export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH
uname=$(uname -s -v -n -m 2>/dev/null || /bin/uname -s -v -n -m 2>/dev/null || /usr/bin/uname -s -v -n -m 2>/dev/null || busybox uname -s -v -n -m 2>/dev/null || ( [ -f /proc/version ] && head -1 /proc/version | cut -d' ' -f1 ) || ( [ -f /etc/os-release ] && grep '^ID=' /etc/os-release | cut -d= -f2 | tr -d '"' ) || echo "")
arch=$(uname -m 2>/dev/null || /bin/uname -m 2>/dev/null || /usr/bin/uname -m 2>/dev/null || busybox uname -m 2>/dev/null || ( [ -f /proc/cpuinfo ] && grep -q "lm" /proc/cpuinfo && echo x86_64 ) || ( [ -f /proc/cpuinfo ] && grep -q "CPU architecture: 8" /proc/cpuinfo && echo aarch64 ) || ( [ -f /proc/cpuinfo ] && grep -q "CPU architecture: 7" /proc/cpuinfo && echo armv7l ) || echo "")
uptime=$(cat /proc/uptime 2>/dev/null || busybox cat /proc/uptime 2>/dev/null)

---

### Threat Intelligence 

-  **AbsueIPDB** - The IP was reported 29,381 times.
-  **Virstotal** - The IP is flagged by 14 vendors.

---

### MITRE Attack ID mapping 
- T1110
- T1078
- T1059 
    - T1059.004
- T1497
    - T1497.001
---
### Verdict/Escalation

True Postive and escalation required.

---

### Response and Recommendations 

- Kill the attacker's active session.
- Disable the compromised account.
- Check for persistance.
- Added the IP to Block list.

---

### Lessons learned

There are many automated credential stuffing bots in the internet which constantly targets public facing IPs with open ssh ports which are obtained by the masscan. Where the automated bots constantly tries different leaked credential's username and password on the target IP to gain access, than perform automated command execution on the victim machine to confirm the legitmacy of the machine.

After gathering all the information of the machine the bot automatically exits in matter of seconds. If found valid/authenctic machine a follow up payload delivery might be attempted on the ip.

---