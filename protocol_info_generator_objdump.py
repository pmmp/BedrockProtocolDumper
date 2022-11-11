import subprocess
import re
import struct
from version import Version
from protocol_info_generator import generate_stuff
import sys
import os
import threading

if len(sys.argv) < 3:
    exit("Required args: BDS binary path, path to BedrockProtocol")

def convert_windows_path(path):
    return path.replace('\\', '/').replace('C:', '/mnt/c')

def valid_paths(list_of_paths):
    return all(os.path.exists(path) for path in list_of_paths)


bds_path = convert_windows_path(sys.argv[1]) if os.name == 'nt' else sys.argv[1]
bedrockprotocol_path = convert_windows_path(sys.argv[2]) if os.name == 'nt' else sys.argv[2] 
if not valid_paths([bds_path, bedrockprotocol_path]):
    raise Exception(f"Invalid arguments provided:{sys.argv[1:3]} check that the paths are correct")
print(f'Dumping data from: {bedrockprotocol_path}')
print(f'BedrockProtocol path: {bds_path}')

asm_regex = re.compile(r'.*\$(0x[A-Fa-f\d]+),%eax.*')
symbol_match_regex = re.compile(r'([\da-zA-Z]+) (.{7}) (\.[A-Za-z\d_]+)\s+([\da-zA-Z]+)\s+(?:Base)?\s+(.+)')
rodata_offset_regex = re.compile(r"^\s*\d+\s+\.rodata\s+[\da-f]+\s+[\da-f]+\s+([\da-f]+)\s+([\da-f]+)")

def get_value_at(file, offset, size, format):
    file = open(file, 'rb')
    if offset == None or offset < 0:
        return -1
    file.seek(offset)
    return struct.unpack(format, file.read(size))[0]

def stop_address(start, size):
    return hex(int('0x' + start, 16) + int('0x' + size, 16))

def dump_packet_id(start, size, symbol):
    proc = subprocess.Popen(['objdump', '--disassemble', '--demangle', '--section=.text', '--start-address=0x' + start, '--stop-address=' + stop_address(start, size), bds_path], stdout=subprocess.PIPE)
    lines = []
    while True:
        line = proc.stdout.readline()
        lines.append(line)
        if not line:
            break
        parts = line.split(b'mov')
        if len(parts) < 2:
            continue
        matches = re.match(asm_regex, parts[1].decode())
        if not matches:
            continue
        return int(matches.groups()[0], 16)
    for l in lines:
        print(l)
    raise Exception("Packet ID not found for symbol " + symbol)

def dump_packet_id_threaded(start, size, symbol, packet_name, packets, packets_lock):
    id = dump_packet_id(start, size, symbol)
    packets_lock.acquire()
    packets[id] = packet_name
    print('Found ' + packet_name + ' ' + hex(id))
    packets_lock.release()

def parse_symbol(symbol):
    parts = re.match(symbol_match_regex, symbol.decode())
    if not parts:
        raise Exception("Regex match failed for \"" + symbol + "\"")
    if len(parts.groups()) < 5:
        raise Exception("Wrong number of matches for \"" + symbol + "\" " + str(len(parts.groups())))
    start = parts.groups()[0]
    flags = parts.groups()[1]
    section = parts.groups()[2]
    size = parts.groups()[3]
    symbol = parts.groups()[4]
    return start, flags, section, size, symbol

def dump_packet_ids():
    packets = {}
    packets_lock = threading.Lock()
    threads = [None] * 8
    proc = subprocess.Popen(['objdump --demangle -tT --dwarf=follow-links \'' + bds_path + '\' | grep Packet | grep \'::getId()\''], shell=True, stdout=subprocess.PIPE)
    while True:
        symbol = proc.stdout.readline()
        if not symbol:
            break
        start, _, _, size, symbol = parse_symbol(symbol)
        packet_name = symbol.split('::')[0]
        thread_index = None
        for i in range(len(threads)):
            if threads[i] is None:
                thread_index = i
                break
        while thread_index is None:
            for i in range(len(threads)):
                threads[i].join(0.1)
                if not threads[i].is_alive():
                    thread_index = i
                    threads[i] = None
                    break

        t = threading.Thread(target=dump_packet_id_threaded, args=(start, size, symbol, packet_name, packets, packets_lock))
        t.start()
        threads[i] = t
    for t in threads:
        t.join()
    return packets

def get_rodata_file_shift():
    proc = subprocess.Popen(['objdump -h -j \'.rodata\' \'' + bds_path + '\''], shell=True, stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        matches = re.match(rodata_offset_regex, line.strip().decode())
        if matches:
            lma = int('0x' + matches.groups()[0], 16)
            physical_address = int('0x' + matches.groups()[1], 16)
            return physical_address - lma
    raise Exception("Unable to calculate offset for .rodata")

def dump_version():
    rodata_shift = get_rodata_file_shift()
    proc = subprocess.Popen(['objdump --demangle -tT --dwarf=follow-links \'' + bds_path + '\' | grep SharedConstants'], shell=True, stdout=subprocess.PIPE)
    major = None
    minor = None
    patch = None
    revision = None
    beta = False
    protocol = None
    while True:
        symbol = proc.stdout.readline()
        if not symbol:
            break
        start, _, _, size, symbol = parse_symbol(symbol)
        if 'MajorVersion' in symbol:
            major = get_value_at(bds_path, int('0x' + start, 16) + rodata_shift, int('0x' + size, 16), 'i')
        elif 'MinorVersion' in symbol:
            minor = get_value_at(bds_path, int('0x' + start, 16) + rodata_shift, int('0x' + size, 16), 'i')
        elif 'PatchVersion' in symbol:
            patch = get_value_at(bds_path, int('0x' + start, 16) + rodata_shift, int('0x' + size, 16), 'i')
        elif 'RevisionVersion' in symbol:
            revision = get_value_at(bds_path, int('0x' + start, 16) + rodata_shift, int('0x' + size, 16), 'i')
        elif 'IsBeta' in symbol:
            beta = get_value_at(bds_path, int('0x' + start, 16) + rodata_shift, int('0x' + size, 16), 'B') == 1
        elif 'NetworkProtocolVersion' in symbol:
            protocol = get_value_at(bds_path, int('0x' + start, 16) + rodata_shift, int('0x' + size, 16), 'i')

    print(major, minor, patch, revision, beta, protocol)
    return Version(major, minor, patch, revision, beta, protocol)

if __name__ == "__main__":
    version = dump_version()
    packets = dump_packet_ids()
    generate_stuff(packets, version, bedrockprotocol_path)
