# ⚡ SkunkScrape

![Version](https://img.shields.io/badge/version-1.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/github/license/skunkworks-africa/SkunkScrape)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Made with ❤️ in Africa](https://img.shields.io/badge/Made%20in-Africa-000000?logo=ubuntu)

> **Smart Web Scraper to Automatically Extract Emails, Phone Numbers, and Addresses from URLs or Keyword Searches**

---

![skunkscrape](https://github.com/user-attachments/assets/b5ec8c4f-a9ae-4794-848d-7488b1351e2a)

## 🎬 Demo

> 📽️ _Video tutorial and walkthrough_  
> [![Watch the video](https://img.shields.io/badge/Watch%20Demo-YouTube-red?logo=youtube)](https://youtu.be/R039Z--IO28)

---

## 🚀 Features

- 🔍 **Auto URL Lookup** via DuckDuckGo (Keyword-based)
- 📥 **Import CSV/XLSX** with URLs
- 📤 **Export Scraped Data** to CSV or Excel
- 🧠 Extract:
  - ✉️ Emails
  - ☎️ Phone Numbers
  - 🏢 Addresses
- 🖥️ Beautiful GUI using **Tkinter**
- 🪪 Custom App Icon & Branding
- 🔔 Optional Email Notification
- 🧩 Error Handling & Logging

---

## 🖼️ App Preview

![image](https://github.com/user-attachments/assets/55aeb122-85f6-4155-8982-b44be46b3939)

---

## 📦 Installation

``` bash
git clone https://github.com/skunkworks-africa/SkunkScrape.git
cd SkunkScrape
pip install -r requirements.txt
python skunkscrape.py
```

### 🐍 Python Requirements

```bash
pip install pandas requests beautifulsoup4 lxml Pillow duckduckgo-search
```

---

## 📁 Folder Structure

```
SkunkScrape/
│
├── assets/                 # Icons, logos, screenshots
├── skunkscrape.py          # Main Python app
├── icon.ico                # App icon
├── README.md               # You are here 🚀
├── requirements.txt        # Dependencies
└── logs/                   # Runtime logs
```

---

## ⚙️ Usage

1. **Launch** the app (`python skunkscrape.py`)
2. Choose to **Import a CSV/XLSX** or **Search via Keyword**
3. Click `Start Web Scraping`
4. Once done, click `Save Results`
5. (Optional) Configure email notifications in the script

---

## 📧 Notifications

You can configure email alerts by updating:

```python
# send_notification() in skunkscrape.py
msg['From'] = "your@email.com"
server.login("your@email.com", "yourpassword")
```

> Use environment variables or `.env` for better security in production.

---

## 🛡️ License

Licensed under the [MIT License](LICENSE).

---

## 🧠 About Skunkworks (Pty) Ltd

SkunkScrape is a product of **Skunkworks Africa** 🇿🇦
Building AI-first automation tools that simplify digital workflows and boost productivity.

* 🌍 [https://www.skunkworks.africa](https://www.skunkworks.africa)
* ✉️ [hello@skunkworks.africa](mailto:hello@skunkworks.africa)

> *“Find Contacts. Fast. Automated.”*

---

## ⭐ Support & Contributions

If you find this useful:

* Leave a ⭐ on the repo
* Share your feedback
* Submit feature requests or bugs via [issues](https://github.com/skunkworks-africa/SkunkScrape/issues)
