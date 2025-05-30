
# Bing Dorker - Real-Time Search & Save

![Bing Dorker](https://img.shields.io/badge/Bing-Dorker-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

Automate your Bing dork reconnaissance with speed, stealth, and precision.
Designed for security researchers, penetration testers, and red teamers
who demand reliable, real-time results without hassle.

Credit: github.com/idhin

## ⚠️ Disclaimer

This tool is intended for **legal and ethical use only**.  
Use it solely on targets you own or have explicit permission to test.  
The author and contributors are **not responsible** for any misuse or damage caused by this tool.  
Use at your own risk.

## Description

This **Bing Dorker** script helps you perform automated Bing dork searches with features like:

- Support for multiple dork queries from a file
- Fetch results from multiple pages per dork
- **Real-time saving of found links to output file**
- Safe to interrupt (Ctrl+C), results found so far remain saved
- No duplicate links saved
- Colorful console output for easy monitoring

---

## Usage

1. Make sure Python 3.8+ is installed on your system.

2. Prepare a `dorks.txt` file containing one dork query per line. Example:

   ```
   intext:"APP_KEY=" filetype:env
   intext:"APP_ENV=local" filetype:env
   site:*.gov inurl:index.php?id=
   ```

3. Run the script with arguments:

   ```bash
   python3 bingdork.py -l dorks.txt -o results.txt -p 3
   ```

   - `-l` or `--list`: path to your dork list file  
   - `-o` or `--output`: output file to save results  
   - `-p` or `--pages`: number of Bing result pages to fetch per dork (default is 1)

4. Wait for the script to finish. Links are saved to the output file as they are found.

---

## Example Output

```
[+] Found: https://example.com/vuln?id=1
[+] Found: https://target.gov/index.php?id=2
[+] Found: https://mysite.com/page.php?cat=3
```

The file `results.txt` will contain these URLs, one per line.

---

## Features

- Saves results in real-time (no waiting until all queries finish)  
- Graceful interruption handling (Ctrl+C saves progress)  
- Removes duplicate URLs automatically  
- Color-coded console output for better visibility  
- Uses `requests` and `BeautifulSoup` for Bing scraping

---

## Dependencies

Install required packages (if not installed):

```bash
pip install requests beautifulsoup4 colorama tqdm
```

---

## License

MIT License — free to use and modify.

---

## Disclaimer

Use this tool responsibly and ethically. Do not use it for illegal activities.

---

## Contact

If you have suggestions or issues, please open an issue on this GitHub repository.