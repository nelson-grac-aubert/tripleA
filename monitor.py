import psutil
import platform
import socket
import os
import time
import getpass
from psutil._common import bytes2human
from datetime import datetime

def cpu_info():
    return {
        "cores": psutil.cpu_count(logical=True),
        "frequency_mhz": psutil.cpu_freq().current,
        "usage_percent": psutil.cpu_percent(interval=1)
    }

def memory_info():
    ram = psutil.virtual_memory()
    return {
        "used_gb": ram.used / (1024**3),
        "total_gb": ram.total / (1024**3),
        "usage_percent": ram.percent
    }

def storage_info():
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

def set_variables() : 
    # Collecte des infos
    cpu = cpu_info()
    ram = memory_info()
    sysinfo = system_info()
    proc = process_info()
    files = file_analysis("/home/" + getpass.getuser() + "/Documents")

    # Assignation variables et print pour vérifications
    cpu_hearts = cpu['cores']
    cpu_frequency = cpu['frequency_mhz']
    cpu_usage_percent = cpu['usage_percent']
    print("=== CPU ===")
    print(f"Cœurs : {cpu_hearts}")
    print(f"Fréquence : {cpu_frequency:.2f} MHz")
    print(f"Utilisation : {cpu_usage_percent} %")

    used_ram_gb = ram['used_gb']
    total_ram_gb = ram['total_gb']
    used_ram_percent = ram['usage_percent']
    print("\n=== RAM ===")
    print(f"Utilisée : {used_ram_gb:.2f} GB")
    print(f"Totale : {total_ram_gb:.2f} GB")
    print(f"Pourcentage : {used_ram_percent} %")

    machine_name = sysinfo['hostname']
    os_version = sysinfo['os']
    start_time = sysinfo['boot_time']
    up_time = sysinfo['uptime']
    user_count = sysinfo['users_connected']
    ip_address = sysinfo['ip_address']
    print("\n=== Système ===")
    print(f"Nom d’hôte : {machine_name}")
    print(f"OS : {os_version}")
    print(f"Démarrage : {start_time}")
    print(f"Uptime : {up_time}")
    print(f"Utilisateurs connectés : {user_count}")
    print(f"Adresse IP : {ip_address}")

    top3 = proc["top3"]
    print("\n=== Processus (Top 3 gourmands) ===")
    for p in top3:
        pid = p['pid']
        name = p['name']
        cpu_p = p['cpu_percent']
        ram_p = p['memory_percent']
        print(f"{name} (PID {pid}) - CPU {cpu_p} %, RAM {ram_p:.2f} %")

    print("\n=== Analyse fichiers ===")
    for ext, count in files["counts"].items():
        print(f"{ext} : {count} fichiers ({files['percentages'][ext]:.2f} %)")

set_variables()