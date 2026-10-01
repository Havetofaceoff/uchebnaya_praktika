import math


# Мок-справочник типов продукции:
# ключ — ID типа, значение — коэффициент типа продукции.
PRODUCT_TYPES = {
    1: 1.0,
    2: 1.5,
    3: 2.0,
}


# Мок-справочник типов материалов:
# ключ — ID материала, значение — процент брака.
MATERIAL_TYPES = {
    1: 0.0,
    2: 5.0,
    3: 10.0,
}


def calculate_required_material(
    product_type_id: int,
    material_type_id: int,
    quantity: int,
    param_1: float,
    param_2: float,
) -> int:
    """
    Рассчитывает необходимое количество материала с учетом
    коэффициента типа продукции и процента брака.

    При некорректных данных возвращает -1.
    """

    # Проверяем существование ID в справочниках.
    if product_type_id not in PRODUCT_TYPES:
        return -1

    if material_type_id not in MATERIAL_TYPES:
        return -1

    # Количество и параметры продукции должны быть положительными.
    if quantity <= 0 or param_1 <= 0 or param_2 <= 0:
        return -1

    try:
        product_coefficient = PRODUCT_TYPES[product_type_id]
        defect_percent = MATERIAL_TYPES[material_type_id]

        # Базовый расход материала на одну единицу продукции.
        material_per_unit = (
            param_1
            * param_2
            * product_coefficient
        )

        # Общий расход без учета брака.
        total_material = material_per_unit * quantity

        # Добавляем материал, необходимый с учетом процента брака.
        total_with_defect = total_material * (
            1 + defect_percent / 100
        )

        # По ТЗ результат округляется вверх до целого числа.
        return math.ceil(total_with_defect)

    except (TypeError, ValueError):
        return -1