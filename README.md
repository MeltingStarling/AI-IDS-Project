Hello! This project is one that I worked on for a long time and am really excited to share with everyone. I chose to start this as an Information Technology student who loves all things tech and really wanted to dip my feet into AI while also learning real-world cybersecurity tools and seeing if I can apply this knowledge later.
AI-Based Intrusion Detection System (AI-IDS)
Machine Learning + Suricata + Real-Time Discord Alerts
Overview

This project implements a real-time AI-powered Intrusion Detection System (IDS) using:

Suricata to generate network flow events

A trained Random Forest anomaly-detection model

Python-based runtime inference engine

Discord webhook alerts for real-time notification

Systemd service for continuous 24/7 deployment

Ubuntu VM inside a homelab, SSH-accessible via Tailscale

The goal of this project was to build a fully functional IDS using machine learning, capable of analyzing live network traffic and reporting suspicious behavior instantly.

Dataset: UNSW-NB15

This project uses the UNSW-NB15 dataset — a widely used public dataset containing both normal and malicious traffic types.

Dataset source:
https://research.unsw.edu.au/projects/unsw-nb15-dataset

Training/Testing sets used:

UNSW_NB15_training-set.csv
UNSW_NB15_testing-set.csv
UNSW-NB15_features.csv

The dataset includes labeled attacks such as:

Fuzzers
Analysis
DoS
Generic
Shellcode
Reconnaissance
Exploits
Backdoors

These labels were used to train a supervised Random Forest that functions as an anomaly detector.

Model Training Summary

The model was trained using Python, pandas, and scikit-learn (Random Forest + RandomizedSearchCV).

Data Preprocessing

Converted malformed headers
Cleaned and normalized data
Label-encoded categorical fields
Split dataset: 80% training / 20% testing

Hyperparameter Tuning
Used RandomizedSearchCV to efficiently test model configurations without long grid-search times.

Model Export
Saved using joblib:
models/ids_model.joblib
This file is used directly by the runtime engine on the Ubuntu VM.

Deployment Architecture (Local VM)
The Ubuntu VM runs:
Suricata for network monitoring
run_model.py for real-time scoring
systemd for persistence and logging
Discord webhook notifications

Systemd Service File
[Unit]
Description=AI-IDS Suricata Anomaly Detector
After=network.target suricata.service

[Service]
Type=simple
User=joshua
WorkingDirectory=/home/joshua/ai-ids-new
ExecStart=/home/joshua/ai-ids-new/.venv/bin/python /home/joshua/ai-ids-new/run_model.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

Start + enable:
sudo systemctl daemon-reload
sudo systemctl enable ai-ids.service
sudo systemctl start ai-ids.service

Live logs:
sudo journalctl -u ai-ids.service -f

Real-Time Discord Alerts
Alerts appear in Discord like this:
🚨 AI-IDS Anomaly Detected 🚨
Time: 2025-11-20T19:58:43Z
Src: 192.168.1.50:54321
Dst: 142.250.72.14:80
Proto: tcp
Score: 0.943
These are triggered immediately whenever the model detects an anomaly.

Testing the IDS
Generate normal traffic
curl http://example.com
curl http://google.com

Generate suspicious-looking traffic
sudo nmap -sS 127.0.0.1 -p 1-200

Watch the live logs
sudo journalctl -u ai-ids.service -f

Check the anomaly log file
tail -n 10 anomalies.jsonl

Project Structure
ai-ids/
│
├── models/
│   └── ids_model.joblib
│
├── run_model.py
├── IDS_Training_Model.py
├── README.md
└── Documentation/

Future Enhancements (Planned)
Phase 2 — Full Network Coverage

Monitor the entire LAN through:
SPAN/mirror port
Gateway Suricata deployment
Router integration

Phase 3 — Full Discord Bot
Commands like:
/aiids status
/aiids anomalies
/aiids last10
/aiids threshold 0.5

Phase 4 — Visualization & Analytics
Grafana dashboards
Loki/Elasticsearch for log indexing
Traffic heatmaps
Attack trend analysis

Phase 5 — Auto-Tuning & Whitelisting
Dynamic threshold adjustment
Automated “known benign” flow suppression
Machine-driven threshold optimization

Conclusion
This project demonstrates:
Practical ML model training
Real-time network monitoring
Automation and alerting
Integration of multiple security technologies
Homelab deployment experience
Strong problem-solving and debugging workflow
It closely mirrors what professional SOC analysts, detection engineers, and cybersecurity researchers build in real-world environments.

Project Development Chat Log
The full iterative development, debugging, and deployment conversation is available here:
https://chatgpt.com/share/67cf6a46-da88-8012-83ad-599eccfca53d
https://chatgpt.com/share/691f86e1-7f54-8012-b2ff-79eb9f72066d
