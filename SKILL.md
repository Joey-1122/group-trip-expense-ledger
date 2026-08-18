---
name: "manage-trip-expenses"
description: "多人旅行由一人统一自然语言记账、分摊、外币换算、统计与结算。"
---

# Group Trip Expense Ledger

Help one designated bookkeeper manage a whole travel group's shared ledger through natural conversation. Optimize for ordinary travel: quick entry, clear corrections, accurate member burdens, and an understandable final settlement.

Read `references/ledger-rules.md` before calculating or changing money.
Read `references/ledger-schema.md` before asking the host Agent to create storage.
Read `references/examples.md` when an input is ambiguous.
Use `scripts/trip_ledger.py` when command execution is available.

## Boundary

The host Agent chooses and creates the actual durable store with its own tools. This Skill does not prescribe a vendor, database, spreadsheet, file format, or device environment.

Require the host Agent to:

- choose one durable writable source of truth;
- create the logical ledger from `references/ledger-schema.md`;
- reopen the same ledger in later messages;
- tell the user where the ledger is and whether it is shared;
- report honestly if persistence is unavailable.

Do not ask the user to design fields. If a new cloud resource needs permission, ask once and state who will own it.

V1 assumes one active trip, one person recording for everyone, and one payer/payment source per recorded expense. If a bill mixes shared and personal items or uses multiple payers, split it into separate ordinary records.


## Start a trip

When no active trip exists, ask only for trip name, traveler names, and which name represents the user.

Defaults:

- base currency from locale when safe, otherwise CNY;
- equal split;
- all members as participants unless the user sets another default;
- date from message time in the user's timezone;
- no wallets until foreign cash or stored value appears.

Reply:

```
旅行账本已就绪：厦门周末
成员：我、同行人B、同行人A
默认：人民币｜三人 AA｜日期按消息当天
账本：<host-reported location>
直接说“同行人B付了 96 打车，三个人”就能记。
```

Introduce these phrases only when useful:

- “刚才那笔改成只有我”
- “以后没说参与人就是我和同行人B”
- “看每个人付了多少、承担多少”
- “现在谁该转给谁”
- “这笔是换汇/充值，不算消费”

## Record an expense

Extract date, title/category, amount/currency, payer, participants, split method, and payment source when it affects conversion.

Apply established defaults. Ask one short question only if missing information changes money, payer, participants, or currency conversion. If the message is not clearly a bookkeeping instruction or travel expense, do not write.

Write immediately when material facts are clear. Show any low-impact assumption in the receipt.

```
已记：打车 ¥96
同行人B付款｜我、同行人B、同行人A AA，各 ¥32
状态：未结算
```

```
已记：药品 ¥45
同行人B付款｜由你个人承担
当前你欠同行人B ¥45
```

“各付各的” creates separate personal records with payer = bearer and no settlement. A bill containing shared and personal items also becomes separate records.

## Split rules

V1 supports:

- equal among named/default participants;
- personal;
- treat: payer bears the full amount, no debt;
- paid separately;
- explicit custom amounts.

Use integer minor units or exact decimals. Splits must close exactly. Assign unavoidable residual to the participating payer first, then stable member order.

Keep separate:

- paid: merchant payment;
- burden: member's consumption share;
- settlement: repayment between travelers.

## Foreign cash and stored value

Do not configure wallets during onboarding. Create them only when foreign cash or stored value appears.

Every wallet using weighted cost stores:

- remaining foreign quantity `Q`;
- remaining base-currency cost `C`;
- current unit cost `C / Q`.

Use exact decimals and round only the final base-currency amount to its minor unit.

### Exchange into a wallet

For source base amount `c` buying foreign amount `q`:

- `Q_new = Q_old + q`
- `C_new = C_old + c`
- `unit_cost = C_new / Q_new`

Record source wallet/amount/currency and destination wallet/amount/currency. Exchange is not consumption.

### Spend from a wallet

For foreign spending amount `x`:

- require `x <= Q_old`;
- if `x == Q_old`, set `base_cost = C_old`; otherwise `base_cost = round_to_minor_unit(x * C_old / Q_old)`;
- `Q_new = Q_old - x`;
- `C_new = C_old - base_cost`.

The expense uses `base_cost` for splitting. If tracked balance is insufficient, ask for the correct funding source; do not fabricate a negative pool.

### Transfer into stored value

For foreign amount `x` moved from cash wallet A to stored-value wallet B:

- if `x == Q_A`, set `transferred_cost = C_A`; otherwise calculate `transferred_cost = round_to_minor_unit(x * C_A / Q_A)`;
- subtract `x` and `transferred_cost` from A;
- add `x` and `transferred_cost` to B.

Top-up is a transfer, not consumption. Later spending from B uses B's weighted cost.

### Foreign card or online payment

If the user provides the actual base-currency charged amount, use it. Otherwise use a current rate supplied by the host Agent's rate source at entry time. Store rate, source, and timestamp; lock the converted amount for splitting. Do not reconcile a later card statement in V1.

Never call a rate real-time without a source. If no rate is available, ask the user for one or mark the conversion as estimated.

## Correct or undo

Resolve the target to exactly one record.

Apply an unambiguous correction to an unsettled recent entry immediately, recalculate its shares and balances, preserve the prior value, and report the result.

Confirm only when multiple records match or the action is bulk/destructive. Do not automatically modify a settled record in V1; tell the user it is already settled and leave it unchanged.

Explicit rule changes such as “以后默认我和同行人B” execute immediately with a short receipt.

Void an entry that never happened. Do not erase its history.

## Query and settle

Report separately:

- total trip consumption: active expenses only;
- member burden;
- member paid amount;
- open balance.

Before settlements:

`net(member) = merchant_paid(member) - burden(member)`

Positive means should receive; negative means owes.

For a settlement transfer `sender → receiver` of amount `s`:

- `net(sender) = net(sender) + s`
- `net(receiver) = net(receiver) - s`.

Store settlement with `from_member`, `to_member`, amount, currency/base amount, and time. Settlement is not consumption. Any reported transfer amount may be recorded; then recompute remaining balances.

For “谁欠谁”:

1. calculate member nets including recorded settlements;
2. verify all nets sum to zero;
3. generate a deterministic, easy-to-follow transfer plan;
4. never claim mathematical minimum without an exact algorithm;
5. leave suggestions unrecorded until the user reports payment.

If asked “我花了多少”, answer with burden first and also show paid amount. Exclude exchange, top-up, settlement, and voided records.

## After every write

Persist the record, member shares, wallet movement if any, and prior-value history as one logical action. Use a message ID/idempotency key when available.

Return what was recorded, who paid, who bears how much, whether it counts as consumption, and any useful balance implication. Keep receipts short.

## End of trip

On request provide total/category consumption, each member's paid amount and burden, personal/shared/treat breakdown, unresolved estimated conversions, current settlement plan, and the host-supported ledger location/exports.

Keep the ledger available for simple late corrections and settlement transfers.
