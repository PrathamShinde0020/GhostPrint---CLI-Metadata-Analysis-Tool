# utils/image_parser.py

from PIL import Image, ExifTags

def extract_image_metadata_human_friendly(file_path):
    """Extracts key metadata from an image file in a human-readable format."""
    metadata_list = []
    summary = {"gps": False, "camera": False, "timestamp": False}
    full_data = {}

    try:
        img = Image.open(file_path)
        exif_data = img._getexif()

        if not exif_data:
            metadata_list.append(["No EXIF Data", "N/A", "Low"])
        else:
            for tag_id, value in exif_data.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                full_data[tag] = value

            key_fields = {
                "Make": ["Camera Make", "Device fingerprint"],
                "Model": ["Camera Model", "Device fingerprint"],
                "DateTime": ["Date Taken", "Reveals user activity timestamp"],
                "Software": ["Software Used", "Reveals software used"],
            }

            for field, (display_name, risk) in key_fields.items():
                if field in full_data:
                    metadata_list.append([display_name, str(full_data[field]), risk])
                    if field in ["Make", "Model"]:
                        summary["camera"] = True
                    elif field == "DateTime":
                        summary["timestamp"] = True

            gps_data = full_data.get("GPSInfo")
            if gps_data:
                summary["gps"] = True
                metadata_list.append(["Location (GPS)", "Available", "Could reveal location"])
            else:
                metadata_list.append(["Location (GPS)", "Not available", "Low"])

        return metadata_list, summary, full_data, img

    except Exception as e:
        metadata_list.append(["Error", str(e), "High"])
        return metadata_list, summary, {}, None