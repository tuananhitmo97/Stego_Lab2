from PIL import Image
import math

def string_to_binary(text):
    res = ''.join(format(ord(i), '08b') for i in text)
    return res

def binary_to_string(binary):
    str = ''
    for i in range(0, len(binary), 8):
        str += ''.join(chr(int(binary[i:i+8],2)))
    return str

def decimal_to_binary(number):
    res = []
    res = "{0:016b}".format(number)
    return res

def binary_to_decimal(binary):
    num = int(binary,2)
    return num

def data_to_list(data,lenght):
    list_data = []
    for i in range(0,lenght):
        list_data += list(data[i])
    return list_data

def data_after_change(data, mes):
    lenght_mes_bin = decimal_to_binary(len(mes))
    for i in range(0,16):
        if lenght_mes_bin[i] == '0':
            if data[i]%2 == 1:
                data[i] = data[i] - 1
        else:
            if data[i]%2 == 0:
                data[i] = data[i] + 1

    mes_bin = string_to_binary(mes)
    for i in range(0, len(mes_bin)):
        if mes_bin[i] == '0':
            if data[i+16]%2 == 1:
               data[i+16] = data[i+16] - 1
        else:
            if data[i+16]%2 == 0:
               data[i+16] = data[i+16] + 1
    return data

def read_data(data):
    lenght_mes_bin = ''
    for i in range(0,16):
        if data[i]%2 == 0:
            lenght_mes_bin += '0'
        else:
            lenght_mes_bin += '1'
    lenght_mes = binary_to_decimal(lenght_mes_bin)
    mes = ''
    for i in range(16, 16+lenght_mes*8):
        if data[i]%2 == 0:
            mes += '0'
        else:
            mes += '1'
    return mes

def secret_mes(file):
    mess = open('message.txt','r').read()
    return mess

def encrypt_file(file,mes):
    image = Image.open(file, 'r')
    new_image = image.copy()
    width, height = new_image.size

    data = data_to_list(list(new_image.getdata()),width*height)
    data = data_after_change(data,mes)

    data_of_image = []
    for i in range(0,width*height*3,3):
        data_of_image.append(tuple(data[i:i+3]))
    new_image.putdata(data_of_image)
    new_image.save('output.bmp')
    image.close()
    new_image.close()

def decrypt_file(file):
    image = Image.open(file, 'r')
    width, height = image.size
    data = data_to_list(list(image.getdata()),width*height)
    mes = binary_to_string(read_data(data))
    file_text = open('text.txt', 'w', encoding ='UTF-8')
    file_text.write(mes)
    file_text.close()
    image.close()

def PSNR(image, new_image):
    image = Image.open(image,'r')
    new_image = Image.open(new_image, 'r')
    width, height = new_image.size
    data_new = data_to_list(list(new_image.getdata()),width*height)
    data = data_to_list(list(image.getdata()),width*height)
    sum = 0
    for i in range(0,len(data_new)):
        sum += math.pow((data_new[i] - data[i]),2)
    MSE = sum/(width*height)
    PSNR = 10 * math.log((255*255/MSE),10)
    return PSNR


def attack_image(file):
    image = Image.open(file, 'r')
    new_image = image.copy()
    width, height = new_image.size
    data = data_to_list(list(new_image.getdata()),width*height)
    for i in range(0,len(data)):
        if data[i]%2 == 0:
            data[i] = 0
        else:
            data[i] = 255

    data_of_image = []
    for k in range(0,width*height*3,3):
        data_of_image.append(tuple(data[k:k+3]))
    new_image.putdata(data_of_image)

    new_image.save('attack.bmp')
    image.close()
    new_image.close()

print("Вводите файл картинки: ")
image = input()
print("Вводите скрытое сообщение: ")
mes = secret_mes('message.txt')
print(mes)
encrypt_file(image,mes)
print("Вводите файл новой картинки:")
new_image = input()
decrypt_file(new_image)
print("Результат вычисления PSNR:")
print(f"PSNR = {PSNR('sample.bmp','output.bmp')}")
print("Вводите файл картинки для атаки:")
file = input()
attack_image(file)
