# Re7 social automation: run 20261105_134559

Model: `claude-sonnet-5-5` · 5 logged API calls in `ai/` · 114 posts · 6 sources

## Coverage

| Entity | Channel | Posts | With metric | How |
|---|---|---:|---:|---|
| Capital | LinkedIn | 45 | 45 | import (screenshot capture) |
| Capital | Telegram | 0 | 0 | no public channel found |
| Capital | X | 31 | 30 | import (screenshot capture) |
| Labs | LinkedIn | 7 | 7 | import (screenshot capture) |
| Labs | Telegram | 20 | 20 | scraped t.me/s/re7labsalpha |
| Labs | X | 11 | 11 | import (screenshot capture) |

## Channel baselines (ranked posts only)

| Entity | Channel | Metric | n | Median | Min | Max |
|---|---|---|---:|---:|---:|---:|
| Capital | LinkedIn | reactions | 45 | 7 | 1 | 34 |
| Capital | X | views | 23 | 374 | 240 | 3,300 |
| Labs | LinkedIn | reactions | 6 | 8 | 1 | 35 |
| Labs | Telegram | views | 19 | 238 | 120 | 354 |
| Labs | X | views | 6 | 1,300 | 630 | 9,000 |

## Theme x format

| Entity | Channel | Theme | Format | n | Median | Median pct | Status |
|---|---|---|---|---:|---:|---:|---|
| Capital | LinkedIn | Media & events | image | 3 | 28 reactions | 93.2 | ok |
| Capital | LinkedIn | Market commentary | link post | 1 | 23 reactions | 88.6 | too few to call |
| Capital | LinkedIn | Research insight | image | 2 | 22 reactions | 86.3 | too few to call |
| Capital | LinkedIn | Company news | image | 1 | 10 reactions | 70.5 | too few to call |
| Capital | LinkedIn | Media & events | video | 4 | 11 reactions | 68.2 | ok |
| Capital | LinkedIn | Media & events | link post | 10 | 8.5 reactions | 63 | ok |
| Capital | LinkedIn | Company news | link post | 3 | 8 reactions | 59.1 | ok |
| Capital | LinkedIn | Weekly promotion | image | 7 | 3 reactions | 28.4 | ok |
| Capital | LinkedIn | Research insight | chart/data visual | 6 | 3 reactions | 28.4 | ok |
| Capital | LinkedIn | Market commentary | chart/data visual | 1 | 2 reactions | 12.5 | too few to call |
| Capital | LinkedIn | Weekly promotion | link post | 7 | 2 reactions | 12.5 | ok |
| Capital | X | Research insight | image | 2 | 594.5 views | 88.7 | too few to call |
| Capital | X | Media & events | video | 2 | 1,738.5 views | 75 | too few to call |
| Capital | X | Media & events | image | 6 | 410 views | 56.8 | ok |
| Capital | X | Weekly promotion | link post | 2 | 398 views | 54.5 | too few to call |
| Capital | X | Research insight | chart/data visual | 3 | 374 views | 50 | ok |
| Capital | X | Weekly promotion | image | 6 | 310 views | 20.4 | ok |
| Capital | X | Media & events | link post | 1 | 301 views | 13.6 | too few to call |
| Capital | X | Company news | image | 1 | 259 views | 4.5 | too few to call |
| Labs | LinkedIn | Product & vault update | image | 2 | 19 reactions | 70 | too few to call |
| Labs | LinkedIn | Product & vault update | link post | 1 | 13 reactions | 70 | too few to call |
| Labs | LinkedIn | Education & explainer | video | 1 | 13 reactions | 70 | too few to call |
| Labs | LinkedIn | Company news | link post | 1 | 1 reactions | 10 | too few to call |
| Labs | LinkedIn | Education & explainer | image | 1 | 1 reactions | 10 | too few to call |
| Labs | Telegram | Media & events | link post | 1 | 354 views | 100 | too few to call |
| Labs | Telegram | Product & vault update | link post | 1 | 290 views | 88.9 | too few to call |
| Labs | Telegram | Product & vault update | image | 5 | 253 views | 66.7 | ok |
| Labs | Telegram | Research insight | image | 2 | 257.5 views | 66.7 | too few to call |
| Labs | Telegram | Weekly promotion | image | 10 | 201 views | 25 | ok |
| Labs | X | Risk & incident update | text-only | 1 | 2,700 views | 80 | too few to call |
| Labs | X | Product & vault update | image | 5 | 1,100 views | 40 | ok |

## Findings

**1. Media and events images lead Capital's LinkedIn results**  
Media & events image posts (3 posts) had a median of 28 reactions, at percentile 93. Video in the same theme (4 posts) sat at percentile 68, and link posts (10 posts) at percentile 63.  
*Action:* Next week, publish Capital's media and event announcements on LinkedIn as image posts rather than link posts.

**2. The Weekly promotion sits low on every channel**  
Weekly promotion images land at percentile 28 on Capital LinkedIn (7 posts), percentile 25 on Labs Telegram (10 posts) and percentile 20 on Capital X (6 posts). Capital LinkedIn link posts for the Weekly are lower again, at percentile 12 (7 posts).  
*Action:* Stop posting the Weekly as a plain title and bullet list. Test one post that leads with a single finding from the issue, and check it against these percentiles.

**3. On Telegram, Labs product updates beat the Weekly**  
Product & vault update images (5 posts) reached a median of 253 views, at percentile 67. Weekly promotion images (10 posts) reached 201 views, at percentile 25.  
*Action:* Give product and vault updates priority in Telegram slots, and cut the Weekly to fewer posts there.

**4. Labs X has one solid group and one early signal**  
Product & vault update images (5 posts) have a median of 1100 views, at percentile 40, so they are middling for Labs on X. The Binance incident text post reached 2700 views, but it is a single post and only an example.  
*Action:* Trial a short, plain-text risk update the next time there is a market event, and track it before treating it as a pattern.

## Drafts

### 1. Capital · X · finding 2

> Since crypto sentiment peaked on 21 September, total market capitalisation has declined just 7%, while Fear & Greed has fallen 38% on an indexed basis. Sentiment is pricing a larger correction than prices have delivered.
>
> https://re7research.substack.com/p/the-weekly-19th-october-2026

Format: Single chart image: total crypto market cap vs Fear & Greed, both indexed from 21 September  
Why: Leads The Weekly with one specific finding rather than a title and bullet list, as the Weekly-promotion finding recommends.  
Source: [The Weekly - 19th October 2026](https://re7research.substack.com/p/the-weekly-19th-october-2026)

### 2. Capital · X · finding 2

> On-chain trading card weekly volumes are approaching $100 million, against less than $20 million at the start of the year. Low transaction costs and integrations across Pump.fun, Jupiter and other Solana applications are widening distribution.
>
> https://re7research.substack.com/p/the-weekly-26th-october-2026

Format: Simple bar chart image: weekly on-chain trading card volume, start of year vs now  
Why: Opens with one number from the issue instead of a plain Weekly title, to test against the low Weekly percentiles on Capital X.  
Source: [The Weekly - 26th October 2026](https://re7research.substack.com/p/the-weekly-26th-october-2026)

### 3. Labs · X · finding 4

> The $6.3bn Binance exploit represented 3.7% of the exchange's $171bn in customer assets. Approximately $2.8bn was rapidly frozen by Circle, Tether and other issuers. Transparent onchain infrastructure made tracing possible, which contained the damage.
>
> https://re7research.substack.com/p/the-weekly-2nd-november-2026

Format: Plain text post, no image  
Why: A short, plain-text risk update on a market event, as the Labs X finding suggests trialling.  
Source: [The Weekly - 2nd November 2026](https://re7research.substack.com/p/the-weekly-2nd-november-2026)

### 4. Capital · LinkedIn · finding 1

> For Yuval Rooz, Co-Founder and CEO of Digital Asset, the company behind Canton Network, RWAs have always been the most compelling use case on-chain, and corporate treasury is where that becomes real.
>
> Speaking with Re7 Founder and CIO Evgeny Gokhberg on Crypto Minutes, Bloomberg TV, he said: “They’ll start doing treasury management using on-chain finance.”
>
> The conversation looks at the next phase of finance moving on-chain, and what it means for institutions that manage cash and liquidity every day.
>
> The full episode is linked below.
>
> https://re7research.substack.com/p/the-weekly-2nd-november-2026

Format: Image post: still from the Crypto Minutes episode with Yuval Rooz and Evgeny Gokhberg, quote overlaid; not a link post  
Why: A media appearance published as an image post rather than a link post, following the media and events finding.  
Source: [The Weekly - 2nd November 2026](https://re7research.substack.com/p/the-weekly-2nd-november-2026)

### 5. Capital · LinkedIn · finding 2

> Institutional adoption of crypto depends less on whether an investment committee likes Bitcoin and more on whether custody, compliance and fiduciary processes permit ownership.
>
> That was our reading of the SEC's proposed custody framework for advisers and regulated funds, which would permit self-custody in certain circumstances and state trust companies as custodians. The SEC describes the objective as giving advisers and funds a compliant pathway to crypto exposure.
>
> Removing those operational constraints expands the addressable pool of capital. The UK is moving in a similar direction, with the focus on how tokenisation fits within existing financial markets. Our team discussed the UK's tokenisation roadmap at the Cross-Border Fund Distribution Conference in London, alongside regulators, lawyers and asset managers.
>
> The full analysis is in The Weekly.
>
> https://re7research.substack.com/p/the-weekly-5th-october-2026

Format: Image post: photo from the Cross-Border Fund Distribution Conference in London with a one-line takeaway  
Why: Leads with a single finding from the issue and recaps the London conference as a past event, as both the Weekly and media and events findings suggest.  
Source: [The Weekly - 5th October 2026](https://re7research.substack.com/p/the-weekly-5th-october-2026)

### 6. Labs · LinkedIn · finding 2

> Institutional DeFi needs a common language for risk. That is the premise of A Framework for Decomposing DeFi Risk in the Age of AI, written in collaboration with Clear Street and led by Re7 Founder and CIO Evgeny Gokhberg.
>
> Built on our own methodology, the framework breaks exposure into chain, protocol and asset layers. Separating the layers matters because a single position can carry different risks at each one, and those risks are easier to assess when they are named separately. The report also explores how AI is reshaping risk monitoring.
>
> For curators and allocators alike, shared definitions make risk easier to compare, challenge and monitor. The report is available to download via the link below.
>
> https://re7research.substack.com/p/the-weekly-2nd-november-2026

Format: Image post: simple three-layer diagram (chain, protocol, asset) with the report title  
Why: Leads with one finding from the issue rather than a title and bullet list, as the Weekly finding recommends.  
Source: [The Weekly - 2nd November 2026](https://re7research.substack.com/p/the-weekly-2nd-november-2026)

### 7. Labs · Telegram · finding 3

> Vault recap for anyone who missed it: Re7 Labs launched a Frax USDai Ecosystem Vault on Mainnet with Frax Finance and USD.AI.
>
> The vault deploys frxUSD across curated opportunities in the USDai ecosystem, a collaboration between Re7 Labs, Frax Finance and USD.AI. It runs on Mainnet.
>
> Full detail is available via the link below.
>
> https://re7research.substack.com/p/the-weekly-19th-october-2026

Format: Vault update image: Frax USDai Ecosystem Vault graphic with partner names  
Why: Gives a vault update a Telegram slot, since product and vault images outperform the Weekly there, and frames the older launch as a recap.  
Source: [The Weekly - 19th October 2026](https://re7research.substack.com/p/the-weekly-19th-october-2026)

### 8. Labs · Telegram · finding 3

> Re7 DeFi Ratings is a risk management framework that evaluates smart contract and other DeFi risks to assign holistic ratings.
>
> Those ratings act as a key input into DeFi asset allocation models. They sit alongside the in-house risk tooling and research that Re7 Labs applies as a curator and advisor to a wide range of DeFi protocols.
>
> More on our products is available via the link below.
>
> https://re7labs.xyz/

Format: Product image: Re7 DeFi Ratings card with a short description  
Why: Prioritises a product update in Telegram slots, as the finding that product updates beat the Weekly recommends.  
Source: [Re7 Labs - Research & Innovation](https://re7labs.xyz/)

### 9. Labs · Telegram · finding 3

> Growing a DeFi ecosystem starts with liquidity and user experience. Re7 Labs works on ecosystem design with that focus, and works across all layers of DeFi, developing it from the ground up.
>
> Alongside this, we curate onchain risk, applying in-house risk tooling and research to support a wide range of DeFi protocols as a curator and advisor.
>
> To talk it through, reach out via the Re7 Labs website.
>
> https://re7labs.xyz/

Format: Product image: Re7 Labs solutions card covering risk curation, ecosystem design and building blocks  
Why: Uses a product-focused post in a Telegram slot instead of another Weekly promotion, following the Telegram finding.  
Source: [Re7 Labs - Research & Innovation](https://re7labs.xyz/)
