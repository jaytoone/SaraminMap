import requests

url = "https://dapi.kakao.com/v2/local/search/address.json"

REST_API_KEY = "cb183416d740686de67786ceffea553c"
headers = {"Authorization": "KakaoAK {}".format(REST_API_KEY)}
address = "서울특별시 금천구 가산동 가산디지털1로"


def location(address):
    params = {"query": "{}".format(address)}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()["documents"][0]

    return data['y'], data['x']


if __name__ == '__main__':
    print(type(location(address)))
