import io, zipfile, json, pprint
from zipfile import ZipFile

def getPackageJson(file): #file = zip file
    with ZipFile(file, 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for fileName in listOfFileNames:
            if fileName.endswith('package.json'):
                zipObj.extract(fileName, path="/tmp")
                return fileName
    return None


def getURL(file): #file = name of file in directory
    f = open(file, )
    data = json.load(f)
    f.close()

    for key, value in data.items():
        if key == "repository":
            if isinstance(value, dict):
                for key1, value1 in value.items():
                    if key1 == 'url':
                        return value1
            else:
                return 'https://github.com/' + value
        elif key == "homepage":
            if 'github.com' in value:
                return value

    return None


def rate(url):
    from PreviousProject.Fetching.PackageFetcher import PackageFetcher
    from PreviousProject.Scoring.BusFactor.BusFactorScore import BusFactorScore
    from PreviousProject.Scoring.Correctness.CorrectnessScore import CorrectnessScore
    from PreviousProject.Scoring.LicenseCompatibility.LicenseCompatibilityScore import LicenseCompatibilityScore
    from PreviousProject.Scoring.RampUp.RampUpTimeScore import RampUpTimeScore
    from PreviousProject.Scoring.Responsiveness.ResponsivenessScore import ResponsivenessScore
    from PreviousProject.Scoring.Dependency.DependencyScore import DependencyScore

    packageFetcher = PackageFetcher(url)
    package = packageFetcher.fetchPackage()

    # Get License Score
    licenseCompatibilityScorer = LicenseCompatibilityScore(package)
    licenseCompatibility = licenseCompatibilityScorer.score()

    # Get Correctness Score
    correctnessScorer = CorrectnessScore(package)
    correctness = correctnessScorer.score()

    # Get Bus Factor Score
    busFactorScorer = BusFactorScore(package)
    busFactor = busFactorScorer.score()

    # Get Ramp Up Score
    rampUpScorer = RampUpTimeScore(package)
    rampUp = rampUpScorer.score()

    # Get Responsiveness Score
    responsivenessScorer = ResponsivenessScore(package)
    responsiveness = responsivenessScorer.score()

    # Get Dependency Score - NEW
    dependencyScorer = DependencyScore(package)
    dependency = dependencyScorer.score()

    data = {
        "BusFactor": busFactor,
        "Correctness": correctness,
        "RampUp": licenseCompatibility,
        "ResponsiveMaintainer": rampUp,
        "LicenseScore": responsiveness,
        "GoodPinningPractice": dependency
    }
    return data


if __name__ == "__main__":
    '''file = getPackageJson("output_file.zip")
    if file != None:
        url = getURL(file)
        rate(url)'''
    print(rate('https://github.com/jonschlinkert/even'))