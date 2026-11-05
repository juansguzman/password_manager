

Checkpoint 2, core requirements implemented (Week 9) - Password Manager

Deliverables. Working code in the repository that a reviewer can build and run, plus a 
short progress note. 

• Basic vault storage working. 

• Simple credentials encrypted at rest using the chosen scheme. 

• Master password authentication implemented. The vault unlocks only on successful 
verification. 

• A usable interface that never prints passwords in cleartext. 

• Build and run instructions that work on a clean machine, and a commit history 
showing incremental progress. 

# Checkpoint 2 (Week 9) - Password Manager

## Progress Note
For this checkpoint, the core cryptographic and authentication requirements for the Password Manager have been successfully implemented:
- **Basic vault storage:** Data is securely persisted locally using a `vault.enc` file.
- **Encrypted at rest:** The vault is encrypted using `AES-GCM` (Authenticated Encryption with Associated Data).
- **Master password authentication:** The vault relies on a Zero-Knowledge architecture. The master password is never stored; instead, `Argon2id` is used to derive a 256-bit key from the password and a randomly generated salt (`salt.bin`). The vault only unlocks if the derived key can successfully decrypt the AES-GCM ciphertext.
- **Secure Interface:** The command-line interface utilizes the Python `getpass` module, ensuring that neither the master password nor the stored credentials are ever printed in cleartext on the terminal during input.

## Build and Run Instructions (Clean Machine)

**Prerequisites:** 
- Python 3.9 or higher.

**1. Clone the repository and set up the environment:**
```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install required cryptographic libraries
pip install argon2-cffi cryptography