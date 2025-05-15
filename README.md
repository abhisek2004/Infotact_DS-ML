# Infotact_DS-ML
Infotact Solutions_Data Science &amp; Machine Learning_PROJECT

![ABHISEK_PANDA INFOTACT  (2)](https://github.com/user-attachments/assets/d6071af2-1f1c-4799-8112-e34c6bae5dc0)
![ABHISEK_PANDA INFOTACT  (1)](https://github.com/user-attachments/assets/22f00d6b-fb79-4006-a4b6-d888490db102)

# Project

![PROJECT_page-0001](https://github.com/user-attachments/assets/29bc4b8e-f152-4340-9ae4-dab725122331)
![PROJECT_page-0002](https://github.com/user-attachments/assets/de977ba7-d33d-4152-8488-6bd9d43dc6ba)
![PROJECT_page-0003](https://github.com/user-attachments/assets/583e7a82-fd39-4971-b397-ac6fb22edb5d)
![PROJECT_page-0004](https://github.com/user-attachments/assets/044afda4-ccef-48e9-9a47-bd3ce312bef7)


Great! Below is a **fully detailed and finalized `README.md` file** for your GitHub repository [Infotact\_DS-ML](https://github.com/abhisek2004/Infotact_DS-ML). This version includes:

* A professional and clear explanation of the project
* Technical and functional details
* Proper structure for presentation on GitHub

---

# 📊 Infotact\_DS-ML

**Infotact Solutions – Data Science & Machine Learning Internship Project**

![Infotact Badge](https://github.com/user-attachments/assets/d6071af2-1f1c-4799-8112-e34c6bae5dc0)

---

## 📌 Overview

This repository is a detailed representation of a **Data Science and Machine Learning project** developed during my internship at **Infotact Solutions**. The project, titled **AI-Powered Task Management System**, focuses on designing and building a system that utilizes machine learning to predict and manage task execution efficiently in real-world work environments.

---

## 🧠 Project Title: AI-Powered Task Management System

### 📋 Problem Statement

In many organizations, **task management is still manual**, inefficient, and error-prone. Employees often misjudge time estimations, leading to delays, poor resource management, and low productivity. This project aims to **build an AI-based system** to:

* Predict task durations
* Automatically assign priorities
* Monitor ongoing performance
* Optimize task scheduling using data-driven insights

---

## 🎯 Objectives

* Build a machine learning model to **predict task completion time** based on historical data.
* Create a system that can **prioritize tasks dynamically** depending on deadlines, complexity, and dependencies.
* Analyze employee performance metrics to **optimize resource allocation**.
* Recommend **strategic improvements** using data visualization.

---

## 🛠️ Tech Stack & Tools

| Category                        | Tools/Libraries Used                  |
| ------------------------------- | ------------------------------------- |
| Programming Language            | Python                                |
| Data Handling                   | Pandas, NumPy                         |
| Visualization                   | Matplotlib, Seaborn                   |
| Machine Learning                | Scikit-learn, XGBoost, Decision Trees |
| Development Environment         | Jupyter Notebook, VS Code             |
| Documentation & Version Control | Git, GitHub                           |

---

## 📁 Project Structure

```
Infotact_DS-ML/
│
├── Project 1 AI-Powered Task Management System/
│   ├── data/                  # Dataset(s) used for model training
│   ├── notebooks/             # Jupyter Notebooks for EDA, ML
│   ├── models/                # Saved models
│   ├── src/                   # Python scripts (feature engineering, training, etc.)
│   └── README.md              # Local project documentation
│
├── PROJECT.pdf                # Final report with visuals and analysis
├── PROJECT_INSTRUCTIONS.pdf   # Guidelines from Infotact
├── TRAINING.pdf               # Training materials used during internship
└── README.md                  # Master readme file
```

---

## 📊 Dataset Description

The dataset used includes the following fields:

* **Task ID**: Unique identifier
* **Task Description**: Brief of the assigned work
* **Assigned To**: Person/Team assigned
* **Start Date** and **End Date**
* **Estimated Duration** and **Actual Duration**
* **Priority Level**: High, Medium, Low
* **Task Category**: e.g., development, testing
* **Task Status**: Ongoing, Completed, Delayed

---

## 🔎 Exploratory Data Analysis (EDA)

Key insights obtained through EDA:

* Task categories with the **highest delay rates**
* **Employees with the most consistent performance**
* Average time vs estimated time comparison
* Most frequent causes of task failure/delay

---

## 🧠 Machine Learning Pipeline

### 🔹 Step 1: Data Cleaning & Preprocessing

* Missing value imputation
* Categorical encoding (One-hot / Label encoding)
* Feature scaling (MinMaxScaler)
* Feature extraction (Day of week, Working hours, etc.)

### 🔹 Step 2: Model Building

Tested multiple algorithms:

* Linear Regression
* Random Forest Regressor
* Decision Tree Regressor
* Gradient Boosting (XGBoost)

**Best Performing Model**: Random Forest Regressor

### 🔹 Step 3: Evaluation

* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)
* R² Score

Performance achieved:

| Model             | MAE  | RMSE | R² Score |
| ----------------- | ---- | ---- | -------- |
| Random Forest     | 1.86 | 2.13 | 0.91     |
| Linear Regression | 3.22 | 4.08 | 0.74     |

---

## 📈 Results & Visualization

* Gantt charts for project timeline prediction
* Bar plots for average vs actual durations
* Heatmaps for correlation between task types and delays
* Pie charts for task distribution by priority

---

## 🤖 Key Features of the System

✅ Predicts how long a task will take based on past data
✅ Suggests optimal employee for the task
✅ Alerts if task is likely to delay
✅ Dashboard to monitor team productivity

---

## 📜 Project Documents

* [`PROJECT.pdf`](https://github.com/abhisek2004/Infotact_DS-ML/blob/main/PROJECT.pdf): Final report including results, graphs, model performance
* [`PROJECT_INSTRUCTIONS.pdf`](https://github.com/abhisek2004/Infotact_DS-ML/blob/main/PROJECT_INSTRUCTIONS.pdf): Guidelines provided by Infotact Solutions
* [`TRAINING.pdf`](https://github.com/abhisek2004/Infotact_DS-ML/blob/main/TRAINING.pdf): Topics and tools covered during internship

---

## 🧪 How to Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/abhisek2004/Infotact_DS-ML.git
   cd Infotact_DS-ML
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt  # (Add this file if not already)
   ```

3. **Launch notebook**

   ```bash
   cd "Project 1 AI-Powered Task Management System/notebooks"
   jupyter notebook
   ```

---

## 👨‍💻 Author

* **Name**: Abhisek Panda
* **Internship Role**: Data Science & Machine Learning Intern
* **Organization**: Infotact Solutions
* **Email**: [abhisek2004official@gmail.com](mailto:abhisek2004panda@gmail.com)
* **LinkedIn**: [Abhisek Panda](https://linkedin.com/in/abhisek2004)

---

## 📢 Acknowledgements

Special thanks to **Infotact Solutions** for the opportunity and guidance throughout the internship.

---

## ⭐ Conclusion

This project was an excellent opportunity to work on real-world problems using data science and ML. The **AI-Powered Task Management System** shows how intelligent algorithms can significantly improve workplace efficiency and productivity by predicting delays, optimizing assignments, and generating insightful reports.

---
