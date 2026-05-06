from typing import Any, Dict

class DataDiscretizer:
    """SRP: Responsible only for converting continuous data to symbolic facts."""
    
    @staticmethod
    def discretize_spindle_temp(temp: float) -> str:
        if temp <= 65: return 'Normal'
        if temp < 110: return 'Elevated'
        return 'High'

    @staticmethod
    def discretize_spindle_vib(vib: float) -> str:
        if vib <= 1.5: return 'Normal'
        if vib < 4.5: return 'Moderate'
        return 'High'
        
    @staticmethod
    def discretize_hyd_press(press: float) -> str:
        if press >= 100: return 'Normal'
        if press <= 20: return 'Critical_Drop'
        return 'Low'

    @staticmethod
    def discretize_cool_press(press: float) -> str:
        if press >= 25: return 'Normal'
        if press <= 10: return 'Low'
        return 'Warning'

    @staticmethod
    def discretize_cool_flow(flow: float) -> str:
        if flow >= 10: return 'Normal'
        if flow <= 5: return 'Severely_Low'
        return 'Low'

    @staticmethod
    def discretize_curr_load(current: float) -> str:
        if current <= 15: return 'Normal'
        if current <= 25: return 'High_Draw'
        return 'Surge'

    @classmethod
    def discretize(cls, raw_data: Dict[str, Any]) -> Dict[str, str]:
        return {
            'Spindle_Temp': cls.discretize_spindle_temp(raw_data['temp']),
            'Spindle_Vib': cls.discretize_spindle_vib(raw_data['vib']),
            'Hyd_Press': cls.discretize_hyd_press(raw_data['hyd_press']),
            'Cool_Press': cls.discretize_cool_press(raw_data['cool_press']),
            'Cool_Flow': cls.discretize_cool_flow(raw_data['cool_flow']),
            'Curr_Load': cls.discretize_curr_load(raw_data['curr_load']),
            'Tool_Cond': raw_data['tool_cond'],
        }
