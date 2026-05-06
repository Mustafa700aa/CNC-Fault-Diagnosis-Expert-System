import streamlit as st
from discretizer import DataDiscretizer
from knowledge_base import KnowledgeBase
from inference_engine import InferenceEngine
from explanation import ExplanationSubsystem

def reset_sliders():
    st.session_state['temp'] = 65
    st.session_state['vib'] = 1.5
    st.session_state['cool_press'] = 30
    st.session_state['cool_flow'] = 15
    st.session_state['hyd_press'] = 100
    st.session_state['curr_load'] = 10
    st.session_state['tool_cond'] = 'Intact'

def main():
    # --- SETUP DEPENDENCIES (Dependency Injection) ---
    kb = KnowledgeBase()
    engine = InferenceEngine(kb.get_rules())

    # --- UI SETUP ---
    st.set_page_config(page_title="CNC Expert System", layout="wide")
    
    st.markdown("""
        <style>
        .report-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .normal { background-color: #0b2e13; color: #d4edda; border: 1px solid #c3e6cb; }
        .warning { background-color: #3e2e00; color: #fff3cd; border: 1px solid #ffeeba; }
        .critical { background-color: #491217; color: #f8d7da; border: 1px solid #f5c6cb; }
        .emergency { background-color: #721c24; color: white; border: 2px solid red; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.title("CNC Fault Diagnosis Expert System")
    st.markdown("---")
    
    # Initialize session state for sliders
    if 'temp' not in st.session_state:
        st.session_state['temp'] = 65
    if 'vib' not in st.session_state:
        st.session_state['vib'] = 1.5
    if 'cool_press' not in st.session_state:
        st.session_state['cool_press'] = 30
    if 'cool_flow' not in st.session_state:
        st.session_state['cool_flow'] = 15
    if 'hyd_press' not in st.session_state:
        st.session_state['hyd_press'] = 100
    if 'curr_load' not in st.session_state:
        st.session_state['curr_load'] = 10
    if 'tool_cond' not in st.session_state:
        st.session_state['tool_cond'] = 'Intact'

    col1, col2 = st.columns([1, 1.5])
    
    # ================== INPUT SECTION ==================
    with col1:
        st.header("Real-Time Sensor Inputs")
        
        tab_mech, tab_fluid, tab_elec, tab_vis = st.tabs(['⚙️ Mechanical', '💧 Fluids', '⚡ Electrical', '👁️ Vision'])
        
        with tab_mech:
            st.subheader("Spindle Motor")
            temp = st.slider("Motor Temperature (°C)", min_value=20, max_value=150, step=1, key='temp')
            vib = st.slider("Vibration Level (mm/s)", min_value=0.0, max_value=10.0, step=0.1, key='vib')
            
        with tab_fluid:
            st.subheader("Hydraulic & Cooling System")
            hyd_press = st.slider("Oil Pressure (Bar)", min_value=0, max_value=150, step=1, key='hyd_press')
            cool_press = st.slider("Coolant Pressure (PSI)", min_value=0, max_value=50, step=1, key='cool_press')
            cool_flow = st.slider("Flow Rate (L/min)", min_value=0, max_value=30, step=1, key='cool_flow')
            
        with tab_elec:
            st.subheader("Electrical System")
            curr_load = st.slider("Current Load (A)", min_value=0, max_value=50, step=1, key='curr_load')
            
        with tab_vis:
            st.subheader("Vision System")
            tool_cond = st.selectbox("Tool Condition", options=['Intact', 'Worn', 'Broken'], key='tool_cond')
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            diagnose_btn = st.button("Run Diagnosis", type="primary", use_container_width=True)
        with btn_col2:
            st.button("Reset Inputs", on_click=reset_sliders, use_container_width=True)

    # ================== OUTPUT SECTION ==================
    with col2:
        if diagnose_btn:
            raw_data = {
                'temp': temp, 
                'vib': vib, 
                'hyd_press': hyd_press, 
                'cool_press': cool_press, 
                'cool_flow': cool_flow,
                'curr_load': curr_load,
                'tool_cond': tool_cond
            }
            
            # 1. Discretization
            working_memory = DataDiscretizer.discretize(raw_data)
            
            # 2. Inference
            diagnosis = engine.run(working_memory)
            
            # 3. Explanation Generation
            explanation = ExplanationSubsystem(raw_data, working_memory, diagnosis)
            
            # UI Output
            st.header("Diagnostic Report")
            css_class = diagnosis.severity.lower()
            
            st.markdown(f"""
            <div class="report-box {css_class}">
                <h3>Status: {diagnosis.severity.upper()}</h3>
                <h4>Detected Fault: {diagnosis.fault}</h4>
                <p><strong>Recommended Action:</strong> {diagnosis.action}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ================== EXPLANATION TRACE UI ==================
            st.header("Explanation Subsystem (Reasoning Trace)")
            
            exp_col1, exp_col2 = st.columns(2)
            
            with exp_col1:
                st.markdown("#### 1. Symptom Analysis (WM)")
                for k, v in explanation.get_symptom_analysis().items():
                    st.write(f"- **{k}** {v}")
                
            with exp_col2:
                st.markdown("#### 2. Rule Mapping")
                mapping = explanation.get_rule_mapping()
                st.info(f"**Triggered Rule:** {mapping['Triggered Rule']}")
                st.write(f"**Conditions Met:** {mapping['Conditions Met']}")
                
                st.markdown("#### 3. Confidence Assessment")
                st.success(f"**Certainty Factor (CF):** {explanation.get_confidence_assessment()}")

if __name__ == "__main__":
    main()
