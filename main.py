import random
from math import gcd


# Helper function: Fast modular exponentiation
def modular_exponentiation(base, exponent, modulus):
    """
    Calculates (base^exponent) % modulus efficiently.
    This function uses the repeated squaring method to reduce the complexity.
    Mathematical Principle:
    - Base case: (a^b) % c = ((a^b/2 % c) * (a^b/2 % c)) % c
    """
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result


# Function to display mathematical explanation
def explain_modular_exponentiation(base, exponent, modulus):
    """
    Step-by-step explanation of modular exponentiation.
    """
    result = 1
    base = base % modulus
    steps = []
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
            steps.append(f"result = (result * base) % modulus = {result}")
        exponent = exponent // 2
        base = (base * base) % modulus
        steps.append(f"base = (base * base) % modulus = {base}, exponent = {exponent}")
    return steps


# Miller-Rabin primality test
def is_prime(n, k=5):
    """
    Checks primality using the Miller-Rabin test with k iterations.
    Mathematical Principle:
    - Primality test based on Fermat's Little Theorem.
    - Decomposes n-1 into 2^r * d and checks for non-trivial roots of unity.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Test for compositeness
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = modular_exponentiation(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = modular_exponentiation(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Generate a large prime number
def generate_prime(bits):
    """
    Generates a prime number of the specified bit size.
    Uses the Miller-Rabin test to ensure primality.
    """
    while True:
        candidate = random.getrandbits(bits)
        if is_prime(candidate):
            return candidate


# Extended Euclidean Algorithm
def extended_gcd(a, b):
    """
    Returns gcd(a, b) and coefficients x, y such that ax + by = gcd(a, b).
    Mathematical Principle:
    - Uses the Euclidean Algorithm to compute the greatest common divisor.
    - Back-substitutes to find coefficients.
    """
    if b == 0:
        return a, 1, 0
    gcd_, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd_, x, y


# Function to explain the extended Euclidean algorithm
def explain_extended_gcd(a, b):
    """
    Step-by-step explanation of the extended Euclidean algorithm.
    """
    steps = []
    if b == 0:
        steps.append(f"Base case: gcd({a}, {b}) = {a}")
        return a, 1, 0, steps
    gcd_, x1, y1, sub_steps = explain_extended_gcd(b, a % b)
    steps.extend(sub_steps)
    x = y1
    y = x1 - (a // b) * y1
    steps.append(f"gcd({a}, {b}): x = {x}, y = {y}")
    return gcd_, x, y, steps


# Generate RSA keys
def generate_rsa_keys(bits=1024):
    """
    Generates public and private RSA keys.
    Mathematical Principle:
    - Selects two large primes p and q.
    - Computes n = p * q and phi = (p-1)(q-1).
    - Chooses e such that gcd(e, phi) = 1 and computes d such that (e * d) % phi = 1.
    """
    print("Generating primes...")
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    print("Calculating public and private keys...")
    while True:
        e = random.randint(2, phi - 1)
        if gcd(e, phi) == 1:
            break

    _, d, _, steps = explain_extended_gcd(e, phi)
    d = d % phi
    if d < 0:
        d += phi

    print("Steps for calculating private key:")
    for step in steps:
        print(step)

    return (e, n), (d, n)


# RSA Encryption
def encrypt_rsa(message, public_key):
    """
    Encrypts a message using the RSA public key.
    Mathematical Principle:
    - Ciphertext = (plaintext^e) % n
    - Operates on each character of the plaintext.
    """
    e, n = public_key
    encrypted = [modular_exponentiation(ord(char), e, n) for char in message]
    return encrypted


# RSA Decryption
def decrypt_rsa(ciphertext, private_key):
    """
    Decrypts a ciphertext using the RSA private key.
    Mathematical Principle:
    - Plaintext = (ciphertext^d) % n
    - Operates on each character of the ciphertext.
    Handles errors if the decrypted value is out of the valid Unicode range.
    """
    d, n = private_key
    decrypted_chars = []
    for char in ciphertext:
        decrypted_value = modular_exponentiation(char, d, n)
        if 0 <= decrypted_value <= 1114111:  # Valid Unicode range
            decrypted_chars.append(chr(decrypted_value))
        else:
            decrypted_chars.append("?")  # Replace invalid characters with a placeholder
    return ''.join(decrypted_chars)


# Menu for user interaction
def rsa_menu():
    """
    Provides a menu for the user to choose encryption, decryption, or key generation.
    """
    public_key, private_key = None, None

    while True:
        print("\nRSA Operations Menu")
        print("1. Generate RSA Keys")
        print("2. Encrypt a Message")
        print("3. Decrypt a Message")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nGenerating RSA Keys...")
            public_key, private_key = generate_rsa_keys(bits=512)
            print(f"Public Key: {public_key}")
            print(f"Private Key: {private_key}")

        elif choice == "2":
            if not public_key:
                print("\nPlease generate keys first (Option 1).")
                continue
            message = input("Enter the message to encrypt: ")
            encrypted = encrypt_rsa(message, public_key)
            print(f"Encrypted Message: {encrypted}")

        elif choice == "3":
            if not private_key:
                print("\nPlease generate keys first (Option 1).")
                continue
            ciphertext = input("Enter the encrypted message (comma-separated numbers): ")
            ciphertext = [int(x) for x in ciphertext.split(",")]
            decrypted = decrypt_rsa(ciphertext, private_key)
            print(f"Decrypted Message: {decrypted}")

        elif choice == "4":
            print("Exiting RSA Operations. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")



# Main program
if __name__ == "__main__":
    rsa_menu()
