# write a function to return a list of drug qualification rules
def fetch_drug_rules(drug: str):
    rules = [
        {"rule": "Patient must be 18 years or older", "logical": "AND"},
        {"rule": "Patient must have a confirmed diagnosis of Type 2 diabetes", "logical": "AND"},
        {"rule": "Patient must have an A1C level of 7.0% or higher", "logical": "AND"},
        {"rule": "Patient must have a fasting plasma glucose (FPG) greater than or equal to 126 mg/dL", "logical": "OR"},
        {"rule": "Patient must have a 2-hour plasma glucose (PG) greater than or equal to 200 mg/dL during OGTT (oral glucose tolerance test)", "logical": "OR"},
        {"rule": "Patient must have a random plasma glucose greater than or equal to 200 mg/dL in patient with classic symptoms of hyperglycemia or hyperglycemic crisis", "logical": "OR"}
    ]
    return " ".join([f"{rule['rule']} {rule['logical']}" if i < len(rules) - 1 else rule['rule'] for i, rule in enumerate(rules)])