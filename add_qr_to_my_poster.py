from PIL import Image
import segno
import json
import os
import pandas as pd

os.makedirs('personalized_posters', exist_ok=True)
os.makedirs('temp_qr', exist_ok=True)

# CENTERED QR POSITION - Adjusted RIGHT and DOWN
QR_CONFIG = {
    "qr_x": 380,  # Moved right to center
    "qr_y": 480,  # Moved down to center
    "qr_size": 480,  # Perfect scanning size
}


def add_qr_only(poster_path, family_data):
    """Add ONLY QR code to poster - perfectly centered"""

    poster = Image.open(poster_path).convert('RGB')

    # Generate QR
    qr_content = json.dumps(family_data)
    qr = segno.make(qr_content, error='h')
    qr_path = f"temp_qr/{family_data['family_id']}.png"
    qr.save(qr_path, scale=15, border=1, dark='black', light='white')

    # Load and resize QR
    qr_img = Image.open(qr_path)
    qr_size = QR_CONFIG['qr_size']
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # Paste QR centered
    poster.paste(qr_img, (QR_CONFIG['qr_x'], QR_CONFIG['qr_y']))

    # Save
    output_path = f"personalized_posters/{family_data['family_id']}_avatarit.png"
    poster.save(output_path, quality=95)

    os.remove(qr_path)
    return output_path


def create_test():
    poster_file = "Avatarit Annual Day Invitation.png"

    if not os.path.exists(poster_file):
        print(f"❌ Poster not found: {poster_file}")
        return

    test_family = {
        "family_id": "FAM-TEST-001",
        "student1": {
            "adm_no": "A12345",
            "name": "Rajesh Kumar",
            "class": "10",
            "section": "A"
        },
        "parents": ["Mr. Suresh Kumar", "Mrs. Anita Kumar"],
        "event": "Avatarit 2025",
        "phone": "9876543210"
    }

    print("🎯 Creating centered QR test poster...")
    output = add_qr_only(poster_file, test_family)
    print(f"✅ {output}")
    print(f"\n📍 QR Position: X={QR_CONFIG['qr_x']}, Y={QR_CONFIG['qr_y']}")
    print(f"📏 QR Size: {QR_CONFIG['qr_size']}px")


def process_all():
    poster_file = "Avatarit Annual Day Invitation.png"
    excel_file = "student_data.xlsx"

    if not os.path.exists(poster_file) or not os.path.exists(excel_file):
        print("❌ Missing files!")
        return

    df = pd.read_excel(excel_file)
    total = len(df)

    print(f"\n🎨 Creating {total} personalized posters...\n")

    for idx, row in df.iterrows():
        family_data = {
            "family_id": str(row['Family_ID']),
            "student1": {
                "adm_no": str(row['Student1_AdmNo']),
                "name": str(row['Student1_Name']),
                "class": str(row['Class']),
                "section": str(row['Section'])
            },
            "parents": [str(row['Parent1_Name'])],
            "event": "Avatarit 2025",
            "phone": str(row['Phone'])
        }

        if pd.notna(row.get('Parent2_Name')):
            family_data['parents'].append(str(row['Parent2_Name']))

        if pd.notna(row.get('Student2_Name')):
            family_data['student2'] = {
                "adm_no": str(row['Student2_AdmNo']),
                "name": str(row['Student2_Name']),
                "class": str(row.get('Student2_Class', '')),
                "section": str(row.get('Student2_Section', ''))
            }

        add_qr_only(poster_file, family_data)
        print(f"[{idx + 1}/{total}] ✅ {family_data['family_id']}")

    print(f"\n🎉 Done! All posters in 'personalized_posters' folder")


if __name__ == '__main__':
    print("🎓 AVATARIT - QR Code Generator")
    print("=" * 50)
    print("\n1. Test (create ONE)")
    print("2. Generate ALL")

    choice = input("\nChoose: ")

    if choice == "1":
        create_test()
    elif choice == "2":
        process_all()