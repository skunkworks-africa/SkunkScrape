import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import threading
import time
import os
import logging
import smtplib
from email.mime.text import MIMEText
import importlib.util
import subprocess
import sys

# Ensure duckduckgo_search is available or install it
def ensure_duckduckgo():
    if importlib.util.find_spec("duckduckgo_search") is None:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "duckduckgo-search"])
        except Exception as e:
            messagebox.showerror("Missing Module", f"Could not install 'duckduckgo-search'.\n\nError: {e}")
            return False
    return True

duckduckgo_available = ensure_duckduckgo()
if duckduckgo_available:
    from duckduckgo_search import DDGS

# Setup logging
logging.basicConfig(filename="skunkscrape.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class ContactScraperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SkunkScrape - Contact Info Scraper")
        self.master.configure(bg="#0b0c10")
        self.master.iconbitmap("icon.ico")
        self.master.geometry("900x750")
        self.master.minsize(700, 600)
        self.file_path = ""
        self.urls = []
        self.results = []

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=10, relief="flat", background="#1f2833", foreground="#66FCF1",
                        font=('Segoe UI', 11, 'bold'))
        style.map("TButton",
                  background=[('active', '#45A29E')],
                  foreground=[('active', 'white')])
        style.configure("TLabel", background="#0b0c10", foreground="#C5C6C7", font=('Segoe UI', 10))
        style.configure("TProgressbar", troughcolor="#1F2833", background="#66FCF1", thickness=20)

        top_frame = tk.Frame(self.master, bg="#0b0c10")
        top_frame.pack(pady=10)

        self.import_button = ttk.Button(top_frame, text="Import CSV/XLSX", command=self.import_file)
        self.import_button.grid(row=0, column=0, padx=5)

        self.search_button = ttk.Button(top_frame, text="Search via Keywords (Auto Lookup)", command=self.keyword_search_info)
        self.search_button.grid(row=0, column=1, padx=5)

        self.sample_button = ttk.Button(top_frame, text="Download Sample File", command=self.download_sample_file)
        self.sample_button.grid(row=0, column=2, padx=5)

        self.message_label = ttk.Label(self.master, text="", font=("Segoe UI", 10))
        self.message_label.pack(pady=5)

        self.start_button = ttk.Button(self.master, text="Start Web Scraping", command=self.start_scraping, state=tk.DISABLED)
        self.start_button.pack(pady=10)

        self.progress = ttk.Progressbar(self.master, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.progress.pack(pady=20)

        self.save_button = ttk.Button(self.master, text="Save Results", command=self.save_results, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        try:
            logo_image = Image.open("icon.png")
            logo_image = logo_image.resize((200, 200), Image.ANTIALIAS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(self.master, image=self.logo_photo, bg="#0b0c10")
            logo_label.pack(pady=10)
        except Exception as e:
            logging.warning("Logo could not be loaded: %s", str(e))

        footer_label = tk.Label(self.master, text="A product of Skunkworks (Pty) Ltd.", bg="#0b0c10", fg="#C5C6C7", font=('Segoe UI', 9, 'italic'))
        footer_label.pack(side=tk.BOTTOM, pady=10)

    def download_sample_file(self):
        sample_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if sample_path:
            sample_data = {
                "Company Name": ["Example Company"],
                "Individual Name": ["John Doe"],
                "Title": ["CTO"],
                "URL": ["https://www.example.com"]
            }
            pd.DataFrame(sample_data).to_csv(sample_path, index=False)
            messagebox.showinfo("Sample File", f"Sample file saved to: {sample_path}")

    def import_file(self):
        filetypes = [("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        self.file_path = filedialog.askopenfilename(title="Select File", filetypes=filetypes)
        if self.file_path:
            try:
                if self.file_path.endswith('.csv'):
                    df = pd.read_csv(self.file_path)
                elif self.file_path.endswith('.xlsx'):
                    df = pd.read_excel(self.file_path)
                else:
                    raise ValueError("Unsupported file format.")

                df.columns = [col.strip().lower().replace("website", "url") for col in df.columns]
                if "url" not in df.columns:
                    raise ValueError("The file must contain a 'URL' column.")

                df = df[df["url"].str.startswith("http")]
                self.urls = df["url"].dropna().tolist()
                self.message_label.config(text=f"Loaded {len(self.urls)} URLs from file.")
                self.start_button.config(state=tk.NORMAL)
                logging.info("Loaded file with %d URLs", len(self.urls))
            except Exception as e:
                logging.error("Failed to read file: %s", str(e))
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def keyword_search_info(self):
        if not duckduckgo_available:
            messagebox.showerror("Missing Module", "The 'duckduckgo_search' module is not installed.\nPlease install it with:\n\npip install duckduckgo-search")
            return

        query = simpledialog.askstring("Search Keywords", "Enter keywords (e.g., accounting firms Johannesburg):")
        if query:
            try:
                with DDGS() as ddgs:
                    results = ddgs.text(query, max_results=50)
                    urls = [r['href'] for r in results if 'href' in r and r['href'].startswith('http')]
                if urls:
                    self.urls = urls
                    self.message_label.config(text=f"Collected {len(urls)} URLs from search.")
                    self.start_button.config(state=tk.NORMAL)
                    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Found URLs")
                    if save_path:
                        pd.DataFrame({"URL": self.urls}).to_csv(save_path, index=False)
                        messagebox.showinfo("Saved", f"Search results saved to: {save_path}")
                else:
                    messagebox.showwarning("No Results", "No URLs found for the given query.")
            except Exception as e:
                logging.error("Search failed: %s", str(e))
                messagebox.showerror("Error", f"Search failed: {e}")

    def start_scraping(self):
        if not self.urls:
            messagebox.showwarning("Warning", "No URLs to process.")
            return

        self.start_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.results = []

        threading.Thread(target=self.scrape_contacts).start()

    def scrape_contacts(self):
        total = len(self.urls)
        for index, url in enumerate(self.urls, start=1):
            contact_info = self.extract_contact_info(url)
            self.results.append({'URL': url, **contact_info})
            self.progress['value'] = (index / total) * 100
            time.sleep(0.1)

        self.message_label.config(text="Scraping completed.")
        self.save_button.config(state=tk.NORMAL)
        logging.info("Scraping completed for all URLs.")
        self.send_notification("SkunkScrape Finished", f"Successfully scraped {len(self.results)} URLs.")

    def extract_contact_info(self, url, retries=3):
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()

                email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
                phone_match = re.search(r'\+?\d[\d\s\-]{7,}\d', text)
                address_match = re.search(r'\d{1,5}\s\w+\s\w+', text)

                return {
                    'Email': email_match.group(0) if email_match else '',
                    'Phone': phone_match.group(0) if phone_match else '',
                    'Address': address_match.group(0) if address_match else ''
                }
            except Exception as e:
                logging.warning("Attempt %d failed for %s: %s", attempt+1, url, e)
                time.sleep(2)
        return {'Email': '', 'Phone': '', 'Address': ''}

    def send_notification(self, subject, message, to_email="youremail@example.com"):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = "youremail@example.com"
        msg['To'] = to_email

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("youremail@example.com", "yourpassword")
                server.send_message(msg)
                logging.info("Notification sent to %s", to_email)
        except Exception as e:
            logging.error("Email notification failed: %s", str(e))

    def save_results(self):
        if not self.results:
            messagebox.showwarning("Warning", "No results to save.")
            return

        filetypes = [("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=filetypes)
        if save_path:
            try:
                df = pd.DataFrame(self.results)
                if save_path.endswith('.csv'):
                    df.to_csv(save_path, index=False)
                elif save_path.endswith('.xlsx'):
                    df.to_excel(save_path, index=False)
                else:
                    raise ValueError("Unsupported file format.")
                messagebox.showinfo("Success", f"Results saved to {save_path}")
                logging.info("Results saved to %s", save_path)
            except Exception as e:
                logging.error("Failed to save results: %s", str(e))
                messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    app = ContactScraperApp(root)
    root.mainloop()
