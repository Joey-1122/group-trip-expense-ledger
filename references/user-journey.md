# User Journey

## A. First activation

Goal: make the user understand what the Skill does and feel safe starting.

- Do not create storage.
- Do not ask trip setup questions before the user expresses a trip intent.
- Explain readable ledger, natural-language entry, receipts, and corrections.
- Give one start phrase.

Pass condition: a non-technical user knows what to say next and knows they will receive a ledger they can open.

## B. Start a domestic trip

1. User expresses trip intent.
2. Ask missing traveler list.
3. Resolve current user only if ambiguous.
4. Recommend one readable ledger and ask approval.
5. Create, verify, and hand off.

Pass condition: no foreign-money questions and no redundant identity question.

## C. Start a foreign trip

1. Resolve travelers.
2. Recommend readable ledger and receive approval.
3. Ask foreign cash and local stored-value preparation.
4. Create only real wallets.
5. Create, verify, and hand off.

Pass condition: no invented foreign balance, no payment-method questionnaire.

## D. Daily entry

1. Parse statement and defaults.
2. Ask only a money-changing missing fact.
3. Calculate.
4. Update source and readable view.
5. Return receipt.

## E. Correction

1. Resolve exactly one record.
2. Modify or void.
3. Recalculate.
4. Sync readable view.
5. Return before/after result.

## F. Query and settlement

1. Separate burden, merchant payment, and open net.
2. Suggest transfers without recording them.
3. Record only reported transfers.
4. Recalculate and sync.

## Failure behavior

Never claim success if creation, persistence, reopening, or readable-view synchronization fails. State what succeeded, what failed, and the next recoverable action.
