✅ README.md
# 🦠 CORD-19 Explorer

A lightweight Streamlit web app that explores trends in COVID-19 research papers using the CORD-19 metadata dataset.

This project visualizes the volume of scientific publications over time, identifies the most active journals, and allows advanced search through paper titles.

## 📂 Features

- 📊 Year-wise publication trends
- 🏢 Top publishing journals
- 🔍 Advanced title keyword search
- 📄 Sample data display
- 💾 Download filtered results as CSV
- 🔗 Large dataset streaming from Google Drive
- 🚀 Built with Python, pandas, matplotlib, seaborn, and Streamlit

---

## 📦 Installation

```bash
git clone https://github.com/Langat1999/COVID-ANALYSIS.git
cd COVID-ANALYSIS
pip install -r requirements.txt

▶️ How to Run
streamlit run app.py

🌐 Live Demo

Deployed version: Visit Streamlit App

(Data loads from Google Drive automatically, no large file upload required.)

🧪 Data Source

CORD-19 Metadata
Provided by the Allen Institute for AI (AI2)
CORD-19 Dataset

CSV streamed from Google Drive:
cleaned_metadata.csv (~500MB+)

📁 Project Structure
COVID-ANALYSIS/
├── app.py                 # Streamlit main app
├── requirements.txt       # Project dependencies
├── README.md              # Project overview

👨‍💻 Author

Jackson Mutiso Langat
📧 mutisojackson55@gmail.com

📜 License

MIT License – free to use and modify.


---

### ✅ `requirements.txt`

```txt
pandas>=1.1.0
matplotlib>=3.2.2
seaborn>=0.11.0
streamlit>=1.0.0
requests>=2.25.0
