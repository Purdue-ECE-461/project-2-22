import os
from project_1_project_1_21.run import run_proj


def rate_module_url(module_url):
    proj_rate.run_proj(module_url)
    return


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/sguad/A_Desktop/College/ECE_461/Project2/" \
                                                   "proj2_code_github/project-2-22/Credentials/" \
                                                   "prime-micron-330718-02ad6bc9672b.json"
    os.environ['GITHUB_TOKEN'] = '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'
    # g = Github()
    # Create.create_bucket("testing_team_advanced_dev_sg")
    # Create.create_bucket("testing_team_new_products_sg")
    # Create.create_bucket("testing_team_marketing_sg")
    rate_module_url("https://github.com/expressjs/express")
