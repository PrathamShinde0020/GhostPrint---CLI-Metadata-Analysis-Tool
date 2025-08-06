# utils/pdf_parser.py

from PyPDF2 import PdfReader
from .analysis import assess_risk  # Import from your own utils

def extract_pdf_metadata_human_friendly(file_path):
    """Extracts key metadata from a PDF file in a human-readable format."""
    metadata_list = []
    summary = {"creator": False, "producer": False, "timestamp": False}
    full_meta = {}

    try:
        reader = PdfReader(file_path)
        doc_info = reader.metadata

        if doc_info is None:
            metadata_list.append(["No PDF Metadata", "N/A", "Low"])
            return metadata_list, summary, full_meta, len(reader.pages)

        full_meta = {k: v for k, v in doc_info.items()} if doc_info else {}

        for key, value in full_meta.items():
            tag = key.replace("/", "")
            value_str = str(value)
            risk = assess_risk(tag)  # Use the imported function

            metadata_list.append([tag, value_str, risk])

            if "creator" in tag.lower() or "author" in tag.lower():
                summary["creator"] = True
            elif "producer" in tag.lower() or "software" in tag.lower():
                summary["producer"] = True
            elif any(x in tag.lower() for x in ["date", "time", "created", "modified"]):
                summary["timestamp"] = True

        return metadata_list, summary, full_meta, len(reader.pages)

    except Exception as e:
        metadata_list.append(["Error", str(e), "High"])
        return metadata_list, summary, {}, 0