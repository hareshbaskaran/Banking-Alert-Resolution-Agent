def extract_finding_values(findings: dict) -> dict:
    """Extracts the 'value' field from each finding in the findings dictionary."""
    return {
        k: v["value"] if isinstance(v, dict) else v
        for k, v in findings.items()
    }