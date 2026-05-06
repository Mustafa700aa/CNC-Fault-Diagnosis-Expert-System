from models import Rule
from typing import List

class KnowledgeBase:
    """SRP: Stores and provides the rules. Closed for modification, open for extension."""
    def __init__(self):
        self.rules = self._initialize_rules()

    def _initialize_rules(self) -> List[Rule]:
        return [
            # Salience 3: Emergency
            Rule('Rule 24 (Emergency)', 3, lambda wm: wm.get('Tool_Cond') == 'Broken' and wm.get('Curr_Load') == 'Surge', 'Severe Jam / Motor Stall', 'Emergency', 'E-STOP IMMINENT; Replace tool and reset spindle drive.', 1.0, 'Tool is Broken and Current is Surge'),
            Rule('Rule 23 (Emergency)', 3, lambda wm: wm.get('Hyd_Press') == 'Critical_Drop' and wm.get('Spindle_Temp') == 'High', 'Catastrophic Heat & Pressure Loss', 'Emergency', 'SYSTEM SHUTDOWN; Major line rupture suspected.', 0.98, 'Hydraulic Pressure is Critical Drop and Spindle Temp is High'),
            Rule('Rule 22 (Emergency)', 3, lambda wm: wm.get('Curr_Load') == 'Surge' and wm.get('Spindle_Vib') == 'High', 'Motor Phase Fault / Bearing Collapse', 'Emergency', 'E-STOP; Isolate power and inspect spindle assembly.', 0.99, 'Current is Surge and Vibration is High'),
            Rule('Rule 21 (Emergency)', 3, lambda wm: wm.get('Spindle_Temp') == 'High' and wm.get('Cool_Flow') == 'Severely_Low', 'Coolant Dry-out Overheating', 'Emergency', 'HALT MACHINING; Refill coolant and clear lines.', 0.95, 'Spindle Temp is High and Coolant Flow is Severely Low'),
            Rule('Rule 20 (Emergency)', 3, lambda wm: wm.get('Tool_Cond') == 'Broken', 'Tool Breakage Detected', 'Emergency', 'STOP CYCLE; Retract spindle and replace broken tool.', 0.95, 'Tool Condition is Broken'),
            Rule('Rule 19 (Emergency)', 3, lambda wm: wm.get('Curr_Load') == 'Surge', 'Spindle Motor Surge', 'Emergency', 'SHUTDOWN; Inspect motor for electrical short or jam.', 0.90, 'Current Load is Surge'),
            Rule('Rule 18 (Emergency)', 3, lambda wm: wm.get('Hyd_Press') == 'Critical_Drop', 'Hydraulic Failure', 'Emergency', 'SHUTDOWN; Inspect hydraulic pump and hoses.', 0.92, 'Hydraulic Pressure is Critical Drop'),
            Rule('Rule 17 (Emergency)', 3, lambda wm: wm.get('Tool_Cond') == 'Broken' and wm.get('Spindle_Vib') == 'High', 'Catastrophic Tool Failure', 'Emergency', 'E-STOP; Clear debris and replace tool.', 1.0, 'Tool Condition is Broken and Vibration is High'),
            
            # Salience 2: Critical
            Rule('Rule 16 (Critical)', 2, lambda wm: wm.get('Spindle_Vib') == 'Moderate' and wm.get('Spindle_Temp') == 'High', 'Severe Bearing Wear', 'Critical', 'Stop operation; Schedule immediate bearing replacement.', 0.88, 'Vibration is Moderate and Spindle Temp is High'),
            Rule('Rule 15 (Critical)', 2, lambda wm: wm.get('Cool_Press') == 'Low' and wm.get('Cool_Flow') == 'Low', 'Coolant Pump Degradation', 'Critical', 'Pause cycle; Check coolant pump intake and filter.', 0.85, 'Coolant Pressure is Low and Flow is Low'),
            Rule('Rule 14 (Critical)', 2, lambda wm: wm.get('Tool_Cond') == 'Worn' and wm.get('Curr_Load') == 'High_Draw', 'Dull Tool Motor Strain', 'Critical', 'Change tool before next pass to prevent overload.', 0.82, 'Tool is Worn and Current is High Draw'),
            Rule('Rule 13 (Critical)', 2, lambda wm: wm.get('Hyd_Press') == 'Low' and wm.get('Spindle_Temp') == 'Elevated', 'Hydraulic Overheating', 'Critical', 'Check hydraulic fluid level and heat exchanger.', 0.80, 'Hydraulic Pressure Low and Spindle Temp Elevated'),
            Rule('Rule 12 (Critical)', 2, lambda wm: wm.get('Spindle_Vib') == 'High', 'Unbalanced Spindle / Crash Risk', 'Critical', 'Stop spindle; Check workpiece clamping and balance.', 0.85, 'Spindle Vibration is High'),
            Rule('Rule 11 (Critical)', 2, lambda wm: wm.get('Spindle_Temp') == 'High', 'Spindle Overheating', 'Critical', 'Stop spindle; Allow to cool and check chiller.', 0.85, 'Spindle Temp is High'),
            Rule('Rule 10 (Critical)', 2, lambda wm: wm.get('Cool_Flow') == 'Severely_Low', 'Coolant Starvation', 'Critical', 'Pause program; Clean coolant nozzles.', 0.90, 'Coolant Flow is Severely Low'),
            Rule('Rule 09 (Critical)', 2, lambda wm: wm.get('Curr_Load') == 'High_Draw' and wm.get('Cool_Press') == 'Low', 'Overworked Tool / Low Coolant', 'Critical', 'Reduce feed rate; Check coolant pressure.', 0.80, 'Current is High Draw and Coolant Pressure is Low'),
            
            # Salience 1: Warning
            Rule('Rule 08 (Warning)', 1, lambda wm: wm.get('Tool_Cond') == 'Worn' and wm.get('Spindle_Vib') == 'Moderate', 'Tool Induced Chatter', 'Warning', 'Plan tool change soon; Decrease feed rate.', 0.75, 'Tool is Worn and Vibration is Moderate'),
            Rule('Rule 07 (Warning)', 1, lambda wm: wm.get('Cool_Flow') == 'Low', 'Suboptimal Coolant Flow', 'Warning', 'Check coolant level and top off if necessary.', 0.60, 'Coolant Flow is Low'),
            Rule('Rule 06 (Warning)', 1, lambda wm: wm.get('Cool_Press') == 'Warning', 'Coolant Pressure Drop', 'Warning', 'Inspect coolant filter for partial clogs.', 0.60, 'Coolant Pressure is Warning'),
            Rule('Rule 05 (Warning)', 1, lambda wm: wm.get('Hyd_Press') == 'Low', 'Hydraulic Pressure Sag', 'Warning', 'Monitor hydraulic system for minor leaks.', 0.65, 'Hydraulic Pressure is Low'),
            Rule('Rule 04 (Warning)', 1, lambda wm: wm.get('Curr_Load') == 'High_Draw', 'Increased Cutting Resistance', 'Warning', 'Monitor motor load; Consider reducing cut depth.', 0.70, 'Current Load is High Draw'),
            Rule('Rule 03 (Warning)', 1, lambda wm: wm.get('Spindle_Vib') == 'Moderate', 'Minor Imbalance / Chatter', 'Warning', 'Verify workpiece rigidity and tool runout.', 0.65, 'Spindle Vibration is Moderate'),
            Rule('Rule 02 (Warning)', 1, lambda wm: wm.get('Spindle_Temp') == 'Elevated', 'Elevated Operating Temp', 'Warning', 'Monitor spindle temp; Ensure chiller is active.', 0.65, 'Spindle Temp is Elevated'),
            Rule('Rule 01 (Warning)', 1, lambda wm: wm.get('Tool_Cond') == 'Worn', 'Tool Wear Detected', 'Warning', 'Schedule tool replacement at end of batch.', 0.70, 'Tool Condition is Worn'),
            
            # Salience 0: Normal
            Rule('Rule 00 (Normal)', 0, lambda wm: wm.get('Spindle_Temp') == 'Normal' and wm.get('Spindle_Vib') == 'Normal' and wm.get('Hyd_Press') == 'Normal' and wm.get('Cool_Press') == 'Normal' and wm.get('Cool_Flow') == 'Normal' and wm.get('Curr_Load') == 'Normal' and wm.get('Tool_Cond') == 'Intact', 'None', 'Normal', 'Continue standard operation. All systems optimal.', 1.0, 'All monitored subsystems are operating within Normal/Intact thresholds.')
        ]

    def get_rules(self) -> List[Rule]:
        return self.rules
