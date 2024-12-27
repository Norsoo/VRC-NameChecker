import os, time, requests
from threading import Thread
from colorama import init, Fore

init()

os.system("title VRC Name Checker || by Xo")
cwd = os.path.dirname(os.path.realpath(__file__))
names = open(f"{cwd}\\names.txt", 'r').read().splitlines()


def logo():
    os.system('cls;clear')
    print("""
    VRC Name Availability Checker
   ♥ https://github.com/Xogot
   """.replace('█', Fore.WHITE + '█' + Fore.LIGHTMAGENTA_EX))


logo()

def check_name(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Python-Requests/2.28)',
    }

    url = f"https://vrchat.com/api/1/auth/exists?username={name}&displayName={name}&apiKey=JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26"
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 403:
            print(f"{Fore.RED}[ERROR]{Fore.WHITE} Forbidden (403) for {name}")
            print(f"Response headers: {r.headers}")
            print(f"Response content: {r.text[:200]}...")
            return
        if r.status_code != 200:
            print(f"{Fore.YELLOW}[WARNING]{Fore.WHITE} Status code {r.status_code} for {name}")
            print(f"Response preview: {r.text[:200]}...")
            return
        try:
            response = r.json()
        except requests.exceptions.JSONDecodeError:
            print(f"{Fore.YELLOW}[WARNING]{Fore.WHITE} Failed to parse JSON for {name}")
            print(f"Response preview: {r.text[:200]}...")
            return

        if not response.get('userExists', True):
            print(f"{Fore.GREEN}[{Fore.LIGHTGREEN_EX}AVAILABLE{Fore.GREEN}]{Fore.WHITE} {name}")
            with open('available.txt', 'a') as f:
                f.write(name + '\n')
        else:
            print(f"{Fore.RED}[{Fore.LIGHTRED_EX}UNAVAILABLE{Fore.RED}]{Fore.WHITE} {name}")

    except requests.RequestException as e:
        print(f"{Fore.RED}[ERROR]{Fore.WHITE} An error occurred: {e}")



threads = []
for name in names:
    threads.append(Thread(target=check_name, args=[name]))

for t in threads:
    t.start()
    time.sleep(1)

for t in threads:
    t.join()


# 