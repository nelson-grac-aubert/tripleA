import psutil
import platform
import os
import socket
import time
import getpass
from datetime import datetime

# Fonctions de collecte

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

def get_file_analysis(path):
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
        "percentages": percentages,
        "directory": path
    }

def get_load_average() : 
    load1, load5, load15 = os.getloadavg()
    return load1, load5, load15

# Création du dictionnaire de variables

def set_variables():
    cpu = get_cpu_info()
    ram = get_memory_info()
    storage = get_storage_info()
    sysinfo = get_system_info()
    proc = get_process_info()
    files = get_file_analysis("/home/" + getpass.getuser() + "/Documents")

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
        "file_counts": files["counts"],
        "file_total": files["total"],
        "file_percentages": files["percentages"],
        "analysed_directory": files["directory"]
    }

# Génération Dashboard 

def generate_dashboard(variables, template_path="template.html", output_path="index.html"):
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

# Remplacements simples
    html = html.replace("{{date_test}}", variables["date_test"])
    html = html.replace("{{machine_name_placeholder}}", variables["machine_name"])
    html = html.replace("{{operating_system_placeholder}}", variables["os_version"])
    html = html.replace("{{start_time_placeholder}}", variables["start_time"])
    html = html.replace("{{up_time_placeholder}}", variables["up_time"])
    html = html.replace("{{user_count_placeholder}}", str(variables["user_count"]))
    html = html.replace("{{cpu_heart_count_placeholder}}", str(variables["cpu_hearts"]))
    html = html.replace("{{cpu_frequency_placeholder}}", f"{variables['cpu_frequency']:.2f}")
    html = html.replace("{{cpu_usage_percent_placeholder}}", f"{variables['cpu_usage_percent']}")
    html = html.replace("{{total_ram_gb_placeholder}}", f"{variables['total_ram_gb']:.2f}")
    html = html.replace("{{used_ram_gb_placeholder}}", f"{variables['used_ram_gb']:.2f}")
    html = html.replace("{{used_ram_percent_placeholder}}", f"{variables['used_ram_percent']}")
    html = html.replace("{{ip_address_placeholder}}", variables["ip_address"])
    html = html.replace("{{analysed_directory_placeholder}}", variables["analysed_directory"])

# Top 3 CPU
    for i in range(3):
        proc = variables['top3_cpu'][i]
        html = html.replace(f"{{{{most_demanding_processus_{i+1}_placeholder}}}}",
                            f"{proc['name']} (PID {proc['pid']})")
        html = html.replace(f"{{{{processus{i+1}_cpu_usage_percent_placeholder}}}}",
                            f"{proc['cpu_percent']}")
        html = html.replace(f"{{{{processus{i+1}_ram_usage_bytes_placeholder}}}}",
                            f"{proc['memory_percent']:.2f}")

# Fichiers
    html = html.replace("{{number_txt_placholder}}", str(variables["file_counts"][".txt"]))
    html = html.replace("{{percent_txt_placholder}}", f"{variables['file_percentages']['.txt']:.2f}")
    html = html.replace("{{number_py_placholder}}", str(variables["file_counts"][".py"]))
    html = html.replace("{{percent_py_placholder}}", f"{variables['file_percentages']['.py']:.2f}")
    html = html.replace("{{number_pdf_placholder}}", str(variables["file_counts"][".pdf"]))
    html = html.replace("{{percent_pdf_placholder}}", f"{variables['file_percentages']['.pdf']:.2f}")
    html = html.replace("{{number_jpg_placholder}}", str(variables["file_counts"][".jpg"]))
    html = html.replace("{{percent_jpg_placholder}}", f"{variables['file_percentages']['.jpg']:.2f}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def print_variables(variables):
    print("CPU")
    print(f"Cœurs : {variables['cpu_hearts']}")
    print(f"Fréquence : {variables['cpu_frequency']:.2f} MHz")
    print(f"Utilisation : {variables['cpu_usage_percent']}")

    print("\nRAM")
    print(f"Totale : {variables['total_ram_gb']:.2f} GB ({variables['total_ram_bytes']} bytes)")
    print(f"Utilisée : {variables['used_ram_gb']:.2f} GB ({variables['used_ram_bytes']} bytes)")
    print(f"Pourcentage : {variables['used_ram_percent']}")

    print("\nStockage")
    print(f"Totale : {variables['total_storage_gb']:.2f} GB")
    print(f"Utilisée : {variables['used_storage_gb']:.2f} GB")
    print(f"Pourcentage : {variables['used_storage_percent']}")

    print("\nSystème")
    print(f"Nom d’hôte : {variables['machine_name']}")
    print(f"OS : {variables['os_version']}")
    print(f"Démarrage : {variables['start_time']}")
    print(f"Uptime : {variables['up_time']}")
    print(f"Utilisateurs connectés : {variables['user_count']}")
    print(f"Adresse IP : {variables['ip_address']}")

    print("\nTop 3 CPU")
    for i, p in enumerate(variables['top3_cpu'], start=1):
        print(f"{i}. {p['name']} (PID {p['pid']}) - CPU {p['cpu_percent']} %")

    print("\nTop 3 RAM")
    for i, p in enumerate(variables['top3_ram'], start=1):
        print(f"{i}. {p['name']} (PID {p['pid']}) - RAM {p['memory_percent']:.2f} %")

    print("\nAnalyse fichiers")
    print(f"Dossier analysé : {variables['analysed_directory']}")
    for ext, count in variables['file_counts'].items():
        print(f"{ext} : {count} fichiers ({variables['file_percentages'][ext]:.2f} %)")

# Main

if __name__ == "__main__" :
    variables = set_variables()
    print_variables(variables)
    generate_dashboard(variables)