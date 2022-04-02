# //////////////////////////////////////////////////////////////////
# @CBgameDev Optimisation Script - Log Blueprints With Tick Enabled
# //////////////////////////////////////////////////////////////////
import unreal
import os

EditAssetLib = unreal.EditorAssetLibrary()
# SkeletalMeshLib = unreal.BlueprintFunctionLibrary() #dont think need
TickFunctionality = unreal.TickFunction()
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

        if _assetClassName == "Blueprint":
            _BlueprintAsset = unreal.Blueprint.cast(_assetData.get_asset())
            unreal.TickFunction.
            unreal.log(_assetData.get_asset().get_editor_property("allow_tick_before_begin_play"))
            # _assetData.get_editor_property("allow_tick_before_begin_play")
            #  unreal.Actor.cast(_BlueprintAsset.get_default_object())
            # unreal.log(_assetData.get_asset().get_default_object())
            # unreal.log(unreal.Actor.cast(_assetData.get_asset()))
            # EditAssetLib.load_blueprint_class(_BlueprintAsset)
            # _BlueprintAsset.TickFunctionality.get_editor_property("start_with_tick_enabled")
            # .get_editor_property("allow_tick_before_begin_play ")
            # _BlueprintAsset.get_default_object(_assetData.get_asset()).TickFunctionality

            unreal.log("is a blueprint")
            LogStringsArray.append("        %s ------------> At Path: %s \n" % (_assetName, _assetPathName))
            # unreal.log("Asset Name: %s Path: %s \n" % (_assetName, _assetPathName))
            numOfOptimisations += 1

        # new way
        asset_obj = EditAssetLib.load_asset(asset)
        # isTickOn = asset_obj.get_editor_property(unreal.TickFunction.get_editor_property)
        # important documentation: https://docs.unrealengine.com/4.26/en-US/PythonAPI/class/TickFunction.html

        if ST.should_cancel():
            break
        ST.enter_progress_frame(1, asset)


# Write results into a log file
# //////////////////////////////
TitleOfOptimisation = "Log Blueprints With Tick Enabled"
DescOfOptimisation = "Searches the entire project for blueprints which have tick enabled and that we could consider turning off"
SummaryMessageIntro = "-- Assets With 0 References That We Could Consider Deleting --"


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
