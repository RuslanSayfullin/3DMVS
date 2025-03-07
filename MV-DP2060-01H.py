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

# Список, кодов  файлов;
Mv3dLpFileType = {
    "Undefined type.": 0,
    "PLY": 1,
    "CSV": 2,
    "OBJ": 3,
    "BMP": 4, 
    "JPG": 5,
    "TIFF (S16)": 6,
    "TIFF (U16)": 7, 
    "TIFF (F32)": 8,
    "PLY (Binary)": 9,
    "PCD": 10
}
 
# Список, возвращаемых кодов;
error_codes = {
    0: "Correct status code.",                                                  # 0x00000000
    2147876864: "Incorrect or invalid handle.",                                 # 0x80060000
    2147876865: "The function is not supported.",                               # 0x80060001
    2147876866: "The buffer is full.",                                          # 0x80060002
    2147876867: "Incorrect calling sequence.",                                  # 0x80060003
    2147876868: "Incorrect parameter.",                                         # 0x80060004
    2147876869: "Requesting for resource failed.",                              # 0x80060005
    2147876870: "No data.",                                                     # 0x80060006
    2147876871: "Incorrect precondition, or running environment has changed.",  # 0x80060007
    2147876872: "The version is mismatched.",                                   # 0x80060008
    2147876873: "Insufficient memory.",                                         # 0x80060009
    2147876874: "Abnormal image. Incomplete image caused by packet loss.",      # 0x8006000A
    2147876875: "Dynamically loading the dynamic link library failed.",         # 0x8006000B
    2147876876: "Algorithm error.",                                             # 0x8006000C
    2147876877: "The device is offline.",                                       # 0x8006000D
    2147876878: "No access permission for device.",                             # 0x8006000E
    2147876879: "The value exceeds range.",                                     # 0x8006000F
    2147877119: "Unknown error.",                                               # 0x800600FF
}

g_bExit = False
def work_thread(camera=0,pdata=0,nDataSize=0):
    """Основная функция, для получения изображения."""
    file_counter = 0

    while True:
        stImageData=MV3D_LP_IMAGE_DATA()
        ret=camera.MV3D_LP_GetImage(ctypes.pointer(stImageData),1000)
        if ret==0:
            #print(f"get image:nFrameNum[{stImageData.nFrameNum}],nDataLen[{stImageData.nDataLen}],nWidth[{stImageData.nWidth}],nHeight[{stImageData.nHeight}]")

            filename = f"cloud_{file_counter}"
            # Кодируем filename в байты, чтобы передать как c_char_p
            filename_bytes = filename.encode('utf-8')
            enFileType = Mv3dLpFileType.get("BMP")  # тип нужного файла

            image_saving_status=camera.MV3D_LP_SaveImage(ctypes.pointer(stImageData), 5, filename_bytes)
            error_message = error_codes.get(image_saving_status)    # Получаем описание ошибки

            file_counter += 1
            if image_saving_status==0:
                print("save image success!")
                time.sleep(5)
            else:
                show_window(f"Ошибка сохранения данных: {error_message} (Номер ошибки: {image_saving_status}).")

        if g_bExit == True:
            break


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
            devices_id += ("device: %d " % i)
            strModeName = ""

            device_model_name = ""
            for per in stDeviceList.DeviceInfo[i].chModelName:
                strModeName = strModeName + chr(per)
            device_model_name += ("device model name: %s, " % strModeName)

            strSerialNumber = ""
            for per in stDeviceList.DeviceInfo[i].chSerialNumber:
                strSerialNumber = strSerialNumber + chr(per)
            devices_serial_number = ("device SerialNumber: %s, " % strSerialNumber)

        # Create device Object
        camera=Mv3dLp()
        # количество доступных устройств 
        nConnectionNum = show_device_info_dialog(devices_id, device_model_name, devices_serial_number, number_of_devices)
        if int(nConnectionNum) >= nDeviceNum.value:
            show_window(f"Введенное значение, больше чем количество доступных устройств.")
            os.system('pause')
            sys.exit()

        # Open Device
        open_device = camera.MV3D_LP_OpenDeviceBySN(stDeviceList.DeviceInfo[int(nConnectionNum)].chSerialNumber)
        if open_device != 0:
            error_message = error_codes.get(open_device) # Получаем описание ошибки
            show_window(f"Ошибка при открытии устройства: {error_message} (Номер ошибки: {open_device}).")
            os.system('pause')
            sys.exit()

        # Start Measure
        start_measure = camera.MV3D_LP_StartMeasure()
        if start_measure != 0:
            error_message = error_codes.get(start_measure) # Получаем описание ошибки
            show_window(f"Измерение не удается: {error_message} (Номер ошибки: {start_measure}).")
            camera.MV3D_LP_CloseDevice()
            os.system('pause')
            sys.exit()


        # вызов основной функции, для получения изоброжения
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
        stop_measure = camera.MV3D_LP_StopMeasure()
        if stop_measure != 0:
            error_message = error_codes.get(stop_measure) # Получаем описание ошибки
            show_window(f"Остановить измерение не удается: {error_message} (Номер ошибки: {stop_measure}).")
            print ("stop measure fail! ret[0x%x]" % ret)
            sys.exit()

        # Close Device
        close_device = camera.MV3D_LP_CloseDevice()
        if close_device != 0:
            error_message = error_codes.get(close_device) # Получаем описание ошибки
            show_window(f"Ошибка при закрытий устройства: {error_message} (Номер ошибки: {close_device}).")
            sys.exit()

    else:
        show_window(f"Устройства для подключения, не найдены.")

        








    
