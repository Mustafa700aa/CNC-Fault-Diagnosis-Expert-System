from models import Diagnosis
from typing import Dict, Any

class ExplanationSubsystem:
    """SRP: Generates a clear, structured reasoning trace for the UI."""
    def __init__(self, raw_data: Dict[str, float], working_memory: Dict[str, str], diagnosis: Diagnosis):
        self.raw_data = raw_data
        self.working_memory = working_memory
        self.diagnosis = diagnosis

    def get_symptom_analysis(self) -> Dict[str, str]:
        return {
            "Spindle Temperature": f"{self.raw_data['temp']}°C ➔ `{self.working_memory['Spindle_Temp']}`",
            "Spindle Vibration": f"{self.raw_data['vib']} mm/s ➔ `{self.working_memory['Spindle_Vib']}`",
            "Cooling Pressure": f"{self.raw_data['cool_press']} PSI ➔ `{self.working_memory['Cool_Press']}`",
            "Cooling Flow Rate": f"{self.raw_data['cool_flow']} L/min ➔ `{self.working_memory['Cool_Flow']}`",
            "Hydraulic Pressure": f"{self.raw_data['hyd_press']} Bar ➔ `{self.working_memory['Hyd_Press']}`",
            "Electrical Load": f"{self.raw_data['curr_load']} A ➔ `{self.working_memory['Curr_Load']}`",
            "Tool Condition (Vision)": f"{self.raw_data['tool_cond']} ➔ `{self.working_memory['Tool_Cond']}`",
        }
    
    def get_rule_mapping(self) -> Dict[str, str]:
        return {
            "Triggered Rule": self.diagnosis.rule_id,
            "Conditions Met": self.diagnosis.antecedents_desc
        }
        
    def get_confidence_assessment(self) -> str:
        if isinstance(self.diagnosis.cf, str):
            return "N/A"
        return f"{self.diagnosis.cf} ({(float(self.diagnosis.cf) * 100):.0f}%)"
