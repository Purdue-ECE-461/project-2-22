import send_requests

# WILL BE ABLE TO TEST THIS AFTER REDEPLOYING

def test_rate():
    res = send_requests.ping_post_package('test_rate', '1.0.0', '78', 'https://github.com/cloudinary/cloudinary_npm', '',
                                          '')
    p_id = res[2]['ID']
    
    print(res)

    print(p_id)

    res = send_requests.ping_rate_package_by_id(p_id)

    print(res)

    # send_requests.ping_delete_package_by_id(p_id)

    assert res[2]['BusFactor'] == 0.5


def test_no_ingestion():
    res = send_requests.ping_post_package('Cloudier', '3.1.2', '68', 'https://github.com/cloudinary/cloudinary_npm', '',
                                          'cloudy with a chance of meatballs')
    code = res[1]

    assert code == 201


def test_get_packages():
    resp = send_requests.ping_get_packages('^3.1.2', 'Cloudier')
    packages = len(resp[2])
    if packages > 0:
        assert True
    else:
        assert False


def test_delete_package_by_name():
    resp = send_requests.ping_delete_package_by_name('Cloudier')
    if resp[1] != 200:
        assert False
    packages = send_requests.ping_get_packages('3.1.2', 'Cloudier')[2]
    if len(packages) > 0:
        assert False
    else:
        assert True


def test_get_package_history():
    res = send_requests.ping_get_package_by_name('Cloudier')

    assert res[2][-1]['PackageMetadata']['Name'] == 'Cloudier'
    assert res[2][-1]['Action'] == 'Delete'




def test_run():
    assert True


if __name__ == '__main__':
    print("fun")
