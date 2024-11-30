# **BeeXSS: Automated Blind XSS Vulnerability Scanner**

**BeeXSS** is a specialized automated tool designed to detect **Blind XSS (Cross-Site Scripting)** vulnerabilities in web applications. Unlike standard XSS vulnerabilities, Blind XSS occurs when the injected script is executed in the web application’s backend or in an admin panel, making it harder to detect through traditional methods. BeeXSS automates the process of scanning URL parameters to find these hard-to-detect vulnerabilities by injecting payloads and analyzing responses.

## **Features**

- **Automated Blind XSS Detection**: Scans URLs with query parameters for Blind XSS vulnerabilities, where the payload is executed in the backend or admin areas.
- **Custom Payloads**: Utilizes a range of Blind XSS-specific payloads that can trigger alerts in the backend.
- **Headless Browsing**: Uses Selenium WebDriver for headless browsing, which allows the tool to scan pages quickly without the need for a visible browser window.
- **Reporting**: Provides detailed results, highlighting potentially vulnerable URLs, and allows saving them for future review.

## **Prerequisites**

- **Python 3.x**
- **Selenium**
- **ChromeDriver**
- **WebDriver Manager**
- **Chrome Browser**
- **xss.report Account**

## **Installation**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AnonKryptiQuz/BeeXSS.git
   cd BeeXSS
   ```

2. **Install required packages:**

   ```bash
    pip install -r requirements.txt
    ```

    Ensure `requirements.txt` contains:
    
    ```plaintext
    selenium
    webdriver-manager
    readline
    ```

3. **Download ChromeDriver:**

   Ensure that **ChromeDriver** is correctly installed and accessible. You can install it via `webdriver_manager`, which will automatically handle the driver setup.

## **Usage**

1. **Run the tool:**

   ```bash
   python BeeXSS.py
   ```

2. **Enter the base URL with a parameter** (e.g., `https://example.com/search?q=test`), or provide a file containing a list of URLs to scan.

3. **Enter the xss.report username** when prompted. This will allow you to send scan results directly to your **xss.report** account for a more detailed analysis of the found vulnerabilities.

4. **Specify the payload encoding** Choose how many times you want to encode the payloads (0-3). Enter the corresponding number to apply the desired number of encoding layers. This helps bypass WAFs (Web Application Firewalls) and test applications that handle multiple layers of encoding.

5. **Review the results** to check if any Blind XSS vulnerabilities were found. Vulnerable URLs will be flagged, and you’ll have the option to save them for future reference.

6. **Save results**: You can optionally save the results to a file by following the prompt after the scan completes.

## **Disclaimer**

- **Educational Purposes Only**: BeeXSS is designed for educational, security research, and ethical penetration testing purposes only. The tool should not be used for illegal or malicious activities. Always ensure you have permission to test the website or application.

## **Credits**

- **xss.report** by [xss.report](https://xss.report/) – For detailed analysis and reporting of vulnerabilities.

All tools are used under their respective open-source licenses.

## **Author**

**Created by:** [AnonKryptiQuz](https://AnonKryptiQuz.github.io/)
