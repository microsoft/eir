from langchain_core.tools import tool as original_tool

def tool(func):
    func = original_tool(func)
    func._is_tool = True
    return func

@tool
def get_patient_notes(patient_id: str):
    """Get patient chart notes by patient ID."""
    return {
        "id": patient_id,
        "notes": "Patient was diagnosed with Type 2 diabetes on 2023-01-09. Patient has an A1C level of 9.5%."
    }
    
@tool
def get_patient_data(patient_id: str):
    """Get demographic patient data by patient ID."""
    return {
        "id": patient_id,
        "name": "John Doe",
        "birthdate": "2010-01-05"
    }