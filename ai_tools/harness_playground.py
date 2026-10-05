from ai_tools.test_reviewer import review_test_code

bad_api_test = '''
import requests
import time

def test_create_withdrawal():
    headers = {"Authorization": "Bearer sk_live_51H8xK2..."}
    response = requests.post(
        "https://api-staging.example.com/withdrawals",
        json={"user_id": 123, "amount": 100.00},
        headers=headers
    )
    assert response.status_code == 200

    time.sleep(5)

    status_response = requests.get(
        "https://api-staging.example.com/withdrawals/latest",
        headers=headers
    )
    assert status_response.status_code == 200
'''

print(review_test_code(bad_api_test))