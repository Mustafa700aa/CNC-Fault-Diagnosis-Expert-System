# test_system.py
from discretizer import DataDiscretizer
from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine

def run_tests():
    # Setup System
    kb = KnowledgeBase()
    engine = InferenceEngine(kb.get_rules())
    
    # Test Cases: (Name, Temp, Vib, Hyd_Press, Cool_Press, Cool_Flow, Curr_Load, Tool_Cond, Expected_Rule_Prefix)
    tests = [
        ("TC1: Ideal Normal",         40,  1.0, 120, 40, 20, 10, "Intact", "Rule 00"),
        ("TC2: Normal Boundaries",    65,  1.5, 100, 25, 10, 15, "Intact", "Rule 00"),
        ("TC3: Warning - Worn Tool",  65,  1.0, 100, 30, 15, 10, "Worn",   "Rule 01"),
        ("TC4: Warning - Elev Temp",  85,  1.0, 100, 30, 15, 10, "Intact", "Rule 02"),
        ("TC5: Warning - Mod Vib",    65,  3.0, 100, 30, 15, 10, "Intact", "Rule 03"),
        ("TC6: Critical - Low Cool",  65,  1.0, 100, 5,  6,  10, "Intact", "Rule 15"),
        ("TC7: Critical - Sev Flow",  65,  1.0, 100, 30, 2,  10, "Intact", "Rule 10"),
        ("TC8: Critical - High Temp", 120, 1.0, 100, 30, 15, 10, "Intact", "Rule 11"),
        ("TC9: Critical - High Vib",  65,  5.0, 100, 30, 15, 10, "Intact", "Rule 12"),
        ("TC10: Emerg - Brk & Vib",   65,  5.0, 100, 30, 15, 10, "Broken", "Rule 17"),
        ("TC11: Emerg - Crit Hyd",    65,  1.0, 10,  30, 15, 10, "Intact", "Rule 18"),
        ("TC12: Emerg - Surge Curr",  65,  1.0, 100, 30, 15, 40, "Intact", "Rule 19"),
        ("TC13: Emerg - Broken Tool", 65,  1.0, 100, 30, 15, 10, "Broken", "Rule 20"),
        ("TC14: Conflict Res",        120, 1.0, 10,  30, 15, 10, "Intact", "Rule 23"),
        ("TC15: Fallback Unknown",    65,  1.0, 100, 30, 15, 10, "Unknown","Unknown Rule")
    ]

    passed = 0
    divider = "=" * 80
    print(f"\n{divider}")
    print("SYSTEM TEST SUITE: CNC Fault Diagnosis Expert System")
    print(f"{divider}\n")
    
    for name, t, v, h, cp, cf, cl, tc, expected in tests:
        raw_data = {
            'temp': t, 
            'vib': v, 
            'hyd_press': h, 
            'cool_press': cp, 
            'cool_flow': cf,
            'curr_load': cl,
            'tool_cond': tc
        }
        wm = DataDiscretizer.discretize(raw_data)
        diagnosis = engine.run(wm)
        
        status = "PASS" if diagnosis.rule_id.startswith(expected) else "FAIL"
        
        if status == "PASS":
            print(f"PASS | {name:25} | Triggered: {diagnosis.rule_id}")
            passed += 1
        else:
            print(f"FAIL | {name:25} | Expected: {expected}, Got: {diagnosis.rule_id}")

    print(f"\n{divider}")
    print(f"FINAL RESULTS: {passed} / {len(tests)} tests passed successfully.")
    print(f"{divider}\n")

if __name__ == "__main__":
    run_tests()
