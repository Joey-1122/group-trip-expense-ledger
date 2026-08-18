# Ledger Rules

## Canonical facts

Keep stable IDs, original user text, trip, members, transactions, member shares, status, and prior values for corrections.

Transaction types in V1:

- expense;
- exchange;
- top-up/transfer;
- settlement.


## Member math

For each expense: `net = merchant_paid - burden`.

For settlement `A → B` amount `s`: add `s` to A's net and subtract `s` from B's net.

Consumption includes active expenses only. Exchange, top-up, settlement, and voided records do not count.

## Interpretations

- “我们一起” uses default participants.
- “我自己的” is personal.
- “请客” is treat.
- “各付各的” becomes separate personal records.
- Shared and personal parts become separate records.
- Another member paying for one person's item creates debt from bearer to payer.

## Risk

Ask only when ambiguity changes money, payer, participants, or conversion. Confirm ambiguous targets, settled-record changes, bulk changes, and destructive actions. Execute explicit low-risk corrections and rule changes immediately.

## Currency

Use currency minor units where known: JPY whole units; CNY/USD cents. Store exact original amounts.

Weighted wallets retain remaining quantity and remaining base cost. Exchanges add both; spending removes proportional cost; wallet-to-wallet transfer moves proportional quantity and cost. When moving or spending the entire remaining quantity, move the entire remaining base cost to avoid a rounding residue. Never allow an untracked negative balance.

Use an explicit actual base-currency charge before any rate lookup. Otherwise foreign card conversions retain rate source/time and stay locked in V1.