# Postman Flow — Expenses API (5 хв)

1. Відкрий Postman → **Flows** → **Create a flow**.
2. Додай блок **Request** і вибери колекцію `Expenses Lab2 API` → `Create user`.
3. Додай блок **Variable** `user_id` і збережи у нього `id` з відповіді (`Response Body → JSON → id`).
4. Додай блок **Request** → `Create category`, аналогічно збережи `category_id`.
5. Додай блок **Request** → `Create record` і передай змінні: `user_id`, `category_id`, `amount` (наприклад, 12.5).
6. Додай блок **Request** → `GET /record?user_id={{user_id}}` (використовуй Query Params у блоці).
7. Додай блок **Request** → `DELETE /record/{{record_id}}` (візьми перший елемент з попереднього масиву і його `id`).
8. Запусти Flow — має відпрацювати послідовність створення/перевірки/видалення.

> Додатково: додай гілку з `DELETE /user/{{user_id}}` і `DELETE /category/{{category_id}}` для повного прибирання.
