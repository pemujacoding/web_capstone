from .connect import cursor, db
import json

def get_by_id(interview_id):
    sql = "SELECT * FROM final_result WHERE interview_id = %s;"
    cursor.execute(sql, (interview_id,))
    result = cursor.fetchone()
    return result  # Return tuple, kolom final_result di index 2

def save_final_result(interview_id, json_data):
    """
    Simpan JSON lengkap (dict) ke kolom final_result.
    """
    json_str = json.dumps(json_data, indent=4, ensure_ascii=False)
    # Jika panjang > 500, pertimbangkan ALTER TABLE ke TEXT
    existing = get_by_id(interview_id)
    if existing:
        sql = "UPDATE final_result SET final_result = %s WHERE interview_id = %s"
        cursor.execute(sql, (json_str, interview_id))
    else:
        sql = "INSERT INTO final_result (interview_id, final_result) VALUES (%s, %s)"
        cursor.execute(sql, (interview_id, json_str))
    db.commit()
    
    
def parse_final_data(json_str):
    if not json_str:
        return {}
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Gagal parse final JSON: {e}")
        return {}