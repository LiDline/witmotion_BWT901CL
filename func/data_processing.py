import pandas as pd
from numpy import zeros, vstack, concatenate
import bluetooth
import time
import os
import serial
import pywitmotion as wit

# Создание таблицы для записи данных
def create_table():
    df = pd.DataFrame() # Создадим таблицу, куда будем созранять все значения
    df = df.reindex(columns=['t, с', 'aX, м/с2', 'aY, м/с2', 'aZ, м/с2', 'wX, °/с', 'wY, °/с', 'wZ, °/с', 'AXA, °', 'AYA, °', 'AZA, °',])
    return df

# Считывание данных по bluetooth или usb, занесение их на график и в таблицу 
def data_capture(fig, device=['bluetooth', "00:0C:BF:0C:24:17"], x_label_size = 50):
    if device[0] == 'bluetooth':
        os.system("rfkill block bluetooth")
        os.system("rfkill unblock bluetooth")
        time.sleep(0.5)   # Иначе будет ошибка
        print('bluetooth перезапущен.')

        # set your device's address
        imu = device[1]
        
        # Create the client socket
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((imu, 1))

    elif device[0] == 'usb':
        port = '/dev/ttyUSB0'
        baud = 115400
        socket = serial.Serial(port, baud, timeout=5)

    # Создадим массивы для графиков
    aa = zeros(3)
    ww = zeros(3)
    AA = zeros(3)

    df = create_table()

    x_label_size = x_label_size # На графике будет отображаться 50 значений
    counter = 0

    print('Устройство подключено, идёт снятие данных.', 'Для завершения нажмите ctrl + C (Interrupt).')

    t_start = time.perf_counter()
    t = []

    try:
        while True:
            if device[0] == 'bluetooth':
                data = socket.recv(1024)    # Считываем один пакет данных
            elif device[0] == 'usb':
                data = socket.read(44)
                if data[1] != 81:
                    print('Второй байт != Q, я умираю.')
                    break
            # split the data into messages
            data = data.split(b'U')

            if len(data) == 5:
                a = wit.get_acceleration(data[1])
                w  = wit.get_gyro(data[2]) 
                A = wit.get_angle(data[3])
    
                if all([a is not None, w is not None, A is not None]):
                    t.append(time.perf_counter() - t_start)
                    aa = vstack((aa, a))
                    ww = vstack((ww, w))
                    AA = vstack((AA, A))
                    with fig.batch_update():  
                        # Меняем заголовки sub'ов (записываем текущие характеристики)  
                        fig.layout.annotations[0].update(
                                                    text=(f"Линейные ускорения (aX = {'{0: <4}'.format(round(a[0], 1))}, aY = {'{0: <4}'.format(round(a[1], 1))}, aZ = {'{0: <4}'.format(round(a[2], 1))})"))
                        fig.layout.annotations[1].update(
                                                    text=(f"Угловые скорости (wX = {'{0: <4}'.format(round(w[0]))}, wY = {'{0: <4}'.format(round(w[1]))}, wZ = {'{0: <4}'.format(round(w[2]))})"))
                        fig.layout.annotations[2].update(
                                                    text=(f"Углы (AX = {'{0: <5}'.format(round(A[0]))}, AY = {'{0: <5}'.format(round(A[1]))}, AZ = {'{0: <5}'.format(round(A[2]))})"))
            
                        for i in range(3):
                            fig.data[i].y = aa[:,i]
                            fig.data[i].x = t
                            fig.data[i+3].y = ww[:,i]
                            fig.data[i+3].x = t
                            fig.data[i+6].y = AA[:,i]
                            fig.data[i+6].x = t
    
                    df.loc[counter,:] = concatenate([[round(time.perf_counter() - t_start, 2)], a, w, A]) 
                    counter += 1
    
                    if len(aa) > x_label_size:  # Ограничение по отображаемым данным
                        t = t[-x_label_size:]
                        aa = aa[-x_label_size:]
                        ww = ww[-x_label_size:] 
                        AA = AA[-x_label_size:]

    except KeyboardInterrupt:
        pass           
    socket.close()
    print('Считывание завершено.')
    print(f'Состояние bluetooth компьютера: {os.system("rfkill block bluetooth")}.')

    return df   