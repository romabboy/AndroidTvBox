import os,threading,myConfig
import time

def main_func():
    ip = myConfig.IP_MASK
    RANGE = myConfig.RANGE
    pingIpL = []

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

    for x in range(*RANGE):
        thr = threading.Thread(target=func, args=[f"{ip}.{x}"], daemon=True)
        thr.start()

    thr.join()
    pingIpL.sort()

    return pingIpL

if __name__ == "__main__":
    a = main_func()
    print(a)