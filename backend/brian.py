import requests

str1 = """ᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLᴾᴾᴾᴾ
    ᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLL
    ᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLᴾᴾᴾᴾᴾ
    ᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLLLLᴾ
    ᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLL
    LLLLLLLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLLLLLLLLᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLLLLLLLLL
    ᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾᴾLLLLLLLLLLLLLLLLLLLL"""


def fetch_brian(session, text, funny_mode=False):
    if funny_mode:
        text = str1

    url = f"https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={text}"
    response = session.get(url)
    return response.content