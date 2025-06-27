import requests
import json
import logging
import config
import random

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_legal_response(query):
    """Получение юридического ответа от OpenRouter API"""
    selected_model = random.choice(config.OPENROUTER_MODELS)

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }

        system_prompt = (
            "Ты профессиональный юрист, специализирующийся на российском законодательстве. "
            "Отвечай точно и по делу. В ответах указывай: "
            "1. Полное название закона/кодекса. "
            "2. Номер статьи (если применимо). "
            "3. Краткое содержание. "
            "4. Практическое применение. "
            "5. Ссылки на официальные источники (если известны). "
            "Отвечай в виде сообщения Telegram, отвечайв кратце, чтобы оно не резалось"
            "Избегай смайлов и неформальных выражений, ССЫЛКА НА КОНСУЛЬТАНТ+ ОБЯЗАТЕЛЬНА."
        )

        data = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            "max_tokens": 1024,
        }

        logger.info(f"Отправка запроса к модели {selected_model}")
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code != 200:
            error_msg = f"Ошибка {response.status_code} для модели {selected_model}: {response.text}"
            logger.error(error_msg)
            return get_legal_response(query)

        result = response.json()["choices"][0]["message"]["content"]
        logger.info(f"Получен ответ от {selected_model} ({len(result)} символов)")
        return result

    except Exception as e:
        logger.error(f"Ошибка OpenRouter API: {e}")
        return (
            get_legal_response(query)
            if len(config.OPENROUTER_MODELS) > 1
            else "Не удалось получить ответ. Пожалуйста, попробуйте позже."
        )
