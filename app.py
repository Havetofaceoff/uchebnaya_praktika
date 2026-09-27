from flask import Flask, render_template, request, redirect, url_for, abort

from partner_service import (
    get_all_partners_with_discount,
    get_partner_by_id,
    create_partner,
    update_partner,
)

app = Flask(__name__, template_folder="partner_ui")

@app.route("/")
def index():
    partners = get_all_partners_with_discount()

    return render_template(
        "index.html",
        partners=partners,
    )

@app.route("/partners/add", methods=["GET", "POST"])
def add_partner():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "inn": request.form["inn"],
            "partner_type": request.form["partner_type"],
            "rating": int(request.form["rating"]),
            "address": request.form["address"],
            "director": request.form["director"],
            "phone": request.form["phone"],
            "email": request.form["email"],
        }

        create_partner(data)

        return redirect(url_for("index"))

    return render_template(
        "partner_edit.html",
        partner=None,
        mode="add",
    )

@app.route("/partners/<int:partner_id>/edit", methods=["GET", "POST"])
def edit_partner(partner_id):
    # ID из URL используется для загрузки и обновления конкретного партнера.
    partner = get_partner_by_id(partner_id)

    if not partner:
        abort(404)

    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "inn": request.form["inn"],
            "partner_type": request.form["partner_type"],
            "rating": int(request.form["rating"]),
            "address": request.form["address"],
            "director": request.form["director"],
            "phone": request.form["phone"],
            "email": request.form["email"],
        }

        if not update_partner(partner_id, data):
            abort(404)

        return redirect(url_for("index"))

    return render_template(
        "partner_edit.html",
        partner=partner,
        mode="edit",
    )

if __name__ == "__main__":
    app.run(debug=True)