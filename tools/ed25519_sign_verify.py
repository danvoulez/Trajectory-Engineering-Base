#!/usr/bin/env python3
"""Assina ou verifica arquivo com Ed25519"""
import argparse
import json
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("Instalando cryptography...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography", "--quiet"])
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.backends import default_backend

def canonical_json(obj):
    """Canonicaliza JSON"""
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')

def sign_file(input_file, priv_key_file, output_file):
    """Assina arquivo JSON"""
    # Carrega chave privada
    with open(priv_key_file, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    # Carrega JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Remove signature se existir para assinar
    original_sig = data.get('signature')
    data['signature'] = None
    
    # Canonicaliza e assina
    canonical = canonical_json(data)
    signature = private_key.sign(canonical)
    
    # Adiciona signature
    data['signature'] = signature.hex()
    
    # Salva
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Arquivo assinado: {output_file}")

def verify_file(input_file, pub_key_file):
    """Verifica assinatura"""
    # Carrega chave pública
    with open(pub_key_file, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())
    
    # Carrega JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extrai signature
    signature_hex = data.get('signature')
    if not signature_hex:
        print("❌ Arquivo não tem signature")
        return False
    
    # Remove signature para verificar
    data['signature'] = None
    canonical = canonical_json(data)
    signature = bytes.fromhex(signature_hex)
    
    # Verifica
    try:
        public_key.verify(signature, canonical)
        print("✅ Assinatura válida")
        return True
    except Exception as e:
        print(f"❌ Assinatura inválida: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Assina ou verifica arquivo com Ed25519')
    parser.add_argument('--sign', help='Arquivo para assinar')
    parser.add_argument('--verify', help='Arquivo para verificar')
    parser.add_argument('--priv', help='Chave privada Ed25519 (PEM)')
    parser.add_argument('--pub', help='Chave pública Ed25519 (PEM)')
    parser.add_argument('--out', help='Arquivo de saída (para --sign)')
    
    args = parser.parse_args()
    
    if args.sign:
        if not args.priv or not args.out:
            print("❌ --sign requer --priv e --out")
            sys.exit(1)
        sign_file(args.sign, args.priv, args.out)
    elif args.verify:
        if not args.pub:
            print("❌ --verify requer --pub")
            sys.exit(1)
        success = verify_file(args.verify, args.pub)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

