import numpy as np
import pickle
import streamlit as st
import plotly.graph_objects as go

# Load the saved model 
loaded_model = pickle.load(open("your-path-to-sat_pred.sav", 'rb'))

# Prediction function
def sat_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data, dtype=np.float64)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    return prediction[0]

# Confidence range function
def get_confidence_range(prediction):
    margin = 0.05  # Static margin
    return max(0, prediction - margin), min(1, prediction + margin)

# Display satisfaction gauge (0 to 1)
def display_gauge(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': " / 1.0"},
        title={'text': "Satisfaction Level"},
        gauge={
            'axis': {'range': [0, 1]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0.0, 0.4], 'color': "red"},
                {'range': [0.4, 0.7], 'color': "yellow"},
                {'range': [0.7, 1.0], 'color': "green"},
            ],
        }
    ))
    st.plotly_chart(fig)

# Emoji-based satisfaction interpretation
def get_emoji_rating(score):
    if score < 0.4:
        return "😞 Very Dissatisfied"
    elif score < 0.7:
        return "😐 Moderately Satisfied"
    else:
        return "😊 Highly Satisfied"

# Generate tailored recommendations
def get_recommendations(satisfaction_level, work_accident):
    recs = []
    if satisfaction_level < 0.5:
        recs.extend([
            "🔻 Provide better work-life balance and flexible working hours.",
            "🔻 Offer training and development opportunities to enhance career growth.",
            "🔻 Improve internal communication and employee feedback mechanisms.",
            "🔻 Consider workload adjustments to reduce burnout."
        ])
        if work_accident == 1:
            recs.append("⚠️ Employees with past accidents and low satisfaction may need more support or safety assurance.")
    elif satisfaction_level > 0.5:
        recs.extend([
            "✅ Keep up the positive workplace environment!",
            "✅ Recognize and reward high-performing employees regularly.",
            "✅ Encourage peer mentorship and knowledge sharing.",
            "✅ Involve satisfied employees in leadership or innovation programs."
        ])
    return recs

# Input validation
def validate_inputs(total_working_years, promotion_last_5_years):
    warnings = []
    if total_working_years == 0 and promotion_last_5_years == 1:
        warnings.append("⚠️ Promotion received with 0 working years? Please verify.")
    return warnings

# Main app
def main():
    st.title("Job Satisfaction Prediction Web App")

    job_role_mapping = {
        0: "Healthcare Representative",    
        1: "Human Resources",
        2: "Laboratory Technician",        
        3: "Manager",                      
        4: "Manufacturing Director",      
        5: "Research Director",            
        6: "Research Scientist",           
        7: "Sales Executive",              
        8: "Sales Representative",
        9: "Technical Support"
    }   

    salary_mapping = {
        1: 'Low',
        2: 'Medium',
        0: 'High'
    }

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        JobRole = st.selectbox("Job Role", options=list(job_role_mapping.keys()), format_func=lambda x: job_role_mapping[x])
        AverageMonthlyHours = st.number_input("Average Monthly Hours", min_value=0)
        TotalWorkingYears = st.number_input("Total Working Years", min_value=0)

    with col2:
        WorkAccident = st.selectbox("Had Work Accident?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        PromotionLast5Years = st.selectbox("Promotion in Last 5 Years?", options=[0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        Salary = st.selectbox("Salary Level", options=list(salary_mapping.keys()), format_func=lambda x: salary_mapping[x])

    st.markdown("---")

    # Validate inputs
    inconsistencies = validate_inputs(TotalWorkingYears, PromotionLast5Years)
    for warning in inconsistencies:
        st.warning(warning)

    if st.button("🔍 Predict"):
        prediction = sat_prediction([
            JobRole,
            AverageMonthlyHours,
            TotalWorkingYears,
            WorkAccident,
            PromotionLast5Years,
            Salary
        ])

        rating = get_emoji_rating(prediction)
        st.markdown(f"### Predicted Satisfaction Level: **{prediction}** → {rating}")

        lower, upper = get_confidence_range(prediction)
        st.info(f"📊 Confidence Range: {lower} - {upper}")

        display_gauge(prediction)

        recommendations = get_recommendations(prediction, WorkAccident)
        if recommendations:
            st.markdown("### 💡 Tailored Recommendations")
            for rec in recommendations:
                st.write(rec)

if __name__ == '__main__':
    main()

