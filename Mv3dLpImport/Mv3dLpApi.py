# -- coding: utf-8 --
import ctypes
import os

from ctypes import *

from Mv3dLpImport.Mv3dLpDefine import MV3D_LP_DEVICE_INFO

# python3.8 and the relevant version can specify the following path for the library
os.add_dll_directory("C:\Program Files (x86)\Common Files\MV3D\Runtime\Win64_x64")
os.add_dll_directory("C:\Program Files (x86)\Common Files\Mv3dLpSDK\Runtime\Win64_x64")

Mv3dLpDll = ctypes.WinDLL("Mv3dLp.dll")

class Mv3dLp():
    def __init__(self):
        # Создается переменная для хранения дескриптора (handle) устройства. 
        # Дескриптор - это указатель на структуру данных или какой-то ресурс, используемый для доступа к объекту.
        self._handle = c_void_p()           # device handle
        # Cоздается указатель на self._handle. Это необходимо, т.к. функции DLL ожидают указатели, если они хотят изменять данные.
        self.handle = pointer(self._handle) # handle pointer

    #  @brief  Get DLL version
    #  @param  
    #  @return Return version info.Eg:1.0.0
    @staticmethod
    def MV3D_LP_GetVersion():
        Mv3dLpDll.MV3D_LP_GetVersion.restype = c_char_p
        # C: MV3D_LP_API const char# MV3D_LP_GetVersion();
        return Mv3dLpDll.MV3D_LP_GetVersion()
    
    #  @brief  Gets the number of devices in the current environment
    #  @param  pDeviceNumber               [OUT]           device number
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_GetDeviceNumber(pDeviceNumber):
        # Определяет тип входных данных функции, то есть что параметр должен быть указателем void*
        # Универсальный указатель: void* - это универсальный указатель. Он может указывать на любой тип данных: int, float, char, структуры и так далее.
        Mv3dLpDll.MV3D_LP_GetDeviceNumber.argtypes = (c_void_p,)
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_GetDeviceNumber.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_GetDeviceNumber(pDeviceNumber)

    #  @brief  Gets 3D cameras list
    #  @param  pstDeviceInfos              [IN OUT]        devices list
    #  @param  nMaxDeviceCount             [IN]            Max Number of device list caches
    #  @param  pDeviceCount                [OUT]           number of devices in the fill list
    @staticmethod
    def MV3D_LP_GetDeviceList(pstDeviceInfos, nMaxDeviceCount, pDeviceNumber):
        # Определяет тип входных данных функции,
        # указатель на всю структуру stDeviceList
        # c_uint`: Это беззнаковое целое число, которое соответствует аргументу `nMaxDeviceCount` (максимальное количество устройств).
        # c_char_p`: Это аналог `char*` из C/C++, то есть указатель на строку. Здесь это используется для передачи указателя на переменную, где будет сохранено количество найденных устройств.  Это потенциальная ошибка, так как передается указатель на беззнаковое целое число, а не на строку.
        Mv3dLpDll.MV3D_LP_GetDeviceList.argtypes = (POINTER(MV3D_LP_DEVICE_INFO), c_uint, POINTER(c_uint))
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_GetDeviceList.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_GetDeviceList(pstDeviceInfos, nMaxDeviceCount, pDeviceNumber)
    
    #  @brief  Open device by serial number 
    #  @param  handle                      [IN OUT]        device handle
    #  @param  chSN                        [IN]            serial number
    def MV3D_LP_OpenDeviceBySN(self, chSN):
        # Устанавливает типы аргументов для вызова функции из DLL.
        Mv3dLpDll.MV3D_LP_OpenDeviceBySN.argtypes = (c_void_p, c_void_p)
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_OpenDeviceBySN.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_OpenDeviceBySN(byref(self.handle), chSN)
    
    #  @brief  Start measurements
    #  @param  handle                      [IN]            device handle
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_StartMeasure(self):
        # Устанавливает типы аргументов для вызова функции из DLL.
        Mv3dLpDll.MV3D_LP_StartMeasure.argtypes = (c_void_p,)
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_StartMeasure.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_StartMeasure(self.handle)
    
    #  @brief  Get image data
    #  @param  handle                      [IN]            device handle
    #  @param  pstImageData                [IN OUT]        data set pointer
    #  @param  nTimeout                    [IN]            timevalue（Unit: ms）
    def MV3D_LP_GetImage(self, pstImageData, nTimeOut):
        # Устанавливает типы аргументов для вызова функции из DLL.
        Mv3dLpDll.MV3D_LP_GetImage.argtypes = (c_void_p, c_void_p, c_uint)
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_GetImage.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_GetImage(self.handle, pstImageData, nTimeOut)
    
    #  @brief  save image to file
    #  @brief  BMP support Mono8/C16/Rgb24
    #  @brief  JPG support C16/JPEG/Rgb24
    #  @brief  TIFF support C16/Rgb24
    #  @brief  TIFF_U16/TIFF_F32 support C16
    #  @brief  PLY/CSV/OBJ support ABC16/ABC32/ABC32f
    #  @brief  PLY_BINARY/PLY_TEXTURE support ABC32f
    #  @param  pstImage                 [IN]            image data 
    #  @param  enFileType               [IN]            file type
    #  @param  chFileName               [IN]            file name
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    @staticmethod
    def MV3D_LP_SaveImage(pstImage,enFileType,chFileName):
        # Устанавливает типы аргументов для вызова функции из DLL.
        Mv3dLpDll.MV3D_LP_SaveImage.argtypes = (c_void_p,c_int,c_char_p)
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_SaveImage.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_SaveImage(pstImage,enFileType,chFileName)
    
    #  @brief  depth image convert to pointcloud image
    #  @param  pstDepthImageData        [IN]          Depth  data
    #  @param  pstPointCloudData        [IN OUT]      Point Cloud data
    #  @return Success, return MV3D_LP_OK. Failure,return error code
    @staticmethod
    def MV3D_LP_MapDepthToPointCloud(pstDepthImageData,pstPointCloudData):
        # Устанавливает типы аргументов для вызова функции из DLL.
        Mv3dLpDll.MV3D_LP_MapDepthToPointCloud.argtypes = (c_void_p, c_void_p)
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_MapDepthToPointCloud.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_MapDepthToPointCloud(pstDepthImageData, pstPointCloudData)
    
    
    #  @brief  Stop measurements
    #  @param  handle                      [IN]            device handle
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_StopMeasure(self):
        # Устанавливает типы аргументов для вызова функции из DLL.
        Mv3dLpDll.MV3D_LP_StopMeasure.argtypes = (c_void_p,)
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_StopMeasure.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_StopMeasure(self.handle)
    
    #  @brief  Close device 
    #  @param  handle                      [IN]            device handle
    #  @return Success, return MV3D_LP_OK. Failure, return error code
    def MV3D_LP_CloseDevice(self):
        # Устанавливает типы аргументов для вызова функции из DLL.
        Mv3dLpDll.MV3D_LP_CloseDevice.argtypes = (c_void_p,)
        # Определяет тип выходных данных функции как unsigned int
        Mv3dLpDll.MV3D_LP_CloseDevice.restype = c_uint
        # Вызывает соответствующую функцию из DLL и возвращает ее результат.
        return Mv3dLpDll.MV3D_LP_CloseDevice(byref(self.handle))