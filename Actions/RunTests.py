import os
from Actions import actions_tests


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/sguad/A_Desktop/College/ECE_461/Project2/proj2_code_github/" \
                                               "project-2-22/Credentials/prime-micron-330718-02ad6bc9672b.json"

if __name__ == "__main__":
    actions_tests.run_test()