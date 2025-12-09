#!/usr/bin/env python3
import psutil
import platform
import socket
import os
import time
import getpass
import json
from psutil._common import bytes2human
from datetime import datetime

def cpu_info():
    return {
        "cores": psutil.cpu_count(logical=True),
        "frequency_mhz": psutil.cpu_freq().current,
        "usage_percent": psutil.cpu_percent(interval=1)
    }

def memory_info():
    mem = psutil.disk_usage(path="/")
    return {
        "used_gb": mem.used / (1024**3),
        "total_gb": mem.total / (1024**3),
        "usage_percent": mem.percent
    }

def system_info():
    uname = platform.uname()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = time.time() - psutil.boot_time()
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    return {
        "hostname": uname.node,
        "os": f"{uname.system} {uname.release}",
        "boot_time": str(boot_time),
        "uptime": uptime,
        "users_connected": len(psutil.users()),
        "ip_address": socket.gethostbyname(socket.gethostname())
    }

def process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)

    top3 = sorted(processes, key=lambda x: (x['cpu_percent'] + x['memory_percent']), reverse=True)[:3]

    return {
        "processes_cpu": processes[:10],
        "processes_ram": processes[:10],
        "top3": top3
    }

def file_analysis(path):
    extensions = ['.txt', '.py', '.pdf', '.jpg']
    counts = {ext: 0 for ext in extensions}

    for root, dirs, files in os.walk(path):
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    counts[ext] += 1

    total_files = sum(counts.values())
    percentages = {ext: (count / total_files * 100) if total_files > 0 else 0 for ext, count in counts.items()}

    return {
        "counts": counts,
        "total": total_files,
        "percentages": percentages
    }

if __name__ == "__main__":
    # Collecte des infos
    cpu = cpu_info()
    mem = memory_info()
    sysinfo = system_info()
    proc = process_info()
    files = file_analysis("/home/" + getpass.getuser() + "/Documents")

    # Affichage texte brut
    print("=== CPU ===")
    print(f"Cœurs : {cpu['cores']}")
    print(f"Fréquence : {cpu['frequency_mhz']:.2f} MHz")
    print(f"Utilisation : {cpu['usage_percent']} %")

    print("\n=== Mémoire ===")
    print(f"Utilisée : {mem['used_gb']:.2f} GB")
    print(f"Totale : {mem['total_gb']:.2f} GB")
    print(f"Pourcentage : {mem['usage_percent']} %")

    print("\n=== Système ===")
    for k, v in sysinfo.items():
        print(f"{k} : {v}")

    print("\n=== Processus (Top 3 gourmands) ===")
    for p in proc["top3"]:
        print(f"{p['name']} (PID {p['pid']}) - CPU {p['cpu_percent']} %, RAM {p['memory_percent']:.2f} %")

    print("\n=== Analyse fichiers ===")
    for ext, count in files["counts"].items():
        print(f"{ext} : {count} fichiers ({files['percentages'][ext]:.2f} %)")

    # Sortie JSON
    data = {
        "cpu": cpu,
        "memory": mem,
        "system": sysinfo,
        "processes": proc,
        "files": files
    }

    print("\n=== Sortie JSON ===")
    print(json.dumps(data, indent=4))
    


    print('MEMORY\n------')
    print(psutil.virtual_memory())
    print('\nSWAP\n----')
    print(psutil.swap_memory())
    print(psutil.disk_partitions())
    print(psutil.disk_usage(path="/"))

