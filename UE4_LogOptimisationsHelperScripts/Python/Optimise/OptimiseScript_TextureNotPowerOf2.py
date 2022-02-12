# ////////////////////////////////////////////////////////////////////////
# @CBgameDev Optimisation Script - Log Textures That Are Not Power Of Two
# ////////////////////////////////////////////////////////////////////////
import unreal
import os
import math

EditAssetLib = unreal.EditorAssetLibrary()
workingPath = "/Game/"  # Using the root directory
notepadFilePath = os.path.dirname(__file__) + "//PythonOptimiseLog.txt"
allAssets = EditAssetLib.list_assets(workingPath, True, False)
selectedAssetsPath = workingPath
LogStringsArray = []
numOfOptimisations = 0


def is_power_of_2(n): 	# check if n is power of 2
    return (math.log(n)/math.log(2)).is_integer()


with unreal.ScopedSlowTask(len(allAssets), selectedAssetsPath) as ST:
    ST.make_dialog(True)

    for asset in allAssets:
        _assetData = EditAssetLib.find_asset_data(asset)
        _assetName = _assetData.get_asset().get_name()
        _assetPathName = _assetData.get_asset().get_path_name()
        _assetClassName = _assetData.get_asset().get_class().get_name()
        # unreal.log(_assetClassName)

        if _assetClassName == "Texture2D":
            _TextureAsset = unreal.Texture2D.cast(_assetData.get_asset())
            _TextureXsize = _TextureAsset.blueprint_get_size_x()
            _TextureYsize = _TextureAsset.blueprint_get_size_y()

            if not is_power_of_2(_TextureYsize):
                LogStringsArray.append("        [%s x %s] %s ------------> At Path: %s \n" % (_TextureXsize, _TextureYsize, _assetName, _assetPathName))
                # unreal.log("Asset Name: %s Path: %s \n" % (_assetName, _assetPathName))
                numOfOptimisations += 1
                # print("Y is a power of 2")

            elif not is_power_of_2(_TextureXsize):
                LogStringsArray.append("        [%s x %s] %s ------------> At Path: %s \n" % (_TextureXsize, _TextureYsize, _assetName, _assetPathName))
                # unreal.log("Asset Name: %s Path: %s \n" % (_assetName, _assetPathName))
                numOfOptimisations += 1
                print("X is a power of 2")

        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset)


# Write results into a log file
# //////////////////////////////
TitleOfOptimisation = "Log Textures That Are Not Power Of Two"
DescOfOptimisation = "Searches the entire project for textures that are not a power of two e.g. 13x64, 100x96 etc. Instead of e.g. 32x32, 128x128 512x256"
SummaryMessageIntro = "-- Textures Which Are Not A Power Of Two --"

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
