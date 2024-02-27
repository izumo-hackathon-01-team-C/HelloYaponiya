import asyncio
from typing import Any

import aiohttp


ISO_TO_GOOGLE_LANG_MAPPING = {
    "jpn": 'ja',
    "eng": 'en',
    "rus": 'ru',
    "spa": 'es',
    "tha": 'th',
    "hin": 'hi',
    "nep": 'ne',
    "por": 'pt',
    "chi": 'zh',
    "fre": 'fr',
    "ben": 'bn',
    "ind": 'id',
    "khm": 'km',
    "bur": 'my',
    "kor": 'ko',
    "fil": 'fil',
    "vie": 'vi',
}


class TranslationClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def translate_key_value_dict(self, data: dict[str, Any], from_lang: str, to_lang: str) -> dict[str, str]:
        coro_list = []
        result = {}

        from_lang = ISO_TO_GOOGLE_LANG_MAPPING.get(from_lang, from_lang)
        to_lang = ISO_TO_GOOGLE_LANG_MAPPING.get(to_lang, to_lang)

        async with aiohttp.ClientSession() as session:
            for key, value in data.items():
                if isinstance(value, str) and not value.isnumeric():
                    coro_list.append(
                        self._translate_pair(
                            session=session,
                            key=key,
                            value=value,
                            from_lang=from_lang,
                            to_lang=to_lang,
                        )
                    )
                else:
                    result[key] = value

            translation_result = await asyncio.gather(*coro_list)

        for item in translation_result:
            result.update(item)

        return result

    async def _translate_pair(
            self,
            session: aiohttp.ClientSession,
            key: str,
            value: str,
            from_lang: str,
            to_lang: str
    ) -> dict[str, str]:
        async with session.get(
            url='https://translation.googleapis.com/language/translate/v2',
            params={
                'key': self._api_key,
                'format': 'text',

                'q': value,
                'source': from_lang,
                'target': to_lang,
            }
        ) as r:
            result = await r.json()
            return {key: result['data']['translations'][0]['translatedText']}


# async def main():
#     data = {
#     "F7": "2023",
#     "I7": "03",
#     "K7": "21",
#     "C8": "Somewhere in Izumo",
#     "C10": "Somewhere in Izumo (furgiana)",
#     "C11": "Tanaka-san",
#     "F9": "000-00-00",
#     "G11": "1996",
#     "I11": "02",
#     "K11": "24",
#     "C14": True,
#     "C16": False,
#     "F16": True,
#     "I16": "Other relations"
# }
#
#     client = TranslationClient(api_key='oh-my')
#     print(await client.translate_key_value_dict(data, from_lang='eng', to_lang='jpn'))
#
# asyncio.run(main())
