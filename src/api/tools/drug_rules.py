# write a function to return a list of drug qualification rules
def fetch_drug_rules(drug: str):
    rules = [
        {"rule": "Patient must be 18 years or older", "logical": "AND"},
        {"rule": "Patient must have a confirmed diagnosis of Type 2 diabetes", "logical": "AND"},
        {"rule": "Patient must have an A1C level of 7.0% or higher", "logical": "AND"}
    ]
    return " ".join([f"{rule['rule']} {rule['logical']}" if i < len(rules) - 1 else rule['rule'] for i, rule in enumerate(rules)])