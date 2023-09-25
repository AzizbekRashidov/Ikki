import aiohttp
import asyncio
import json

async def coderun(text):
    url = "https://rextester.com/rundotnet/Run"

    # So'rovnoma ma'lumotlari
    payload = {
        'LanguageChoiceWrapper': 24,
        'EditorChoiceWrapper': 1,
        'LayoutChoiceWrapper': 1,
        'Program': f'#python 3.6.9\n\n{text}',
        'Input': '',
        'Privacy': '',
        'PrivacyUsers': '',
        'Title': '',
        'SavedOutput': '',
        'WholeError': '',
        'WholeWarning': '',
        'StatsToSave': '',
        'CodeGuid': '',
        'IsInEditMode': False,
        'IsLive': False
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            code = await response.text()
            codes = json.loads(code)
            print(json.dumps(codes, indent=4))
            if codes['Result'] == '':
                res = codes['Errors']
                if 'source' in codes['Errors']:

                    print(res.replace("source", "app"))
                    return res.replace("source", "app")
                else:
                    return codes['Errors']
            else:
                result = codes['Result']
                if "rextester_linux_2.0" in result:
                    return result.replace("rextester_linux_2.0", "xudoberdi.uz")
                else:
                    return result


