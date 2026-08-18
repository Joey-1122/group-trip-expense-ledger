# Logical Ledger Contract

The host Agent chooses the physical implementation. Member shares may be embedded in a transaction or stored separately.

## Required

### Trip

Stable ID/name, timezone, base currency, default participants/split, active status.

### Members

Stable ID, display name, current-user marker, active status.

### Transactions

Common fields:

- stable ID and optional source message/idempotency key;
- type, time, title/category, status;
- original input and prior values.

Expense fields:

- original amount/currency;
- base amount and conversion source/time when needed;
- payer/payment source;
- participants, split method, member shares.

Exchange/top-up fields:

- from wallet, amount, currency;
- to wallet, amount, currency;
- transferred base cost;
- wallet balances/costs before and after.

Settlement fields:

- from member;
- to member;
- amount, currency/base amount;
- time.

### Wallets, only when needed

Stable ID, owner, type, currency, remaining quantity, remaining base-currency cost, cost method.

## Ready check

Verify trip/members/transaction shapes round-trip, one equal split closes, transfer types do not count as consumption, member nets sum to zero, the ledger reopens later, and no fake expense remains.