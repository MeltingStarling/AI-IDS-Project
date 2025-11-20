#!/usr/bin/env python3
import json
import time
import os
from pathlib import Path
import requests

from joblib import load
import pandas as pd

EVE = "/var/log/suricata/eve.json"
MODEL_PATH = "models/ids_model.joblib"
THRESH = 0.5  # threshold if predict_proba is available

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1441114252155818128/FIDCaUDl9FONDDdIBxI_IflUnOSNhGLno9K11iZFsfPUxUiIUSf5kAWx9QaUE0d0Fe_u"

def send_discord_alert(record: dict):
    if not DISCORD_WEBHOOK_URL:
        return

    try:
        msg = (
            "🚨 **AI-IDS Anomaly Detected** 🚨\n"
            f"**Time:** {record.get('ts')}\n"
            f"**Src:** {record.get('src')}:{record.get('sport')}\n"
            f"**Dst:** {record.get('dst')}:{record.get('dport')}\n"
            f"**Proto:** {record.get('proto')}\n"
            f"**Score:** {record.get('score'):.3f}"
        )
        payload = {"content": msg}
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"[AI-IDS] Discord send failed: {e}", flush=True)



FEATURE_ORDER = [
    "proto_num",
    "dur",
    "sbytes",
    "dbytes",
    "spkts",
    "dpkts",
    "sttl",
    "dttl",
]

PROTO_MAP = {
    "tcp": 6,
    "udp": 17,
    "icmp": 1,
    "arp": 252,
    "ospf": 89,
}


def proto_to_num(p):
    if isinstance(p, str):
        return PROTO_MAP.get(p.lower(), 0)
    return 0


print(f"[AI-IDS] Loading model from {MODEL_PATH} ...", flush=True)
model = load(MODEL_PATH)
print("[AI-IDS] Model loaded.", flush=True)


def features_from_event(evt: dict) -> dict:
    flow = evt.get("flow", {}) or {}

    dur = flow.get("age", 0) or 0
    sbytes = flow.get("bytes_toserver", 0) or 0
    dbytes = flow.get("bytes_toclient", 0) or 0
    spkts = flow.get("pkts_toserver", 0) or 0
    dpkts = flow.get("pkts_toclient", 0) or 0

    sttl = flow.get("toserver_timedelta", 0) or 0
    dttl = flow.get("toclient_timedelta", 0) or 0

    proto_num = proto_to_num(evt.get("proto", ""))

    return {
        "proto_num": proto_num,
        "dur": dur,
        "sbytes": sbytes,
        "dbytes": dbytes,
        "spkts": spkts,
        "dpkts": dpkts,
        "sttl": sttl,
        "dttl": dttl,
    }


def df_from_event(evt: dict) -> pd.DataFrame:
    feats = features_from_event(evt)
    for k in FEATURE_ORDER:
        feats.setdefault(k, 0)
    return pd.DataFrame([[feats[k] for k in FEATURE_ORDER]], columns=FEATURE_ORDER)


def score_event(X: pd.DataFrame):
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X)[0]
        score = float(prob[-1]) if len(prob) == 2 else float(max(prob))
        label = 1 if score >= THRESH else 0
        return label, score
    else:
        y = int(model.predict(X)[0])
        return y, None


def follow(path: str):
    with open(path, "r", buffering=1) as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line


def main():
    out_file = Path("anomalies.jsonl")
    print(f"[AI-IDS] Streaming Suricata events from {EVE}", flush=True)

    for line in follow(EVE):
        try:
            evt = json.loads(line)
        except Exception:
            continue

        if evt.get("event_type") != "flow":
            continue

        X = df_from_event(evt)
        label, score = score_event(X)

	# DEBUG: see what the model thinks about each flow
        print(
            f"[FLOW] {evt.get('src_ip')}:{evt.get('src_port')} -> "
            f"{evt.get('dest_ip')}:{evt.get('dest_port')}, "
            f"label={label}, score={score}",
            flush=True,
        )
        if label == 1:
            record = {
                "ts": evt.get("timestamp"),
                "src": evt.get("src_ip"),
                "sport": evt.get("src_port"),
                "dst": evt.get("dest_ip"),
                "dport": evt.get("dest_port"),
                "proto": evt.get("proto"),
                "score": score,
            }
            line_out = json.dumps(record)
            print("[ANOMALY]", line_out, flush=True)
            with out_file.open("a") as f:
                f.write(line_out + "\n")

		# 🔔 NEW: send Discord alert
            send_discord_alert(record)


if __name__ == "__main__":
    main()
