from models import Rule, Diagnosis
from typing import Dict, List

class InferenceEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def _conflict_resolution(self) -> List[Rule]:
        return sorted(
            self.rules, 
            key=lambda r: (r.salience, r.antecedents_desc.lower().count(' and ')), 
            reverse=True
        )

    def run(self, working_memory: Dict[str, str]) -> Diagnosis:
        agenda = self._conflict_resolution()
        
        for rule in agenda:
            if rule.evaluate(working_memory):
                # Refraction: Fire only the most salient matched rule
                return Diagnosis(
                    rule_id=rule.rule_id,
                    fault=rule.fault,
                    severity=rule.severity,
                    action=rule.action,
                    cf=rule.cf,
                    antecedents_desc=rule.antecedents_desc
                )
        
        # Fallback Diagnosis
        return Diagnosis(
            rule_id="Unknown Rule",
            fault="Undiagnosed Anomaly / Mixed Conditions",
            severity="Warning",
            action="Please inspect machine manually. Sensor combinations are outside standard rule definitions.",
            cf="N/A",
            antecedents_desc="No exact rule match for the current combination of facts."
        )
