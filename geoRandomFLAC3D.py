from inspect import getsourcefile
import itasca as it
import os
import shutil
import numpy as np

it.command("python-reset-state false")

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = current_path  # os.path.dirname(current_path)

numberOfModels = 20

buildingLoad = []
tunnelDepth = []
waterTable = []
modelCaseOld = []
solveModel = []
FtList = []
MtList = []
CtList = []
StList = []
GtList = []
loList = []

for td in range(10, 15, 2):
    for bi in range(130, 9, -60):
        for wt in range(3, 6, 2):
            modelCaseOld.append("model_" + str(wt) + "_" + str(bi) + "_" + str(td))

for el in range(numberOfModels):

    # Soil Thickness
    soilLocation = np.random.randint(1, 7)
    if soilLocation == 1:  # GranPlaza
        firstL, secondL, thirdL, fourthL, loc = 0.9, 4, 1, 9, "A"
    elif soilLocation == 2:  # SanBernardo
        firstL, secondL, thirdL, fourthL, loc = 1.5, 5, 1.5, 8.5, "B"
    elif soilLocation == 3:  # SanSebastian
        firstL, secondL, thirdL, fourthL, loc = 2.5, 3, 3.5, 9, "C"
    elif soilLocation == 4:  # PurtaJerez
        firstL, secondL, thirdL, fourthL, loc = 3, 12, 1, 7, "D"
    elif soilLocation == 5:  # PlazaCuba
        firstL, secondL, thirdL, fourthL, loc = 2, 1.5, 13, 8.5, "E"
    elif soilLocation == 6:  # ParqueLosP
        firstL, secondL, thirdL, fourthL, loc = 2, 4, 11, 6, "F"
    lastL = 1000

    # Tunnel depth, building load, and water table
    tDepth = (round(np.random.uniform(10, 15)))
    wTable = (round(np.random.uniform(3, 6)))
    bLoad = (round(np.random.uniform(0.1, 1.4), 2))
    nameModel = "model_" + str(wTable) + "_" + str(round(bLoad * 100)) + "_" + str(tDepth)

    # Check the model
    if nameModel not in solveModel and nameModel not in modelCaseOld:
        nameModelWithLocation = nameModel + "_" + loc
        solveModel.append(nameModelWithLocation)
        FtList.append(firstL)
        CtList.append(secondL)
        StList.append(thirdL)
        GtList.append(fourthL)
        MtList.append(lastL)
        loList.append(loc)
        buildingLoad.append(round(bLoad * (-100000), 1))
        tunnelDepth.append(tDepth)
        waterTable.append(wTable)

print(solveModel)

for k, c in enumerate(solveModel):
    oPath = current_dir + '/' + c
    if not os.path.exists(oPath):
        os.makedirs(oPath)

    aaa = []
    if os.path.exists(current_dir + '\\myRuns.txt'):
        f = open(current_dir + '\\myRuns.txt', 'r')
        for line in f:
            aaa.append(line.strip("\n"))
        f.close()
    if c not in aaa:
        aaa.append(c)
        with open(current_dir + '\\myRuns.txt', 'w') as f:
            f.writelines("%s\n" % l for l in aaa)
        f.close()

        oPathCurr = oPath
        if not os.path.exists(oPathCurr):
            os.makedirs(oPathCurr)

        it.command(f"""
        model new
            [Ft=  {FtList[k]}]
            [Mt=  {MtList[k]}]
            [Ct=  {CtList[k]}]
            [St=  {StList[k]}]
            [Gt=  {GtList[k]}]
            [Tunnel_Depth  = {tunnelDepth[k]}]
            [WaterTable    = {waterTable[k]}]
            
            program call "GeoDimension.f3dat"
            
            [stress_normal = {buildingLoad[k]}]
            program call "DeadLoad_Building.f3dat"
            
            model save './{c}/Ready_Excavate.sav'
            """)
