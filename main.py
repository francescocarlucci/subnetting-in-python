import re
import sys
from builtins import input # python 2 compatibility

max_bits = 32 # because it's IPv4

def validate_ip(ip):

    pattern = re.compile("^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))$")

    is_valid = pattern.match(str(ip))

    return bool(is_valid)

def binary_to_decimal_octets(binary_address):

    binary_address = list(map(''.join, zip(*[iter(binary_address)]*8)))

    octets = []

    for octet in binary_address:
        octets.append(str(int(octet, 2)))

    decimal_address = '.'.join(octets)

    return decimal_address

def destructure_ip(ip):

    ip = ip.split('/')

    destructured_ip = {
        'ip': ip[0],
        'network_bits': ip[1]
    }

    binary_ip = []

    for ip_part in ip[0].split('.'):
        binary_ip.append(bin(int(ip_part)).replace('0b','').zfill(8))

    destructured_ip['binary_ip'] = '.'.join(binary_ip)

    destructured_ip['binary_ip_clean'] = ''.join(binary_ip) # no dots

    return destructured_ip

def get_hosts(network_bits):

    host_bits = max_bits - int(network_bits)

    hosts = pow(2, host_bits)

    hosts -= 2 # remove network id and broadcast

    return hosts

def get_network_mask(network_bits):

    network_bits = int(network_bits)

    network_mask = ''

    for i in range(0, network_bits):
        network_mask += '1'

    for i in range(network_bits, max_bits):
        network_mask += '0'

    network_mask = binary_to_decimal_octets(network_mask)

    return network_mask

def get_network_or_broadcast(binary_ip, network_bits, output):

    network_bits = int(network_bits)

    if output == 'network_id':
        fill = '0'
    elif output == 'broadcast':
        fill = '1'
    else:
        return

    address = binary_ip[0:network_bits].ljust(32, fill)

    address = binary_to_decimal_octets(address)

    return address

def main():

    # check if there is an IP as cli arg
    if len(sys.argv) > 1:
        ip = sys.argv[1] # 192.168.0.0/24
    else:
        ip = input("Enter an IPv4 in CIDR notation: ")

    if validate_ip(ip):

        ip_parts = destructure_ip(ip)

        dot_decimal_ip = ip_parts['ip']

        binary_ip = ip_parts['binary_ip']
        binary_ip_clean = ip_parts['binary_ip_clean']

        network_bits = ip_parts['network_bits']

        hosts = get_hosts(network_bits)

        network_mask = get_network_mask(network_bits)

        network_id = get_network_or_broadcast(binary_ip_clean,network_bits,'network_id')

        broadcast = get_network_or_broadcast(binary_ip_clean,network_bits,'broadcast')

        print('-'*50)
        print(f'IP: {ip}')
        print('-'*50)
        print(f'Binary IP: {binary_ip}')
        print('-'*50)
        print(f'Hosts: {hosts}')
        print('-'*50)
        print(f'Network Mask: {network_mask}')
        print('-'*50)
        print(f'Network ID: {network_id}')
        print('-'*50)
        print(f'Broadcast Address: {broadcast}')
        print('-'*50)

    else :

        print(f'IP: {ip} is invalid.')

if __name__ == '__main__':
    main()
