# /////////////////////////////////////////////////////////////////////
# @CBgameDev Optimisation Script - Log Skel Mesh Missing Physics Asset
# /////////////////////////////////////////////////////////////////////
import unreal
import os

EditAssetLib = unreal.EditorAssetLibrary()
SystemsLib = unreal.SystemLibrary
workingPath = "/Game/"  # Using the root directory
notepadFilePath = os.path.dirname(__file__) + "//PythonOptimiseLog.txt"
allAssets = EditAssetLib.list_assets(workingPath, True, False)
selectedAssetsPath = workingPath
LogStringsArray = []
numOfOptimisations = 0


with unreal.ScopedSlowTask(len(allAssets), selectedAssetsPath) as ST:
    ST.make_dialog(True)

    for asset in allAssets:
        _assetData = EditAssetLib.find_asset_data(asset)
        _assetName = _assetData.get_asset().get_name()
        _assetPathName = _assetData.get_asset().get_path_name()
        _assetClassName = _assetData.get_asset().get_class().get_name()

        if _assetClassName == "SkeletalMesh":
            #asset_obj = EditAssetLib.load_asset(asset)
            _SkeletalMeshAsset = unreal.SkeletalMesh.cast(EditAssetLib.load_asset(asset))
            _PhysicsAsset = unreal.SkeletalMesh.cast(_SkeletalMeshAsset).physics_asset
            # unreal.log(SkelMeshLib.get_lod_count(_SkeletalMeshAsset))
            # unreal.log(_SkeletalMeshAsset)

           # StringToCheck = _assetData.get_asset().get_editor_property("phys_material")  # asset_obj.get_editor_property("phys_material")
            # unreal.log("Used Phys Mat = %s" % StringToCheck)

            if not SystemsLib.is_valid(_PhysicsAsset):
                LogStringsArray.append("        %s ------------> At Path: %s \n" % (_assetName, _assetPathName))
                # unreal.log("Asset Name: %s Path: %s \n" % (_assetName, _assetPathName))
                numOfOptimisations += 1

        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset)


# Write results into a log file
# //////////////////////////////
TitleOfOptimisation = "Log Skeletal Meshes Missing Physics Assets"
DescOfOptimisation = "Searches the entire project for Skeletal Meshes With No Physics Asset Plugged In"
SummaryMessageIntro = "-- Skeletal Meshes Without Physics Assets Plugged In --"

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
