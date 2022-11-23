import requests


class ApiClient:
    """api client for using backend server apis"""

    base_url = "http://127.0.0.1:8000"

    def get_candidate_info_by_id(self, candidate_id):
        """get candidate info from backend"""

        url = f"{self.base_url}/candidate/{candidate_id}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        return response

    def get_assignment_info_by_id(self, assignment_id):
        """get assignment info from backend"""

        url = f"{self.base_url}/assignment/{assignment_id}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        return response

    def get_assignment_questions(self, assignment_id):
        """get assignment questions info from backend"""

        url = f"{self.base_url}/question/{assignment_id}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        return response

    def dummy_get_candidate_info_by_id(self, candidate_id):
        """returns dummy candidate info"""

        response = {
            "id": 1,
            "name": "abc",
            "email": "abc@sef.com",
            "phoneNumber": "8282828282",
            "location": "gurugram",
            "collegeName": "sss",
            "degree": "ss",
            "fieldOfStudy": "ss",
            "yearOfPassing": "1111",
            "sscScore": "12",
            "hscScore": "12",
            "graduationAgg": "12",
            "updated_on": "2022-11-23T04:22:49.726607Z",
            "created_on": "2022-11-23T04:22:49.726660Z",
            "isActive": True,
            "hasConsented": False,
            "status_code": 200
        }

        print(response)
        return response

    def dummy_get_assignment_info_by_id(self, assignment_id):
        """returns dummy assignment info"""

        response = {
            "id": 1,
            "name": "dummy_assignment",
            "question_set": [1, 2, 3, 4, 5],
            "status_code": 200
        }

        print(response)
        return response

    def dummy_get_assignment_questions(self, assignment_id):
        """dummy assignment questions"""

        response = {
            "data": [
                {"id": 1, "question": "Hi how are you?"}
            ],
            "status_code": 200
        }

        print(response)
        return response
