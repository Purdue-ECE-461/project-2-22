import send_requests


def test_get_packages():
    resp = send_requests.ping_get_packages('^1.0', 'Underscore')
    pid = resp[2][0]['ID']
    if pid == 'underscore':
        assert True
    else:
        assert False


def test_run():
    assert True


if __name__ == '__main__':
    print("fun")
