from flask import Flask, render_template, request, redirect, url_for, flash, session
import model.users as conn_users
import model.interview as conn_interview
import model.candidates as conn_candidates
import model.final_result as conn_final
import os
import json
import processing.input_process as p_input
import processing.gemini as g_input
import tempfile
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_i_am_fixing_my_app'

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = conn_users.check_user(username,password)
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            return redirect(url_for("homepage"))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        email = request.form.get("email")

        try:
            conn_users.create_user(username,password,fullname,email)
            
            flash(f"Account for {username} created successfully! Please log in.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            print(f"Error creating user: {e}")
            flash("Could not create account. Username might already exist.", "error")
            return render_template("signin.html")

    return render_template("signin.html")

@app.route("/dashboard/", methods=["GET", "POST"])

@app.route("/dashboard/homepage", methods=["GET", "POST"])
def homepage():
    if 'user_id' not in session:
        flash("Please log in to view the dashboard.", "error")
        return redirect(url_for('login'))
    username = session.get('username', 'Guest')
    return render_template("homepage.html",username=username)

@app.route('/logout')
def logout():
    # Remove the user_id and username from the session
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route("/dashboard/history", methods=["GET", "POST"])
def history():
    if 'user_id' not in session:
        flash("Please log in to view the dashboard.", "error")
        return redirect(url_for('login'))
    user_id = session.get('user_id', 'Guest_id')
    interview_list = conn_interview.get_history(user_id)
    return render_template("history.html",interview_list=interview_list)

@app.route("/dashboard/candidates", methods=["GET", "POST"])
def candidates():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "error")
        return redirect(url_for('login'))
    candidates = conn_candidates.get_candidates()
    return render_template('candidates.html',candidates = candidates)

@app.route("/dashboard/add_candidates", methods=["GET", "POST"])
def add_candidates():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "error")
        return redirect(url_for('login'))
    
    if request.method == "POST" :
        name = request.form.get("name")
        email = request.form.get("email")
        photo = request.form.get("photo")
        try:
            conn_candidates.insert(name,email,photo)
            
            flash(f"Candidate {name} succesfully added", "success")
            return redirect(url_for("candidates"))

        except Exception as e:
            flash("Could not add candidate", "error")
            return render_template("add_candidate.html")
    return render_template('add_candidates.html')

@app.route("/dashboard/edit_candidate/<int:candidate_id>", methods=["GET", "POST"])
def edit_candidate(candidate_id):
    candidate = conn_candidates.get_by_id(candidate_id)
    if not candidate:
        flash("Candidate not found!", "error")
        return redirect(url_for("candidates"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        photoUrl = request.form.get("photoUrl")

        if not name or not email:
            flash("Name and email are required!", "error")
            return redirect(request.url)
        
        try :
            conn_candidates.update(candidate_id, name, email, photoUrl)
            flash("Candidate updated successfully!", "success")
            return redirect(url_for("candidates"))
        except :
            flash("Update failed", "danger")
    return render_template("edit_candidate.html", candidate=candidate)

@app.route("/dashboard/delete_candidate/<int:candidate_id>", methods=["GET","POST"])
def delete_candidate(candidate_id):
    candidate = conn_candidates.get_by_id(candidate_id)
    if not candidate:
        flash("Candidate not found!", "error")
        return redirect(url_for("candidates"))

    conn_candidates.delete(candidate_id)
    flash("Candidate deleted successfully!", "success")
    return redirect(url_for("candidates"))


@app.route("/dashboard/final_result/<int:interview_id>", methods=["GET", "POST"])
def final_result(interview_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "error")
        return redirect(url_for('login'))
    
    interview = conn_interview.get_for_final(session['user_id'], interview_id)
    if not interview:
        flash("Interview not found!", "error")
        return redirect(url_for("history"))
    
    # Data candidate untuk assessorProfile (index: 2=id, 6=name, 8=photoUrl)
    candidate_id = interview[2]
    candidate_name = interview[6]
    candidate_photo = interview[8] or ""  # Default kosong jika None
    
    final_tuple = conn_final.get_by_id(interview_id)
    final_json_str = final_tuple[2] if final_tuple else None  # Untuk tampilan jika perlu
    
    interview_json_raw = interview[3]  # result dari interview
    
    # Hitung interview_score untuk overview
    interview_score = conn_interview.parse_interview_score_normalized(interview_json_raw)
    
    existing_recommendation = "No recommendation available"
    if final_tuple:
        try:
            existing_data = json.loads(final_tuple[2])
            existing_recommendation = existing_data.get("recommendation", "No recommendation available")
        except:
            pass
    
    if request.method == "POST":
        project_name = request.form.get("project_name", "").strip()
        project_score = float(request.form.get("project_score", 0))
        notes = request.form.get("notes", "")

        # Validasi project name (minimal tidak kosong)
        if not project_name:
            flash("Project name is required.", "error")
            return redirect(request.url)
        
        if project_score < 0 or project_score > 100:
            flash("Project score must be between 0 and 100.", "error")
            return redirect(request.url)
        
        # Hitung total dengan bobot
        total_score = round((project_score * 0.715) + (interview_score * 0.285), 2)
        
        # Ambil interviews checklist
        interviews_checklist = conn_interview.get_interviews_checklist(interview_json_raw)
        
        if total_score >= 90:
            recommendation = "PASS - Candidate exceeds expectations and is recommended for hiring based on industry standards."
        elif 70 <= total_score < 90:
            recommendation = "CONSIDERED - Candidate meets basic requirements but may need further evaluation or training for industry fit."
        else:
            recommendation = "REJECTED - Candidate does not meet the required thresholds for this role based on industry benchmarks."
        
        # Buat JSON lengkap
        final_data = {
            "assessorProfile": {
                "id": candidate_id,
                "name": candidate_name,
                "photoUrl": candidate_photo
            },
            "decision": "Need Human",
            "reviewedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scoresOverview": {
                "project": project_score,
                "interview": interview_score,
                "total": total_score
            },
            "reviewChecklistResult": {
                "project": [project_name],
                "interviews": interviews_checklist
            },
            "Overall notes": notes,
            "recommendation": recommendation
        }
        
        
        conn_final.save_final_result(interview_id, final_data)
        
        flash("Final result saved successfully!", "success")
        return redirect(request.url)
    
    # Parsing existing JSON untuk pre-fill form (jika ada)
    existing_project_name = ""
    existing_project_score = ""
    existing_notes = ""
    if final_tuple:
        try:
            existing_data = json.loads(final_tuple[2])
            existing_project_name = existing_data.get("reviewChecklistResult", {}).get("project", [""])[0]
            existing_project_score = existing_data.get("scoresOverview", {}).get("project", 0)
            existing_notes = existing_data.get("Overall notes", "")
        except json.JSONDecodeError as e:
            print(f"[ERROR] Gagal parse existing final JSON: {e}")
        except Exception as e:
            print(f"[ERROR] Exception parsing existing: {e}")

    # Tambah debug untuk interviews_checklist (opsional, bisa hapus nanti)
    interviews_checklist = conn_interview.get_interviews_checklist(interview_json_raw)
    print(f"[DEBUG] Interviews Checklist extracted: {interviews_checklist}")
        
    return render_template(
    "final_result.html",
    interview=interview,
    final_json_str=final_tuple[2] if final_tuple else None,
    interview_score=interview_score,
    existing_project_name=existing_project_name,
    existing_project_score=existing_project_score,
    existing_notes=existing_notes,
    existing_recommendation=existing_recommendation
    )
    
@app.route("/dashboard/delete_interview/<int:interview_id>", methods=["GET","POST"])
def delete_interview(interview_id):
    interview = conn_interview.get_by_id(interview_id)
    if not interview:
        flash("Candidate not found!", "error")
        return redirect(url_for("history"))
    conn_interview.delete_interview(interview_id)
    flash("Interview deleted successfully!", "success")
    return redirect(url_for("history"))

@app.route("/dashboard/new_interview", methods=["GET", "POST"])
def new_interview():
    if 'user_id' not in session:
        flash("Please log in to view this page.", "error")
        return redirect(url_for('login'))

    candidates = conn_candidates.get_candidates()
   
    if request.method == "POST":
        user_id = session.get("user_id")
        candidate_id = request.form.get("candidate_id")

        questions = request.form.getlist("questions[]")
        videos = request.files.getlist("videos[]")

        # Validasi
        if not candidate_id:
            flash("Please select a candidate.", "error")
            return redirect(request.url)
        if len(questions) == 0 or len(videos) == 0:
            flash("Please add at least 1 question and 1 video.", "error")
            return redirect(request.url)
        if len(questions) != len(videos):
            flash("Number of questions and videos must match.", "error")
            return redirect(request.url)

        # Buat session interview baru (Pending)
        session_id = conn_interview.insert_new_interview_session(user_id, candidate_id)

        all_results_cd = []
        all_results_stt = []

        try:
            # === PROSES VIDEO + STT (WAJIB SUKSES) ===
            for idx, (q, file) in enumerate(zip(questions, videos), start=1):
                if file.filename == "":
                    raise ValueError(f"Missing video for Question {idx}.")

                filename, ext = os.path.splitext(file.filename)
                ext = ext.lower()
                if ext not in ['.mp4', '.webm']:
                    raise ValueError(f"Invalid file extension for Question {idx}. Only MP4 and WebM allowed.")

                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                    file.save(tmp.name)
                    temp_path = tmp.name

                try:
                    result_cd, result_stt = p_input.input_files(
                        temp_path, filename, ext, session_id, q
                    )
                    if not (result_cd and result_stt):
                        raise RuntimeError(f"STT/processing failed for Question {idx}.")
                    all_results_cd.append(result_cd)
                    all_results_stt.append(result_stt)
                finally:
                    os.remove(temp_path)

            # === GEMINI PROCESSING (BOLEH GAGAL) ===
            gemini_result = g_input.gemini_analyze(all_results_stt)
            if gemini_result is None:
                # Gemini gagal → STT tetap tersimpan, status tetap Pending
                flash("Gemini analysis failed (overload/quota exceeded). STT saved. Status: Pending. You can re-analyze later.", "warning")
            else:
                # Gemini sukses
                gemini_result_clean = re.sub(r'^```json\s*', '', gemini_result, flags=re.MULTILINE)
                gemini_result_clean = re.sub(r'^```\s*', '', gemini_result_clean, flags=re.MULTILINE)
                gemini_result_clean = re.sub(r'```$', '', gemini_result_clean).strip()

                conn_interview.update_interview(gemini_result_clean, session_id)
                flash("Interview processed successfully!", "success")

        except ValueError as ve:
            # Validasi gagal → rollback total
            flash(str(ve), "error")
            conn_interview.delete_interview(session_id)
            return redirect(request.url)

        except RuntimeError as rte:
            # STT gagal → rollback total
            flash("Video/STT processing failed. Interview canceled.", "error")
            conn_interview.delete_interview(session_id)
            return redirect(request.url)

        except Exception as e:
            # Error tak terduga (termasuk quota dari Gemini yang raise)
            print(f"[ERROR] Unexpected in new_interview: {e}")
            flash("Unexpected error. STT saved if possible. Status: Pending.", "error")
            # Tidak delete session_id → biarkan Pending

        # Selalu redirect ke history (sukses/gagal Gemini)
        return redirect(url_for('history'))

    return render_template("interview.html", candidates=candidates)

@app.route("/dashboard/reanalyze_gemini/<int:interview_id>", methods=["GET", "POST"])
def reanalyze_gemini(interview_id):
    if 'user_id' not in session:
        flash("Please log in to view this page.", "error")
        return redirect(url_for('login'))
    
    # Ambil interview data
    interview = conn_interview.get_by_id(interview_id)
    if not interview or interview[1] != session['user_id']:  # Pastikan milik user
        flash("Interview not found or access denied.", "error")
        return redirect(url_for('history'))
    
    # Cek syarat: status Pending dan result None/kosong
    if interview[4] != 'Pending' or (interview[3] and interview[3].strip()):
        flash("This interview cannot be re-analyzed (already processed or not pending).", "error")
        return redirect(url_for('history'))
    
    # Ambil semua STT dari videos terkait interview_id
    videos = conn_interview.get_history(session['user_id'])  # Reuse get_history untuk ambil videos
    current_interview = next((i for i in videos if i['interview_id'] == interview_id), None)
    if not current_interview or not current_interview.get('videos'):
        flash("No STT data found for this interview.", "error")
        return redirect(url_for('history'))
    
    all_results_stt = []
    for video in current_interview['videos']:
        try:
            stt_json = json.loads(video['result_stt']) if video['result_stt'] else {}
            all_results_stt.append({
                "Question": stt_json.get("Question", "Unknown question"),
                "Answer": stt_json.get("Answer", "No answer")
            })
        except:
            flash("Failed to parse STT for one video.", "error")
            return redirect(url_for('history'))
    
    if not all_results_stt:
        flash("No valid STT data to analyze.", "error")
        return redirect(url_for('history'))
    
    # Jalankan Gemini
    try:
        gemini_result = g_input.gemini_analyze(all_results_stt)
        if gemini_result is None:
            flash("Gemini analysis failed (overload or error). Please try again later.", "error")
            return redirect(url_for('history'))
        
        # Clean dan simpan
        gemini_result_clean = re.sub(r'^```json\s*', '', gemini_result, flags=re.MULTILINE)
        gemini_result_clean = re.sub(r'^```\s*', '', gemini_result_clean, flags=re.MULTILINE)
        gemini_result_clean = re.sub(r'```$', '', gemini_result_clean).strip()
        
        conn_interview.update_interview(gemini_result_clean, interview_id)
        
        flash("Gemini re-analysis completed successfully!", "success")
    except Exception as e:
        print(f"[ERROR] Re-analyze Gemini failed: {e}")
        flash("Unexpected error during Gemini analysis. Please try again.", "error")
    
    return redirect(url_for('history'))


if __name__ == "__main__":
    app.run(debug=True)
