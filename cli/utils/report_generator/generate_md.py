import pandas as pd


def generate_md(df: pd.DataFrame, output_path: str) -> str:
    # Bastet Markdown Template
    BASTET_TEMPLATE = """
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
{{SEVERITY_ROWS}}

<div style="page-break-before: always;"></div>

# Findings
{{FINDINGS}}

"""

    severity_counter = dict()
    findings = ""

    # Check if DataFrame is empty
    if df.empty:
        print("⚠️ DataFrame is empty, cannot generate report")
        exit(1)

    # Check if required columns exist
    required_columns = {
        "File Name",
        "Summary",
        "Severity",
        "Vulnerability",
        "Recommendation",
    }
    missing = required_columns - set(df.columns)
    if missing:
        print(f"❌ Missing required columns: {', '.join(missing)}")
        exit(1)

    # Get file name
    file_name = str(df["File Name"].iloc[0]).strip()

    # Process findings and count severity levels
    for _, row in df.iterrows():

        severity = str(row["Severity"]).strip().lower()
        summary = str(row["Summary"]).strip()
        recommendation = str(row["Recommendation"]).strip()

        vulnerability_function_name = row["Vulnerability"].function_name
        vulnerability_description = row["Vulnerability"].description
        vulnerability_code_snippet = row["Vulnerability"].code_snippet

        # Update severity count
        severity_counter[severity] = severity_counter.get(severity, 0) + 1

        # Append finding entry to the Markdown block
        findings += f"""### {summary}
* **Severity**: {severity.capitalize()}
* **Vulnerability**: 
* * **Function Name**: {vulnerability_function_name}
* * **Description**: {vulnerability_description}
* * **Code Snippet**: 
```
{row["Vulnerability"].code_snippet}
```
* **Recommendation**: 
{recommendation}

---

"""

    # Build severity table rows
    severity_levels = ["high", "medium", "low", "informational"]
    severity_rows = ""

    for level in severity_levels:
        count = severity_counter.get(level, 0)
        severity_rows += f"| {level.capitalize():<13} | {count:^5} |\n"

    total_vulnerabilities = sum(severity_counter.values())
    severity_rows += f"| **Total**     | {total_vulnerabilities:^5} |"

    # Replace placeholders in the template
    result = (
        BASTET_TEMPLATE.replace("{{FILE_NAME}}", file_name)
        .replace("{{SEVERITY_ROWS}}", severity_rows)
        .replace("{{FINDINGS}}", findings)
    )

    # Write to file if an output path is specified
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

    return result
