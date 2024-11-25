# write a function to return a list of drug qualification rules
def fetch_drug_rules(drug: str):
    return [
        {"rule": "Patient must be 18 years or older", "logical": "AND"},
        {"rule": "Patient must have a confirmed diagnosis of Type 2 diabetes", "logical": "AND"},
        {"rule": "Patient must have an A1C level of 7.0% or higher", "logical": "AND"}
    ]
        