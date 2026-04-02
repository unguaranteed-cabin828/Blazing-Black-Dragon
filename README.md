<p align="center">
  <pre>
  ████████╗██╗  ██╗███████╗    ██████╗ ██╗      █████╗ ███████╗██╗███╗   ██╗ ██████╗
  ╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██║     ██╔══██╗╚══███╔╝██║████╗  ██║██╔════╝
     ██║   ███████║█████╗      ██████╔╝██║     ███████║  ███╔╝ ██║██╔██╗ ██║██║  ███╗
     ██║   ██╔══██║██╔══╝      ██╔══██╗██║     ██╔══██║ ███╔╝  ██║██║╚██╗██║██║   ██║
     ██║   ██║  ██║███████╗    ██████╔╝███████╗██║  ██║███████╗██║██║ ╚████║╚██████╔╝
     ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝
  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗    ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗
  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║
  ██████╔╝██║     ███████║██║     █████╔╝     ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║
  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗     ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║
  ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗    ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
  </pre>
</p>

<h1 align="center">🐉 THE BLAZING BLACK DRAGON<br>WITH FIERY BREATH 🔥</h1>

<p align="center">
  <strong>Professional Web Vulnerability Assessment Engine — v4.0.0</strong><br>
  <em>26 fire‑breathing attack vectors • For authorised penetration testing only</em>
</p>

<p align="center">
  <a href="https://github.com/Ali-Haidar-Sy/BlazingBlackDragon/stargazers"><img src="https://img.shields.io/github/stars/Ali-Haidar-Sy/BlazingBlackDragon?style=for-the-badge&color=yellow"></a>
  <a href="https://github.com/Ali-Haidar-Sy/BlazingBlackDragon/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Ali-Haidar-Sy/BlazingBlackDragon?style=for-the-badge&color=blue"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
  <a href="https://t.me/P33_9"><img src="https://img.shields.io/badge/Telegram-@P33_9-2CA5E0?style=for-the-badge&logo=telegram"></a>
  <a href="https://www.instagram.com/_ungn"><img src="https://img.shields.io/badge/Instagram-@_ungn-E4405F?style=for-the-badge&logo=instagram"></a>
  <a href="https://github.com/Ali-Haidar-Sy"><img src="https://img.shields.io/badge/GitHub-Ali--Haidar--Sy-181717?style=for-the-badge&logo=github"></a>
</p>

---

## ⚠️ YOU MUST UPDATE THE TOOL

> **This is a living project.** Always pull the latest version before each scan:
> ```bash
> git pull origin main
> ```
> New modules, payloads, and fixes are added regularly. **Do not use an outdated copy.**

---

## ✨ FEATURES — 26 ATTACK VECTORS

| Category | Modules |
|----------|---------|
| **Reconnaissance** | Port scanner (nmap/TCP) • WAF/CDN fingerprinting • Web server fingerprinting • Subdomain enumeration |
| **Configuration** | Security headers analysis • SSL/TLS deep inspection • robots.txt / sitemap analysis • CMS detection (13 platforms) |
| **Content Discovery** | Directory & file brute‑force • JavaScript secret scanner • Form & email harvester |
| **Injection Attacks** | XSS (reflected) • SQLi (error + time‑blind) • SSTI • LFI / Path Traversal • Command injection • Open redirect |
| **Logic Flaws** | CORS misconfiguration • HTTP method tampering • Host header injection • CSRF token analysis |
| **Modern / API** | GraphQL introspection • OAuth / JWT misconfiguration • HTTP request smuggling (CL.TE) |
| **External Tools** | Nikto • Nuclei • sqlmap hooks |
| **Reporting** | HTML • JSON • TXT • CSV • XML + Clickjacking PoC generator |

---

## 🚀 QUICK START

```bash
# 1. Clone the dragon's lair
git clone https://github.com/Ali-Haidar-Sy/BlazingBlackDragon.git
cd BlazingBlackDragon

# 2. Install dependencies (auto‑installer will also run)
pip install -r requirements.txt

# 3. Launch the dragon
python dragon_scanner.py
```
Example session
🐉 Enter target URL: https://example.com

⚠️ LEGAL NOTICE
Unauthorised scanning is illegal.
Do you have explicit written permission? [yes/no]: yes

Scan mode:
  1 = Full scan (all 26 modules)
  2 = Fast scan
  3 = Stealth scan
Choice [1]: 1

🔥 The Dragon hunts...
After the scan, choose from 5 report formats and save them locally.

📸 PREVIEW
   NO 

🛡️ LEGAL DISCLAIMER
This tool is for educational purposes and authorized penetration testing only.
The author is not responsible for any misuse. Always obtain written permission before scanning any system.

🤝 CONTRIBUTING
Found a bug? Want a new module?
Open an Issue or submit a Pull Request. Contributions are warmly welcomed.

📞CONNECT WITH ME
Platform Handle
Telegram @P33_9
Instagram @_ungn
GitHub Ali-Haidar-Sy
<p align="center"> <strong>🐉 May your scans be thorough and your targets be authorized. 🔥</strong><br> ⭐ If this dragon saved you time, give it a star on GitHub! ⭐ </p> ```
✅ What makes this README “very, very, very beautiful and attractive”?
ASCII dragon banner – instant “wow” factor

Shields.io badges – professional, colourful, clickable

Table of 26 modules – scannable and impressive

Emojis – every section pops

Clear update warning – highlighted with a red note

Contact badges right at the top – Telegram, Instagram, GitHub

Legal disclaimer – shows responsibility

Call-to-action to star the repository
