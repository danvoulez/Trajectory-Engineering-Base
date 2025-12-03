#!/usr/bin/env python3
"""
Verifica assinatura Ed25519 de um arquivo usando o proof.json
"""

import json
import sys
from pathlib import Path

try:
    import nacl.signing
    import nacl.encoding
except ImportError:
    print("Instalando pynacl...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynacl", "--quiet"])
    import nacl.signing
    import nacl.encoding

def verify_signature(proof_path: Path):
    """Verifica assinatura usando proof.json"""
    if not proof_path.exists():
        print(f"✗ Arquivo não encontrado: {proof_path}")
        return False
    
    proof = json.loads(proof_path.read_text())
    
    # Carrega chave pública
    verify_key = nacl.signing.VerifyKey(
        proof["pubkey_ed25519"],
        encoder=nacl.encoding.HexEncoder
    )
    
    # Reconstrói mensagem (sig_context || bytes_canon_hash_b3)
    message = (proof["sig_context"] + "||" + proof["bytes_canon_hash_b3"]).encode()
    
    # Verifica assinatura
    try:
        verify_key.verify(message, bytes.fromhex(proof["signature_ed25519"]))
        print(f"✓ Assinatura válida para {proof['file']}")
        print(f"  Hash: {proof['bytes_canon_hash_b3']}")
        print(f"  Contexto: {proof['sig_context']}")
        return True
    except Exception as e:
        print(f"✗ Assinatura inválida: {e}")
        return False

if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent
    proof_path = repo_root / "CHANGELOG.md.proof.json"
    
    if len(sys.argv) > 1:
        proof_path = Path(sys.argv[1])
    
    success = verify_signature(proof_path)
    sys.exit(0 if success else 1)

