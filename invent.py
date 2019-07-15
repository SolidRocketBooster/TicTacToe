import os, platform, psutil, netifaces, argparse, json, yaml

parser = argparse.ArgumentParser()
parser.add_argument('format', type=str, choices=['yaml', 'json'])
parser.add_argument('path', type=str)
args = parser.parse_args()


def os_info():
    info = {}
    uptime = os.popen('uptime').read().split(" ")[1]
    info["uptime"] = uptime
    proc = [proc for proc in psutil.process_iter()]
    info["of_proc"] = len(proc)
    zombie = [proc for proc in psutil.process_iter() if proc.status() == psutil.STATUS_ZOMBIE]
    info["of_zombies"] = len(zombie)
    info["linux"] = platform.platform()
    info["kernel"] = platform.version()
    vim_ver = os.popen('vim --version').read().split("\n")[0]
    ssh_ver = os.popen('dpkg -l | grep openssh-server').read().split(" ")[25]
    info["soft"] = {"python": platform.python_version(), "vim": vim_ver, "ssh": ssh_ver}
    return info

def ram_info():
    info = {}
    info["memory"] = psutil.virtual_memory().total
    return info

def cpu_info():
    info = {}
    info["model"] = os.popen('lscpu | grep "Model name:"').read()[21:][:-1]
    info["of_cpu"] = os.popen('lscpu | grep -m 1 "CPU(s):"').read()[21:][:-1]
    info["frequency"] = os.popen('lscpu | grep "CPU MHz:"').read()[21:][:-1]
    info["virtualization"] = os.popen('lscpu | grep "Virtualization type:"').read()[21:][:-1]
    return info

def hdd_info():
    info = {}
    info["of_hdds"] = os.popen('df -h | grep sda | wc -l').read()[:-1]
    info["hdds"] = os.popen('df -h | grep sda').read()
    return info

def net_info():
    info = {}
    info["nics"] = { inf: netifaces.ifaddresses(inf) for inf in netifaces.interfaces()}
    info["gateways"] = netifaces.gateways()
    info["dns"] = os.popen('resolvectl dns').read().split("\n")[1:][:-1]
    return info

def make_json():
    payload = {"os_info": os_info(), "memory_info": ram_info(), "cpu_info": cpu_info(), "hdd_info": hdd_info(), "net_info": net_info()}
    json_format = json.dumps(payload, indent=4)
    return json_format

def make_yaml():
    payload = [os_info(), ram_info(), cpu_info(), hdd_info(), net_info()]
    yaml_format = yaml.dump(payload, indent=4)
    return yaml_format

system = os_info()
print(f'''
System {system["linux"]} on {system["kernel"]} for {system["uptime"]}
Processes running: {system["of_proc"]}/ Zombie Process: {system["of_zombies"]}
Python version: {system["soft"]["python"]}
Vim version: {system["soft"]["vim"]}
SSH version: {system["soft"]["ssh"]}''')

cpu = cpu_info()
print(f'''
CPU model: {cpu["model"]}
Frequency: {cpu["frequency"]}
CPUs #: {cpu["of_cpu"]}
Virtualization: {cpu["virtualization"]}''')

ram = ram_info()
print(f'''
Total Ram: {ram["memory"]}''')

hdd = hdd_info()
print(f'''
Total HHDs #: {hdd["of_hdds"]}
{hdd["hdds"]}''')


net = net_info()
print(f'''
Information about network interfaces
{net["nics"]}

Information about Gateways
{net["gateways"]}

Information about DNSs
{net["dns"]}
''')

print("End of report")


if os.path.isdir(args.path) == True:
    file_path = os.path.join(os.path.relpath(args.path), "output." + args.format)
    with open(file_path, "w") as work_file:
        if args.format == "json":
            work_file.write(make_json())
        elif args.format == "yaml":
            work_file.write(make_yaml())
else:
    print("Wrong path")
