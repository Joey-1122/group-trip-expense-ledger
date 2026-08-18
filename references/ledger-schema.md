# Logical Ledger Contract

The host chooses the physical implementation. A readable ledger is mandatory; internal JSON/database alone is insufficient.

## Readable expense view

Show at minimum:

- date/time;
- item/category;
- original amount/currency;
- base-currency amount;
- payer;
- participants and shares;
- payment source when relevant;
- status.

Provide a member summary with paid, burden, and open balance. Refresh after every successful write or correction.

## Logical data

### Trip

Stable ID, name/destination, timezone, base currency, default participants/split, status, readable-ledger location/ownership.

### Member

Stable ID, display name, current-user marker, active status.

### Transaction

Common: stable ID/idempotency key, type, time, title/category, status, original wording, change history.

Expense: original amount/currency, locked base amount, conversion source/time, payer, payment source, participants, split method, member shares.

Exchange/top-up: source wallet/amount/currency, destination wallet/amount/currency, transferred base cost, balances/costs before and after.

Settlement: sender, receiver, amount, currency/base amount, time.

### Wallet, only for real funds

Stable ID, owner, type, currency, remaining foreign quantity, remaining base-currency cost, cost method.

## Ready check

Verify:

1. trip, members, and transactions reopen correctly;
2. user can open the readable ledger;
3. one equal split closes;
4. transfers do not count as consumption;
5. member nets sum to zero;
6. no fake expense or wallet balance remains.
