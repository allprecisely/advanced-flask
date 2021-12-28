import os
from typing import List, Union

import requests

DOMAIN_NAME = os.getenv('DOMAIN_NAME')
API_KEY = os.getenv('API_KEY')


class MailgunError(Exception):
    """Raised when problems with MailgunLib"""


def send_email(emails: Union[List[str], str], subject: str, text: str) -> requests.Response:
    if not DOMAIN_NAME or not API_KEY:
        raise MailgunError('DOMAIN_NAME or API_KEY are not defined.')
    response = requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN_NAME}/messages",
        auth=("api", API_KEY),
        data={
            "from": f"Excited User <mailgun@{DOMAIN_NAME}>",
            "to": emails,
            "subject": subject,
            "text": text,
        },
    )

    if response.status_code != 200:
        raise MailgunError('Response code from mailgun is not 200')

    return response
