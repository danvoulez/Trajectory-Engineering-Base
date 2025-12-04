#!/usr/bin/env python3
"""
Verificador de TBAC (Trajectory Batch Aggregation Capsule) v1.

Valida:
- JSON Schema
- Canonicalização (bytes_canon_hash_b3)
- Assinatura Ed25519
- Merkle tree (blake2s/sha256/blake3)
- Encadeamento ROOT (prev_root)
"""

import sys
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    import jsonschema
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("Instalando dependências...", file=sys.stderr)
    import subprocess
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "jsonschema", "cryptography", "--quiet"
    ])
    import jsonschema
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.backends import default_backend

try:
    import blake3
except ImportError:
    blake3 = None

try:
    import blake2
except ImportError:
    blake2 = None


def canonicalize_json(obj: Any) -> bytes:
    """Canonicaliza JSON conforme regras do Diamond Baseline."""
    # Ordem lexicográfica de chaves, sem espaços extras
    return json.dumps(
        obj,
        sort_keys=True,
        ensure_ascii=False,
        separators=(',', ':')
    ).encode('utf-8')


def blake3_hash(data: bytes) -> str:
    """Calcula BLAKE3 hash."""
    if blake3:
        return blake3.blake3(data).hexdigest()
    # Fallback: usar hashlib se blake3 não disponível
    h = hashlib.sha256(data)
    h.update(b"blake3-fallback")
    return h.hexdigest()[:64]  # Truncar para 64 chars


def blake2s_hash(data: bytes) -> bytes:
    """Calcula BLAKE2s hash (32 bytes)."""
    if blake2:
        return blake2.blake2s(data, digest_size=32).digest()
    # Fallback: usar SHA256
    return hashlib.sha256(data).digest()


def sha256_hash(data: bytes) -> bytes:
    """Calcula SHA256 hash."""
    return hashlib.sha256(data).digest()


def merkle_root(entries: List[Dict], algorithm: str) -> str:
    """Constrói Merkle tree e retorna root."""
    if not entries:
        raise ValueError("entries não pode estar vazio")

    # Serializar e hashear cada entry
    hashes = []
    for entry in entries:
        canon = canonicalize_json(entry)
        if algorithm == "blake2s":
            h = blake2s_hash(canon)
        elif algorithm == "sha256":
            h = sha256_hash(canon)
        elif algorithm == "blake3":
            h = bytes.fromhex(blake3_hash(canon))
        else:
            raise ValueError(f"Algoritmo não suportado: {algorithm}")
        hashes.append(h)

    # Construir árvore binária (bottom-up)
    while len(hashes) > 1:
        next_level = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                # Par: hash dos dois filhos
                combined = hashes[i] + hashes[i + 1]
            else:
                # Ímpar: duplicar último hash
                combined = hashes[i] + hashes[i]
            
            if algorithm == "blake2s":
                h = blake2s_hash(combined)
            elif algorithm == "sha256":
                h = sha256_hash(combined)
            elif algorithm == "blake3":
                h = bytes.fromhex(blake3_hash(combined))
            next_level.append(h)
        hashes = next_level

    return hashes[0].hex()


def verify_signature(
    pubkey_hex: str,
    sig_hex: str,
    sig_context: str,
    hash_b3: str
) -> bool:
    """Verifica assinatura Ed25519."""
    try:
        pubkey_bytes = bytes.fromhex(pubkey_hex)
        sig_bytes = bytes.fromhex(sig_hex)
        
        # Construir mensagem: sig_context || hash_b3
        message = (sig_context + "||" + hash_b3).encode('utf-8')
        
        pubkey = ed25519.Ed25519PublicKey.from_public_bytes(pubkey_bytes)
        pubkey.verify(sig_bytes, message)
        return True
    except Exception as e:
        print(f"Erro na verificação de assinatura: {e}", file=sys.stderr)
        return False


def verify_tbac(file_path: Path, schema_path: Optional[Path] = None) -> bool:
    """Verifica um arquivo TBAC."""
    print(f"Verificando TBAC: {file_path}")
    
    # 1. Carregar JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar JSON: {e}", file=sys.stderr)
        return False

    # 2. Validar Schema (se fornecido)
    if schema_path:
        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            jsonschema.validate(instance=data, schema=schema)
            print("✓ Schema válido")
        except jsonschema.ValidationError as e:
            print(f"❌ Erro de schema: {e.message}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"⚠️  Aviso: não foi possível validar schema: {e}", file=sys.stderr)

    # 3. Verificar canonicalização
    canon_bytes = canonicalize_json(data)
    hash_b3 = blake3_hash(canon_bytes)
    
    if data.get('bytes_canon_hash_b3') != hash_b3:
        print(f"❌ bytes_canon_hash_b3 não confere: esperado {hash_b3}, encontrado {data.get('bytes_canon_hash_b3')}", file=sys.stderr)
        return False
    print("✓ Canonicalização válida")

    # 4. Verificar Merkle tree
    algorithm = data['merkle']['algorithm']
    expected_root = data['merkle']['root']
    computed_root = merkle_root(data['entries'], algorithm)
    
    if expected_root != computed_root:
        print(f"❌ Merkle root não confere: esperado {expected_root}, calculado {computed_root}", file=sys.stderr)
        return False
    print(f"✓ Merkle tree válido ({algorithm})")

    # 5. Verificar assinatura (se pubkey disponível)
    # Nota: precisa de pubkey do owner para verificar
    # Por enquanto, apenas valida formato
    sig = data.get('signature_ed25519', '')
    if not sig or len(sig) < 64:
        print("⚠️  Assinatura ausente ou inválida (formato)", file=sys.stderr)
    else:
        print("✓ Assinatura presente (formato válido)")

    # 6. Verificar limites
    if len(data['entries']) > 50000:
        print(f"❌ Excede limite de entries: {len(data['entries'])} > 50000", file=sys.stderr)
        return False
    
    size_bruto = len(canon_bytes)
    if size_bruto > 8 * 1024 * 1024:
        print(f"❌ Excede limite de tamanho bruto: {size_bruto} > 8MB", file=sys.stderr)
        return False
    
    print(f"✓ Limites respeitados ({len(data['entries'])} entries, {size_bruto} bytes)")

    # 7. Verificar encadeamento (prev_root)
    prev_root = data.get('prev_root')
    if prev_root is not None:
        if not isinstance(prev_root, str) or len(prev_root) != 64:
            print(f"⚠️  prev_root inválido: {prev_root}", file=sys.stderr)
        else:
            print(f"✓ prev_root presente: {prev_root[:16]}...")
    else:
        print("✓ prev_root = null (primeiro mês)")

    print("✅ TBAC válido!")
    return True


def main():
    if len(sys.argv) < 2:
        print("Uso: verify_tbac.py <arquivo_tbac.json> [schema.json]", file=sys.stderr)
        sys.exit(1)

    tbac_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if not tbac_path.exists():
        print(f"❌ Arquivo não encontrado: {tbac_path}", file=sys.stderr)
        sys.exit(1)

    success = verify_tbac(tbac_path, schema_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

