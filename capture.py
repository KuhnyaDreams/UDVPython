import subprocess
import time
from datetime import datetime
import os

OUTPUT_DIR = "capture/"
INTERFACE = "enp4s0"
CAPTURE_DURATION = 3600
TCPDUMP_PATH = "/usr/bin/tcpdump"

# Исключаем TLS трафик по сигнатурам записей TLS (без портов)
TCPDUMP_FILTER = (
    'tcp and not ('
    'tcp[((tcp[12] & 0xf0) >> 2):1] = 0x16 or '
    'tcp[((tcp[12] & 0xf0) >> 2):1] = 0x14 or '
    'tcp[((tcp[12] & 0xf0) >> 2):1] = 0x15 or '
    'tcp[((tcp[12] & 0xf0) >> 2):1] = 0x17'
    ')'
)

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def generate_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(OUTPUT_DIR, f"capture_{timestamp}.pcap")

def capture_traffic():
    ensure_output_dir()
    while True:
        filename = generate_filename()
        print(f"Начат захват в файл: {filename}")
        try:
            subprocess.run([
                TCPDUMP_PATH,
                "-i", INTERFACE,
                "-w", filename,
                "-G", str(CAPTURE_DURATION),
                "-W", "1",
                "-f"
            ] + TCPDUMP_FILTER.split(), check=True)
        except KeyboardInterrupt:
            print("Захват прерван пользователем.")
            break
        except Exception as e:
            print(f"Ошибка при захвате: {e}")
            time.sleep(10)

if __name__ == "__main__":
    capture_traffic()

