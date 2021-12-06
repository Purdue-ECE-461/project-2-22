import database_helper
import send_requests


def test_post_rate():
    send_requests.ping_post_package('Cloudier', '3.1.2', '68', 'https://github.com/cloudinary/cloudinary_npm', '',
                                          'cloudy with a chance of meatballs')
    p_id = (database_helper.get_package_id('Cloudier', '3.1.2', '68'))
    res = send_requests.ping_rate_package_by_id(p_id)
    assert res[2]['BusFactor'] == 0.5


def test_get_packages():
    resp = send_requests.ping_get_packages('^3.1.2', 'Cloudier')
    k_id = (database_helper.get_package_id('Cloudier', '3.1.2', '68'))
    pid = resp[2][0]['ID']
    if pid == k_id:
        assert True
    else:
        assert False


def test_delete_package_by_name():
    resp = send_requests.ping_delete_package_by_name('Cloudier')
    if resp[1] != 200:
        assert False
    packages = database_helper.get_all_packages()
    for p in packages:
        if p[0] == 'Cloudier':
            assert False
    assert True


def test_run():
    assert True


if __name__ == '__main__':
    print("fun")
