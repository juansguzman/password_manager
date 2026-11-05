import os
import sys
import json
import getpass
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

VAULT_FILE = "vault.enc"
SALT_FILE = "salt.bin"
MAX_ATTEMPTS = 3

def derive_key(master_password: str, salt: bytes) -> bytes:
    ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2, hash_len=32, salt_len=16)
    hash_bytes = ph.hash(master_password, salt=salt).encode('utf-8')
    return hash_bytes[:32] 

def encrypt_and_save(vault_data: dict, master_password: str, salt: bytes):
    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    plaintext = json.dumps(vault_data).encode('utf-8')
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    with open(VAULT_FILE, "wb") as f:
        f.write(nonce + ciphertext)

def init_vault() -> tuple[str, bytes]:
    print("\nNo se encontró una bóveda. Iniciando configuración por primera vez...")
    master_pwd = getpass.getpass("Crea tu nueva contraseña maestra: ")
    confirm_pwd = getpass.getpass("Confirma tu contraseña maestra: ")
    
    if master_pwd != confirm_pwd:
        print("Las contraseñas no coinciden. Ejecuta el programa de nuevo.")
        sys.exit(1)
        
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
        
    encrypt_and_save({}, master_pwd, salt)
    print("Bóveda vacía inicializada y cifrada con éxito.\n")
    return master_pwd, salt

def login() -> tuple[dict, str, bytes]:
    with open(SALT_FILE, "rb") as f:
        salt = f.read()
        
    with open(VAULT_FILE, "rb") as f:
        data = f.read()
        
    nonce, ciphertext = data[:12], data[12:]
    
    for attempt in range(1, MAX_ATTEMPTS + 1):
        master_pwd = getpass.getpass(f"Ingresa la contraseña maestra (Intento {attempt}/{MAX_ATTEMPTS}): ")
        key = derive_key(master_pwd, salt)
        aesgcm = AESGCM(key)
        
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            vault_data = json.loads(plaintext.decode('utf-8'))
            print("\n¡Autenticación exitosa! Bóveda desbloqueada.")
            return vault_data, master_pwd, salt
        except Exception:
            print("Contraseña incorrecta.")
            
    # Mantenemos el cierre automático aquí solo si se superan los 3 intentos por seguridad contra ataques
    print("\nLímite de intentos superado. Cerrando programa por seguridad.")
    sys.exit(1)

if __name__ == "__main__":
    print("=== Gestor de Contraseñas Seguro ===")
    
    if not os.path.exists(VAULT_FILE) or not os.path.exists(SALT_FILE):
        master_pwd, salt = init_vault()
        vault_data = {}
    else:
        vault_data, master_pwd, salt = login()
        
    # Bucle infinito: el programa no saldrá de aquí a menos que se escriba 'exit'
    while True:
        print("\nOpciones: [ver] bóveda | [agregar] credencial | [exit]")
        action = input("Selecciona una acción: ").strip().lower()
        
        if action == "exit":
            print("Cerrando bóveda de forma segura. ¡Adiós!")
            break  # Esto rompe el bucle y permite que el programa termine naturalmente
            
        elif action == "ver":
            if not vault_data:
                print("La bóveda está vacía.")
            else:
                print("\nCuentas guardadas:")
                for sitio in vault_data.keys():
                    print(f"- {sitio}")
                    
        elif action == "agregar":
            print("\n--- Agregar nueva credencial ---")
            sitio = input("Sitio web o identificador: ")
            password_sitio = getpass.getpass(f"Contraseña para {sitio}: ")
            
            vault_data[sitio] = password_sitio
            encrypt_and_save(vault_data, master_pwd, salt)
            print(f"Credencial para '{sitio}' guardada y bóveda cifrada nuevamente.")
            
        else:
            # Si el usuario escribe cualquier otra cosa, el programa le avisa y vuelve a preguntar
            print("Comando no reconocido. Por favor, escribe 'ver', 'agregar' o 'exit'.")