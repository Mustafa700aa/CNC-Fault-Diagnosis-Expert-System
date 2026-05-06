#  CNC Fault Diagnosis Expert System

##  Project Overview
Unexpected breakdowns in CNC machines lead to costly downtime. This system acts as a "Senior Maintenance Engineer", continuously analyzing sensor data from three critical subsystems:
1. **Spindle Motor** (Temperature, Vibration)
2. **Cooling System** (Pressure, Flow Rate)
3. **Hydraulic System** (Oil Pressure)

By utilizing **Forward Chaining** reasoning and **Certainty Factors (CF)**, the system manages environmental uncertainty and outputs the detected fault, severity level, and recommended actions before critical failures occur.

---

##  Key Features
- **Data-Driven Inference:** Uses a Forward Chaining mechanism to deduce conclusions from raw numeric telemetry.
- **Explainable AI (White-Box):** Includes a built-in Explanation Subsystem (Reasoning Trace) that maps exactly which rules and facts led to the diagnosis.
- **Conflict Resolution Engine:** Implements advanced strategies like *Refraction*, *Salience* (Prioritizing Emergencies), and *Complexity*.
- **SOLID Object-Oriented Design:** The project is modularized into dedicated classes (`KnowledgeBase`, `InferenceEngine`, `DataDiscretizer`) ensuring high maintainability and scalability.
- **Interactive Dashboard:** Features a beautiful, dark-themed UI built with Streamlit.

---

##  System Architecture

The project is structured following strict Single Responsibility Principles (SRP):

- `app.py`: The main orchestrator and Streamlit UI dashboard.
- `models.py`: Defines the core `Rule` and `Diagnosis` data structures.
- `discretizer.py`: Transforms raw numerical sensor data into symbolic Object-Attribute-Value (OAV) facts.
- `knowledge_base.py`: The repository of heuristics, containing rules prioritized by severity (Normal, Warning, Critical, Emergency).
- `inference_engine.py`: The core engine that pattern-matches facts against rules and handles conflict resolution.
- `explanation.py`: Generates the reasoning trace to justify the final diagnosis.
- `test_system.py`: An automated test suite covering 10 distinct boundary and conflict scenarios.

---

##  Getting Started

### 1. Prerequisites
Ensure you have Python installed on your machine. Then, install the required UI framework:
```bash
pip install streamlit
```

### 2. Running the Expert System
To launch the interactive dashboard, navigate to the project directory and run:
```bash
streamlit run app.py
```
The system will open in your default web browser (usually at `http://localhost:8501`).

### 3. Running Automated Tests
To verify the logical integrity of the Inference Engine against the predefined test cases, run:
```bash
python test_system.py
```
This will execute 10 rigorous test cases (including boundaries and emergency conflicts) and print the results to the console.

---

##  Example Scenarios
- **Normal Operation:** All sensors within optimal thresholds. Action: Continue standard operation.
- **Warning (Early Bearing Wear):** Elevated spindle temperature and moderate vibration. Action: Schedule inspection, reduce speed.
- **Critical (Cooling Failure):** High temperature coupled with severe pressure drops. Action: Stop cutting cycle immediately.
- **Emergency (Hydraulic Collapse):** Critical drop in hydraulic pressure. Action: Automatic System Shutdown.

---
*Developed for Alamein University - Faculty of Computer Science & Engineering.*
