import base64
import random
import string

def generate_ssh_key():
    """Generate a realistic-looking SSH private key"""
    # Generate random components
    key_length = 2048
    exponent = random.getrandbits(16)
    modulus = random.getrandbits(key_length)
    
    # Create key header
    header = "-----BEGIN RSA PRIVATE KEY-----\n"
    footer = "-----END RSA PRIVATE KEY-----"
    
    # Generate pseudo key content
    key_data = base64.b64encode(str(modulus).encode()).decode()
    key_content = '\n'.join(key_data[i:i+64] for i in range(0, len(key_data), 64))
    
    return f"{header}{key_content}\n{footer}"

def generate_key_fingerprint():
    """Generate an SSH key fingerprint"""
    chars = string.hexdigits[:16]
    return ':'.join(''.join(random.choice(chars) for _ in range(2)) for _ in range(16))
