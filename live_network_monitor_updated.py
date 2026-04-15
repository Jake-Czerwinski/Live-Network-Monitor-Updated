import subprocess
import time
from datetime import datetime

def ping(ip_address):
    try:
        # Execute ping command
        result = subprocess.run(['ping', '-n', '1', 'w', '200', ip_address],
                                stdout=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except:
        return False

def scan_network(base_ip):
    active_devices = set()

    for i in range(45, 60):
        ip_address = f"{base_ip}.{i}"
        if ping(ip_address):
            active_devices.add(ip_address)
    return active_devices

def monitor_network(base_ip):
    known_devices = set()

    print('== Network Monitor ==')

    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{timestamp}] Scanning network...\n')

        current_scan = scan_network(base_ip)

        new_devices = current_scan - known_devices

        if new_devices:
            for device in sorted(new_devices):
                print(f'[ALERT] New device detected: {device}')
        else:
            print(' [OK] No new devices detected.')

        print(f'Known device count: {len(current_scan)}')
        print('-' * 40)

        known_devices.update(current_scan)
        time.sleep(10)

def main():
    base_ip = '192.168.1'
    monitor_network(base_ip)

if __name__ == "__main__":
    main()