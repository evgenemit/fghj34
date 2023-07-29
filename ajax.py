import json
import os
from datetime import datetime


def handle_uploaded_file(file):
    """Обработка файла и сохранение данных"""

    try:
        records = []
        file_content = file.read()
        if os.path.splitext(file.filename)[1] != '.json':
            return {'status': 'error', 'message': 'Неверное расширение файла.'}
        json_data = json.loads(file_content)
        for record in json_data:
            name = record.get('name', None)
            date = record.get('date', None)
            if name is None:
                return {'status': 'error', 'message': 'Не передан ключ name.'}
            if date is None:
                return {'status': 'error', 'message': 'Не передан ключ date.'}
            if len(name) >= 50:
                return {
                    'status': 'error',
                    'message': 'Длина значения name должна быть меньше 50 символов.'
                }
            try:
                date = datetime.strptime(date, '%Y-%m-%d_%H:%M')
            except ValueError:
                return {
                    'status': 'error',
                    'message': 'Неправильный формат поля date. Требуемый формат: YYYY-MM-DD_HH:mm.'
                }
            records.append({'name': name, 'date': date})
        return {'status': 'ok', 'records': records}
    except Exception:
        return {'status': 'error', 'message': 'Неизвестная ошибка.'}
