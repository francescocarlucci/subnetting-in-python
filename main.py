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
        'network_bits': ip[1]
    }

    binary_ip = []

    for ip_part in ip[0].split('.'):
        binary_ip.append(bin(int(ip_part)).replace('0b','').zfill(8))

    destructured_ip['binary_ip'] = '.'.join(binary_ip)
    
    destructured_ip['binary_ip_no_separator'] = ''.join(binary_ip)

    return destructured_ip

def get_hosts(network_bits):

    host_bits = max_bits - int(network_bits)

    return pow(2, host_bits)

def get_network_mask(network_bits):

    network_bits = int(network_bits)

    network_mask = ''

    for i in range(0, network_bits):
        network_mask += '1'

    for i in range(network_bits, max_bits):
        network_mask += '0'

    network_mask = list(map(''.join, zip(*[iter(network_mask)]*8)))

    network_mask_bin = []
    network_mask_dec = []

    for mask_part in network_mask:
        network_mask_bin.append(str(mask_part))
        network_mask_dec.append(str(int(mask_part, 2)))

    network_mask = [ '.'.join(network_mask_dec), '.'.join(network_mask_bin) ]

    return network_mask

def main():

    ip = input("Enter an IPv4 in CIDR notation: ")
    #ip = '192.168.0.0/24'

    if validate_ip(ip):

        ip_parts = destructure_ip(ip)

        dot_decimal_ip = ip_parts['ip']

        binary_ip = ip_parts['binary_ip']

        network_bits = ip_parts['network_bits']

        hosts = get_hosts(network_bits)

        network_mask = get_network_mask(network_bits)
        network_mask = network_mask[0] # 0 is dec, 1 is bin

        print('-'*50)
        print(f'IP: {dot_decimal_ip}')
        print('-'*50)
        print(f'Binary IP: {binary_ip}')
        print('-'*50)
        print(f'Hosts: {hosts}')
        print('-'*50)
        print(f'Network Mask: {network_mask}')
        print('-'*50)

    else :

        print(f'IP: {ip} is invalid.')

if __name__ == '__main__':
    main()
