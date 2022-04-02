# ////////////////////////////////////////////////////////////////////////////
# @CBgameDev Optimisation Script - Log Static Mesh UV Channel Count For LOD 0
# ////////////////////////////////////////////////////////////////////////////
import unreal
import sys  # So we can grab arguments fed into the python script
import os

EditAssetLib = unreal.EditorAssetLibrary()
StatMeshLib = unreal.EditorStaticMeshLibrary()
workingPath = "/Game/"  # Using the root directory
notepadFilePath = os.path.dirname(__file__) + "//PythonOptimiseLog.txt"
allAssets = EditAssetLib.list_assets(workingPath, True, False)
selectedAssetsPath = workingPath
LogStringsArray = []
numOfOptimisations = 0
numOfChannelsToCheckFor = int(float(sys.argv[1]))  # pull value sent with script


with unreal.ScopedSlowTask(len(allAssets), selectedAssetsPath) as ST:
    ST.make_dialog(True)

    for asset in allAssets:
        _assetData = EditAssetLib.find_asset_data(asset)
        _assetName = _assetData.get_asset().get_name()
        _assetPathName = _assetData.get_asset().get_path_name()
        _assetClassName = _assetData.get_asset().get_class().get_name()

        if _assetClassName == "StaticMesh":
            _staticMeshAsset = unreal.StaticMesh.cast(_assetData.get_asset())
            _howManyUV_channels = StatMeshLib.get_num_uv_channels(_staticMeshAsset, 0)

            if _howManyUV_channels >= numOfChannelsToCheckFor:
                LogStringsArray.append("        [%s] - %s ------------> At Path: %s \n" % (_howManyUV_channels, _assetName, _assetPathName))
                # unreal.log("Asset Name: [%s] %s Path: %s \n" % (_howManyUV_channels, _assetName, _assetPathName))
                numOfOptimisations += 1

        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset)

# Write results into a log file
# //////////////////////////////
TitleOfOptimisation = "Log Static Mesh UV Channel Count For LOD 0"
DescOfOptimisation = "Searches the entire project for static mesh assets that have a UV channel count above the value that you have set"
SummaryMessageIntro = "-- Static Mesh Assets With UV Channels Numbering >= %s --" % numOfChannelsToCheckFor


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
