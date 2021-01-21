import requests
import credentials
import datetime as dt

nutritionix_exersise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
google_sheet_endpoint = "https://api.sheety.co/3033aaca49063d28ad1fce51d6ed3b21/myWorkouts/sheet1"


def nutritionix_post_request():
    query = input("What have you done today?\n")

    nutritionix_post_request_header = {
        "x-app-id": credentials.app_id,
        "x-app-key": credentials.api_key,
        "x-remote-user-id": "0"
    }

    nutritionix_post_request_body = {
        "query": query,
        "gender": "male",
        "weight_kg": 92,
        "height_cm": 180,
        "age": 21
    }

    response = requests.post(url=nutritionix_exersise_endpoint,
                             json=nutritionix_post_request_body, headers=nutritionix_post_request_header)

    return response.json()


def send_to_google_sheets(response):
    body = {
        "sheet1": {
            # "date": "20210120"
            "date": str(dt.datetime.today().strftime('%d/%m/%Y')),
            "time": str(dt.datetime.now().strftime("%H:%M")),
            "exercise": response["exercises"][0]["user_input"],
            "duration": response["exercises"][0]["duration_min"],
            "calories": response["exercises"][0]["nf_calories"],
        }
    }
    headers = {
        "Authorization": credentials.sheety_auth_token
    }
    response = requests.post(url=google_sheet_endpoint,
                             json=body, headers=headers)


def main():
    response = nutritionix_post_request()
    send_to_google_sheets(response)


main()
