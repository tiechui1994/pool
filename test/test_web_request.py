from utils.WebRequest import WebRequest


def test_web_request():
    """
    test class WebRequest in utils/WebRequest.py
    """
    wr = WebRequest()
    request_object = wr.get('https://www.baidu.com/')
    assert request_object.status_code == 200


if __name__ == '__main__':
    test_web_request()
