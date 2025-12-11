import psutil
import platform
import os
import socket
import time
import getpass
from datetime import datetime
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

# --- Fonctions de collecte ---

def get_cpu_info():
    return {
        "cores": psutil.cpu_count(logical=True),
        "frequency_mhz": psutil.cpu_freq().current,
        "usage_percent": psutil.cpu_percent(interval=1)
    }

def get_memory_info():
    ram = psutil.virtual_memory()
    return {
        "used_gb": ram.used / (1024**3),
        "total_gb": ram.total / (1024**3),
        "usage_percent": ram.percent,
        "used_bytes": ram.used,
        "total_bytes": ram.total
    }

def get_storage_info():
    mem = psutil.disk_usage(path="/")
    return {
        "used_gb": mem.used / (1024**3),
        "total_gb": mem.total / (1024**3),
        "usage_percent": mem.percent
    }

def get_system_info():
    uname = platform.uname()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = time.time() - psutil.boot_time()
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

    ip_address = "N/A"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "127.0.0.1"

    return {
        "hostname": uname.node,
        "os": f"{uname.system} {uname.release}",
        "boot_time": str(boot_time),
        "uptime": uptime,
        "users_connected": len(psutil.users()),
        "ip_address": ip_address
    }

def get_process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(1)

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top3_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:3]
    top3_ram = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:3]

    return {
        "processes": processes,
        "top3_cpu": top3_cpu,
        "top3_ram": top3_ram
    }

# --- Analyse de fichiers approfondie ---
def analyze_files(root_dir, extensions):
    file_info = defaultdict(lambda: {"count": 0, "size": 0})
    largest_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in extensions:
                filepath = os.path.join(dirpath, filename)
                try:
                    size = os.path.getsize(filepath)
                except OSError:
                    size = 0
                file_info[ext]["count"] += 1
                file_info[ext]["size"] += size

                # Top 10 fichiers les plus volumineux
                if len(largest_files) < 10:
                    largest_files.append((filepath, size))
                    largest_files.sort(key=lambda x: x[1], reverse=True)
                else:
                    if size > largest_files[-1][1]:
                        largest_files[-1] = (filepath, size)
                        largest_files.sort(key=lambda x: x[1], reverse=True)

    total_files = sum(info["count"] for info in file_info.values())
    percentages = {ext: (info["count"] / total_files * 100) if total_files > 0 else 0
                   for ext, info in file_info.items()}

    return file_info, largest_files, percentages, root_dir

def get_load_average():
    load1, load5, load15 = os.getloadavg()
    load1 = load1 / psutil.cpu_count(logical=True) * 100
    load5 = load5 / psutil.cpu_count(logical=True) * 100
    load15 = load15 / psutil.cpu_count(logical=True) * 100
    return load1, load5, load15

# --- Création du dictionnaire de variables ---
def set_variables():
    cpu = get_cpu_info()
    ram = get_memory_info()
    storage = get_storage_info()
    sysinfo = get_system_info()
    proc = get_process_info()

    # Extensions suivies (10+)
    extensions = ['.txt', '.py', '.pdf', '.jpg', '.png', '.docx', '.xlsx', '.csv', '.log', '.json', '.html', '.mp3', '.mp4']
    files_info, largest_files, percentages, analysed_dir = analyze_files("/home/" + getpass.getuser() + "/Documents", extensions)
    loads = get_load_average()

    return {
        "date_test": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_hearts": cpu['cores'],
        "cpu_frequency": cpu['frequency_mhz'],
        "cpu_usage_percent": cpu['usage_percent'],
        "used_ram_gb": ram['used_gb'],
        "total_ram_gb": ram['total_gb'],
        "used_ram_percent": ram['usage_percent'],
        "used_ram_bytes": ram['used_bytes'],
        "total_ram_bytes": ram['total_bytes'],
        "used_storage_gb": storage['used_gb'],
        "total_storage_gb": storage['total_gb'],
        "used_storage_percent": storage['usage_percent'],
        "machine_name": sysinfo['hostname'],
        "os_version": sysinfo['os'],
        "start_time": sysinfo['boot_time'],
        "up_time": sysinfo['uptime'],
        "user_count": sysinfo['users_connected'],
        "ip_address": sysinfo['ip_address'],
        "processes": proc["processes"],
        "top3_cpu": proc["top3_cpu"],
        "top3_ram": proc["top3_ram"],
        "file_info": files_info,
        "file_percentages": percentages,
        "largest_files": largest_files[:5],
        "analysed_directory": analysed_dir,
        "load1": loads[0],
        "load5": loads[1],
        "load15": loads[2]
    }

# --- Génération Dashboard ---
def generate_dashboard(variables, output_path, template_path="template.html"):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    html = template.render(**variables)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    while True:
        variables = set_variables()
        generate_dashboard(variables, output_path="index.html")
        generate_dashboard(variables, output_path="/var/www/html/index.html")
        print("Dashboard mis à jour :", variables["date_test"])
        time.sleep(30)