
import numpy as np
import pickle
import streamlit as st
from streamlit_extras.colored_header import colored_header
import sklearn

# Load the trained model
loaded_model = pickle.load(open("C:/FP/income_pred/trained_model.sav", 'rb'))

# Fixed prediction function with realistic scaling and confidence
def income_prediction(input_data):
    JobLevel, JobRole, TotalWorkingYears, Department = input_data

    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    raw_prediction = float(loaded_model.predict(input_data_reshaped)[0])

    # Confidence estimation (if model supports predict_proba)
    try:
        confidence = loaded_model.predict_proba(input_data_reshaped).max()
    except AttributeError:
        confidence = None

    # Apply realistic scaling based on JobLevel and Experience
    level_factor = 0.6 + 0.1 * (JobLevel - 1)
    experience_factor = 0.6 + 0.02 * TotalWorkingYears
    adjusted_prediction = raw_prediction * level_factor * experience_factor

    return adjusted_prediction, confidence

def main():
    st.set_page_config(
        page_title="Income Prediction App",
        page_icon="💰",
        layout="centered"
    )

    # Custom CSS styling
    st.markdown("""
    <style>
        .stSelectbox, .stTextInput, .stNumberInput {
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            border: none;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .prediction-result {
            font-size: 18px;
            padding: 15px;
            border-radius: 5px;
            background-color: #e6f7e6;
            border-left: 5px solid #4CAF50;
            color: #333333 !important;
        }
        .prediction-value {
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32 !important;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # App title
    colored_header(
        label="Income Prediction App",
        description="Predict monthly income based on job factors",
        color_name="blue-green-70"
    )

    st.markdown("""
    This app predicts monthly income in Indian Rupees based on job level, role, experience, and department.
    """)

    # Mappings
    job_level_mapping = {
        1: "Entry-level", 
        2: "Intermediate", 
        3: "Mid-level", 
        4: "Senior/Executive", 
        5: "C-Suite"
    }

    job_role_mapping = {
        0: "Healthcare Representative",    
        1: "Human Resources",
        2: "Laboratory Technician",        
        3: "Manager",                      
        4: "Manufacturing Director",      
        5: "Research Director",            
        6: "Research Scientist",           
        7: "Sales Executive",              
        8: "Sales Representative"
    }

    department_mapping = {
        0: "Human Resources", 
        1: "Research & Development", 
        2: "Sales"
    }

    # Input form
    with st.expander("🔍 Enter Job Details", expanded=True):
        JobLevel = st.selectbox(
            "Job Level", 
            options=list(job_level_mapping.keys()), 
            format_func=lambda x: job_level_mapping[x],
            help="1 = Entry, 5 = C-Suite. Higher levels typically require more experience."
        )

        # Restrict roles based on JobLevel
        if JobLevel == 5:
            role_options = {3: "Manager", 5: "Research Director"}
        else:
            role_options = job_role_mapping

        JobRole = st.selectbox(
            "Job Role", 
            options=list(role_options.keys()), 
            format_func=lambda x: role_options[x],
            help="Role available depends on your selected job level."
        )

        TotalWorkingYears = st.number_input(
            "Total Working Years", 
            min_value=0, 
            max_value=50, 
            value=5,
            help="Enter your total years of work experience."
        )

        # Warning for unrealistic combos
        if JobLevel == 5 and TotalWorkingYears < 15:
            st.warning("⚠️ C-Suite level usually requires 15+ years of experience.")

        Department = st.selectbox(
            "Department", 
            options=list(department_mapping.keys()), 
            format_func=lambda x: department_mapping[x],
            help="Select the department from the dropdown."
        )

    # Predict button
    if st.button('Predict Income', help="Click to predict monthly income"):
        with st.spinner('Predicting...'):
            inr_pred, confidence = income_prediction([JobLevel, JobRole, TotalWorkingYears, Department])
            st.success("Prediction Complete!")

            st.markdown(f"""
            <div class="prediction-result">
                <h3>Predicted Monthly Income:</h3>
                <div class="prediction-value">₹{inr_pred:,.2f} / Month</div>
                {f'<p><b>Confidence:</b> {confidence:.2%}</p>' if confidence else ''}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Note: This is a predictive model. Actual salaries may vary based on additional factors.")

if __name__ == '__main__':
    main()
