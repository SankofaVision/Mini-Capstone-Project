[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/dNK7xGxu)
# SPARK Academy 2026 | Mini Capstone Project

## 📌 Scan Scheduling & Queue ManageR

---

## 👥 Team Name & Members

**Team Name:** Team Ghana-Accra -SankofaVision

| Full Name | Task Carried Out |
|-----------|------------------|
|Samuel Ankapong | Worked on data loading and cleaning using Pandas |
| Emmanuel Oppong | Worked on data loading and cleaning using Pandas |
| Bernice Awinpang | Developed Patient and Scan classes |
| Stella Quansah | Developed Patient and Scan classes |
| Ignatius Boadi | Implemented queue prioritisation and scheduling logic |
| Ophelia Dankyi | Implemented queue prioritisation and scheduling logic |
| Mariama Musa | Created visualisations using Matplotlib |
| Nicholas Hisrich Addisi | Created visualisations using Matplotlib |
| Thomas Kangah| Wrote README and contributed to report |
| Swallah Alhaji Suraka| Wrote PDF report and coordinated final submission |

---

## 📖 What This Project Does

> - What the program does:
>   
> The program simulates a hospital scan department that manages patient queues for MRI, CT, Ultrasound, PET and X-Ray scans throughout a typical working day. It models how patients arrive with different urgency levels and how these requests are scheduled and processed using a prioritisation system. 
> - The problem it addresses:
>   
> The program addresses the challenge of efficiently ordering patients based on urgency while minimizing waiting times. By incorporating queue management logic and tracking wait times, the system provides insights into how scan resources are utilized over time. 
> - Who would use it:
>   
> The program can be used by hospital administrators and healthcare planners to optimise scheduling decisions, improve patient flow and enhance overall operational efficiency in real healthcare settings.

---

## 🗂️ Repository Structure

```
├── data/
│   └── 11_scan_requests.csv        # Dataset provided for this project
├── PROJECT_REPORT.pdf                # One-page project report (push PDF here)
├── main.py                     # Main program entry point 
├── patient.py
├── scan.py
├── scheduler.py 
├── Visualizations.py
├── README.md                    
└── requirements.txt              # List of Python libraries used
```

---

## ⚙️ How to Run This Project

### 1. Clone the repository
```bash
git clone https://github.com/SankofaVision/Mini-Capstone-Project.git
cd Mini-Capstone-Project
```

### 2. Install required libraries
```bash
pip install -r requirements.txt
```

### 3. Run the program

```bash
python main.py
```



## 📊 Visualisations

> Below are the 3 charts the project produces:
>
> 1. **Chart 1** —  Bar chart showing queue by scan type
> 2. **Chart 2** — Line chart showing wait times across day
> 3. **Chart 3** — Pie chart showing urgency breakdown

---

## 🧱 Classes & Functions

> Briefly list the classes and standalone functions in your project:
>
> **Classes:**
> - `ClassName` — what it does
> - `ClassName` — what it does
>
> **Standalone Functions:**
> - `function_name()` — what it does
> - `function_name()` — what it does
> - `function_name()` — what it does

---

## 📄 Report

The one-page PDF report is located in the `report/` folder.
It covers: project overview, technical summary, challenges faced, and team contributions.

---

## ⚠️ Academic Integrity

This project was built independently by our team.
We did not share code or collaborate with any other team assigned to the same project.

---

*SPARK Academy 2026 · Mini Capstone · Submitted via GitHub Classroom*
