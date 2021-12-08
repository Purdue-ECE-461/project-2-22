import os
import actions_tests


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\sguad\\A_Desktop\\College\\ECE_461\\Project2\\" \
                                               "Credentials\\ece-461-project-2-22-29ce8b9991bd.json"

if __name__ == "__main__":
    actions_tests.run_test()
