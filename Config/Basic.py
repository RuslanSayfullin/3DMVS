# -- coding: utf-8 --
import threading
import os, sys, time

from Mv3dLpImport.Mv3dLpApi import Mv3dLp
from Mv3dLpImport.Mv3dLpDefine import MV3D_LP_DEVICE_INFO_LIST, MV3D_LP_IMAGE_DATA

# позволяет взаимодействовать с низкоуровневыми библиотеками (например, C или C++) 
# и манипулировать данными, как если бы они были представлены в памяти на уровне C, 
# когда нужно работать с API, написанными на C/C++.
import ctypes

g_bExit = False
def work_thread(camera=0,pdata=0,nDataSize=0):
    file_counter = 0

    while True:
        stImageData=MV3D_LP_IMAGE_DATA()
        ret=camera.MV3D_LP_GetImage(ctypes.pointer(stImageData),1000)
        if ret==0:
            print("get image:nFrameNum[%d],nDataLen[%d],nWidth[%d],nHeight[%d]" % (
                stImageData.nFrameNum, stImageData.nDataLen, stImageData.nWidth, stImageData.nHeight))
            
            filename = f"image_{file_counter}"
            # Кодируем filename в байты, чтобы передать как c_char_p
            filename_bytes = filename.encode('utf-8')

            ret1=camera.MV3D_LP_SaveImage(ctypes.pointer(stImageData), 5, filename_bytes)
            file_counter += 1
            if ret1==0:
                print("save image success!")
            else:
                print("save image failed...")

            stDstImageData=MV3D_LP_IMAGE_DATA()
            ret2=camera.MV3D_LP_MapDepthToPointCloud(ctypes.pointer(stImageData),ctypes.pointer(stDstImageData))
            print("ret2", ret2)
            if ret2==0:
                print("map depth to point cloud success!")
            else:
                print("map depth to point cloud failed...")

            time.sleep(5)

        if g_bExit == True:
            break

if __name__ == "__main__":
    #  создает переменную nDeviceNum, которая хранит беззнаковое целое число 0
    nDeviceNum = ctypes.c_uint(0)
    # ctypes.byref(nDeviceNum) возвращает объект, который представляет собой указатель на память, где хранится nDeviceNum
    # nDeviceNum_p теперь хранит адрес памяти, где находится значение нашего беззнакового целого числа.
    nDeviceNum_p = ctypes.byref(nDeviceNum)

    ret = Mv3dLp.MV3D_LP_GetDeviceNumber(nDeviceNum_p)  # Get Device Number
    if ret != 0:
        print("enum devices fail! ret[0x%x]" % ret)
        os.system('pause')
        sys.exit()
    print("ret:", ret)

    if nDeviceNum == 0:
        print("find no device!")
        os.system('pause')
        sys.exit()
    print("find devices numbers:", nDeviceNum.value)

    """Этот код пытается получить список подключенных устройств"""
    # Создается экземпляр структуры, которая предназначена для хранения списка информации об устройствах
    # На этом этапе stDeviceList инициализируется, но еще не содержит данных об устройствах.
    stDeviceList = MV3D_LP_DEVICE_INFO_LIST()
    # ctypes.pointer(stDeviceList.DeviceInfo[0]) - Указатель на начало массива структур MV3D_LP_DEVICE_INFO, куда функция запишет информацию об устройствах.
    # 20: Максимальное количество устройств, которое функция может вернуть.
    # nDeviceNum_p: Указатель на переменную, в которую функция запишет фактическое количество найденных устройств.
    net = Mv3dLp.MV3D_LP_GetDeviceList(ctypes.pointer(stDeviceList.DeviceInfo[0]), 20, nDeviceNum_p)
    print("net:", net)

    if nDeviceNum.value != 0:
        for i in range(0, nDeviceNum.value):
            # Печатаем id, название и серийный номер
            print("\ndevice: [%d]" % i)
            strModeName = ""
            for per in stDeviceList.DeviceInfo[i].chModelName:
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)
            
            strSerialNumber = ""
            for per in stDeviceList.DeviceInfo[i].chSerialNumber:
                strSerialNumber = strSerialNumber + chr(per)
            print("device SerialNumber: %s" % strSerialNumber)

        # Create device Object
        camera=Mv3dLp()
        nConnectionNum = input("please input the number of the device to connect:")
        if int(nConnectionNum) >= nDeviceNum.value:
            print("intput error!")
            os.system('pause')
            sys.exit()

        # Open Device
        ret0 = camera.MV3D_LP_OpenDeviceBySN(stDeviceList.DeviceInfo[int(nConnectionNum)].chSerialNumber)
        if ret0 != 0:
            print("open device fail! ret[0x%x]" % ret)
            os.system('pause')
            sys.exit()

        Version = camera.MV3D_LP_GetVersion()
        print(Version)

        # Start Measure
        ret1=camera.MV3D_LP_StartMeasure()
        if ret1 != 0:
            print ("start measure fail! ret[0x%x]" % ret)
            camera.MV3D_LP_CloseDevice()
            os.system('pause')
            sys.exit()

        try:
            hthreadhandle=threading.Thread(target=work_thread,args=(camera,None,None))
            hthreadhandle.start()
        except:
            print("error: unable to start thread")

        print("press a key to stop measure.")
        os.system('pause')
        g_bExit = True

        hthreadhandle.join()

        # Stop Measure
        ret=camera.MV3D_LP_StopMeasure()
        if ret != 0:
            print ("stop measure fail! ret[0x%x]" % ret)
            sys.exit()

        # Close Device
        ret=camera.MV3D_LP_CloseDevice()
        if ret != 0:
            print ("close device fail! ret[0x%x]" % ret)
            sys.exit()

    else:
        print("No find devices")


    