import os
import Tests


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/sguad/A_Desktop/College/ECE_461/Project2/proj2_code_github/" \
                                               "project-2-22/Credentials/prime-micron-330718-02ad6bc9672b.json"

if __name__ == "__main__":
    Tests.run_test()
    # read in json file 1 test_report.json
    # test_file = open('.report.json', )
    # test_coverage = open('coverage.json', )
    # test_data = json.load(test_file)
    # cov_data = json.load(test_coverage)
    # test_file.close()
    # test_coverage.close()
    #
    # total_tests = test_data['summary']['total']
    #
    # if 'passed' in test_data['summary']:
    #     total_passed = test_data['summary']['passed']
    # else:
    #     total_passed = 0
    #
    # coverage = cov_data['totals']['percent_covered']
    #
    # print("Total: {}".format(total_tests))
    # print("Passed: {}".format(total_passed))
    # print("Coverage: {:.2f}%".format(coverage))
    #
    # print("{}/{} test cases passed. {:.2f}% line coverage acheived".format(total_passed, total_tests, coverage))
