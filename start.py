"""
start.py - Ứng dụng Quản lý Thư viện Báo cáo KPIMATRIX (Edufit)
Chạy ứng dụng: python start.py
"""

import json
import os
import sys
import unicodedata

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__, template_folder='templates')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')


# ==========================================
# 1. DATA ACCESS LAYER (EX-02)
# ==========================================
def load_data():
    """Đọc dữ liệu từ file cấu hình data.json."""
    if not os.path.exists(DATA_FILE):
        return {"groups": [], "menus": [], "reports": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalize_vietnamese(text: str) -> str:
    """
    Chuẩn hóa chuỗi tiếng Việt: bỏ dấu, xử lý chữ đ/Đ, chuyển chữ thường (FR-06).
    """
    if not text:
        return ""
    # Chuẩn hóa Unicode NFD để tách các ký tự dấu
    text = unicodedata.normalize('NFD', text)
    # Loại bỏ các combining accents
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # Xử lý riêng ký tự đ / Đ
    text = text.replace('đ', 'd').replace('Đ', 'D')
    return text.lower().strip()


def filter_reports(reports, group=None, query=None):
    """
    Hàm lọc và tìm kiếm báo cáo (Dùng chung cho API và Unit Test).
    """
    result = reports
    if group:
        result = [r for r in result if r.get('group', '').upper() == group.upper()]
    if query:
        norm_q = normalize_vietnamese(query)
        result = [r for r in result if norm_q in normalize_vietnamese(r.get('title', ''))]
    return result


# ==========================================
# 2. REST API ROUTES
# ==========================================
@app.route('/api/data', methods=['GET'])
def api_get_all_data():
    """Trả về toàn bộ dữ liệu cấu hình (Groups, Menus, Reports)."""
    data = load_data()
    return jsonify(data)


@app.route('/api/reports', methods=['GET'])
def api_get_reports():
    """Lọc danh sách báo cáo theo ?group=... và ?q=..."""
    data = load_data()
    group = request.args.get('group')
    query = request.args.get('q') or request.args.get('search')
    filtered = filter_reports(data.get('reports', []), group=group, query=query)
    return jsonify(filtered)


@app.route('/api/reports/<report_id>', methods=['GET'])
def api_get_report_by_id(report_id):
    """Lấy chi tiết một báo cáo theo ID."""
    data = load_data()
    report = next((r for r in data.get('reports', []) if r.get('id', '').upper() == report_id.upper()), None)
    if report:
        return jsonify(report)
    return jsonify({"error": "Report not found", "id": report_id}), 404


@app.route('/api/reports', methods=['POST'])
def api_create_report():
    """Tạo mới một báo cáo và lưu trực tiếp vào data.json."""
    req_data = request.get_json() or {}
    title = req_data.get('title')
    group = req_data.get('group')
    if not title or not group:
        return jsonify({"error": "Thiếu tên báo cáo hoặc nhóm phòng ban"}), 400
    
    data = load_data()
    reports = data.get('reports', [])
    new_id = req_data.get('id') or f"R{len(reports) + 1:02d}"

    # Xử lý nếu tạo nhóm mới (ví dụ HR)
    new_group_name = req_data.get('new_group_name')
    new_group_color = req_data.get('new_group_color', '#8b5cf6')
    if group == 'NEW' and new_group_name:
        group_id = new_group_name.upper().replace(' ', '')
        if not any(g['id'] == group_id for g in data.get('groups', [])):
            data['groups'].append({
                "id": group_id,
                "name": new_group_name,
                "color": new_group_color
            })
        group = group_id

    group_obj = next((g for g in data.get('groups', []) if g['id'] == group), None)
    color = req_data.get('color') or (group_obj['color'] if group_obj else '#4f46e5')
    
    new_report = {
        "id": new_id,
        "title": title,
        "group": group,
        "color": color,
        "seed": float(req_data.get('seed', len(reports) + 3)),
        "updated_at": req_data.get('updated_at', '18/10/2026'),
        "embed_url": req_data.get('embed_url') or f"https://bi.example.vn/embed/{new_id}"
    }
    
    # Tránh trùng ID
    reports = [r for r in reports if r['id'] != new_id]
    reports.append(new_report)
    data['reports'] = reports
    
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Lỗi ghi data.json:", e)
        
    return jsonify(new_report), 201


# ==========================================
# 3. WEB PAGE ROUTES (SPA Shell)
# ==========================================
@app.route('/')
def route_root():
    return redirect('/thu-vien-bao-cao')


@app.route('/thu-vien-bao-cao')
@app.route('/thu-vien-bao-cao/<report_id>')
@app.route('/phan-ra-kpi')
@app.route('/giao-kpi')
@app.route('/danh-sach-coi')
@app.route('/hoc-sinh')
def route_pages(report_id=None):
    """
    Phục vụ giao diện chính Home.html.
    Client-side routing (JS) sẽ đọc URL pathname và query params để hiển thị trang tương ứng.
    """
    data = load_data()
    return render_template('Home.html', initial_data=data, current_report_id=report_id)


@app.errorhandler(404)
def handle_404(e):
    data = load_data()
    return render_template('Home.html', initial_data=data, not_found=True), 404


# ==========================================
# 4. KHỞI CHẠY SERVER
# ==========================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Server Thư viện Báo cáo đang chạy tại: http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
