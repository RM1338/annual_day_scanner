from PIL import Image, ImageDraw, ImageFont
import segno
import json
import os
import pandas as pd

os.makedirs('event_posters', exist_ok=True)
os.makedirs('temp_qr', exist_ok=True)

# Event Configuration - CUSTOMIZE THIS!
EVENT_CONFIG = {
    "title": "ANNUAL DAY",
    "subtitle": "INVITE",
    "school_name": "High School",
    "date": "MARCH 15, 2028",
    "description": "Come and join us for a day filled with fun,\ncelebration and music",
    "venue": "123 Anywhere St., Any City, ST 12345",
    "website": "www.reallygreatsite.com",
    "bg_color": (19, 55, 43),  # Dark green #13372B
    "gold_color": (197, 166, 109)  # Gold #C5A66D
}


def create_elegant_poster(family_data):
    """Create elegant green and gold themed poster"""

    width, height = 1080, 1920

    # Dark green background
    poster = Image.new('RGB', (width, height), EVENT_CONFIG['bg_color'])
    draw = ImageDraw.Draw(poster)

    # Load fonts
    try:
        font_school = ImageFont.truetype("arial.ttf", 80)
        font_title = ImageFont.truetype("arialbd.ttf", 110)
        font_subtitle = ImageFont.truetype("arial.ttf", 85)
        font_date = ImageFont.truetype("arialbd.ttf", 55)
        font_text = ImageFont.truetype("arial.ttf", 42)
        font_small = ImageFont.truetype("arial.ttf", 38)
        font_info = ImageFont.truetype("arialbd.ttf", 45)
    except:
        font_school = font_title = font_subtitle = font_date = font_text = font_small = font_info = ImageFont.load_default()

    gold = EVENT_CONFIG['gold_color']
    white = (255, 255, 255)

    # Draw decorative corner borders
    border_width = 8
    corner_length = 250

    # Top-left
    draw.line([(80, 80), (80 + corner_length, 80)], fill=gold, width=border_width)
    draw.line([(80, 80), (80, 80 + corner_length)], fill=gold, width=border_width)

    # Top-right
    draw.line([(width - 80, 80), (width - 80 - corner_length, 80)], fill=gold, width=border_width)
    draw.line([(width - 80, 80), (width - 80, 80 + corner_length)], fill=gold, width=border_width)

    # Bottom-left
    draw.line([(80, height - 80), (80 + corner_length, height - 80)], fill=gold, width=border_width)
    draw.line([(80, height - 80), (80, height - 80 - corner_length)], fill=gold, width=border_width)

    # Bottom-right
    draw.line([(width - 80, height - 80), (width - 80 - corner_length, height - 80)], fill=gold, width=border_width)
    draw.line([(width - 80, height - 80), (width - 80, height - 80 - corner_length)], fill=gold, width=border_width)

    y_pos = 180

    # School name
    school_name = EVENT_CONFIG['school_name']
    bbox = draw.textbbox((0, 0), school_name, font=font_school)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, y_pos), school_name, fill=gold, font=font_school)
    y_pos += 140

    # ANNUAL DAY title
    title = EVENT_CONFIG['title']
    bbox = draw.textbbox((0, 0), title, font=font_title)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, y_pos), title, fill=white, font=font_title)
    y_pos += 140

    # INVITE subtitle
    subtitle = EVENT_CONFIG['subtitle']
    bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, y_pos), subtitle, fill=white, font=font_subtitle)
    y_pos += 140

    # Graduation cap icon
    cap_center_x = width // 2
    cap_y = y_pos + 50
    cap_size = 180

    # Cap top
    draw.rectangle([
        (cap_center_x - cap_size // 2, cap_y),
        (cap_center_x + cap_size // 2, cap_y + 15)
    ], outline=gold, width=4)

    # Cap base
    draw.polygon([
        (cap_center_x - 60, cap_y + 15),
        (cap_center_x + 60, cap_y + 15),
        (cap_center_x + 50, cap_y + 70),
        (cap_center_x - 50, cap_y + 70)
    ], outline=gold, width=4)

    # Tassel
    draw.line([(cap_center_x + cap_size // 2 - 20, cap_y),
               (cap_center_x + cap_size // 2 + 20, cap_y + 80)],
              fill=gold, width=4)
    draw.ellipse([
        (cap_center_x + cap_size // 2 + 10, cap_y + 80),
        (cap_center_x + cap_size // 2 + 30, cap_y + 100)
    ], outline=gold, width=4)

    y_pos += 250

    # Date
    date_text = EVENT_CONFIG['date']
    bbox = draw.textbbox((0, 0), date_text, font=font_date)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, y_pos), date_text, fill=white, font=font_date)
    y_pos += 100

    # Description
    desc_lines = EVENT_CONFIG['description'].split('\n')
    for line in desc_lines:
        bbox = draw.textbbox((0, 0), line, font=font_text)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, y_pos), line, fill=white, font=font_text)
        y_pos += 55

    y_pos += 30

    # Venue
    venue_text = EVENT_CONFIG['venue']
    bbox = draw.textbbox((0, 0), venue_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, y_pos), venue_text, fill=white, font=font_small)
    y_pos += 120

    # Decorative line
    line_width = 400
    draw.line([
        (width // 2 - line_width // 2, y_pos),
        (width // 2 + line_width // 2, y_pos)
    ], fill=gold, width=3)
    y_pos += 80

    # "Your Entry Pass"
    pass_text = "YOUR ENTRY PASS"
    bbox = draw.textbbox((0, 0), pass_text, font=font_info)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, y_pos), pass_text, fill=gold, font=font_info)
    y_pos += 100

    # Generate QR code
    qr_content = json.dumps(family_data)
    qr = segno.make(qr_content, error='h')
    qr_path = f"temp_qr/{family_data['family_id']}.png"
    qr.save(qr_path, scale=12, border=2)

    # Load QR
    qr_img = Image.open(qr_path)
    qr_size = 400
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    # White border around QR
    qr_border = 20
    qr_bg = Image.new('RGB', (qr_size + qr_border * 2, qr_size + qr_border * 2), white)
    qr_bg.paste(qr_img, (qr_border, qr_border))

    # Gold border
    gold_border = 8
    qr_final = Image.new('RGB',
                         (qr_size + qr_border * 2 + gold_border * 2,
                          qr_size + qr_border * 2 + gold_border * 2),
                         gold)
    qr_final.paste(qr_bg, (gold_border, gold_border))

    qr_x = (width - qr_final.width) // 2
    poster.paste(qr_final, (qr_x, y_pos))

    y_pos += qr_final.height + 60

    # Family details box
    box_padding = 80
    box_width = width - box_padding * 2
    box_height = 220

    draw.rectangle([
        (box_padding, y_pos),
        (width - box_padding, y_pos + box_height)
    ], outline=gold, width=6)

    info_y = y_pos + 40

    # Family ID
    id_text = f"Family ID: {family_data['family_id']}"
    bbox = draw.textbbox((0, 0), id_text, font=font_info)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, info_y), id_text, fill=gold, font=font_info)
    info_y += 60

    # Student name
    student_text = family_data['student1']['name']
    bbox = draw.textbbox((0, 0), student_text, font=font_text)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, info_y), student_text, fill=white, font=font_text)
    info_y += 55

    # Class
    class_text = f"Class {family_data['student1']['class']}-{family_data['student1']['section']}"
    bbox = draw.textbbox((0, 0), class_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, info_y), class_text, fill=white, font=font_small)

    y_pos += box_height + 60

    # Bottom line
    draw.line([
        (width // 2 - line_width // 2, y_pos),
        (width // 2 + line_width // 2, y_pos)
    ], fill=gold, width=3)
    y_pos += 50

    # Website
    website_text = f"More information:\n{EVENT_CONFIG['website']}"
    lines = website_text.split('\n')
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_small)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, y_pos), line, fill=white, font=font_small)
        y_pos += 50

    # Save
    output_path = f"event_posters/{family_data['family_id']}_poster.png"
    poster.save(output_path, quality=95)

    os.remove(qr_path)

    return output_path


def process_all_families(excel_path):
    """Generate posters for all families"""
    df = pd.read_excel(excel_path)
    total = len(df)

    print(f"\n🎨 Generating {total} elegant event posters...\n")
    print("=" * 60)

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
            "event": "Annual Day 2025",
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

        print(f"[{idx + 1}/{total}] Creating poster for {family_data['family_id']}...")
        poster_path = create_elegant_poster(family_data)
        print(f"           ✅ Saved: {poster_path}\n")

    print("=" * 60)
    print(f"✅ All {total} posters created!")
    print(f"📁 Check 'event_posters' folder")


if __name__ == '__main__':
    excel_file = "student_data.xlsx"
    if os.path.exists(excel_file):
        print("🎭 ANNUAL DAY 2025 - ELEGANT POSTER GENERATOR")
        print("=" * 60)
        print(f"\n📝 Event Configuration:")
        print(f"   School: {EVENT_CONFIG['school_name']}")
        print(f"   Title: {EVENT_CONFIG['title']}")
        print(f"   Date: {EVENT_CONFIG['date']}")
        print(f"   Venue: {EVENT_CONFIG['venue']}")
        print()
        process_all_families(excel_file)
    else:
        print(f"❌ {excel_file} not found!")
        print("\nCreate an Excel file with columns:")
        print("Family_ID, Student1_Name, Student1_AdmNo, Class, Section, Parent1_Name, Phone")