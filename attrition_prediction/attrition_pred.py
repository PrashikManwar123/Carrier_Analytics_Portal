import numpy as np
import pickle
import streamlit as st
import warnings

warnings.filterwarnings("ignore")

# Load the saved model
model = pickle.load(open("your-path-to-attrition_pred.sav", 'rb'))

# Mapping Dictionaries
job_level_mapping = {1: "Entry-level", 2: "Intermediate", 3: "Mid-level", 4: "Senior/Executive", 5: "C-Suite"}
job_role_mapping = {
    0: "Healthcare Representative", 1: "Human Resources", 2: "Laboratory Technician", 3: "Manager",
    4: "Manufacturing Director", 5: "Research Director", 6: "Research Scientist", 7: "Sales Executive", 8: "Sales Representative"
}
edu_field_mapping = {1: "Life Sciences", 3: "Medical", 2: "Marketing", 5: "Technical Degree", 4: "Other", 0: "Human Resources"}
marital_status_mapping = {1: "Married", 2: "Single", 0: "Divorced"}
overtime_mapping = {0: "No", 1: "Yes"}
department_mapping = {0: "Human Resources", 1: "Research & Development", 2: "Sales"}

# Function to predict attrition with confidence interval
def predict_attrition(input_data):
    input_np = np.asarray(input_data).reshape(1, -1)
    prediction = model.predict(input_np)[0]
    proba = model.predict_proba(input_np)[0][1]
    confidence_range = (max(0, proba - 0.05), min(1, proba + 0.05))
    return prediction, proba, confidence_range

# Validation for contradictory inputs
def validate_inputs(job_satisfaction, overtime):
    inconsistencies = []
    if job_satisfaction == 4 and overtime == 1:
        inconsistencies.append("⚠️ Very High Job Satisfaction but also working Overtime? Consider verifying employee morale.")
    return inconsistencies

# Recommendations
def get_recommendations(job_satisfaction, overtime, income, years_at_company):
    recs = []
    if job_satisfaction == 1:
        recs.append("✅ Improve job satisfaction through career development programs.")
    if overtime == 1:
        recs.append("✅ Reduce overtime workload to improve work-life balance.")
    if income < 50000:
        recs.append("✅ Consider competitive salary or performance bonuses.")
    if years_at_company < 2:
        recs.append("✅ Enhance onboarding and mentorship initiatives.")
    if not recs:
        recs.append("✅ Maintain a positive and supportive work culture.")
    return recs

# Streamlit UI
def main():
    st.set_page_config(page_title="Attrition Predictor", layout="centered")
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Attrition Prediction Web App</h1>", unsafe_allow_html=True)

    st.subheader("📋 Enter Employee Details")
    col1, col2 = st.columns(2)

    with col1:
        JobLevel = st.selectbox("Job Level", list(job_level_mapping.keys()), format_func=lambda x: job_level_mapping[x])
        JobRole = st.selectbox("Job Role", list(job_role_mapping.keys()), format_func=lambda x: job_role_mapping[x])
        TotalWorkingYears = st.number_input("Total Working Years", min_value=0, max_value=50, step=1)
        Department = st.selectbox("Department", list(department_mapping.keys()), format_func=lambda x: department_mapping[x])
        EducationField = st.selectbox("Education Field", list(edu_field_mapping.keys()), format_func=lambda x: edu_field_mapping[x])

    with col2:
        MaritalStatus = st.selectbox("Marital Status", list(marital_status_mapping.keys()), format_func=lambda x: marital_status_mapping[x])
        OverTime = st.selectbox("OverTime", list(overtime_mapping.keys()), format_func=lambda x: overtime_mapping[x])
        YearsAtCompany = st.number_input("Years At Company", min_value=0, step=1)
        Age = st.number_input("Age", min_value=18, max_value=100, step=1)
        YearsWithCurrManager = st.number_input("Years With Current Manager", min_value=0, step=1)

    MonthlyIncome = st.number_input("Monthly Income (INR)", min_value=0, step=500)
    JobSatisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4], format_func=lambda x: {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}[x])

    input_data = [
        Department, EducationField, JobRole, MaritalStatus, OverTime, TotalWorkingYears,
        JobLevel, YearsAtCompany, Age, YearsWithCurrManager, MonthlyIncome, JobSatisfaction
    ]

    inconsistencies = validate_inputs(JobSatisfaction, OverTime)
    if inconsistencies:
        st.warning("\n".join(inconsistencies))

    if st.button("Predict Attrition"):
        with st.spinner("Analyzing..."):
            prediction, prob, conf_range = predict_attrition(input_data)
            lower = round(conf_range[0] * 100, 2)
            upper = round(conf_range[1] * 100, 2)
            
            if prediction == 1:
                st.error("⚠️ The employee may leave the job.")
            else:
                st.success("✅ The employee is unlikely to leave the job.")

            st.info(f"📊 Attrition Probability: {round(prob*100,2)}% (Confidence Range: {lower}% - {upper}%)")

            st.markdown("### 💡 Tailored Recommendations")
            for rec in get_recommendations(JobSatisfaction, OverTime, MonthlyIncome, YearsAtCompany):
                st.write(rec)

if __name__ == '__main__':
    main()

