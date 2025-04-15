# Career Analytics Portal

A simple and useful tool that uses machine learning to understand employees' better. It predicts **income**, **attrition (whether someone might leave the company)**, and **job satisfaction**, and gives helpful suggestions for improvement.

## 🌟 Purpose

This project helps HR teams use employee data to make smart decisions. It gives insights into employee behavior and helps improve retention, satisfaction, and salary planning.

---

## ✨ Features

- ✅ Predict if an employee might leave the company (Attrition)
- ✅ Predict an employee's monthly income
- ✅ Predict how satisfied an employee is with their job
- ✅ Give recommendations based on prediction results

---

## 🧰 Tools and Libraries Used

- **Languages/Frameworks**: Python, Streamlit
- **Libraries**: `numpy`, `pandas`, `scikit-learn`, `CatBoostRegressor`, `RandomForestRegressor`, `plotly`, `pickle`, `warnings`
- **UI**: HTML (index.html), `streamlit_extras`
- **Others**: Windows Batch File to run apps easily

---

## 📊 ML Models and Their Results

- **Income Prediction**: `CatBoostRegressor`
  - R² Score: **0.89** (very good)
- **Job Satisfaction Prediction**: `RandomForestRegressor`
  - Accuracy: **83.75%**
- **Attrition Prediction**: `RandomForestClassifier`
  - Accuracy: **86.31%**

---

## 🔧 How to Use the Project

1. Download all files and place them in a single folder.
2. Open each `.py` file and update the path to the correct `.sav` model file.
3. Edit the batch file (`run_all_apps.bat`) with the correct file paths.
4. Run `run_all_apps.bat` to open all the apps (each will open in a separate window).
   - Don’t close the command prompt (CMD) windows.
5. Open `index.html` in a web browser to view the homepage and navigate to any app.

You can now use the apps through the website!

---

## 📌 Future Improvements

1. **Live Data**: Connect with real-time HR systems to get updated employee data.
2. **Login System**: Add login for different users like HR, managers, and employees.
3. **Feedback Forms**: Collect employee feedback and analyze it using text analysis.
4. **Auto Model Updates**: Automatically train the models again with new data.
5. **Better Charts**: Add more interactive charts and dashboards.
6. **Download Reports**: Allow users to save predictions as PDF reports.
7. **Cloud Hosting**: Host the website on platforms like Heroku or Streamlit Cloud.
8. **Mobile Friendly**: Make the website easier to use on phones and tablets.
9. **Chatbot Help**: Add a chatbot to assist users.
10. **Track Employee Life Events**: Use predictions to help with onboarding, promotions, or resignations.

---

## 👥 Contributers:

- **Prashik Manwar**

---

## ⚠️ Disclaimer

Please note that the predictions made by this portal may not always be accurate. The results depend heavily on the quality and structure of the dataset used for training the models. Real-world employee behavior can be influenced by many other factors not included in this dataset.
