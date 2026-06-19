import pytest

# Тест для проверки главной страницы
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200 # Проверка, что код ответа 200 (OK)
    assert b'Hello' in response.data # Проверка, что текст 'Hello' присутствует на странице

# Тест для маршрута, возвращающего данные
def test_data_page(client):
    response = client.get('/data')
    assert response.status_code == 200
    assert b'This is some data!' in response.data # Проверка наличия кэшированных данных
