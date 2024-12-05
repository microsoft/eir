from langchain_core.tools import tool as original_tool

def tool(func):
    func = original_tool(func)
    func._is_tool = True
    return func

@tool
def get_patient_notes(patientId: str):
    """Get patient chart notes by patient ID available in the task details."""
    return {
        "id": patientId,
        "notes": "Patient was diagnosed with Type 2 diabetes on 2023-01-09. Patient has an A1C level of 9.5%."
    }
    
@tool
def get_patient_data(patientId: str):
    """Get demographic patient data by patient ID available in the task details."""
    return {
        "id": patientId,
        "name": "John Doe",
        "birthdate": "2010-01-05"
    }