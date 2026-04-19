# cyber-threat-detection-hybrid-model
#  Hybrid Cyber Threat Detection Model

This project implements an AI-powered Network Intrusion Detection System (NIDS) using a **Hybrid Model (XGBoost + LightGBM)**. It includes a real-time Streamlit dashboard for monitoring packet flows and detecting anomalies.

##  Features
* **Hybrid AI Architecture**: Combines XGBoost and LightGBM using a Voting Classifier for high accuracy.
* **Real-time SOC Dashboard**: Built with Streamlit to visualize threat alerts and system safety metrics.
* **KDD Cup '99 Preprocessing**: Handles complex network data with automated cleaning and encoding.

##  Installation
1. Clone the repository: `git clone <your-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run app.py`
4. pip install numpy
5.pip install pandas
6.pip install matplotlib
7.pip install seaborn
8.pip install scapy          # Packet manipulation
9.pip install pyshark        # Packet capture analysis
10.pip install networkx       # Graph-based threat modeling
11.pip install joblib         # Model persistence
12.pip install xgboost
13.pip install lightgbm



##  Model Performance
The model is trained on the NSL-KDD dataset and uses a `VotingClassifier` with "soft" voting to maximize detection confidence.
