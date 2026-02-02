import pyshark
from threading import Thread, Lock
from ipaddress import ip_address, IPv6Address
import time
import os

packets = []
dns_leaks = []
ipv6_leaks = []
lock = Lock()

EXPECTED_INTERFACE = "tun0"

def wait_for_tun():
    """Wait until tun0 exists before capturing."""
    while not os.path.exists("/sys/class/net/tun0"):
        time.sleep(1)
    time.sleep(1)  # Give it time to initialize


def capture_packets():
    wait_for_tun()

    # Correct: capture ALL VPN traffic
    cap_all = pyshark.LiveCapture(interface="tun0")

    for pkt in cap_all:
        try:
            src = pkt.ip.src if hasattr(pkt, "ip") else "N/A"
            dst = pkt.ip.dst if hasattr(pkt, "ip") else "N/A"
            proto = pkt.highest_layer
            length = pkt.length

            info = {"src": src, "dst": dst, "proto": proto, "length": length}

            with lock:
                packets.append(info)
                if len(packets) > 200:
                    packets.pop(0)

        except Exception:
            continue


def capture_dns():
    wait_for_tun()

    # Correct: capture DNS only on tun0 (inside VPN)
    cap_dns = pyshark.LiveCapture(interface="tun0", display_filter="dns")

    for pkt in cap_dns:
        try:
            src = pkt.ip.src if hasattr(pkt, "ip") else "N/A"
            dst = pkt.ip.dst if hasattr(pkt, "ip") else "N/A"
            iface = EXPECTED_INTERFACE

            with lock:
                dns_leaks.append({"src": src, "dst": dst, "iface": iface})
                if len(dns_leaks) > 20:
                    dns_leaks.pop(0)

        except:
            continue


def capture_ipv6():
    wait_for_tun()

    # IPv6 capture ONLY on tun0
    cap6 = pyshark.LiveCapture(interface="tun0", display_filter="ip.version == 6")

    for pkt in cap6:
        try:
            src = pkt.ipv6.src
            dst = pkt.ipv6.dst

            info = {"src": src, "dst": dst, "iface": EXPECTED_INTERFACE}

            with lock:
                ipv6_leaks.append(info)
                if len(ipv6_leaks) > 50:
                    ipv6_leaks.pop(0)

        except:
            continue


def start_capture():
    Thread(target=capture_packets, daemon=True).start()
    Thread(target=capture_dns, daemon=True).start()
    Thread(target=capture_ipv6, daemon=True).start()
