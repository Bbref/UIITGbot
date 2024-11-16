from flask import Flask, request, make_response, jsonify
from transformers import pipeline

# Указываем явную модель
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")

# Инициализация Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Добро пожаловать в API для анализа тональности текста!"

# Создаем эндпоинт для анализа текста
@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    # Проверяем, что запрос содержит текст
    if 'text' not in request.json:
        return make_response(jsonify({'error': 'Текст не найден в запросе'}), 400)

    # Получаем текст из запроса
    text = request.json['text']

    # Анализируем тональность
    result = sentiment_analyzer(text)

    # Возвращаем результат
    return make_response(jsonify({'result': result}), 200)

if __name__ == '__main__':
    app.run(debug=True)
