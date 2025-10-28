from PIL import Image
import segno
import json
import os
import pandas as pd

BASE_OUTPUT_FOLDER = 'personalized_posters'
os.makedirs(BASE_OUTPUT_FOLDER, exist_ok=True)
os.makedirs('temp_qr', exist_ok=True)

QR_CONFIG = {
    "qr_x": 380,
    "qr_y": 480,
    "qr_size": 480,
}


def get_class_label(class_value):
    """Convert class value to proper label"""
    class_str = str(class_value).strip().upper()

    # Handle pre-primary specially
    if class_str in ['LKG', 'UKG', 'NURSERY', 'PRE-KG', 'PRE-PRIMARY']:
        return class_str

    # Regular classes (1-12)
    return class_str


def add_qr_only(poster_path, family_data, output_folder):
    """Add QR code and save to organized folder"""

    poster = Image.open(poster_path).convert('RGB')

    qr_content = json.dumps(family_data)
    qr = segno.make(qr_content, error='h')
    qr_path = f"temp_qr/{family_data['family_id']}.png"
    qr.save(qr_path, scale=15, border=1, dark='black', light='white')

    qr_img = Image.open(qr_path)
    qr_size = QR_CONFIG['qr_size']
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    poster.paste(qr_img, (QR_CONFIG['qr_x'], QR_CONFIG['qr_y']))

    os.makedirs(output_folder, exist_ok=True)

    student_name = family_data['student1']['name'].replace(' ', '_')
    filename = f"{family_data['family_id']}_{student_name}.png"
    output_path = os.path.join(output_folder, filename)

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

    test_folder = os.path.join(BASE_OUTPUT_FOLDER, "TEST")

    print("🧪 Creating test poster...")
    output = add_qr_only(poster_file, test_family, test_folder)
    print(f"✅ Test poster: {output}")


def process_all_organized():
    poster_file = "Avatarit Annual Day Invitation.png"
    excel_file = "student_data.xlsx"

    if not os.path.exists(poster_file):
        print(f"❌ Poster not found: {poster_file}")
        return

    if not os.path.exists(excel_file):
        print(f"❌ Excel not found: {excel_file}")
        print("\n💡 Create student_data.xlsx with columns:")
        print("   Family_ID, Student1_Name, Student1_AdmNo, Class, Section,")
        print("   Parent1_Name, Parent2_Name, Phone, Email")
        print("\n📋 For Class column, use:")
        print("   LKG, UKG (for pre-primary)")
        print("   1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 (for regular classes)")
        return

    df = pd.read_excel(excel_file)
    total = len(df)

    class_stats = {}
    grade_stats = {}

    print(f"\n🎨 Creating {total} posters organized by Class & Section...\n")
    print("=" * 70)

    for idx, row in df.iterrows():
        class_value = get_class_label(row['Class'])
        section = str(row['Section']).strip().upper()

        class_folder = f"Class_{class_value}"
        section_folder = f"Section_{section}"
        output_folder = os.path.join(BASE_OUTPUT_FOLDER, class_folder, section_folder)

        class_key = f"{class_value}-{section}"
        if class_key not in class_stats:
            class_stats[class_key] = 0
        class_stats[class_key] += 1

        if class_value not in grade_stats:
            grade_stats[class_value] = 0
        grade_stats[class_value] += 1

        family_data = {
            "family_id": str(row['Family_ID']),
            "student1": {
                "adm_no": str(row['Student1_AdmNo']),
                "name": str(row['Student1_Name']),
                "class": class_value,
                "section": section
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

        output_path = add_qr_only(poster_file, family_data, output_folder)

        print(f"[{idx + 1}/{total}] {class_value}-{section}: {family_data['student1']['name']}")
        print(f"          📁 {output_folder}")
        print(f"          ✅ {os.path.basename(output_path)}\n")

    print("=" * 70)
    print(f"\n✅ All {total} posters created!\n")

    # Summary by grade level
    print("📊 SUMMARY BY GRADE:\n")

    grade_order = ['LKG', 'UKG', 'NURSERY', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    for grade in grade_order:
        if grade in grade_stats:
            count = grade_stats[grade]
            print(f"   Grade {grade:>3}: {count:>3} students")

    print("\n📊 SUMMARY BY CLASS-SECTION:\n")
    for class_key in sorted(class_stats.keys()):
        count = class_stats[class_key]
        print(f"   Class {class_key}: {count} students")

    print(f"\n📁 All organized in: {BASE_OUTPUT_FOLDER}/")


def create_distribution_guide():
    excel_file = "student_data.xlsx"

    if not os.path.exists(excel_file):
        print("❌ Excel file needed")
        return

    df = pd.read_excel(excel_file)

    # Process class labels
    df['Class_Label'] = df['Class'].apply(get_class_label)
    df['Section'] = df['Section'].astype(str).str.strip().str.upper()

    grouped = df.groupby(['Class_Label', 'Section'])

    guide_content = """
🎓 CHRISTUKULA MISSION HIGHER SECONDARY SCHOOL
   AVATARIT 2025 - POSTER DISTRIBUTION GUIDE
═══════════════════════════════════════════════════════════════

📋 DISTRIBUTION INSTRUCTIONS:

Each class teacher receives ONE folder containing all posters
for their class-section. Folder contains individual posters
with student names in the filename for easy identification.

═══════════════════════════════════════════════════════════════

"""

    for (class_label, section), group in sorted(grouped):
        count = len(group)
        folder_path = f"personalized_posters/Class_{class_label}/Section_{section}/"

        guide_content += f"\n{'─' * 65}\n"
        guide_content += f"📚 CLASS {class_label}-{section}\n"
        guide_content += f"{'─' * 65}\n"
        guide_content += f"👥 Total Students: {count}\n"
        guide_content += f"📁 Folder: {folder_path}\n\n"
        guide_content += f"Students:\n"

        for idx, (_, row) in enumerate(group.iterrows(), 1):
            student_name = row['Student1_Name']
            family_id = row['Family_ID']
            guide_content += f"   {idx:>2}. {student_name:<30} ({family_id})\n"

        guide_content += f"\n✅ Give to: Class {class_label}-{section} teacher\n"

    guide_content += """

═══════════════════════════════════════════════════════════════
📱 TEACHER INSTRUCTIONS:

1. Receive folder for your class-section
2. Each poster filename = Family_ID + Student_Name
3. Send to parents via WhatsApp/Email
4. Ask parents to save/print for event day (November 12)

💡 BULK SENDING TIP:
   - Select all images in your folder
   - Share to class WhatsApp group
   - Or email all at once

═══════════════════════════════════════════════════════════════

📞 For support, contact: School Admin Office
   Phone: [Your Contact Number]
   Email: christukulamissionschool.com

═══════════════════════════════════════════════════════════════
"""

    guide_path = os.path.join(BASE_OUTPUT_FOLDER, "DISTRIBUTION_GUIDE.txt")
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)

    print(f"✅ Distribution guide: {guide_path}")
    return guide_path


if __name__ == '__main__':
    print("🎓 CHRISTUKULA MISSION - AVATARIT 2025")
    print("   QR Poster Generator (LKG - Class 12)")
    print("=" * 70)
    print("\n1. Test (create ONE poster)")
    print("2. Generate ALL (organized by Class → Section)")
    print("3. Create Distribution Guide")

    choice = input("\nChoose: ")

    if choice == "1":
        create_test()

    elif choice == "2":
        process_all_organized()
        print("\n💡 Next: Run option 3 to create distribution guide!")

    elif choice == "3":
        guide_path = create_distribution_guide()
        print(f"\n📄 Guide created! Print and give to teachers.")

    else:
        print("Invalid choice!")