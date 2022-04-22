import requests

async def get_item_list(keyword, token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-length": "561",
        "content-type": "application/json",
        "dpop": token,
        "origin": "https://jp.mercari.com",
        "referer": "https://jp.mercari.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
        "x-platform": "web"
    }

    payload = {
        "searchCondition": {
            "keyword": keyword,
            "order": "ORDER_DESC",
            "sort": "SORT_CREATED_TIME",
        },
        "searchSessionId": "9aeb470816d1f272a03be48ba7207a44",
    }

    # make request to search endpoint
    r = requests.post('https://api.mercari.jp/v2/entities:search', json=payload, headers=headers)

    # if request can be made return json response
    if r.status_code == 200:
        return r.json()
    else:
        print(r.status_code)
        print(r.reason)
        print(r.text)
        return False 
