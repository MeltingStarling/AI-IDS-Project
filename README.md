Hello! This project is one that I worked on for a long time and am really excited to share with everyone. I chose to start this as an Information Technology student who loves anything tech and really wanted to dip my feet into AI while also learning real cybersecurity tools and seeing if I can put this information to use for later.
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
This is Phase 1 of a multi-phase project, with future expansion planned to cover the entire home network via NIC mirroring, gateway routing, and Discord bot integration.
+--------------------+        +-----------------------+       +-----------------+
|   Network Traffic  | -----> |       Suricata        | ----> |     eve.json    |
+--------------------+        +-----------------------+       +-----------------+
                                         |
                                         v
                                +------------------+
                                |  AI-IDS Detector |
                                |  (Python + ML)   |
                                +------------------+
                                   |          |
                                   v          v
                          anomalies.jsonl   Discord Alerts
Dataset: UNSW-NB15

This project uses the UNSW-NB15 dataset — a widely used public dataset containing both normal and malicious traffic types.

Dataset source:
https://research.unsw.edu.au/projects/unsw-nb15-dataset
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

✔️ Data Preprocessing

Converted malformed headers

Cleaned and normalized data

Label-encoded categorical fields

Split dataset: 80% training / 20% testing

✔️ Hyperparameter Tuning

Used RandomizedSearchCV to efficiently test model configurations without long grid-search times.

✔️ Model Export

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
