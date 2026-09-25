from flask import Flask, render_template
from partner_service import get_all_partners_with_discount

app = Flask(__name__, template_folder="partner_ui")

@app.route("/")
def index():
    partners = get_all_partners_with_discount()

    return render_template(
        "index.html",
        partners=partners,
    )
    
@app.route("/partners/add")
def add_partner():
    return render_template("partner_edit.html")

if __name__ == "__main__":
    app.run(debug=True)