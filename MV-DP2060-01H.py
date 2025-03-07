# -- coding: utf-8 --
import threading
import os, sys, time

# импортируем функцию show_window для вывода сообщений
from GUI.gui_alert import show_window  
from GUI.connect_to_device import show_device_info_dialog

# позволяет взаимодействовать с низкоуровневыми библиотеками (например, C или C++)  и манипулировать данными, как если бы они были представлены в памяти на уровне C, когда нужно работать с API, написанными на C/C++.
import ctypes

from Mv3dLpImport.Mv3dLpApi import Mv3dLp
from Mv3dLpImport.Mv3dLpDefine import MV3D_LP_DEVICE_INFO_LIST, MV3D_LP_IMAGE_DATA

if __name__ == "__main__":
    #  создает переменную nDeviceNum, которая хранит беззнаковое целое число 0
    nDeviceNum = ctypes.c_uint(0)
    # ctypes.byref(nDeviceNum) возвращает объект, который представляет собой указатель на память, где хранится nDeviceNum
    # nDeviceNum_p теперь хранит адрес памяти, где находится значение нашего беззнакового целого числа.
    nDeviceNum_p = ctypes.byref(nDeviceNum)

    # версия библиотеки
    DLL_version = Mv3dLp.MV3D_LP_GetVersion()

    ret = Mv3dLp.MV3D_LP_GetDeviceNumber(nDeviceNum_p)  # Get Device Number
    if ret != 0:
        show_window(f"Отсутсвуют устройства, для подключения: {ret}")
        os.system('pause')
        sys.exit()

    if nDeviceNum == 0:
        show_window(f"Отсутсвуют устройства, для подключения")
        os.system('pause')
        sys.exit()
    
    # количество доступных устройств 
    number_of_devices = nDeviceNum.value

    # Этот код пытается получить список подключенных устройств
    # Создается экземпляр структуры, которая предназначена для хранения списка информации об устройствах
    # На этом этапе stDeviceList инициализируется, но еще не содержит данных об устройствах.
    stDeviceList = MV3D_LP_DEVICE_INFO_LIST()
    # ctypes.pointer(stDeviceList.DeviceInfo[0]) - Указатель на начало массива структур MV3D_LP_DEVICE_INFO, куда функция запишет информацию об устройствах.
    # 20: Максимальное количество устройств, которое функция может вернуть.
    # nDeviceNum_p: Указатель на переменную, в которую функция запишет фактическое количество найденных устройств.
    number_of_devices_found = Mv3dLp.MV3D_LP_GetDeviceList(ctypes.pointer(stDeviceList.DeviceInfo[0]), 20, nDeviceNum_p)

    if nDeviceNum.value != 0:
        # если присутсвуют доступные устройства
        for i in range(0, nDeviceNum.value):
            # Печатаем id, название и серийный номер
            devices_id = ""
            devices_id += ("device: %d, " % i)
            strModeName = ""

            device_model_name = ""
            for per in stDeviceList.DeviceInfo[i].chModelName:
                strModeName = strModeName + chr(per)
            device_model_name += ("device model name: %s, " % strModeName)

            strSerialNumber = ""
            for per in stDeviceList.DeviceInfo[i].chSerialNumber:
                strSerialNumber = strSerialNumber + chr(per)
            devices_serial_number = ("device SerialNumber: %s, " % strSerialNumber)

        print(devices_id,  device_model_name, devices_serial_number)

        # Create device Object
        camera=Mv3dLp()
        # количество доступных устройств 
        nConnectionNum = show_device_info_dialog(devices_id, device_model_name, devices_serial_number, number_of_devices)

        if int(nConnectionNum) > nDeviceNum.value:
            show_window(f"Введенное значение, больше чем количество доступных устройств.")
            os.system('pause')
            sys.exit()
        








    
