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

if __name__ == "__main__":
    app.run(debug=True)