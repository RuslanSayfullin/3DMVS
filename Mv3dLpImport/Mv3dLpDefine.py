# Mv3dLpDefine.py
from ctypes import *
from enum import Enum

class _MV3D_LP_DEVICE_INFO_(Structure):
    # промежуточный класcа, поля будут определены позже.
    # Это делается для того, чтобы избежать циклического импорта: поля структуры определяются с помощью _fields_, 
    # а в _fields_ используются уже объявленные структуры.
    pass

# Объявляет тип данных Mv3dLpIpCfgMode как целое число (c_int). Вероятно, он используется в качестве типа для перечисления (enum) конфигурации IP-адреса в структуре MV3D_LP_DEVICE_INFO
Mv3dLpIpCfgMode = c_int # enum

# Здесь определяются поля структуры _MV3D_LP_DEVICE_INFO_. Это ключевое место, где создается соответствие между структурой в C/C++ и ее представлением в Python.
# Каждый элемент - это кортеж из двух частей: Имя поля, Тип поля
# Эти поля, вероятно, соответствуют информации о подключенном устройстве (имя производителя, модель, серийный номер, IP-адрес, маска подсети и т.д.)
_MV3D_LP_DEVICE_INFO_._fields_ = [
    ('chManufacturerName', c_ubyte * 32),                     # Manufacturer
    ('chModelName', c_ubyte * 32),                            # Device model
    ('chDeviceVersion', c_ubyte * 32),                        # Device version
    ('chManufacturerSpecificInfo', c_ubyte * 48),             # The specific information about manufacturer
    ('chSerialNumber', c_ubyte * 16),                         # Device serial number
    ('chUserDefinedName', c_ubyte * 16),                      # User-defined name of device
    
    ('chMacAddress', c_ubyte * 8),                            # MAC address
    ('enIPCfgMode', Mv3dLpIpCfgMode),                         # Current IP type
    ('chCurrentIp', c_ubyte * 16),                            # Device‘s IP address
    ('chCurrentSubNetMask', c_ubyte * 16),                    # Device’s subnet mask
    ('chDefultGateWay', c_ubyte * 16),                        # Device‘s default gateway
    ('chNetExport', c_ubyte * 16),                            # Network interface IP address
    ('nDevTypeInfo', c_uint),                                 # Device type info
    ('nReserved', c_byte * 12),                               # Reserved
]

# Создает псевдоним для уже определенной структуры _MV3D_LP_DEVICE_INFO_. Это улучшает читаемость кода.
MV3D_LP_DEVICE_INFO = _MV3D_LP_DEVICE_INFO_

class _MV3D_LP_DEVICE_INFO_LIST_(Structure):
    # здесь определяется структура _MV3D_LP_DEVICE_INFO_LIST_
    pass

# Это указывает, что поле DeviceInfo является указателем на массив из 20 структур MV3D_LP_DEVICE_INFO. Это предполагает, что в системе может быть максимум 20 таких устройств.
_MV3D_LP_DEVICE_INFO_LIST_._fields_ = [
    ('DeviceInfo', MV3D_LP_DEVICE_INFO * 20),   # Device info list, max 20
]

# Создает псевдоним для уже определенной структуры _MV3D_LP_DEVICE_INFO_LIST_. Это улучшает читаемость кода.
MV3D_LP_DEVICE_INFO_LIST = _MV3D_LP_DEVICE_INFO_LIST_



# ПОЛУЧЕНИЕ ИЗОБРАЖЕНИЯ
class _MV3D_LP_IMAGE_DATA_(Structure):
    # промежуточный класcа, поля будут определены позже.
    pass

# Объявляет тип данных Mv3dLpIpCfgMode как целое число (c_int).
Mv3dLpImageType = c_int # enum

# Здесь определяются поля структуры _MV3D_LP_IMAGE_DATA_. Это ключевое место, где создается соответствие между структурой в C/C++ и ее представлением в Python.
# Каждый элемент - это кортеж из двух частей: Имя поля, Тип поля
_MV3D_LP_IMAGE_DATA_._fields_=[
    ('enImageType', Mv3dLpImageType),                      # Image type
    ('nWidth', c_uint),                                    # Image width
    ('nHeight', c_uint),                                   # Image height
    ('pData', POINTER(c_ubyte)),                           # Image data, which is outputted by the camera
    ('nDataLen', c_uint),                                  # Image data length (bytes)
    ('pIntensityData', POINTER(c_ubyte)),                  # Intensity image data, which is outputted by the camera
    ('nIntensityDataLen', c_uint),                         # Intensity image data length (bytes)
    ('nFrameNum', c_uint),                                 # Frame number, which indicates the frame sequence
    ('nTimeStamp', c_int64),                               # Timestamp uploaded by the device. It starts from 0 when the device is powered on. Refer to the device user manual for detailed rules
    ('bValid', c_int32),                                   # Image valid flag,invalid if there is packet loss
    ('fXScale', c_float),                                  # X scale
    ('fYScale', c_float),                                  # Y scale
    ('fZScale', c_float),                                  # Z scale
    ('nXOffset', c_int),                                   # X offset
    ('nYOffset', c_int),                                   # Y offset
    ('nZOffset', c_int),                                   # Z offset
    ('nReserved', c_byte * 16),                            # Reserved
]
# Создает псевдоним для уже определенной структуры _MV3D_LP_IMAGE_DATA_. Это улучшает читаемость кода.
MV3D_LP_IMAGE_DATA=_MV3D_LP_IMAGE_DATA_




# 3D点（S32） | 3D Point（F32）
class _MV3D_LP_POINT_XYZ_S32_(Structure):
    pass
_MV3D_LP_POINT_XYZ_S32_._fields_=[
    ('fX', c_float),
    ('fY', c_float),
    ('fZ', c_float),
]
MV3D_LP_POINT_XYZ_S32 = _MV3D_LP_POINT_XYZ_S32_

# PointCloud Data
class _MV3D_LP_POINTCLOUD_DATA_(Structure):
    # промежуточный класcа, поля будут определены позже.
    pass

# Здесь определяются поля структуры. Это ключевое место, где создается соответствие между структурой в C/C++ и ее представлением в Python.
# Каждый элемент - это кортеж из двух частей: Имя поля, Тип поля
_MV3D_LP_POINTCLOUD_DATA_._fields_=[
    ('pData', POINTER(_MV3D_LP_POINT_XYZ_S32_)),    # Pointcloud data
    ('nDataLen', c_uint),                           #  Pointcloud data length (bytes)
    ('nFrameNum', c_uint),                          # Frame number, which indicates the frame sequence
    ('nTimeStamp', c_int64),                        # Timestamp uploaded by the device. It starts from 0 when the device is powered on. Refer to the device user manual for detailed rules
    ('bValid', c_int32),                            # Image valid flag,invalid if there is packet loss
    ('nReserved', c_byte * 16),                     # Reserved
]

# Создает псевдоним для уже определенной структуры. Это улучшает читаемость кода.
MV3D_LP_POINTCLOUD_DATA=_MV3D_LP_POINTCLOUD_DATA_