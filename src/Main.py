import json
import git_commit

from shodan import Shodan
from colorama import Fore, init

def read_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def check_dupe(ip_port, dupe_set):
    return ip_port in dupe_set

def get_existing_ips(IP_file):
    existing_ips = set()
    with open(IP_file, "r", encoding="utf-8") as honeypot_list:
        for line in honeypot_list:
            existing_ips.add(line.strip())
    return existing_ips

def get_updated_list(api_key, IP_file):
    api = Shodan(api_key)
    total_new_ips = 0

    try:
        existing_ips = get_existing_ips(IP_file)
        
        with open(IP_file, "a", encoding="utf-8") as log_ip:
            for banner in api.search_cursor('honeypot'):
                ip = banner.get('ip_str', 'N/A')
                port = banner.get('port', 'N/A')
                ip_port = f'{ip}:{port}'
                
                if check_dupe(ip_port, existing_ips):
                    print(f"{Fore.RED}[DUPE]{Fore.RESET} {ip_port}")
                else:
                    log_line = f'{ip_port}\n'
                    print(f"{Fore.GREEN}[NEW] {Fore.RESET} {ip_port}")
                    total_new_ips += 1
                    log_ip.write(log_line)
                    existing_ips.add(ip_port)
    
        return total_new_ips
                    

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    config_file_path = 'config.json'
    config = read_config(config_file_path)
    api_key = config.get('Shodan_API_key')
    IP_file = config.get('IP_file')
    
    # new_ips = get_updated_list(api_key, IP_file)
    new_ips = 1425
    git_commit.UPLOAD(new_ips)

