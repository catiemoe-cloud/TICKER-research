# Apple Peer P/E Comparison — September 17, 2026

## Scope and unresolved policy item

Target: Apple (AAPL). Comparison date: **September 17, 2026**. All three prices below are closing prices for that date; annual GAAP diluted EPS had to be public by that date.

No peer-policy text or pre-approved candidate list was included with this request. Microsoft and Alphabet are therefore **qualified leads, not ranked recommendations**. They are included only because they are listed operating companies with platform, software, services, cloud, and/or device activities relevant to Apple; their material business-model differences remain important limitations.

## Sources opened and candidate decisions

| Company | Status | Primary-source business support | Important difference from Apple | Latest annual GAAP diluted EPS public by Sep. 17, 2026 | Fiscal period / publication date | Sep. 17 close and locator |
|---|---|---|---|---:|---|---|
| Apple (AAPL), target | Target; excluded from peer set | [Apple FY2025 10-K, Item 1—Business](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm): designs, manufactures, and markets devices and related services. | Target; not eligible as its own peer. | $7.46 | FY ended Sep. 27, 2025; 10-K filed Oct. 31, 2025. [Filing index](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/0000320193-25-000079-index.htm) | $337.00. [Historical-price locator](https://www.financecharts.com/stocks/AAPL/summary/price) |
| Microsoft (MSFT) | Qualify | [Microsoft FY2026 10-K](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm): Productivity and Business Processes, Intelligent Cloud, and More Personal Computing segments. | Much more enterprise software and cloud-subscription exposure; less consumer-device dependence than Apple. | $17.95 | FY ended Jun. 30, 2026; 10-K published Jul. 29, 2026. [Microsoft SEC-filings page](https://microsoft.gcs-web.com/financial-information/sec-filings) | $497.75. [Historical-price locator](https://www.financecharts.com/stocks/MSFT/summary/price) |
| Alphabet (GOOGL) | Qualify | [Alphabet FY2025 10-K, Item 1—Business](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm): Google Services, Google Cloud, and Other Bets. | Advertising is its primary monetization engine, unlike Apple’s hardware-led sales and services ecosystem. | $10.81 | FY ended Dec. 31, 2025; 10-K filed Feb. 5, 2026. [Filing index](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/0001652044-26-000018-index.htm) | $347.33. [Historical-price locator](https://www.financecharts.com/stocks/GOOGL/summary/price) |

No additional candidates were excluded because no candidate list or peer policy was provided. This omission is unresolved and should be checked before treating the pair as a final peer set.

## Peer P/E output

Run:

```bash
python3 peer_valuation.py
```

The script uses only the two qualified candidates above and retains unrounded multiples internally.

| Item | Result |
|---|---:|
| Microsoft P/E | 27.729805x |
| Alphabet P/E | 32.130435x |
| Median peer P/E | 29.930120x |
| Apple implied range | $206.86–$239.69 |
| Apple at peer median | $223.28 |

## Validation and peer-removal interpretation

Manual Microsoft check: $497.75 / $17.95 = **27.729805x** before display rounding.

Microsoft has the lower P/E. Removing it leaves Alphabet’s higher multiple and raises the median-implied Apple value from $223.28 to $239.69, a change of **+$16.41**. With only one peer, the result is a reference estimate—not a range—because there is no cross-peer minimum and maximum.

The peer set was not altered to improve the valuation result. The business-model limitations above, rather than the output, are the reasons to revisit peer inclusion.

## DCF and peer comparison — Lab 08 table

| Method | Comparison date / inputs | Value per Apple share | Limitation |
|---|---|---:|---|
| FCFF DCF | Sep. 17, 2026 case; 7% five-year FCFF growth, 8% WACC, 3% terminal growth | $224.42 | Value is sensitive to growth, WACC, and the terminal-value assumption. At the $337.00 price, the reverse DCF requires a +9.9550 percentage-point shift to each explicit FCFF-growth rate. |
| Peer P/E | Sep. 17, 2026 closes; Microsoft and Alphabet annual GAAP diluted EPS | $206.86–$239.69; median $223.28 | Neither peer is a close hardware-led business-model match for Apple. |
| Market price | Sep. 17, 2026 | $337.00 | Price is not an intrinsic-value estimate. |

**Provisional call: watch—defer.** Both the base DCF and qualified-peer P/E results are below the observed market price. This is provisional because the peer policy was not provided and the candidates have material revenue-mix differences.

## Skeptical-colleague review prompt and response

Prompt: “Review my valuation comparison as a skeptical colleague. Identify the weakest supported assumption and any mismatch in company, date, valuation object or earnings definition. Do not invent a missing range or average the methods. Ask one question that could change my decision.”

Response: The weakest supported assumption is peer comparability: Microsoft’s enterprise/cloud mix and Alphabet’s advertising-led model are not close to Apple’s hardware-led ecosystem, so their P/E multiples may not transfer cleanly. The dates match September 17, 2026 and the earnings definitions are annual GAAP diluted EPS, but Apple’s FY2025 ends in September while Microsoft’s FY2026 ends in June and Alphabet’s FY2025 ends in December; the fiscal periods are not identical. Question: **Does the course peer policy permit diversified software/advertising platforms for a hardware-led target, or require a more direct device manufacturer?**

## Partner conclusion

Microsoft and Alphabet belong only as qualified operating-company leads, not as interchangeable versions of Apple. Both operate large technology platforms with software, services, cloud, devices, and AI investment; that provides some evidence about how the market values durable technology ecosystems. Microsoft differs because enterprise software and cloud subscriptions are much more important to its economics. Alphabet differs because advertising is its primary monetization engine. Those differences are why the comparison remains a limitation rather than a claim that either company is a close Apple peer.

The P/E comparison adds an independent market-based check to the FCFF DCF. The two qualified peers imply $206.86–$239.69 per Apple share, with a $223.28 median, while the base FCFF DCF is $224.42. I do not average those methods: the DCF is based on Apple cash-flow assumptions, and P/E is only a transfer of imperfect peers’ market multiples. The two results happen to point to a similar lower valuation region, but that agreement does not remove the assumptions behind either method.

**Decision: watch—defer.** The defensible peer-based range is $206.86–$239.69 and the base DCF value is $224.42, both below the September 17, 2026 price of $337.00. This conclusion is provisional, not a declaration that the market is wrong, because the peer policy was not supplied and the two candidates have important business-model differences.

I would reconsider if either (1) the course policy confirms that these diversified platform peers are acceptable or identifies more directly comparable device-led companies, (2) sourced evidence supports a sustainably higher Apple cash-flow-growth or margin path, or (3) the market price moves into the DCF/peer valuation region without a deterioration in Apple’s operating outlook. I would also revisit the conclusion if updated annual GAAP EPS or a matching-date price changes the P/E inputs.

**Answer to the skeptical question:** without an explicit peer policy, I cannot verify that Microsoft and Alphabet are final acceptable peers. For this lab, they should remain qualified leads and their P/E range should be presented with its comparability limitation; I would not add, remove, or substitute a peer merely to obtain a preferred valuation result.

## Lab 08 rubric self-assessment

| Criterion | Evidence in this submission | Score | Reason |
|---|---|---:|---|
| Problem/decision | Apple and the September 17, 2026 valuation date are explicit before selection. | 2 | The underlying peer-policy text was not supplied; this important boundary is unresolved. |
| Data/evidence | Two candidate decisions cite opened primary annual-report sources; price and annual GAAP diluted-EPS bases are recorded. | 5 | Sources, periods, publication dates, and differences are stated. |
| Validation | Microsoft P/E is checked by hand; both removal results are calculated and interpreted. | 5 | The changed-peer effect and loss of range information are explained. |
| Financial judgment | The DCF and peer outputs sit side by side with a conditional watch—defer call. | 4 | The call is soundly limited, but peer-policy uncertainty prevents a fully supported conclusion. |
| Explanation/transfer | The memo gives causal peer differences and responds to the skeptical critique without averaging methods. | 4 | The judgment is owned and source-linked, with the policy gap still unresolved. |

The missing peer policy is one underlying defect and is scored once under **Problem/decision**, not repeatedly as separate failures in other rows.
