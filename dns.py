import socketpool
import select
import asyncio
import wifi
import gc



class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.domain = ''
        self.parse_query()

    def parse_query(self):
        domain_parts = []
        state = 0
        expected_length = 0
        for byte in self.data[12:]:
            if state == 1:
                domain_parts.append(chr(byte))
                expected_length -= 1
                if expected_length == 0:
                    state = 0
                    domain_parts.append('.')
            else:
                if byte == 0:
                    break
                state = 1
                expected_length = byte
        if domain_parts:
            self.domain = ''.join(domain_parts[:-1])

    def response(self, ip):
        packet = self.data[:2] + b'\x81\x80' # Transaction ID and flags
        packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00' # Questions and Answers
        packet += self.data[12:] # Original domain query
        packet += b'\xc0\x0c' # Pointer to domain name
        packet += b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04' # Type A response with TTL of 60 seconds
        packet += bytes(map(int, ip.split('.'))) # IP address
        return packet

async def run_dns_server(SERVER_IP):
    pool = socketpool.SocketPool(wifi.radio)

    # Create a new UDP socket
    udps = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
    udps.settimeout(0)  # Non-blocking socket

    # Bind to port 53 on all interfaces
    udps.bind(('0.0.0.0', 53))

    print("DNS Server started on port 53")

    while True:
        try:
            gc.collect()

            data = bytearray(128)
            ready = select.select([udps], [], [], 1)  # 1 second timeout
            if ready[0]:
                num_bytes, addr = udps.recvfrom_into(data)
                print("Incoming data...")
                if num_bytes > 0:
                    query = DNSQuery(data[:num_bytes])

                    dnsResponse = query.response(SERVER_IP)
                    udps.sendto(dnsResponse, addr)
                
                print("Replying: {:s} -> {:s}".format(query.domain, SERVER_IP))

            await asyncio.sleep(0.1)

        except Exception as e:
            print("Exception: ", e)
            await asyncio.sleep(3)

    udps.close()