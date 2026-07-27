#!/usr/bin/env python3
"""A cryptocurrency WITHOUT mining — Proof-of-Authority ledger in the NOTARIUS style.

The whole conversation led here: instead of buying the right to append a block
with energy (proof-of-work, leading zeros), we buy it with a SIGNATURE. This is
exactly the NOTARIUS model (a signed, hash-linked append-only chain) turned into
a coin:

    CREATED     = emission  — only the trusted mint AUTHORITY may sign it
    TRANSFERRED = a payment  — only the SENDER (holder of that address's key) may sign it

Security here does NOT come from mining. It comes from:
  * Ed25519 signatures      — you cannot spend from an address without its key;
  * a prev_hash chain       — tamper with any past event and the links break;
  * a single trusted root   — every verifier knows the authority's public key.

Honest cost (no free lunch — it just moved): mining pays with ENERGY and trusts
no one; this pays with TRUST — the authority controls emission, and resolving a
FORK / double-spend across parties needs an external witness (NOTARIUS cosign),
because a lone local chain cannot detect it. Demonstrated at the end.

Identity = an Ed25519 public key (like a real crypto address). Names are display
only. Requires the `cryptography` package. Run:  python3 poa_ledger.py
"""
from __future__ import annotations

import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

# ---------------------------- Ed25519 helpers -------------------------------
def new_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.generate()


def pub_hex(sk: Ed25519PrivateKey) -> str:
    return sk.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()


def sign(sk: Ed25519PrivateKey, data: bytes) -> str:
    return sk.sign(data).hex()


def verify_sig(pub_hex_: str, data: bytes, sig_hex: str) -> bool:
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex_)).verify(
            bytes.fromhex(sig_hex), data
        )
        return True
    except (InvalidSignature, ValueError):
        return False


def _canonical(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


_BODY_KEYS = ("seq", "type", "sender", "recipient", "amount", "at", "prev_hash")


# ------------------------------- The ledger ---------------------------------
class PoALedger:
    """Append-only, hash-linked, signature-secured coin ledger. No mining."""

    def __init__(self, authority_pub: str):
        self.authority = authority_pub          # the one trusted root key
        self.chain: list[dict] = []

    def _digest(self, event: dict) -> str:
        return hashlib.sha256(_canonical(event)).hexdigest()

    def _append(self, body: dict, signer_sk: Ed25519PrivateKey) -> dict:
        body = {**body, "prev_hash": self._digest(self.chain[-1]) if self.chain else None}
        ev = {**body, "sig": sign(signer_sk, _canonical(body)),
              "actor_pub": pub_hex(signer_sk)}
        self.chain.append(ev)
        return ev

    def mint(self, authority_sk, recipient: str, amount: int, at: str) -> dict:
        """CREATED — emission. The demo assumes authority_sk IS the authority."""
        return self._append({"seq": len(self.chain), "type": "CREATED",
                             "sender": None, "recipient": recipient,
                             "amount": amount, "at": at}, authority_sk)

    def transfer(self, sender_sk, sender: str, recipient: str, amount: int, at: str) -> dict:
        return self._append({"seq": len(self.chain), "type": "TRANSFERRED",
                             "sender": sender, "recipient": recipient,
                             "amount": amount, "at": at}, sender_sk)

    def verify(self) -> dict:
        """Independently replay + check every rule. Returns a report; stops
        reporting balances if a break is found (like NOTARIUS verify_trace)."""
        balances: dict[str, int] = {}
        reasons: list[str] = []

        def fail(step, why):
            reasons.append(f"step {step}: {why}")

        prev = None
        for step, ev in enumerate(self.chain):
            body = {k: ev[k] for k in _BODY_KEYS}
            # 1. signature valid for the claimed signer
            if not verify_sig(ev["actor_pub"], _canonical(body), ev["sig"]):
                fail(step, "invalid signature"); break
            # 2. chain link
            if step == 0:
                if ev["prev_hash"] is not None:
                    fail(step, "first event carries a prev_hash"); break
            elif ev["prev_hash"] != self._digest(prev):
                fail(step, "prev_hash mismatch — chain broken (tampering)"); break
            # 3. amount sanity
            if not isinstance(ev["amount"], int) or ev["amount"] <= 0:
                fail(step, "amount must be a positive integer"); break
            # 4. authorization + balances
            if ev["type"] == "CREATED":
                if ev["actor_pub"] != self.authority:
                    fail(step, "unauthorized mint — signer is not the authority"); break
                balances[ev["recipient"]] = balances.get(ev["recipient"], 0) + ev["amount"]
            elif ev["type"] == "TRANSFERRED":
                if ev["actor_pub"] != ev["sender"]:
                    fail(step, "transfer not signed by the sender (spending a foreign address)"); break
                if balances.get(ev["sender"], 0) < ev["amount"]:
                    fail(step, f"overspend — sender has {balances.get(ev['sender'],0)}, sends {ev['amount']}"); break
                balances[ev["sender"]] -= ev["amount"]
                balances[ev["recipient"]] = balances.get(ev["recipient"], 0) + ev["amount"]
            else:
                fail(step, f"unknown event type {ev['type']!r}"); break
            prev = ev

        ok = not reasons
        return {"ok": ok, "reasons": reasons,
                "balances": balances if ok else None, "steps": len(self.chain)}


# --------------------------------- Demo -------------------------------------
def main() -> None:
    # Keys. Identity = public key; names are for humans only.
    authority = new_key()
    alice, bob, carol, mallory = new_key(), new_key(), new_key(), new_key()
    NAME = {pub_hex(authority): "Authority", pub_hex(alice): "Alice",
            pub_hex(bob): "Bob", pub_hex(carol): "Carol", pub_hex(mallory): "Mallory"}

    def show(ledger, title):
        rep = ledger.verify()
        print(f"  {title}: verify -> {'OK' if rep['ok'] else 'ОТКЛОНЕНО'}")
        if rep["ok"]:
            bal = {NAME.get(k, k[:6]): v for k, v in rep["balances"].items()}
            print(f"    балансы: {bal}")
        else:
            for r in rep["reasons"]:
                print(f"    ! {r}")

    print("=" * 72)
    print("МОНЕТА БЕЗ МАЙНИНГА — PoA-реестр (право дать блок = подпись, не нули)")
    print("=" * 72)

    L = PoALedger(authority_pub=pub_hex(authority))
    L.mint(authority, pub_hex(alice), 1000, at="2026-07-27T10:00")
    print("\n[1] Authority эмитировал 1000 монет Alice (CREATED, подпись authority)")
    show(L, "после эмиссии")

    L.transfer(alice, pub_hex(alice), pub_hex(bob), 300, at="2026-07-27T10:05")
    L.transfer(bob, pub_hex(bob), pub_hex(carol), 100, at="2026-07-27T10:06")
    print("\n[2] Alice→Bob 300, Bob→Carol 100 (каждый подписал СВОЙ перевод)")
    show(L, "после переводов")

    print("\n" + "-" * 72)
    print("АТАКИ — тот же verify() их ловит, без всякого майнинга:")

    # A. Forged transfer: Mallory tries to move Alice's coins with her OWN key.
    Lf = PoALedger(pub_hex(authority)); Lf.chain = list(L.chain)
    Lf.transfer(mallory, pub_hex(alice), pub_hex(mallory), 500, at="x")  # sender=Alice, signer=Mallory
    print("\n[A] Mallory двигает монеты Alice, подписав своим ключом:")
    show(Lf, "подделка")

    # B. Overspend: Bob sends more than he holds.
    Lo = PoALedger(pub_hex(authority)); Lo.chain = list(L.chain)
    Lo.transfer(bob, pub_hex(bob), pub_hex(carol), 9999, at="x")
    print("\n[B] Bob шлёт 9999, имея 200:")
    show(Lo, "перерасход")

    # C. Tamper: flip an amount in a committed past event.
    Lt = PoALedger(pub_hex(authority)); Lt.chain = [dict(e) for e in L.chain]
    Lt.chain[0]["amount"] = 1_000_000
    print("\n[C] Кто-то подменил сумму эмиссии в блоке 0 на 1 000 000:")
    show(Lt, "подмена истории")

    # D. Unauthorized mint: Mallory mints to herself.
    Lm = PoALedger(pub_hex(authority)); Lm.chain = list(L.chain)
    Lm.mint(mallory, pub_hex(mallory), 1000, at="x")
    print("\n[D] Mallory чеканит себе 1000 своим ключом (не authority):")
    show(Lm, "самочеканка")

    # E. The honest limit — fork / double-spend (needs an external witness).
    print("\n" + "-" * 72)
    print("ЧЕСТНЫЙ ПРЕДЕЛ — форк/двойная трата (цена доверия вместо энергии):")
    # Carol has 100. She signs TWO conflicting spends of the SAME 100.
    b1 = PoALedger(pub_hex(authority)); b1.chain = list(L.chain)
    b1.transfer(carol, pub_hex(carol), pub_hex(bob), 100, at="t")
    b2 = PoALedger(pub_hex(authority)); b2.chain = list(L.chain)
    b2.transfer(carol, pub_hex(carol), pub_hex(mallory), 100, at="t")
    print("\n[E] Carol подписала ДВА перевода своих 100 — Bob'у и Mallory:")
    show(b1, "ветка 1 (показана Bob'у)")
    show(b2, "ветка 2 (показана Mallory)")
    print("    Каждая ветка ПО ОТДЕЛЬНОСТИ валидна — подпись Carol настоящая, баланс есть.")
    print("    Локальный verify() конфликт НЕ видит: нужен внешний свидетель/порядок")
    print("    (NOTARIUS cosign / консенсус). Это и есть та задача, которую в PoW")
    print("    решает майнинг энергией, а здесь — доверие к свидетелям.")


if __name__ == "__main__":
    main()
