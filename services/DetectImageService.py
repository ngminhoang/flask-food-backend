import requests


def analyze_image(api_key, image_path):
    url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
    headers = {"Authorization": f"Api-Key {api_key}"}

    with open(image_path, "rb") as image:
        response = requests.post(url, headers=headers, files={"image": image})
        response.raise_for_status()


    return response.json()