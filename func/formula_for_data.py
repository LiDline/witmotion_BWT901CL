# Вся инфа: https://github.com/WITMOTION/BWT901CL/blob/master/BWT901CL%20Datasheet.pdf
# Вычисляем характеристики исходя из второго байта [Q, R, S] - ускорение, угловая скорость, угол

def formula_for_data(number, file):       # Принимаем 16-тиричное и файл
        num1 = int.from_bytes(file.read(2), byteorder='little', signed = True)  # little - см. стр 13 шапку таблицы
        num2 = int.from_bytes(file.read(2), byteorder='little', signed = True)  # На одну характеристику идёт 2 байта
        num3 = int.from_bytes(file.read(2), byteorder='little', signed = True)
        
        di = {'51' : [num1 / 32768 * 2, 
                        num2 / 32768 * 2, 
                        num3 / 32768 * 2],
                '52' :  [num1 / 32768 * 2000, 
                        num2 / 32768 * 2000, 
                        num3 / 32768 * 2000],
                '53' : [num1 / 32768 * 180, 
                        num2 / 32768 * 180, 
                        num3 / 32768 * 180]}
        return di.get(number, None)