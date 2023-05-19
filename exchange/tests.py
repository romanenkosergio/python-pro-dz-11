import json
import os
import pathlib

import responses

from .exchange_provider import MonoExchange, PrivatExchange, NBUExchange, VkurseExchange, MinfinExchange

root = pathlib.Path(__file__).parent


# Create your tests here.


@responses.activate
def test_exchange_mono():
    mocked_response = json.load(open(root / "fixtures/mono_response.json"))
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=mocked_response,
    )
    e = MonoExchange("mono", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.4406


def test_privat_rate():
    mocked_response = json.load(open(root / "fixtures/privat_response.json"))
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11",
        json=mocked_response,
    )
    e = PrivatExchange("privat", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.45318


def test_nbu_rate():
    mocked_response = json.load(open(root / "fixtures/nbu_response.json"))
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=mocked_response,
    )
    e = NBUExchange("nbu", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 36.5686


def test_vkurse_rate():
    mocked_response = json.load(open(root / "fixtures/vkurse_response.json"))
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json=mocked_response,
    )
    e = VkurseExchange("vkurse", "Dollar", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.50


def test_minfin_rate():
    minfin_api_key = os.getenv('MINFIN_API_KEY')
    mocked_response = json.load(open(root / "fixtures/minfin_response.json"))
    responses.get(
       "https://minfin.com.ua/api/currency/simple/?base=UAH&list=usd",
        json=mocked_response,
    )
    e = MinfinExchange("minfin", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.6000
