# Secure Password Manager (CLI)

## Scope
A Python-based, 100% offline password manager supporting strong master password enforcement, encrypted vault storage, and password generation. Built to mitigate common attack vectors including brute-force cracking, database extraction, and memory scraping.

## System Use Cases & Commands
- `init`: Setup a new vault, enforce a strong master password (UC-002), and configure optional MFA (UC-003).
- `login`: Authenticate into the manager (UC-001).
- `add`: Store a new encrypted password entry (UC-004).
- `get <service>`: View stored credentials after authentication (UC-005).
- `update <service>`: Update existing password entries (UC-006).
- `generate`: Generate cryptographically strong random passwords (UC-008).

## Build and Run Instructions
1. **Clone the repository:** 
   ```bash
   git clone https://github.com/juansguzman/password_manager.git
   cd password_manager