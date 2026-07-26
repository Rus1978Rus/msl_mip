#!/usr/bin/env python3
"""Toy Proof-of-Work blockchain — an educational demo of mining.

It shows the whole loop discussed in the conversation:
  * a miner iterates a nonce, searching for a block hash with N leading zeros
  * the block's first transaction (the "coinbase") pays the miner the reward
  * every node validates each block and REJECTS one whose reward breaks the rules

The point: a miner writes the reward to itself, but only the exact amount the
protocol allows (block subsidy + collected fees). Anyone can re-check it, so a
greedy miner who overpays gets their block thrown out — even with valid work.

Pure standard library, no dependencies (matches this repo's style).
Run:  python3 mining_demo.py
"""

import hashlib
import json
import time
from dataclasses import dataclass
from typing import List, Tuple

DIFFICULTY = 4      # required number of leading zeros (in hex) of the block hash
BLOCK_SUBSIDY = 50  # brand-new coins minted per block — this is the "emission"
COINBASE = "COINBASE"  # sentinel "sender" for the reward transaction


@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    fee: float = 0.0

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
        }


@dataclass
class Block:
    index: int
    prev_hash: str
    transactions: List[Transaction]
    timestamp: float
    nonce: int = 0

    def _header(self) -> str:
        # Deterministic serialization of everything the hash commits to.
        # Changing the nonce changes this string, and thus the hash.
        payload = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "transactions": [t.to_dict() for t in self.transactions],
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def hash(self) -> str:
        return hashlib.sha256(self._header().encode()).hexdigest()


def mine(block: Block, difficulty: int) -> int:
    """Increment the nonce until the block hash starts with `difficulty` zeros.

    Returns the number of attempts — this is the "work" in proof-of-work.
    """
    target = "0" * difficulty
    attempts = 0
    while not block.hash().startswith(target):
        block.nonce += 1
        attempts += 1
    return attempts


class Blockchain:
    def __init__(self, difficulty: int = DIFFICULTY, subsidy: float = BLOCK_SUBSIDY):
        self.difficulty = difficulty
        self.subsidy = subsidy
        self.mempool: List[Transaction] = []
        self.chain: List[Block] = [self._genesis()]

    def _genesis(self) -> Block:
        block = Block(index=0, prev_hash="0" * 64, transactions=[], timestamp=time.time())
        mine(block, self.difficulty)
        return block

    @property
    def tip(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, tx: Transaction) -> None:
        self.mempool.append(tx)

    def mine_block(self, miner_address: str) -> Tuple[Block, int]:
        """Assemble a block from the mempool and mine it for `miner_address`."""
        pending = list(self.mempool)
        reward = self.subsidy + sum(t.fee for t in pending)
        coinbase = Transaction(COINBASE, miner_address, amount=reward, fee=0.0)
        block = Block(
            index=self.tip.index + 1,
            prev_hash=self.tip.hash(),
            transactions=[coinbase] + pending,
            timestamp=time.time(),
        )
        attempts = mine(block, self.difficulty)
        self.mempool.clear()
        return block, attempts

    def validate_block(self, block: Block) -> Tuple[bool, str]:
        """What every node independently checks before accepting a block."""
        # 1. Proof of work: the hash must actually meet the difficulty.
        if not block.hash().startswith("0" * self.difficulty):
            return False, "hash does not meet difficulty"
        # 2. It must extend the current tip.
        if block.prev_hash != self.tip.hash():
            return False, "prev_hash does not match chain tip"
        if block.index != self.tip.index + 1:
            return False, "index is not sequential"
        # 3. Exactly one coinbase, and it must be the first transaction.
        coinbases = [t for t in block.transactions if t.sender == COINBASE]
        if len(coinbases) != 1 or block.transactions[0].sender != COINBASE:
            return False, "block must have exactly one coinbase, as its first tx"
        # 4. THE KEY RULE: the reward must equal subsidy + fees, no more.
        regular = block.transactions[1:]
        allowed = self.subsidy + sum(t.fee for t in regular)
        claimed = block.transactions[0].amount
        if claimed != allowed:
            return (
                False,
                f"reward {claimed} != allowed {allowed} "
                f"(subsidy {self.subsidy} + fees {allowed - self.subsidy})",
            )
        return True, "ok"

    def add_block(self, block: Block) -> None:
        ok, reason = self.validate_block(block)
        if not ok:
            raise ValueError(reason)
        self.chain.append(block)

    def balances(self) -> dict:
        bal: dict = {}
        for block in self.chain:
            for t in block.transactions:
                if t.sender != COINBASE:
                    bal[t.sender] = bal.get(t.sender, 0) - t.amount - t.fee
                bal[t.recipient] = bal.get(t.recipient, 0) + t.amount
        return bal


def main() -> None:
    chain = Blockchain(difficulty=DIFFICULTY, subsidy=BLOCK_SUBSIDY)
    print(
        f"Genesis-блок создан. Правило сложности: хеш должен начинаться с "
        f"{chain.difficulty} нулей. Награда (эмиссия) за блок: {chain.subsidy} монет.\n"
    )

    # --- Раунд 1: первый блок. Новые монеты появляются "из ниоткуда" (эмиссия). ---
    print("=== Майним блок #1 (мемпул пуст) ===")
    block1, attempts1 = chain.mine_block("Майнер-Аня")
    chain.add_block(block1)
    print(f"  перебрано вариантов nonce: {attempts1}")
    print(f"  подошедший nonce = {block1.nonce}")
    print(f"  хеш блока        = {block1.hash()}")
    print(
        f"  coinbase: Аня начислила себе {block1.transactions[0].amount} монет "
        f"(эмиссия {chain.subsidy} + комиссии 0)\n"
    )

    # --- Раунд 2: обычные транзакции с комиссиями. Комиссии достаются майнеру. ---
    print("=== В сеть поступили транзакции ===")
    chain.add_transaction(Transaction("Майнер-Аня", "Борис", amount=10, fee=1))
    chain.add_transaction(Transaction("Майнер-Аня", "Вера", amount=5, fee=2))
    print("  Аня -> Борис: 10 (комиссия 1)")
    print("  Аня -> Вера:   5 (комиссия 2)")
    print("=== Майним блок #2 (майнер — Дима) ===")
    block2, attempts2 = chain.mine_block("Майнер-Дима")
    chain.add_block(block2)
    print(f"  перебрано вариантов nonce: {attempts2}")
    print(f"  хеш блока = {block2.hash()}")
    print(
        f"  coinbase: Дима начислил себе {block2.transactions[0].amount} монет "
        f"(эмиссия {chain.subsidy} + комиссии 3)\n"
    )

    print("Балансы после двух блоков:")
    for who, amount in sorted(chain.balances().items()):
        print(f"  {who:12s} {amount}")
    total = sum(chain.balances().values())
    print(f"  (всего в обороте: {total} = 2 блока x {chain.subsidy} эмиссии)\n")

    # --- Раунд 3: майнер-мошенник пытается начислить себе больше, чем разрешено. ---
    print("=== Майнер-мошенник пытается схитрить ===")
    greedy = chain.subsidy + 1000  # хочет 1050 вместо положенных 50
    coinbase = Transaction(COINBASE, "Майнер-Жулик", amount=greedy, fee=0.0)
    cheat = Block(
        index=chain.tip.index + 1,
        prev_hash=chain.tip.hash(),
        transactions=[coinbase],
        timestamp=time.time(),
    )
    cheat_attempts = mine(cheat, chain.difficulty)
    print(f"  Жулик честно нашёл валидный хеш (перебрал {cheat_attempts} nonce):")
    print(f"    {cheat.hash()}")
    print(f"  но вписал себе {greedy} монет вместо разрешённых {chain.subsidy}.")
    print("  Отправляем блок в сеть на проверку...")
    try:
        chain.add_block(cheat)
        print("  Блок ПРИНЯТ (так быть не должно!)")
    except ValueError as reason:
        print(f"  Сеть ОТВЕРГЛА блок -> {reason}")

    print(
        "\nВывод: работа (proof-of-work) у Жулика настоящая, но правило награды "
        "нарушено,\nпоэтому каждый узел независимо отвергает блок. "
        "Смошенничать с суммой награды нельзя."
    )


if __name__ == "__main__":
    main()
