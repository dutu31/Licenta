import sqlite3
import os

db_path = r"dataset\database.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Numele imaginilor pe care vrem sa le scoatem definitiv din baza de date
    bad_images = ["query_test.png", "query_test_cropped.png"]
    
    for img_name in bad_images:
        cursor.execute("SELECT image_id FROM images WHERE name=?", (img_name,))
        row = cursor.fetchone()
        if row:
            img_id = row[0]
            cursor.execute("DELETE FROM images WHERE image_id=?", (img_id,))
            cursor.execute("DELETE FROM keypoints WHERE image_id=?", (img_id,))
            cursor.execute("DELETE FROM descriptors WHERE image_id=?", (img_id,))
            print(f"SUCCES: Am sters '{img_name}' (ID: {img_id}) din baza de date!")
        else:
            print(f"INFO: '{img_name}' nu a fost gasita in baza de date. E curat.")
            
    conn.commit()
    conn.close()
    print("\nBaza de date este acum curata si gata pentru o extindere corecta!")
else:
    print(f"Eroare: Nu am gasit baza de date la {db_path}")