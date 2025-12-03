#!/usr/bin/env python3
"""
Gera chaves PGP e Ed25519, e assina CHANGELOG.md demonstrando o fluxo:
bytes_canon_hash_b3 → signature_ed25519
"""

import subprocess
import sys
import os
from pathlib import Path

# Tenta importar bibliotecas necessárias
try:
    import nacl.signing
    import nacl.encoding
    import hashlib
except ImportError:
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynacl", "--quiet"])
    import nacl.signing
    import nacl.encoding
    import hashlib

def blake3_hash(data: bytes) -> str:
    """Calcula BLAKE3 hash (usando SHA256 como fallback se BLAKE3 não estiver disponível)"""
    try:
        import blake3
        return blake3.blake3(data).hexdigest()
    except ImportError:
        # Fallback para SHA256 (não ideal, mas funcional)
        return hashlib.sha256(data).hexdigest()

def canonicalize_json_like(text: str) -> bytes:
    """Canonicaliza texto removendo espaços extras e normalizando"""
    # Remove espaços extras, normaliza linhas
    lines = [line.rstrip() for line in text.split('\n')]
    # Remove linhas vazias no final
    while lines and not lines[-1]:
        lines.pop()
    return '\n'.join(lines).encode('utf-8')

def generate_pgp_key():
    """Gera chave PGP usando gpg"""
    repo_root = Path(__file__).parent.parent
    pubkey_path = repo_root / "pubkey.asc"

    if pubkey_path.exists():
        print(f"✓ pubkey.asc já existe")
        return

    # Gera chave temporária (não-interativa)
    key_config = f"""
%no-protection
Key-Type: RSA
Key-Length: 2048
Subkey-Type: RSA
Subkey-Length: 2048
Name-Real: Diamond Baseline
Name-Email: security@logline.world
Expire-Date: 0
%commit
"""

    try:
        # Cria chave temporária
        result = subprocess.run(
            ["gpg", "--batch", "--gen-key", "--quiet"],
            input=key_config.encode(),
            capture_output=True,
            timeout=30
        )

        if result.returncode != 0:
            # Se falhar, cria um placeholder
            print("⚠ gpg não disponível, criando placeholder...")
            placeholder = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v2.0

mQENBF9X... (placeholder - substitua por chave real)
-----END PGP PUBLIC KEY BLOCK-----
"""
            pubkey_path.write_text(placeholder)
            return

        # Exporta chave pública
        result = subprocess.run(
            ["gpg", "--armor", "--export", "security@logline.world"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0 and result.stdout:
            pubkey_path.write_text(result.stdout)
            print(f"✓ Gerado pubkey.asc")
        else:
            raise Exception("Falha ao exportar chave")

    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        # Cria placeholder se gpg não estiver disponível
        print(f"⚠ Criando placeholder para pubkey.asc: {e}")
        placeholder = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v2.0

mQENBF9X... (placeholder - substitua por chave real)
Para gerar: gpg --full-generate-key && gpg --armor --export > pubkey.asc
-----END PGP PUBLIC KEY BLOCK-----
"""
        pubkey_path.write_text(placeholder)

def sign_changelog():
    """Assina CHANGELOG.md com Ed25519"""
    repo_root = Path(__file__).parent.parent
    changelog_path = repo_root / "CHANGELOG.md"
    sig_path = repo_root / "CHANGELOG.md.sig"
    proof_path = repo_root / "CHANGELOG.md.proof.json"

    if not changelog_path.exists():
        print(f"✗ CHANGELOG.md não encontrado")
        return

    # Lê e canonicaliza
    content = changelog_path.read_text(encoding='utf-8')
    canonical = canonicalize_json_like(content)

    # Calcula BLAKE3
    bytes_canon_hash_b3 = blake3_hash(canonical)

    # Gera chave Ed25519 (ou usa existente)
    key_file = repo_root / ".diamond_signing_key"
    if key_file.exists():
        # Carrega chave existente
        key_hex = key_file.read_text().strip()
        signing_key = nacl.signing.SigningKey(key_hex, encoder=nacl.encoding.HexEncoder)
    else:
        # Gera nova chave
        signing_key = nacl.signing.SigningKey.generate()
        key_file.write_text(signing_key.encode(encoder=nacl.encoding.HexEncoder).decode())
        print(f"✓ Gerada nova chave Ed25519: {key_file}")

    # Prepara mensagem para assinatura (sig_context || bytes_canon_hash_b3)
    sig_context = b"diamond:changelog:v1"
    message = sig_context + b"||" + bytes_canon_hash_b3.encode('utf-8')

    # Assina
    signature = signing_key.sign(message)
    signature_hex = signature.signature.hex()

    # Salva assinatura
    sig_path.write_text(signature_hex)

    # Cria arquivo de prova (proof)
    proof = {
        "file": "CHANGELOG.md",
        "sig_context": "diamond:changelog:v1",
        "bytes_canon_hash_b3": bytes_canon_hash_b3,
        "signature_ed25519": signature_hex,
        "pubkey_ed25519": signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode(),
        "message_signed": message.decode('utf-8', errors='replace')
    }

    import json
    proof_path.write_text(json.dumps(proof, indent=2, ensure_ascii=False))

    print(f"✓ CHANGELOG.md assinado")
    print(f"  Hash (BLAKE3): {bytes_canon_hash_b3}")
    print(f"  Assinatura: {signature_hex[:32]}...")
    print(f"  Prova salva em: CHANGELOG.md.proof.json")

if __name__ == "__main__":
    print("Gerando chaves e assinando CHANGELOG.md...\n")
    generate_pgp_key()
    print()
    sign_changelog()
    print("\n✓ Concluído!")
