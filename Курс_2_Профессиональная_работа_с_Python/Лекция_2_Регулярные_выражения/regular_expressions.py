#1. поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
#2. привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
#3. объединить все дублирующиеся записи о человеке в одну.

import csv
import re

with open("./text_storage.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

#Созданание словаря feo_plus_index, в каждой строчке файла регуляркой искать ФИО и в конце сделать словавь по примеру  key=ИНДЕКС СТРОЧКИ  val=НАЙДЕННОЕ ФИО
def feo_plus_index(contacts_list1):

    errors = 0
    feo_plus_index = {}                                       #Словарь Ключи = 'Индекс строчки списка где искала регулярка', Значение = 'Найденное регуляркой ФИО'
    for x in contacts_list1:
        u = (','.join(str(z) for z in x))
        name = re.search(r'^([А-я\d]+(?:( |,)[А-я\d]{2,}( |,)[А-я\d]{2,}))|^([А-я\d]+(?:( |,)[А-я\d]{2,}))', u)
        try:                                                       #Убрал в исключения ошибки если регулярка ничего не находит в строчке 
            key_for_dict = re.split(',| ', name.group(0))          #Сохраняю в переменную то что нашла регулярка 
            val_for_dict = contacts_list1.index(x)                 #Сохраняю в переменную индекс строчки где искала регулярка 
            feo_plus_index[val_for_dict] = key_for_dict            #Леплю словарь
        except:
            errors = errors + 1
    return feo_plus_index
# print()
# print(feo_plus_index(contacts_list))
# print()

#Функция получения словаря где key = Фамилия value = Список со всеми номерами строчек где встречается фамилия   
def create_dict_surname(feo_plus_index):

    #Создание словаря с уникальным ФИО и значением объедененных строчек
    double_string = []
    double_string2 = {}
    for x, y in feo_plus_index.items():          #x - номер строк в сроваре contacts_list, y - список с ФИО 
        for x2, y2 in feo_plus_index.items():
            if 100 - (sum(i != j for i, j in zip(y, y2)) / float(len(y))) * 100 == 100.0:  #Cложный не мой алгоритм
                if x != x2:
                    double_string.append(y[0])                                                                                             # получаю словать где одинаковые ФИО но разные строчки в основном файле 
                    double_string2[x] = y

    out_list = {}
    for x in set(double_string): 
        out_list2 = []
        for x2, y2 in double_string2.items():
            if x == y2[0]:
                out_list2.append(x2)
                out_list[x] = out_list2
        out_list2 = []

    #Словарь ключ - фамилия, значение - списко номеров строчек
    surname_for_dict = {}
    for x in feo_plus_index:
        surname_for_dict[feo_plus_index[x][0]] = x


    for x in out_list:
        surname_for_dict[x] = out_list[x]

    return surname_for_dict
# print(create_dict_surname(feo_plus_index(contacts_list)))
# print()

#Функция, объединяет все существующие строчки в которых находит поданную фамилию и делат один большой список
def create_list_str(surname):

    wow_list = []
    for x in [create_dict_surname(feo_plus_index(contacts_list))[surname]]:
        if type(x) == int:
            for x2 in contacts_list[x]:
                wow_list.append(x2)
        else:
            for x2 in x:
                for x3 in contacts_list[x2]:
                    wow_list.append(x3) 

    return wow_list
# print(create_list_str('Мартиняхин'))
# print()

#Достать фио из списка функции create_list_str
def serarc_fio(surname):
    try:
        u = ' '.join(create_list_str(surname)) 
        name = re.search(r'^([А-я\d]+(?:( |,)[А-я\d]{2,}( |,)[А-я\d]{2,}))|^([А-я\d]+(?:( |,)[А-я\d]{2,}))', u)
        return name.group(0)
    except:
        return f'Фио не указано'

#Достать Емаил из списка функции create_list_str 
def serarc_email(surname):
    try:
        u = ' '.join(create_list_str(surname)) 
        name = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}', u)
        return name.group(0)
    except:
        return f'Емал не указан'   

#Достать место работы из списка функции create_list_str 
def serarc_organiza(surname):
    return create_list_str(surname)[3]

#Достать позицию из списка функции create_list_str 
def serarc_position(surname):
    try:
        if create_list_str(surname)[4] == '':
            return create_list_str(surname)[11]
        else:
            return create_list_str(surname)[4] 
    except:
        return f'Позиция не указана'

#Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999; из списка функции create_list_str
def serarc_phone(surname):
    try: 
        u = ','.join(create_list_str(surname))
        name = re.search(r'(\+7|8)[- _]*\(?[- _]*(\d{3}[- _]*\)?([- _]*\d){7}|\d\d[- _]*\d\d[- _]*\)?([- _]*\d){6}).*', u)
        phone = name.group(0).split(',')[0]
        name = re.findall(r'[0-9]', phone)
        if len(name) > 11:
            return f"+7({''.join(name[1:4])}){''.join(name[4:10])} доб.{''.join(name[11:])}"
        else:
            return f"+7({''.join(name[1:4])}){''.join(name[4:10])}"

    except:
        return f'Телефон не найден'


#Функция финально заполняет список и добавляет этот список как строчку в новый файл csv
def info_aboute_fio(surname): 
    final_list = []
    for x in serarc_fio(surname).split():
        final_list.append(x)
    final_list.append(serarc_organiza(surname))
    final_list.append(serarc_position(surname))
    final_list.append(serarc_phone(surname))
    final_list.append(serarc_email(surname))
    print(final_list)


print()
for x in create_dict_surname(feo_plus_index(contacts_list)).keys():
    info_aboute_fio(x)






























# def serarc_phone2(phone):
#     try:
#         name = re.findall(r'[0-9]', phone)
#         return f"+7({''.join(name[1:4])}){''.join(name[4:10])} доб.{''.join(name[11:])}"
#     except:         
#         return f'что-то не так'


#print(serarc_phone2(serarc_phone('Лагунцов')))







#Регулярками найти
#1 Найти ФИО записать в список 
#2 Найти Организацию записать в список 
#3 Найти Должность записать в список
#4 Найти телефон записать в список 
#5 Найти емаил записать в список 




















#print(u)








# for x in create_dict_surname(feo_plus_index(contacts_list))['Мартиняхин']:
#     list_fio = {} 
#     #u = ''                                      
#     for x2 in contacts_list[x]:
#         u += x2 
#         #print(x2)
# print(u)


    #     name = re.search(r'^([А-я\d]+(?:( |,)[А-я\d]{2,}( |,)[А-я\d]{2,}))|^([А-я\d]+(?:( |,)[А-я\d]{2,}))', u)
    #     try:    #Убрал в исключения ошибки если регулярка ничего не находит в строчке 
    #         key_for_dict = re.split(',| ', name.group(0))          #Сохраняю в переменную то что нашла регулярка 
    #         val_for_dict = contacts_list.index(x2)                 #Сохраняю в переменную индекс строчки где искала регулярка 
    #         feo_plus_index[val_for_dict] = key_for_dict            #Леплю словарь
    #     except:
    #         errors = errors + 1
    # print(list_fio)







































































#копирую словарь для того чтобы можно было его редактировать в двойном форе 
#feo_plus_index_copy = dict(feo_plus_index)





































# for x in double_string.values


#print(feo_plus_index_copy)

# for x, y in double_string.items():
#     print(x)


#если ключ мартиняхин есть в словаре то добавить в списко индекс 
















# # print()
# # print()
# #print(double_string)        


# #Нахожу одинаковые фио и складываю все строчки в одну 

# for x, y in double_string.items():
#     print(x,y)
    
#         # if 100 - (sum(i != j for i, j in zip(y, y2)) / float(len(y))) * 100 == 100.0:











#     for x2, y2 in feo_plus_index.items():    # x2 - номер строк в сроваре contacts_list, y2 - список с ФИО
#         if 100 - (sum(i != j for i, j in zip(y, y2)) / float(len(y))) * 100 == 100.0:   #строчка черный ящик =D Сложный, не мой алгоритм сравнения строчек в списке
#             print(y)
#     #         if x != x2: 
#     #             double_string[f"{x * 2}"] = [x, x2]             
#     #             #print(y)
#     # #print(double_string.values())    


# print(double_string)


















# double_string2 = {}                
# for x, y in double_string.items():
#     for x2, y2 in double_string.items():
#         if 100 - (sum(i != j for i, j in zip(y, y2)) / float(len(y))) * 100 == 100.0:
#             #print(y)
#             if x != x2:
#                 double_string2[x] = y
#                 print(x)

# print(double_string2)


















#print(double_string)




















# double_string = {}
# for x, y in feo_plus_index.items(): # x - номер строк в сроваре contacts_list, y - список с ФИО 
#     for x2, y2 in feo_plus_index.items(): 
#         if 100 - (sum(i != j for i, j in zip(y, y2)) / float(len(y))) * 100 == 100.0:   #строчка черный ящик =D Сложный, не мой алгоритм сравнения строчек в списке
#             #print(y)
#             #if x != x2: 
#             #    double_string[x] = y









# print()
# print(double_string.keys()) #Этот словарь надо както разделить по группам 
# print(double_string)
# print()
# print(feo_plus_index)
# print()
# print(contacts_list[4])
#Объединить значения одинаковых строчек в одну новую строчку 












                #double_string[x] = (','.join(str(z) for z in y)) + (f",{','.join(str(z) for z in y2)}")
                #double_string[x2] = y2
                #print(x,feo_plus_index[x], x2,feo_plus_index[x2])
                #print(feo_plus_index[x2])
                # print(contacts_list[x])
                # print(contacts_list[x2])



# print(feo_plus_index[4])
# print(feo_plus_index[2])

#print( 100 - (sum(i != j for i, j in zip(a, b)) / float(len(a))) * 100 )


#ПОИСК ОДИНАКОВЫХ ФИО
# a = list_without_nule[2]
# print(list_without_nule[2])
# b = list_without_nule[4]
# print(list_without_nule[4])

#Сложный, не мой, алгоритм сравнения строчек в списке
#print( 100 - (sum(i != j for i, j in zip(a, b)) / float(len(a))) * 100 )













    #Создать ключ "словарь Фио" с значением "индекс всей строчки из списка "
    #Пройтись отсальными регулярками и собрать все в один списко списков 
    #Придумать как сравнивать списки 





#ПОИСК ОДИНАКОВЫХ ФИО
# a = list_without_nule[2]
# print(list_without_nule[2])
# b = list_without_nule[4]
# print(list_without_nule[4])

# #Сложный, не мой, алгоритм сравнения строчек в списке
#print( 100 - (sum(i != j for i, j in zip(a, b)) / float(len(a))) * 100 )













#print(contacts_list[1])

#print(contacts_list[1])

# u = (','.join(str(z) for z in contacts_list[1]))
# pattern = re.search(r'^([А-я\d]+(?:( |,)[А-я\d]{2,}( |,)[А-я\d]{2,}))|^([А-я\d]+(?:( |,)[А-я\d]{2,}))', u)
# print(pattern.group(0))


























    # pone = re.findall(r'(\+7|8)[- _]*\(?[- _]*(\d{3}[- _]*\)?([- _]*\d){7}|\d\d[- _]*\d\d[- _]*\)?([- _]*\d){6}).*,', u)
    # list_with_fio.append(pone)
    # email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}', u)
    # list_with_fio.append(email)
    #print(list_with_fio[0])
    #list_with_fio = []

# for x in list_with_fio[1:]:
#     print(x[0][0])
#     u = list(x[0])
#     # u2 = re.split(',| ',u)
#     # print(u2)


    # for x2 in list(x[0]):
    #     print(x2)



# # print(list(list_with_fio[1][0]))
# # #print(list(list_with_fio[8][0]))
# # # print(list_with_fio[7][0])
# # # print(list_with_fio[6][0])




































# length_dict = len(contacts_list) - 1
# print(range(length_dict))

# list_with_fio = []
# for x in contacts_list:
#     y = x[:3]
#     print(y)
#     u = (','.join(str(z) for z in y))
#     u2 = re.split(',| ', u)
#     u2.append(x[2])
#     list_with_fio.append(u2)

# list_without_nule = []    
# for x in list_with_fio:
#     list_without_nule.append(list(filter(None, x)))

#print(list_without_nule)
# for x in list_without_nule:
#     print(x)






























#print(list_with_fio)

#print(list_without_nule)





# list_with_fio = []
# for x in contacts_list:
#     y = x[:2]
#     u = (','.join(str(z) for z in y))
#     u2 = re.split(',| ',u)
#     u2.append(x[2])
#     list_with_fio.append(u2)

# list_without_nule = []    
# for x in list_with_fio:
#     list_without_nule.append(list(filter(None, x)))

# print(list_with_fio)

# print(list_without_nule)

#ПОИСК ОДИНАКОВЫХ ФИО
# a = list_without_nule[2]
# print(list_without_nule[2])
# b = list_without_nule[4]
# print(list_without_nule[4])

# #Сложный, не мой, алгоритм сравнения строчек в списке
#print( 100 - (sum(i != j for i, j in zip(a, b)) / float(len(a))) * 100 )
































































# list_with_fio = []
# for x in contacts_list:
#     u = (','.join(str(z) for z in x))
#     name = re.findall(r'^([А-я\d]+(?:( |,)[А-я\d]{2,}( |,)[А-я\d]{2,}))|^([А-я\d]+(?:( |,)[А-я\d]{2,}))', u)
#     #print(name)
#     list_with_fio.append(name)
#     # pone = re.findall(r'(\+7|8)[- _]*\(?[- _]*(\d{3}[- _]*\)?([- _]*\d){7}|\d\d[- _]*\d\d[- _]*\)?([- _]*\d){6}).*,', u)
#     # list_with_fio.append(pone)
#     # email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}', u)
#     # list_with_fio.append(email)
#     #print(list_with_fio[0])
#     #list_with_fio = []

# for x in list_with_fio[1:]:
#     print(x[0][0])
#     u = list(x[0])
#     # u2 = re.split(',| ',u)
#     # print(u2)


#     # for x2 in list(x[0]):
#     #     print(x2)



# # print(list(list_with_fio[1][0]))
# # #print(list(list_with_fio[8][0]))
# # # print(list_with_fio[7][0])
# # # print(list_with_fio[6][0])































#Найти имена 
#^([А-я\d]+(?:( |,)[А-я\d]{2,}( |,)[А-я\d]{2,}))|^([А-я\d]+(?:( |,)[А-я\d]{2,}))

#Найти емаил
#[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}

#Найти телефон 
#(\+7|8)[- _]*\(?[- _]*(\d{3}[- _]*\)?([- _]*\d){7}|\d\d[- _]*\d\d[- _]*\)?([- _]*\d){6}).*,























# list_with_fio = []
# for x in contacts_list:
#     y = x[:4]
#     #print(x[4])
#     u = (','.join(str(z) for z in y))
#     #print(u)
#     u2 = re.split(',| ',u)
#     u2.append(x[4])
#     u2.append(x[5])
#     u2.append(x[6])

#     list_with_fio.append(u2)


# list_without_nule = []    
# for x in list_with_fio:
#     list_without_nule.append(list(filter(None, x)))

# #print(list_without_nule)

# for x in list_without_nule:
#     print(x)





















# list_with_fio = []
# for x in contacts_list:
#     y = x[:3]
#     #print(x[4])
#     u = (','.join(str(z) for z in y))
#     #print(u)
#     u2 = re.split(',| ',u)
#     u2.append(x[2])
#     # u2.append(x[5])
#     # u2.append(x[6])

#     list_with_fio.append(u2)


# list_without_nule = []    
# for x in list_with_fio:
#     list_without_nule.append(list(filter(None, x)))

# #print(list_without_nule)

# for x in list_without_nule:
#     print(x)





