# RSA Encryption and Decryption: Mathematical and Code Explanation

## Introduction
The RSA algorithm is a widely used cryptographic system based on the principles of number theory. It relies on the difficulty of factorizing large composite numbers to ensure security.

---

## Mathematical Principles

### 1. Modular Exponentiation
The core of RSA involves efficient computation of:
\[
C = M^e \mod n \quad \text{and} \quad M = C^d \mod n
\]
This is achieved using the **repeated squaring method**:
- **Base Case:**
  \[
  (a^b) \mod c = ((a^{b/2} \mod c) \times (a^{b/2} \mod c)) \mod c
  \]

### 2. Primality Testing (Miller-Rabin)
To generate large primes \( p \) and \( q \), RSA uses the Miller-Rabin test:
1. Express \( n-1 \) as:
   \[
   n-1 = 2^r \cdot d
   \]
2. For a randomly chosen base \( a \), check:
   \[
   a^d \mod n = 1 \quad \text{or} \quad a^{2^j \cdot d} \mod n = n-1
   \]

### 3. Extended Euclidean Algorithm
Used to compute the modular inverse \( d \) of \( e \) modulo \( \phi(n) \):
\[
e \cdot d \equiv 1 \mod \phi(n)
\]
The algorithm solves:
\[
ax + by = \text{gcd}(a, b)
\]

---

## Code Explanation

### Modular Exponentiation
```python
def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent // 2
        base = (base * base) % modulus
    return result
