# ///////////////////////////////////////////////////////////////////////
# @CBgameDev Optimisation Script - Log Textures That Are Equal To X Size
# ///////////////////////////////////////////////////////////////////////
import unreal
import sys  # So we can grab arguments fed into the python script
import os

EditAssetLib = unreal.EditorAssetLibrary()
workingPath = "/Game/"  # Using the root directory
notepadFilePath = os.path.dirname(__file__) + "//PythonOptimiseLog.txt"
allAssets = EditAssetLib.list_assets(workingPath, True, False)
selectedAssetsPath = workingPath
LogStringsArray = []
numOfOptimisations = 0
SizeOfTexToCheckAgainst = int(float(sys.argv[1]))  # pull value sent with script


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

            if _TextureYsize == SizeOfTexToCheckAgainst or _TextureXsize == SizeOfTexToCheckAgainst:
                LogStringsArray.append("        [%sx%s] %s ------------> At Path: %s \n" % (_TextureXsize, _TextureYsize, _assetName, _assetPathName))
                # unreal.log("Asset Name: %s Path: %s \n" % (_assetName, _assetPathName))
                numOfOptimisations += 1

        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset)


# Write results into a log file
# //////////////////////////////
TitleOfOptimisation = "Log Textures That Are Equal To X Size"
DescOfOptimisation = "Searches the entire project for Textures which are equal to the size you have set. Use to help find textures which are larger than what you need them for"
SummaryMessageIntro = "-- Textures Of Size %s  --" % SizeOfTexToCheckAgainst

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
