# Conversation Examples

## First activation

Agent: 我可以帮你管一趟多人旅行的账：先确认同行人，再创建一份你能直接打开的账本。之后你只要自然语言报账；每笔都有回执，记错也能改。准备好时说“我要去 XX 旅行，帮我记账”就行。

## Start with destination only

User: 我要去韩国旅行，帮我记账。
Agent: 可以，同行人都有谁？

User: 我、同行人 A、同行人 B、同行人 C。
Agent: 我建议创建一份你能直接打开的 Excel 账本，保存在“文档/旅行账本”，以后每笔都会自动同步，可以吗？

User: 可以。
Agent: 你已经换韩元现金了吗？会用或已经充值 T-money 吗？

## Identity already known

User: 我和同行人 A 去韩国，帮我记账。
Agent: Do not ask which name is the user. Proceed to readable-ledger recommendation.

## Identity ambiguous

User: 同行人是甲、乙、丙。
Agent: 这三个名字里哪个是你？

## No foreign cash

User: 没换现金，也不用 T-money。
Agent: Create no wallet. Create and verify the readable ledger.

## Foreign cash

User: 换了 10 万韩元，花了 500 人民币。
Agent: Create KRW cash wallet with Q=100000 and C=500; exchange is not consumption.

## Foreign expense missing source

User: 同行人 A 付了 30000 韩元吃饭，四个人。
Agent: 同行人 A 是用韩元现金、T-money，还是信用卡/线上支付？

## Ordinary entry

User: 我付了晚饭 240，四个人 AA。
Agent: 已记：晚饭 ¥240｜你付款｜四人 AA，各 ¥60｜账本已更新。

## Mixed shared/personal

User: 我付了晚饭 240，其中 60 是我自己的酒，剩下四个人平分。
Agent: Split into shared dinner ¥180 and personal drink ¥60, both paid by the user.

## Correction

User: 刚才那笔其实只有我和同行人 A。
Agent: Update the uniquely matched recent unsettled record, recalculate, sync, and return the result.

## Settlement query

User: 现在谁欠谁？
Agent: Show an easy-to-follow transfer plan. Do not record it until the user reports an actual transfer.
