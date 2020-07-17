#!/usr/bin/env python3

import argparse
from pprint import pprint
from urllib.parse import urlencode

import requests

ROOT_URL = "https://corona.lmao.ninja/v2/"
ENDPOINTS = {
    "all": "all/",
    "country": "countries/",
}


class ApiException(Exception):
    pass


def reverse(url_name, args=None, kwargs=None):
    try:
        base_url = f"{ROOT_URL}{ENDPOINTS[url_name]}"
    except KeyError:
        raise Exception(f"No URL match name '{url_name}'")
    else:
        if args:  # path variables
            base_url = f'{base_url}{",".join(args)}'
        if kwargs:  # request params
            base_url = f"{base_url}?{urlencode(kwargs)}"
        return base_url


def retrieve_cases(countries=None, yesterday=False, *args, **kwargs):
    countries = countries or []
    is_global = not countries
    params = {}
    if yesterday:
        params["yesterday"] = "true"

    if is_global:
        url = reverse("all")
    elif any(countries):
        url = reverse("country", args=countries, kwargs=params)
    else:
        raise TypeError("No valid parameters provided")
    r = requests.get(url)
    if r.status_code == 200:
        response = r.json()
        display_response(response)
    else:
        raise ApiException(
            f"Got error while retrieving from API.\n {r.status_code}\n{r.text}"
        )
    return response


def display_response(response):
    pprint(response)


def run():
    parser = argparse.ArgumentParser(description="Get to know latest COVID-19 cases")  # noqa
    parser.add_argument(
        "--country",
        action="append",
        dest="countries",
        help="Single or multiple country names, country id,"
        "or ISOs (ISO 2 | ISO 3) 3166 Country Standards. "
        "Omit to show global.",
    )
    parser.add_argument(
        "-y", "--yesterday", action="store_true", help="Show yesterday's data"
    )
    args = parser.parse_args()

    retrieve_cases(**vars(args))


if __name__ == "__main__":
    run()
