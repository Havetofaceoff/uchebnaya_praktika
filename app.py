import logging
from flask import Flask, render_template, request, abort

from partner_service import (
    get_all_partners_with_discount,
    get_partner_by_id,
    get_partner_sales_history,
    create_partner,
    update_partner,
)

from material_calculator import calculate_required_material


app = Flask(__name__, template_folder="partner_ui")
logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def validate_partner_form(form):
    """Проверяет данные формы перед отправкой в базу данных."""

    name = form.get("name", "").strip()
    email = form.get("email", "").strip()
    rating_text = form.get("rating", "").strip()

    if not name:
        raise ValueError(
            "Наименование не может быть пустым. "
            "Введите наименование партнера и повторите попытку."
        )

    if not email:
        raise ValueError(
            "Email не может быть пустым. "
            "Введите email компании и повторите попытку."
        )

    try:
        rating = int(rating_text)
    except ValueError:
        raise ValueError(
            "Рейтинг должен быть целым числом от 0. "
            "Удалите буквы и знаки препинания и повторите попытку."
        )

    if rating < 0:
        raise ValueError(
            "Рейтинг не может быть отрицательным. "
            "Введите целое число от 0 и повторите попытку."
        )

    return {
        "name": name,
        "inn": form.get("inn", "").strip(),
        "partner_type": form.get("partner_type", "").strip(),
        "rating": rating,
        "address": form.get("address", "").strip(),
        "director": form.get("director", "").strip(),
        "phone": form.get("phone", "").strip(),
        "email": email,
    }


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
        try:
            data = validate_partner_form(request.form)
            create_partner(data)

            return render_template(
                "partner_edit.html",
                partner=None,
                mode="add",
                message="Партнер успешно добавлен в базу данных.",
                message_type="info",
                redirect_after_message=True,
            )

        except ValueError as error:
            logging.error(
                 "Ошибка валидации при добавлении партнера: %s",
                 error,
)
            return render_template(
                "partner_edit.html",
                partner=request.form,
                mode="add",
                message=str(error),
                message_type="error",
            )

        except Exception:
            return render_template(
                "partner_edit.html",
                partner=request.form,
                mode="add",
                message=(
                    "Не удалось сохранить данные в базе данных. "
                    "Проверьте введенные данные и подключение к базе, "
                    "затем повторите попытку."
                ),
                message_type="error",
            )

    return render_template(
        "partner_edit.html",
        partner=None,
        mode="add",
    )


@app.route("/partners/<int:partner_id>/edit", methods=["GET", "POST"])
def edit_partner(partner_id):
    # ID используется для загрузки и обновления конкретного партнера.
    partner = get_partner_by_id(partner_id)

    if not partner:
        abort(404)

    if request.method == "POST":
        try:
            data = validate_partner_form(request.form)

            if not update_partner(partner_id, data):
                abort(404)

            return render_template(
                "partner_edit.html",
                partner=data,
                mode="edit",
                message="Изменения партнера успешно сохранены.",
                message_type="info",
                redirect_after_message=True,
            )

        except ValueError as error:
            return render_template(
                "partner_edit.html",
                partner=request.form,
                mode="edit",
                message=str(error),
                message_type="error",
            )

        except Exception:
            return render_template(
                "partner_edit.html",
                partner=request.form,
                mode="edit",
                message=(
                    "Не удалось сохранить изменения в базе данных. "
                    "Проверьте введенные данные и подключение к базе, "
                    "затем повторите попытку."
                ),
                message_type="error",
            )

    return render_template(
        "partner_edit.html",
        partner=partner,
        mode="edit",
    )


@app.route("/partners/<int:partner_id>/history")
def partner_history(partner_id):
    # ID определяет, историю какого партнера необходимо показать.
    partner = get_partner_by_id(partner_id)

    if not partner:
        abort(404)

    history = get_partner_sales_history(partner_id)

    return render_template(
        "partner_history.html",
        partner=partner,
        history=history,
    )


@app.route("/material-calculator", methods=["GET", "POST"])
def material_calculator():
    result = None
    error_message = None

    if request.method == "POST":
        try:
            product_type_id = int(request.form["product_type_id"])
            material_type_id = int(request.form["material_type_id"])
            quantity = int(request.form["quantity"])
            param_1 = float(request.form["param_1"])
            param_2 = float(request.form["param_2"])

            result = calculate_required_material(
                product_type_id,
                material_type_id,
                quantity,
                param_1,
                param_2,
            )

                        # Значение -1 означает, что метод получил некорректные данные.
            if result == -1:
                logging.error(
                    "Некорректные данные для расчета материалов."
                )

                error_message = (
                    "Расчет невозможен. Проверьте ID типа продукции и "
                    "материала. Количество и параметры изделия должны "
                    "быть больше нуля."
                )

        except (ValueError, TypeError) as error:
            logging.error(
                "Ошибка ввода в калькуляторе материалов: %s",
                error,
            )

            error_message = (
                "Некорректный формат данных. ID и количество должны быть "
                "целыми числами, а параметры изделия — числами."
            )
    return render_template(
        "material_calculator.html",
        result=result,
        error_message=error_message,
    )


if __name__ == "__main__":
    app.run(debug=True)