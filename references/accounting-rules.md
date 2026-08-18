# Accounting Rules

## Split

V1 supports equal split, personal, treat, paid separately, and explicit custom amounts.

Use integer minor units or exact decimals. The sum of shares must equal the expense exactly. Assign unavoidable residual to the participating payer first, then stable member order.

## Net

Before member settlements:

`net(member) = merchant_paid(member) - burden(member)`

Positive means should receive; negative means owes. Sum of all member nets must equal zero.

For settlement `sender -> receiver` amount `s`:

- `net(sender) += s`
- `net(receiver) -= s`

Settlement is not consumption.

## Foreign weighted-cost wallet

Store remaining foreign quantity `Q` and remaining base-currency cost `C`.

Exchange base amount `c` into foreign amount `q`:

- `Q_new = Q_old + q`
- `C_new = C_old + c`

Spend foreign amount `x`:

- require `x <= Q_old`;
- if `x == Q_old`, base cost is all `C_old`;
- otherwise base cost is `round_minor(x * C_old / Q_old)`;
- subtract `x` and its base cost.

Transfer `x` from wallet A to wallet B:

- if `x == Q_A`, move all remaining cost;
- otherwise move `round_minor(x * C_A / Q_A)`;
- subtract quantity/cost from A and add them to B.

Exchange and top-up are transfers, not consumption. If a wallet balance is insufficient, ask for the actual payment source.
