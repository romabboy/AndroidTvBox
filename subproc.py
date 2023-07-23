import subprocess
import os
import time
import threading

# result = subprocess.run("dir venv\Scripts", shell=True)
# print(result)
# print(result.returncode)
#
# result = subprocess.run("ping 3 -n 10.1.1.1", shell=True)
# print(result)

# arr = [1,2,3,4]
# a,b = arr
#
# print(a,b)

ip = "192.168.1."
pingIpL = []


file = os.popen("ping 192.168.1.11")
#
# for x in file:
#     print(x)
#     if x.find("Reply") != -1:
#         pingIpL.append("lol")
#         file.close()

def func(ip):
    try:
        file = os.popen(f"ping {ip}")
        for row in file:
            if row.find("Pinging") != -1:
                continue
            elif row.find("bytes") != -1:
                pingIpL.append(ip)
                file.close()
    except:
        _ = 0




for x in range(50):
    thr = threading.Thread(target=func, args=[f"{ip}{x}"])
    thr.start()

thr.join()
pingIpL.sort()
print(pingIpL)
