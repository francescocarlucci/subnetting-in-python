import re
from builtins import input # python 2 compatibility

max_bits = 32 # because it's IPv4

def validate_ip(ip):

    pattern = re.compile("^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))$")

    is_valid = pattern.match(str(ip))

    return bool(is_valid)

def destructure_ip(ip):

    ip = ip.split('/')

    destructured_ip = {
        'ip': ip[0],
        'bits': ip[1]
    }

    ip_key = 0

    for ip_part in ip[0].split('.'):
        destructured_ip[ip_part] = int(ip_part)
        ip_key +=1

    return destructured_ip

def get_hosts(bits):

    available_bits = 32 - int(bits)

    return pow(2, available_bits)

def get_network_mask(bits):

    bits = int(bits)

    network_mask = ''

    for i in range(0, bits):
        network_mask += '1'

    for i in range(bits, max_bits):
        network_mask += '0'

    network_mask = list(map(''.join, zip(*[iter(network_mask)]*8)))

    network_mask_32 = []

    for mask_part in network_mask:
        network_mask_32.append(str(int(mask_part, 2)))

    return '.'.join(network_mask_32)

def main():

    ip = input("Enter an IPv4 in CIDR notation: ")
    # ip = '192.168.0.0/24'

    if validate_ip(ip):

        ip_parts = destructure_ip(ip)

        bits = ip_parts['bits']

        hosts = get_hosts(bits)

        network_mask = get_network_mask(bits)

        print('-'*50)
        print(f'Available hosts: {hosts}')
        print(f'Network Mask: {network_mask}')
        print('-'*50)

    else :

        print(f'IP: {ip} is invalid.')

if __name__ == '__main__':
    main()
