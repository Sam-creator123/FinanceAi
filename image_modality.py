# image_metadata_extractor.py
import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

try:
    import exifread
    HAS_EXIFREAD = True
except Exception:
    HAS_EXIFREAD = False

def _convert_ratio_to_float(ratio):
    # ratio is usually a tuple like (num, den)
    try:
        num, den = ratio
        return float(num) / float(den) if den != 0 else 0.0
    except Exception:
        return float(ratio)

def _dms_to_decimal(dms, ref):
    # dms is ((deg_num,deg_den), (min_num,min_den), (sec_num,sec_den))
    try:
        degrees = _convert_ratio_to_float(dms[0])
        minutes = _convert_ratio_to_float(dms[1])
        seconds = _convert_ratio_to_float(dms[2])
        dec = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            dec = -dec
        return dec
    except Exception:
        return None

def extract_exif_pillow(image_path):
    """Extract EXIF using Pillow and return a dict with human-readable tags."""
    img = Image.open(image_path)
    exif_raw = img._getexif()  # may be None
    exif = {}
    if not exif_raw:
        return exif

    for tag_id, value in exif_raw.items():
        tag = TAGS.get(tag_id, tag_id)
        # If GPSInfo, decode nested tags
        if tag == "GPSInfo":
            gps_data = {}
            for t in value:
                sub_tag = GPSTAGS.get(t, t)
                gps_data[sub_tag] = value[t]
            exif["GPSInfo"] = gps_data
        else:
            exif[tag] = value
    return exif

def extract_exif_exifread(image_path):
    """Extract EXIF using exifread (if installed) for extra robustness."""
    if not HAS_EXIFREAD:
        return {}
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
    # convert tags to simple dict
    out = {}
    for k, v in tags.items():
        out[k] = str(v)
    return out

def get_image_metadata_features(image_path):
    """
    Returns a structured dict with:
      - basic file info (size, format, dimensions)
      - EXIF tags (DateTimeOriginal, Make, Model, Software, GPS)
      - parsed fields: datetime object, lat, lon
    """
    features = {}
    # Basic file info
    try:
        features['file_path'] = os.path.abspath(image_path)
        features['file_size_bytes'] = os.path.getsize(image_path)
    except Exception:
        features['file_size_bytes'] = None

    try:
        img = Image.open(image_path)
        features['format'] = img.format
        features['mode'] = img.mode
        features['width'], features['height'] = img.size
    except Exception:
        features['format'] = features['mode'] = None
        features['width'] = features['height'] = None

    # EXIF via Pillow
    exif = extract_exif_pillow(image_path)
    features['exif'] = exif  # keep raw exif for debugging

    # Common fields extracted if present
    #  - Date/time
    dt = exif.get('DateTimeOriginal') or exif.get('DateTime') or exif.get('DateTimeDigitized')
    parsed_dt = None
    if dt:
        # EXIF date format: "YYYY:MM:DD HH:MM:SS"
        try:
            parsed_dt = datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
        except Exception:
            try:
                parsed_dt = datetime.fromisoformat(dt)
            except Exception:
                parsed_dt = None
    features['datetime_original'] = parsed_dt.isoformat() if parsed_dt else None

    # Camera make/model/software
    features['camera_make'] = exif.get('Make')
    features['camera_model'] = exif.get('Model')
    features['software'] = exif.get('Software')

    # GPS extraction and conversion
    gps = exif.get('GPSInfo')
    lat = lon = None
    if gps:
        gps_lat = gps.get('GPSLatitude')
        gps_lat_ref = gps.get('GPSLatitudeRef')
        gps_lon = gps.get('GPSLongitude')
        gps_lon_ref = gps.get('GPSLongitudeRef')
        try:
            if gps_lat and gps_lat_ref and gps_lon and gps_lon_ref:
                lat = _dms_to_decimal(gps_lat, gps_lat_ref)
                lon = _dms_to_decimal(gps_lon, gps_lon_ref)
        except Exception:
            lat = lon = None
    features['gps_latitude'] = lat
    features['gps_longitude'] = lon
    features['has_gps'] = int(lat is not None and lon is not None)

    # Optional: EXIF via exifread (stringified)
    if HAS_EXIFREAD:
        features['exifread_raw'] = extract_exif_exifread(image_path)

    return features

# ---------------- Example usage ----------------
if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Extract image metadata features")
    parser.add_argument("image_path", help="Path to image file")
    parser.add_argument("--out", help="Write JSON output to file", default=None)
    args = parser.parse_args()

    feats = get_image_metadata_features(args.image_path)
    pretty = json.dumps(feats, indent=2, default=str)
    print(pretty)

    if args.out:
        with open(args.out, "w") as f:
            f.write(pretty)
        print(f"Wrote metadata to {args.out}")
