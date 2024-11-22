from langchain_core.tools import tool

@tool
def get_patient_notes(patient_id: str):
    """Get patient notes by patient ID."""
    return {
        "id": patient_id,
        "notes": "Patient was diagnosed with Type 2 diabetes on 2023-01-09. Patient has an A1C level of 9.5%."
    }
    
@tool
def get_patient_data(patient_id: str):
    """Get patient data by patient ID."""
    return {
        "id": patient_id,
        "name": "John Doe",
        "birthdate": "2001-01-05"
    }