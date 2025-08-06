# utils/analysis.py

def assess_risk(field):
    """Assesses the OSINT risk level of a given metadata field."""
    field = field.lower()
    if any(x in field for x in ["gps", "location"]):
        return "Could reveal location"
    elif any(x in field for x in ["date", "time", "timestamp"]):
        return "Reveals timestamp"
    elif any(x in field for x in ["make", "model", "camera", "device"]):
        return "Device fingerprint"
    elif "software" in field or "producer" in field:
        return "Reveals software used"
    else:
        return "Low"