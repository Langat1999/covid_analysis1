# 🦠 CORD-19 Explorer

A lightweight and interactive **Streamlit web app** that explores trends in COVID-19 research papers using the **CORD-19 metadata dataset**.  
This tool enables users to upload a CSV file (`metadata.csv`) and visualize publication trends, top journals, keyword clouds, and more.

---

## 📊 Features

- 📈 **Publications by Year** – Visualize paper publication trends over time
- 🏆 **Top Journals** – View the most active journals publishing COVID-19 research
- ☁️ **Word Cloud** – Generate word clouds from paper titles
- 📦 **Source Distribution** – Bar plot of sources (e.g., PMC, Elsevier)
- 📄 **Sample Data Display** – Preview paper titles, journals, and publish dates
- 💾 **Download Filtered Data** – Export filtered dataset as CSV
- 📂 **Upload Interface** – Upload your own `metadata.csv` (from CORD-19)

---

## ▶️ How to Use

1. Clone or download this repository:
   ```bash
   git clone https://github.com/Langat1999/covid_analysis1
   cd CORD19-Explorer
Create a virtual environment (recommended):

bash
Copy code
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On macOS/Linux
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Launch the app:

bash
Copy code
streamlit run app.py
In your browser, upload the metadata.csv file from the CORD-19 dataset to begin exploring.

🧠 About the CORD-19 Dataset
The CORD-19 (COVID-19 Open Research Dataset) is a collection of scholarly articles about COVID-19, SARS-CoV-2, and related coronaviruses. It is provided by the Allen Institute for AI (AI2).

🔗 Download the latest metadata:
https://www.semanticscholar.org/cord19

Typical file: metadata.csv
(~500MB+ in size, includes paper titles, abstracts, journals, dates, etc.)

📁 Project Structure
bash
Copy code
CORD19-Explorer/
├── app.py                 # ✅ Streamlit main app
├── requirements.txt       # ✅ Python dependencies
├── README.md              # ✅ You're reading this
└── .streamlit/
    └── config.toml        # ✅ Streamlit layout & theming
📦 requirements.txt
txt
Copy code
pandas>=1.1.0
matplotlib>=3.2.2
seaborn>=0.11.0
streamlit>=1.10.0
wordcloud>=1.8.1
Install with:

bash
Copy code
pip install -r requirements.txt
⚙️ .streamlit/config.toml (optional theme)
toml
Copy code
[server]
headless = true
enableCORS = false

[theme]
base = "light"
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#000000"
font = "sans serif"
🌐 Deployment
You can deploy this app on Streamlit Cloud:

Push your project to GitHub

Go to Streamlit Cloud → “Deploy an app”

Connect your GitHub repo

Set the main file path to app.py

Click Deploy

Users will be prompted to upload their own metadata.csv after launch.

🧪 Example Screenshot

Add a screenshot or GIF of your app here to show users what to expect.

👨‍💻 Author
Jackson Mutiso Langat
📧 mutisojackson55@gmail.com
🌐 [Langat1999](https://github.com/Langat1999)

📜 License
This project is licensed under the MIT License – you are free to use, modify, and distribute this software with attribution.