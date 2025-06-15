import os
import argparse
from scapy.all import rdpcap, wrpcap
from scapy.layers.l2 import Ether
from datetime import datetime

def split_by_size(packets, output_prefix, max_size_mb):
    file_index = 1
    current_packets = []
    current_size = 0

    for pkt in packets:
        pkt_bytes = bytes(pkt)
        pkt_size = len(pkt_bytes)
        if (current_size + pkt_size) > (max_size_mb * 1024 * 1024):
            wrpcap(f"{output_prefix}_{file_index}.pcap", current_packets)
            print(f"Written {output_prefix}_{file_index}.pcap with {len(current_packets)} packets")
            file_index += 1
            current_packets = []
            current_size = 0
        current_packets.append(pkt)
        current_size += pkt_size

    if current_packets:
        wrpcap(f"{output_prefix}_{file_index}.pcap", current_packets)
        print(f"Written {output_prefix}_{file_index}.pcap with {len(current_packets)} packets")


def split_by_packets(packets, output_prefix, max_packets):
    file_index = 1
    for i in range(0, len(packets), max_packets):
        chunk = packets[i:i+max_packets]
        wrpcap(f"{output_prefix}_{file_index}.pcap", chunk)
        print(f"Written {output_prefix}_{file_index}.pcap with {len(chunk)} packets")
        file_index += 1


def split_by_time(packets, output_prefix, interval_sec):
    file_index = 1
    current_packets = []
    start_time = None

    for pkt in packets:
        pkt_time = pkt.time
        if start_time is None:
            start_time = pkt_time

        if pkt_time - start_time >= interval_sec:
            wrpcap(f"{output_prefix}_{file_index}.pcap", current_packets)
            print(f"Written {output_prefix}_{file_index}.pcap with {len(current_packets)} packets")
            file_index += 1
            current_packets = []
            start_time = pkt_time

        current_packets.append(pkt)

    if current_packets:
        wrpcap(f"{output_prefix}_{file_index}.pcap", current_packets)
        print(f"Written {output_prefix}_{file_index}.pcap with {len(current_packets)} packets")


def main():
    parser = argparse.ArgumentParser(description="Split PCAP file by size, packet count, or time.")
    parser.add_argument("input", help="Input PCAP file")
    parser.add_argument("output_prefix", help="Output file prefix (e.g., out -> out_1.pcap)")
    parser.add_argument("--mode", choices=["size", "packets", "time"], required=True, help="Split mode")
    parser.add_argument("--value", type=int, required=True, help="Value for the chosen mode (MB, packet count, or seconds)")

    args = parser.parse_args()

    print(f"Reading packets from {args.input}...")
    packets = rdpcap(args.input)

    if args.mode == "size":
        split_by_size(packets, args.output_prefix, args.value)
    elif args.mode == "packets":
        split_by_packets(packets, args.output_prefix, args.value)
    elif args.mode == "time":
        split_by_time(packets, args.output_prefix, args.value)
    else:
        print("Unknown mode.")

if __name__ == "__main__":
    main()

