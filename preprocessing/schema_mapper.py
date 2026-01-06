# preprocessing/schema_mapper.py

POSSIBLE_LABEL_COLUMNS = [
    "label",
    "Label",
    "class",
    "Class",
    "attack",
    "Attack",
    "attack_type",
    "Attack Type",
    "Attack_Type",
    "target",
    "Target",
    "result",
    "Result",
    "outcome",
    "Outcome",
    "severity",
    "Severity Level"
]

COLUMN_MAP = {
    "protocol_type": "protocol",
    "proto": "protocol",
    "Protocol": "protocol",
    "svc": "service"
}

def normalize_schema(df):
    # Normalize feature names
    df = df.rename(columns=COLUMN_MAP)

    # Detect and normalize label column
    for col in POSSIBLE_LABEL_COLUMNS:
        if col in df.columns:
            df = df.rename(columns={col: "label"})
            return df

    raise ValueError(
        f"[SCHEMA ERROR] No label column found. Columns present: {list(df.columns)}"
    )
