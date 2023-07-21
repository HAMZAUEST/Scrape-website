import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []
proxy_count = 0
max_proxies = 30

with open("proxylist.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxies():
    global q, valid_proxies, proxy_count
    while not q.empty() and proxy_count < max_proxies:
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",
                               proxies={"http": proxy,
                                        "https": proxy})
        except:
            continue
        if res.status_code == 200:
            valid_proxies.append(proxy)
            proxy_count += 1
            print(proxy)

threads = []

for t in range(10):
    thread = threading.Thread(target=check_proxies)
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("Valid Proxies Found:", valid_proxies)
