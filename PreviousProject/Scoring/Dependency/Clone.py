import os
from git import Repo
from git import rmtree
import json
import re


def clone_module(url, module_name):
    # Check if the repo already is cloned, if not then clone
    repo = Repo.clone_from(url, module_name)  # could maybe use giturl but we dont have that yet

    # Analyze cloned repository
    score = module_clone_readme_analyzer(module_name)

    # Remove cloned repo
    cwd = os.getcwd()
    directory_folder_empty = os.path.join(cwd, module_name.split("/")[0])
    rmtree(directory_folder_empty)
    return score


def module_clone_readme_analyzer(module_name):
    #cwd = os.getcwd()
    #directory = os.path.join(cwd, module_name)
    directory = os.path.join("/tmp", module_name) #comment change to push
    count = 0
    total = 0
    score = 0
    for filename in os.listdir(directory):
        if filename == "package.json":
            name = directory + "/package.json"
            file = open(name)
            data = json.load(file)

            dep = 0
            for key, value in data.items():
                if key == 'dependencies':
                    dep = 1

            if dep == 0:
                return 0

            for key, value in data["dependencies"].items():
                p = re.compile("[~^<>]?[=]?\d+\.\d+\.?[X|x|\d+]?")
                x = p.search(value)
                if x is not None:
                    count += 1
                #    print(x.group(), value, "yes")
                #else:
                #    print(value, "no")
                total += 1
            score = count/total
    #print(score)
    return score
