#!/usr/bin/env python3
"""Deterministic equal/custom split validation and settlement suggestion."""
import json
import sys

def fail(message):
    raise ValueError(message)

def split_equal(amount, participants, payer=None):
    if not isinstance(amount, int) or amount <= 0:
        fail("amount_minor must be a positive integer")
    if not participants or len(set(participants)) != len(participants):
        fail("participants must be a non-empty unique list")
    base, remainder = divmod(amount, len(participants))
    order = list(participants)
    if payer in order:
        order.remove(payer)
        order.insert(0, payer)
    shares = {member: base for member in participants}
    for member in order[:remainder]:
        shares[member] += 1
    return shares

def validate_custom(amount, shares):
    if not isinstance(amount, int) or amount <= 0:
        fail("amount_minor must be a positive integer")
    if not shares or any(not isinstance(value, int) or value < 0 for value in shares.values()):
        fail("custom_minor values must be non-negative integers")
    if sum(shares.values()) != amount:
        fail("custom split does not close")
    return shares

def suggest_settlement(nets):
    if not nets or any(not isinstance(value, int) for value in nets.values()):
        fail("net_minor must map members to integer minor units")
    if sum(nets.values()) != 0:
        fail("member nets must sum to zero")
    receivers = sorted([[member, value] for member, value in nets.items() if value > 0], key=lambda item: (-item[1], item[0]))
    payers = sorted([[member, -value] for member, value in nets.items() if value < 0], key=lambda item: (-item[1], item[0]))
    transfers = []
    payer_index = receiver_index = 0
    while payer_index < len(payers) and receiver_index < len(receivers):
        amount = min(payers[payer_index][1], receivers[receiver_index][1])
        transfers.append({"from": payers[payer_index][0], "to": receivers[receiver_index][0], "amount_minor": amount})
        payers[payer_index][1] -= amount
        receivers[receiver_index][1] -= amount
        if payers[payer_index][1] == 0:
            payer_index += 1
        if receivers[receiver_index][1] == 0:
            receiver_index += 1
    return transfers

def apply_settlement(nets, sender, receiver, amount):
    if sender not in nets or receiver not in nets or sender == receiver:
        fail("sender and receiver must be distinct known members")
    if not isinstance(amount, int) or amount <= 0:
        fail("amount_minor must be a positive integer")
    updated = dict(nets)
    updated[sender] += amount
    updated[receiver] -= amount
    if sum(updated.values()) != 0:
        fail("updated member nets must sum to zero")
    return updated

def main():
    data = json.load(sys.stdin)
    action = data.get("action")
    if action == "split":
        amount = data.get("amount_minor")
        shares = validate_custom(amount, data["custom_minor"]) if "custom_minor" in data else split_equal(amount, data.get("participants"), data.get("payer"))
        output = {"split_minor": shares, "sum_minor": sum(shares.values())}
    elif action == "settle":
        output = {"transfers": suggest_settlement(data.get("net_minor"))}
    elif action == "apply_settlement":
        output = {"net_minor": apply_settlement(data.get("net_minor"), data.get("from"), data.get("to"), data.get("amount_minor"))}
    else:
        fail("action must be split, settle, or apply_settlement")
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        sys.exit(1)
