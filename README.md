# Zero-Knowledge Password Manager (CLI)

## Scope
A Python-based, 100% offline password manager supporting strong master password enforcement, encrypted vault storage, and password generation. Built to mitigate common attack vectors including brute-force cracking, database extraction, and memory scraping.

## Architecture & Security Features
This application strictly adheres to a Zero-Knowledge model and includes built-in defenses against common vulnerabilities:
- **Key Derivation:** The master password is never stored. It is passed through `Argon2id` (along with a randomly generated 16-byte salt) to derive a strong 256-bit cryptographic key.
- **Data Encryption:** The vault contents are encrypted at rest using `AES-GCM` (Authenticated Encryption with Associated Data). This ensures both the confidentiality and the integrity of the stored credentials.
- **Input Security (Shoulder Surfing Protection):** The command-line interface utilizes secure input methods (`getpass`) to prevent passwords from lingering in terminal history or being printed in cleartext.
- **Memory & Injection Protection:** Built on Python, the application dynamically manages memory allocation, inherently preventing **Buffer Overflow** attacks. Furthermore, the use of strict `json` parsing and sanitized inputs prevents **Code/Command Injection**.
- **Brute Force Mitigation:** The authentication flow includes a hardcoded maximum attempt limit (3 tries) before forcefully terminating the execution to slow down local brute-force attacks.

## System Use Cases & Commands
- `init`: Setup a new vault and enforce a strong master password (UC-002).
- `login`: Authenticate into the manager (UC-001).
- `add`: Store a new encrypted password entry (UC-004).
- `ver`: View stored credentials after authentication (UC-005).
- `exit`: Securely close the vault and terminate the program.

*(Note: Features like MFA, update, and generate are slated for future milestones).*

## Build and Run Instructions

**1. Clone the repository:** 
```bash
git clone [https://github.com/juansguzman/password_manager.git](https://github.com/juansguzman/password_manager.git)
cd password_manager



## Checkpoints & Progress
Specific deliverables, run instructions, and progress notes for the course checkpoints are documented in their respective files:
- [Checkpoint 2 (Week 9) - Core Requirements](./Checkpoint\ 2.md)

## AI Usage Disclosure
In the development of this repository, Artificial Intelligence tools were utilized as an assistive technology. AI was used to:
- Guide the architectural design and threat modeling.
- Generate boilerplate code and structural templates.
- Refine documentation and assist with syntax debugging.

**Human Oversight:** All AI-generated outputs were strictly reviewed, refactored, and validated for cryptographic security and logic flaws prior to committing. The repository owner takes full responsibility for the accuracy, security, and functionality of the codebase.