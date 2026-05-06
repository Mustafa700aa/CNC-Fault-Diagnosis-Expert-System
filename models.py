from dataclasses import dataclass
from typing import Callable, Dict, Union

@dataclass
class Diagnosis:
    rule_id: str
    fault: str
    severity: str
    action: str
    cf: Union[float, str]
    antecedents_desc: str

class Rule:
    def __init__(self, rule_id: str, salience: int, conditions: Callable[[Dict[str, str]], bool], 
                 fault: str, severity: str, action: str, cf: float, antecedents_desc: str):
        self.rule_id = rule_id
        self.salience = salience
        self.conditions = conditions
        self.fault = fault
        self.severity = severity
        self.action = action
        self.cf = cf
        self.antecedents_desc = antecedents_desc

    def evaluate(self, working_memory: Dict[str, str]) -> bool:
        return self.conditions(working_memory)
