import os
from project_1_project_1_21.run import run_proj


def rate_module_url(module_url):
    proj_rate.run_proj(module_url)
    return


if __name__ == '__main__':
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "..."
    os.environ['GITHUB_TOKEN'] = '...'
    # g = Github()
    # Create.create_bucket("testing_team_advanced_dev_sg")
    # Create.create_bucket("testing_team_new_products_sg")
    # Create.create_bucket("testing_team_marketing_sg")
    rate_module_url("https://github.com/expressjs/express")
