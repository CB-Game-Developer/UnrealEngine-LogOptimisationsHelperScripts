# /////////////////////////////////////////////////////////////////////////////////
# @CBgameDev Optimisation Script - LOG Skeletal Mesh Assets With X Num Of Materials
# /////////////////////////////////////////////////////////////////////////////////
import unreal
import sys  # So we can grab arguments fed into the python script
import os

EditAssetLib = unreal.EditorAssetLibrary()
SkeletalMeshLib = unreal.EditorSkeletalMeshLibrary()
workingPath = "/Game/"  # Using the root directory
notepadFilePath = os.path.dirname(__file__) + "//PythonOptimiseLog.txt"
allAssets = EditAssetLib.list_assets(workingPath, True, False)
selectedAssetsPath = workingPath
LogStringsArray = []
numOfOptimisations = 0
NumOfMatsToCheckFor = int(float(sys.argv[1]))  # pull value sent with script


with unreal.ScopedSlowTask(len(allAssets), selectedAssetsPath) as ST:
    ST.make_dialog(True)

    for asset in allAssets:
        _assetData = EditAssetLib.find_asset_data(asset)
        _assetName = _assetData.get_asset().get_name()
        _assetPathName = _assetData.get_asset().get_path_name()
        _assetClassName = _assetData.get_asset().get_class().get_name()

        if _assetClassName == "SkeletalMesh":
            _skeletalMeshAsset = unreal.SkeletalMesh.cast(_assetData.get_asset())
            _howManyMaterials = len(_skeletalMeshAsset.get_editor_property("materials"))
            # unreal.log(_howManyMaterials)

            if _howManyMaterials >= NumOfMatsToCheckFor:
                LogStringsArray.append("        [%s] - %s ------------> At Path: %s \n" % (_howManyMaterials, _assetName, _assetPathName))
                unreal.log("Asset Name: [%s] %s Path: %s \n" % (_howManyMaterials, _assetName, _assetPathName))
                numOfOptimisations += 1

        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset)

# Write results into a log file
# //////////////////////////////
TitleOfOptimisation = "LOG Skeletal Mesh Assets With X Num Of Materials"
DescOfOptimisation = "Searches the entire project for skeletal mesh assets that have a material count above the value that you have set"
SummaryMessageIntro = "-- Skeletal Mesh Assets With Material Count Numbering >= %s --" % NumOfMatsToCheckFor

if unreal.Paths.file_exists(notepadFilePath):  # Check if txt file already exists
    os.remove(notepadFilePath)  # if does remove it

# Create new txt file and run intro text
file = open(notepadFilePath, "a+")  # we should only do this if have a count?
file.write("OPTIMISING SCRIPT by @CBgameDev \n")
file.write("==================================================================================================== \n")
file.write("    SCRIPT NAME: %s \n" % TitleOfOptimisation)
file.write("    DESCRIPTION: %s \n" % DescOfOptimisation)
file.write("==================================================================================================== \n \n")


if numOfOptimisations <= 0:
    file.write(" -- NONE FOUND -- \n \n")
else:
    for i in range(len(LogStringsArray)):
        file.write(LogStringsArray[i])


# Run summary text
file.write("\n")
file.write("======================================================================================================= \n")
file.write("    SUMMARY: \n")
file.write("        %s \n" % SummaryMessageIntro)
file.write("              Found: %s \n \n" % numOfOptimisations)
file.write("======================================================================================================= \n")
file.write("        Logged to %s \n" % notepadFilePath)
file.write("======================================================================================================= \n")
file.close()
os.startfile(notepadFilePath)  # Trigger the notepad file to open
