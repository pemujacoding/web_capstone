from .connect import cursor, db
import json

def insert_new_interview_session(user_id,candidate_id):
    sql = "INSERT INTO interview (user_id, candidate_id, status) VALUES (%s,%s,'Pending')"
    cursor.execute(sql, (user_id,candidate_id))
    new_session_id = cursor.lastrowid
    db.commit() 
    return new_session_id

def update_interview(result,id) :
    sql = "UPDATE interview SET status='Succeed',result=%s WHERE id = %s"
    cursor.execute(sql, (result,id))
    db.commit()

def get_by_id(interview_id) :
    sql = "SELECT * FROM interview WHERE id = %s"
    cursor.execute(sql, (interview_id,))
    result = cursor.fetchone()
    return result

def delete_interview(interview_id) :
    sql = "DELETE FROM interview WHERE id = %s"
    cursor.execute(sql, (interview_id,))
    db.commit()

def get_for_final(user_id,interview_id) :
    sql = '''
    SELECT 
    i.id AS interview_id,
    i.user_id,
    i.candidate_id,
    i.result,
    u.full_name,
    u.email AS user_email,
    c.name,
    c.email AS candidate_email,
    c.photoUrl
    FROM interview i
    INNER JOIN users u ON i.user_id = u.id
    INNER JOIN candidates c ON i.candidate_id = c.id
    WHERE i.user_id = %s AND i.id = %s 
    '''
    cursor.execute(sql, (user_id,interview_id))
    result = cursor.fetchone()
    return result

def get_history(user_id):
    sql = '''
    SELECT 
        i.id AS interview_id,
        i.user_id,
        i.candidate_id,
        i.result,
        i.status,
        i.created_at,
        v.id AS video_id,
        v.file_name,
        v.result_cd,
        v.result_stt
    FROM interview i
    LEFT JOIN input v ON v.interview_id = i.id
    WHERE i.user_id = %s
    ORDER BY i.created_at DESC, v.id ASC;
    '''
    cursor.execute(sql, (user_id,))
    rows = cursor.fetchall()

    interviews = {}

    for r in rows:
        iid = r[0]

        # hanya buat interview sekali saja
        if iid not in interviews:
            interviews[iid] = {
                "interview_id": r[0],
                "user_id": r[1],
                "candidate_id":r[2],
                "result_interview":r[3],
                "status": r[4],
                "created_at": r[5],
                "videos": []
            }

        # tambahkan video jika ada
        if r[4] is not None:  # video_id
            interviews[iid]["videos"].append({
                "video_id": r[6],
                "file_name": r[7],
                "result_cd": r[8],
                "result_stt": r[9]
            })

    return list(interviews.values())

# Tambahkan di akhir file model/interview.py

import json
import re

def clean_json_string(json_str):
    if not json_str:
        return "{}"
    cleaned = re.sub(r'^```json\s*', '', json_str, flags=re.MULTILINE)
    cleaned = re.sub(r'^```\s*', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'```$', '', cleaned)
    return cleaned.strip()

def get_interviews_checklist(json_str):
    cleaned = clean_json_string(json_str)
    try:
        data = json.loads(cleaned)
        scores_list = data.get("scores", [])
        valid_scores = []
        for item in scores_list:
            score_item = {
                "id": item.get("id", 0),  # Default jika kosong
                "score": item.get("score", 0),
                "reason": item.get("reason", "No reason provided")  # Default jika tidak ada
            }
            valid_scores.append(score_item)
        
        interviews = {
            "minScore": data.get("minScore", 0),
            "maxScore": data.get("maxScore", 4),
            "scores": valid_scores
        }
        return interviews
    except json.JSONDecodeError as e:
        print(f"[ERROR] Gagal parse interview JSON: {e} - Cleaned string: {cleaned}")
        return {
            "minScore": 0,
            "maxScore": 4,
            "scores": []
        }
    except Exception as e:
        print(f"[ERROR] Exception in checklist: {e}")
        return {
            "minScore": 0,
            "maxScore": 4,
            "scores": []
        }

def parse_interview_score_normalized(json_str):
    """Sama seperti sebelumnya, untuk hitung interview score 0-100"""
    cleaned = clean_json_string(json_str)
    try:
        data = json.loads(cleaned)
        scores_list = data.get("scores", [])
        if not scores_list:
            return 0.0
        total = sum(item.get("score", 0) for item in scores_list if isinstance(item.get("score"), (int, float)))
        count = len([s for s in scores_list if isinstance(s.get("score"), (int, float))])
        if count == 0:
            return 0.0
        avg = total / count
        return round((avg / 4.0) * 100, 2)
    except:
        return 0.0