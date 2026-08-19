# 外币模块（仅国际行加载）

trip profile 判定为国际行时才用本文件。国内行不加载。

## 折算总口径（真实用法沉淀）

- **现金 / 储值卡（Suica、八达通等）→ 走该资金池的实际加权成本，不用实时汇率。**
- **线上支付（信用卡、支付宝、微信、移动钱包）→ 用实时汇率，或用户给的实际本币扣款。**
- **换汇、充值、钱包间转移 → 资金转移，不计消费。**

一句判断：钱是从"预先换好/充好的池子"出的就走池成本；是"当场线上扣"的就走实时汇率。

## 钱包与资金池（只为真实资金创建，不虚构）

每个钱包记：`剩余外币量 Q`、`剩余本币成本 C`。

- **换汇** 本币 c 换外币 q：`Q += q`，`C += c`。成本汇率 = c / q。
- **花外币 x**（要求 x ≤ Q）：本币成本 = `x == Q ? C : round(x * C / Q)`；然后 `Q -= x`，`C -= 本币成本`。
- **转移 x**（钱包 A→B，如现金充进 Suica）：搬走的成本 = `x == Q_A ? C_A : round(x * C_A / Q_A)`；A 减、B 加。

余额不足以支撑一笔外币消费时，别硬扣——问用户这笔实际用什么付。

## 实时汇率接口（写死进 skill，免临时检索、免密钥）

取"1 外币 = ? CNY"，直接就是要锁定的实时汇率。

```bash
# 主：读外币文件里的 .cny 字段。{foreign} 用小写币种码：jpy krw thb vnd twd usd sgd hkd ...
curl -s "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{foreign}.json"
# 解析路径：.{foreign}.cny

# 备用域名（jsDelivr 不可达时，结构相同）：
curl -s "https://latest.currency-api.pages.dev/v1/currencies/{foreign}.json"

# 补记历史某天的汇率：把 @latest 换成 @YYYY-MM-DD
curl -s "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@2026-08-18/v1/currencies/jpy.json"

# 交叉验证备选（想要 ECB 权威数；只约 30 种主要币种，缺 VND/TWD）：
curl -s "https://api.frankfurter.dev/v1/latest?base=JPY&symbols=CNY"   # -> {"rates":{"CNY":0.04222}}
```

选 fawazahmed0/jsDelivr 为主：免密钥、CDN 稳定（国内一般可达）、覆盖全部币种（含越南盾 VND、台币 TWD，这两个 ECB 没有）。

宿主无关：任何能发 HTTP GET 的宿主（OpenClaw web fetch、Coze HTTP 节点、WorkBuddy）都能用，解析同一 JSON。

**兜底不阻塞**：主域名失败 → 备用域名 → 仍失败或宿主无 HTTP 能力 → 问用户实际本币扣款，或标"估算"。**绝不因为查不到汇率就卡住记账。**

## 信用卡 / 线上外币消费

1. 用户给了实际本币扣款 → 直接用，`金额状态 = 锁定`。
2. 否则用记账当时实时汇率折算并**锁定**，记 `汇率来源=实时汇率(fawazahmed0)`、`汇率日期`、`汇率值`（满足 SKILL 不变量 3 的可追溯）。
3. 没有可靠汇率 → 问用户或明确标"估算"。
4. 用户希望等信用卡真实出账再定 → 记为 `金额状态 = 待出账` 占位，先用估算参与分账；出账后**只更新待出账记录**为实际本币（可能是 USD 等其它币种，按当天实时汇率折算），锁定。**已锁定的记录不回头改**（不变量 3）。

## 补记（backfill）

用户补记过去某天的消费时，日期用**显式过去日期**，不用当天；需要汇率就用该日期的历史汇率接口。

## 标题

用户说了具体买了什么，就写进标题（如"镰仓一日电车券"而非"车票"），至少写进备注；不要只写"午饭/晚饭"。

## 目的地支付方式对照表

onboarding 时按目的地主动问该充的卡；记账时据此识别支付来源走哪条口径。储值/交通卡走资金池成本，线上/移动支付走实时汇率或实际扣款。

| 地区 | 储值/交通卡 → 资金池成本 | 常见线上/移动支付 → 实时汇率或实际扣款 |
|---|---|---|
| 日本 | Suica、PASMO、ICOCA | 信用卡、PayPay、现金 |
| 香港 | 八达通 Octopus | 信用卡、AlipayHK、支付宝/微信跨境 |
| 澳门 | 澳门通 | 信用卡、MPay |
| 台湾 | 悠游卡 EasyCard、一卡通 iPASS | 信用卡、LINE Pay |
| 韩国 | T-money、Cashbee | 信用卡、KakaoPay、Naver Pay |
| 新加坡 | EZ-Link、SimplyGo | 信用卡、PayNow |
| 泰国 | Rabbit 卡(BTS) | 信用卡、PromptPay、TrueMoney |
| 英国 | Oyster(伦敦) | 信用卡 contactless |
| 欧洲通用 | 各城市交通卡 | 信用卡 contactless |
| 美国 | Clipper / MetroCard 等 | 信用卡、Apple Pay |

正向规则：表里没有的卡也照判——是储值卡（先充值=资金转移，消费按池成本）还是线上支付（走实时汇率）；拿不准追问一句。移动钱包默认按线上支付，除非用户说明从某资金池出。
