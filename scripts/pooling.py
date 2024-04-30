from time import sleep
import requests

WAIT_TIME = 60
BACKEND_URL = ""
LAB_ZAP_URL = "http://labzap:3000/"

def check_schedules():
    # response = requests.get(f"{BACKEND_URL}/schedule/?has_sync=0")
    # response_data = response.json()
    sleep(WAIT_TIME)


def main():
    try:
        while True:
            check_schedules()
    except KeyboardInterrupt:
        print("Interrupted!")


if __name__ == '__main__':
    main()
