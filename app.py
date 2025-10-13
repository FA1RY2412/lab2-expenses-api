from flask import Flask, request, jsonify, abort
from datetime import datetime
from typing import Dict, Any, List

app = Flask(__name__)

# -------- In-memory storage (no DB as per lab) --------
users: List[Dict[str, Any]] = []
categories: List[Dict[str, Any]] = []
records: List[Dict[str, Any]] = []

_counters = {"user": 1, "category": 1, "record": 1}

def _next_id(name: str) -> int:
    _counters[name] += 1
    return _counters[name] - 1

def _find_by_id(items, _id):
    return next((x for x in items if x["id"] == _id), None)

def _remove_by_id(items, _id):
    idx = next((i for i, x in enumerate(items) if x["id"] == _id), None)
    if idx is None:
        return False
    items.pop(idx)
    return True

# -------- Seed data for easier Postman testing --------
def seed():
    if not users and not categories and not records:
        u1 = {"id": _next_id("user"), "name": "Alice"}
        u2 = {"id": _next_id("user"), "name": "Bob"}
        users.extend([u1, u2])

        c1 = {"id": _next_id("category"), "name": "Food"}
        c2 = {"id": _next_id("category"), "name": "Transport"}
        categories.extend([c1, c2])

        r1 = {
            "id": _next_id("record"),
            "user_id": u1["id"],
            "category_id": c1["id"],
            "created_at": datetime.utcnow().isoformat() + "Z",
            "amount": 12.5
        }
        r2 = {
            "id": _next_id("record"),
            "user_id": u1["id"],
            "category_id": c2["id"],
            "created_at": datetime.utcnow().isoformat() + "Z",
            "amount": 50.0
        }
        records.extend([r1, r2])

seed()

# -------- Users --------
@app.get("/user/<int:user_id>")
def get_user(user_id: int):
    u = _find_by_id(users, user_id)
    if not u:
        abort(404, description="User not found")
    return jsonify(u)

@app.delete("/user/<int:user_id>")
def delete_user(user_id: int):
    ok = _remove_by_id(users, user_id)
    if not ok:
        abort(404, description="User not found")
    # Also remove user's records to keep consistency (optional but handy)
    removed = [rec for rec in list(records) if rec["user_id"] == user_id]
    for rec in removed:
        _remove_by_id(records, rec["id"])
    return jsonify({"status": "ok", "deleted_user_id": user_id, "deleted_records": [r["id"] for r in removed]})

@app.post("/user")
def create_user():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name")
    if not name:
        abort(400, description="Field 'name' is required")
    u = {"id": _next_id("user"), "name": name}
    users.append(u)
    return jsonify(u), 201

@app.get("/users")
def list_users():
    return jsonify(users)

# -------- Categories --------
@app.get("/category")
def list_categories():
    return jsonify(categories)

@app.post("/category")
def create_category():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name")
    if not name:
        abort(400, description="Field 'name' is required")
    c = {"id": _next_id("category"), "name": name}
    categories.append(c)
    return jsonify(c), 201

# Support both DELETE /category and DELETE /category/<id>
@app.delete("/category")
def delete_category_query():
    cid = request.args.get("id", type=int)
    if cid is None:
        abort(400, description="Provide category id as query param ?id=<id> or use /category/<id>")
    return _delete_category(cid)

@app.delete("/category/<int:category_id>")
def delete_category_path(category_id: int):
    return _delete_category(category_id)

def _delete_category(category_id: int):
    ok = _remove_by_id(categories, category_id)
    if not ok:
        abort(404, description="Category not found")
    # Remove records in this category (optional but handy)
    removed = [rec for rec in list(records) if rec["category_id"] == category_id]
    for rec in removed:
        _remove_by_id(records, rec["id"])
    return jsonify({"status": "ok", "deleted_category_id": category_id, "deleted_records": [r["id"] for r in removed]})

# -------- Records --------
@app.get("/record/<int:record_id>")
def get_record(record_id: int):
    r = _find_by_id(records, record_id)
    if not r:
        abort(404, description="Record not found")
    return jsonify(r)

@app.delete("/record/<int:record_id>")
def delete_record(record_id: int):
    ok = _remove_by_id(records, record_id)
    if not ok:
        abort(404, description="Record not found")
    return jsonify({"status": "ok", "deleted_record_id": record_id})

@app.post("/record")
def create_record():
    data = request.get_json(force=True, silent=True) or {}
    try:
        user_id = int(data.get("user_id"))
        category_id = int(data.get("category_id"))
    except (TypeError, ValueError):
        abort(400, description="'user_id' and 'category_id' must be integers")

    amount = data.get("amount")
    if amount is None:
        abort(400, description="'amount' is required")
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        abort(400, description="'amount' must be a number")

    if not _find_by_id(users, user_id):
        abort(400, description="Unknown user_id")
    if not _find_by_id(categories, category_id):
        abort(400, description="Unknown category_id")

    created_at = data.get("created_at") or datetime.utcnow().isoformat() + "Z"

    rec = {
        "id": _next_id("record"),
        "user_id": user_id,
        "category_id": category_id,
        "created_at": created_at,
        "amount": amount
    }
    records.append(rec)
    return jsonify(rec), 201

@app.get("/record")
def list_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)
    if user_id is None and category_id is None:
        abort(400, description="Provide at least one of query params: user_id or category_id")

    filtered = records
    if user_id is not None:
        filtered = [r for r in filtered if r["user_id"] == user_id]
    if category_id is not None:
        filtered = [r for r in filtered if r["category_id"] == category_id]

    return jsonify(filtered)

# -------- Healthcheck --------
@app.get("/healthcheck")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})

# -------- Error handlers for nicer messages --------
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "bad_request", "message": e.description}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "not_found", "message": e.description}), 404

if __name__ == "__main__":
    # For local dev only
    app.run(host="0.0.0.0", port=8080, debug=True)
