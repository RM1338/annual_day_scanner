import qrcode
import json
import os

os.makedirs('test_qr_codes', exist_ok=True)

families = [
    {
        "family_id": "FAM-2025-0001",
        "student1": {"adm_no": "A12345", "name": "Rahul Kumar", "class": "10", "section": "A"},
        "parents": ["Mr. Suresh Kumar", "Mrs. Anita Kumar"],
        "event": "Annual Day 2025",
        "phone": "9876543210"
    },
    {
        "family_id": "FAM-2025-0002",
        "student1": {"adm_no": "A12346", "name": "Priya Sharma", "class": "9", "section": "B"},
        "student2": {"adm_no": "A12399", "name": "Rohan Sharma", "class": "7", "section": "B"},
        "parents": ["Mr. Amit Sharma", "Mrs. Neha Sharma"],
        "event": "Annual Day 2025",
        "phone": "9876543211"
    },
    {
        "family_id": "FAM-2025-0003",
        "student1": {"adm_no": "A12347", "name": "Anjali Patel", "class": "11", "section": "C"},
        "parents": ["Mr. Rajesh Patel", "Mrs. Meera Patel"],
        "event": "Annual Day 2025",
        "phone": "9876543212"
    },
    {
        "family_id": "FAM-2025-0004",
        "student1": {"adm_no": "A12348", "name": "Vikram Singh", "class": "8", "section": "A"},
        "parents": ["Mr. Harpreet Singh", "Mrs. Simran Singh"],
        "event": "Annual Day 2025",
        "phone": "9876543213"
    },
    {
        "family_id": "FAM-2025-0005",
        "student1": {"adm_no": "A12349", "name": "Sneha Reddy", "class": "10", "section": "B"},
        "parents": ["Mr. Venkat Reddy", "Mrs. Lakshmi Reddy"],
        "event": "Annual Day 2025",
        "phone": "9876543214"
    }
]

for family in families:
    qr_content = json.dumps(family)

    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"test_qr_codes/{family['family_id']}.png"
    img.save(filename)
    print(f"✅ Created: {filename}")

print("\n🎉 Generated 5 test QR codes!")