import signal
import subprocess
import database_helper
import psutil

def test_cloud():
    result = subprocess.Popen(args=['./cloud_sql_proxy -instances=\"ece-461-project-2-22:us-east1:proj-2-database-mysql\"'
                                   '=tcp:3306'], shell=True)
    print(result.stderr)
    print(result.stdout)

    conn = database_helper.mysql_connect()
    # initialize_db(conn.cursor())
    database_helper.post_package(conn, 'name1', '1.0.0', '2', 'test1234.com', 'name1.txt')
    database_helper.post_package(conn, 'name1', '1.0.0', '3', 'test1234.com', 'name1.txt')
    database_helper.get_all_packages(conn)
    database_helper.mysql_close(conn)

    print(result.pid)
    parent = (psutil.Process(result.pid))
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()
    result.send_signal(signal.SIGINT)

if __name__ == '__main__':
    test_cloud()
    print("why")