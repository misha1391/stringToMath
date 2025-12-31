from typing import List, Any
from forExpressions import *
from math import sin, cos, tan, factorial
# Делит строку на числа и операторы и возвращает их в виде списка со списками(если число) и с строками(если оператор)
def separateToVar(expression: str) -> List[Any]:
    expresSpited = expression.split()
    firstWordsOper = []
    firstWordsOper += (i.split()[0] for i in possibleOperators.keys())
    maxlen = max(len(k.split()) for k in possibleOperators) if possibleOperators else 1
    answer = []
    temp = []
    i = 0
    wasfunc = False
    isOpenedBra = False
    isCombinatory = None
    while i < len(expresSpited):
        # isOperator = False
        for L in range(maxlen, 0, -1):
            if i+L <= len(expresSpited):
                check = " ".join(expresSpited[i:i+L])
                if check in possibleOperators:
                    if check in combinat and isCombinatory == False:
                        raise Exception("Ошибка, комбинаторика была инициализирована не в начале")
                    if check in possibleFunctions:
                        wasfunc = True
                    else:
                        wasfunc = False
                    
                    if temp:
                        answer.append(temp)
                    answer.append(check)

                    if check in combinat and isCombinatory == None:
                        isCombinatory = True
                        answer.append(bracketsRev["("])
                    else:
                        isCombinatory = False
                    
                    temp = []
                    i += L
                    # isOperator = True
                    break
        else: # Выполняется блок ниже, если цикл закончился обычно(не через break)
            if isCombinatory == None:
                isCombinatory = False
            if isCombinatory:
                if expresSpited[i] == combinatSep:
                    answer.append(temp)
                    answer.append(expresSpited[i])
                    temp = []
                    i += 1
                    continue
            elif wasfunc:
                answer.append(bracketsRev["("])
                wasfunc = False
                isOpenedBra = True
            if expresSpited[i] in checkNumbers: # Если это не оператор
                if not isOpenedBra:
                    temp.append(expresSpited[i])
                else:
                    answer.append([expresSpited[i]])
                    answer.append(bracketsRev[")"])
                    isOpenedBra = False
                i += 1
            else:
                raise Exception("Ошибка, не найдено такое число/операция!(возможно опечатка) ->", expresSpited[i], "возможно в: ", expresSpited[i:i+maxlen])
        # if not isOperator:
        #     answer.append(expresSpited[i])
        #     i += 1
    if temp:
        answer.append(temp)
    if isCombinatory:
        answer.append(bracketsRev[")"])
    return answer
# Переводит строку в целое число
def strLsToInt(string: List[str]) -> int:
    if not (1 <= len(string) <= 2):
        if len(string) < 1:
            raise Exception("Ошибка, была введена пустая строка")
        else:
            raise Exception("Ошибка, числа в диапозоне 0-100 не могут содержать более 1 пробела", string)
    number = 0
    containUnits = False # Единицы
    containTens = False
    for i in string:
        if possibleNumbers.get(i) != None and not containUnits:
            num = possibleNumbers[i]
            if containTens and num == 0:
                raise Exception("Ошибка, при наличии десятков нельзя писать ноль")
            number += possibleNumbers[i]
            containUnits = True
        elif possibleTens.get(i) != None and not containTens and not containUnits:
            number += possibleTens[i]
            containTens = True
        else:
            if possibleTens.get(i) != None:
                raise Exception("Ошибка, похоже нарушена позиция цифр в строке", "полученное число:", number, "последняя цифра:", i)
            elif possibleTens.get(i) != None and containTens:
                raise Exception("Ошибка, похоже было использовано более 1 десятка", "полученное число:", number, "последняя цифра:", i)
            elif possibleNumbers.get(i) != None and containUnits:
                raise Exception("Ошибка, похоже было использовано более 1 единицы или числа в диапозоне 11-19", "полученное число:", number, "последняя цифра:", i)
            else:
                raise Exception("Неопознанная ошибка, не удалось обработать число", "полученное число:", number, "последняя цифра:", i)
    if not (0 <= number <= 100):
        if number < 0:
            raise Exception("Ошибка, число не может быть отрицательным")
        else:
            raise Exception("Ошибка, число не может больше 100")
    return number
# Переводит строку в число
def strToNum(string: List[str]) -> int | float:
    # Это условие улавливает значения для числел вида <число> внутри <число><опрация><число>
    if "и" not in string:
        return strLsToInt(string)
    else: # Это условие улавливает значения для чисел вида <число>и<число><дробная часть>
        floatMul = possibleFloats.get(string[-1])
        if floatMul == None:
            raise Exception("Ошибка, была инициализация десятичной дроби, но не указан знаменатель, или он указан не в конце")
        intPart = strLsToInt(string[:string.index("и")])
        floatPart = strLsToInt(string[string.index("и")+1:-1]) * floatMul
        floatPart = round(floatPart, 3)
        if floatPart >= 1.0:
            raise Exception("Ошибка, знаменатель оказался больше числителя", "floatPart:", floatPart)
        return intPart + floatPart
def strToOperator(string: str) -> str:
    result = possibleOperators.get(string)
    if result == None:
        if string == combinatSep:
            result = ","
        else:
            raise Exception("Ошибка, не найден оператор", string)
    return result
def strToBracket(string: str) -> str:
    result = brackets.get(string)
    if result == None:
        raise Exception("Ошибка, не найдена скобка", string)
    return result
# Переводит целое число в строку
def intToStr(number: int) -> str:
    minus = ""
    if number < 0:
        minus = "минус "
        number = abs(number)
    result = ""
    subUnit = number % 10
    subTen = (number - subUnit) % 100
    subHundred = number - subTen - subUnit
    if subTen != 10: # \ - Означает, что команда продолжается на следующей строке(к слову, после нее нельзя писать комментарии)
        result = minus+(possibleHundredsRev[subHundred]+" " if subHundred != 0 else "")+ \
            (possibleTensRev[subTen]+" " if subTen != 0 else "")+ \
            (possibleNumbersRev[subUnit] if subUnit != 0 or subHundred == subTen == 0 else "")
    else:
        result = minus+(possibleHundredsRev[subHundred]+" " if subHundred != 0 else "")+ \
            possibleNumbersRev[subTen+subUnit]
    return result
# Переводит число в строку
def numToStr(number: int | float) -> str:
    if isinstance(number, int):
        return intToStr(number)
    else:
        intPart = int(number)
        floatPart = round(number % 1, 3)
        floatMul = round(0.1**len(str(floatPart).split('.')[-1]), 3)
        result = intToStr(intPart)+" и "+intToStr(round(floatPart/floatMul, 3))+" "+possibleFloatsRev[floatMul]
        return result
# Перестановки
def permutations(items: int) -> int:
    if items < 0:
        raise Exception("Ошибка, количество перестановок не может быть отрицательным", items)
    return factorial(items)
# Размешения
def placements(items: int, places: int) -> int:
    if items < 0:
        raise Exception("Ошибка, количество предметов не может быть отрицательным", items)
    if places <= 0:
        raise Exception("Ошибка, количество мест может быть только положительным значением", places)
    if places > items:
        raise Exception("Ошибка, количество мест не может быть больше количества предметов", places, ">", items)
    answer = factorial(items)/factorial(items-places)
    return answer
# Сочетания
def combinations(items: int, places: int) -> int:
    if items < 0:
        raise Exception("Ошибка, количество предметов не может быть отрицательным", items)
    if places <= 0:
        raise Exception("Ошибка, количество мест может быть только положительным значением", places)
    if places > items:
        raise Exception("Ошибка, количество мест не может быть больше количества предметов", places, ">", items)
    answer = factorial(items)/(factorial(places)*factorial(items-places))
    return answer
def calc(expression: str, test: bool = False) -> str:
    expLs = separateToVar(expression)
    if test:
        print(expLs)
    evalStr = ""
    for i in expLs:
        evalStr += str(strToNum(i) if isinstance(i, List)
                    else strToBracket(i) if brackets.get(i) != None
                    else strToOperator(i))
    result = eval(evalStr)
    if test:
        print(result)
    return numToStr(int(result) if int(result) == round(result, 3) else result) # Перевод числа в int, если он является float без знаков после '.'
def testProgram():
    # exp = "один плюс два"
    # print(separatorPos("Что-то плюс хрень"))
    # print(separateToVar(exp, separatorPos(exp)))
    print(strToNum(["двадцать", "один"]))
    print(strToNum(["три", "и", "четырнадцать", "сотых"]))
    print(intToStr(210))
    print(numToStr(3.14159))
    print(separateToVar("двадцать два плюс одиннадцать плюс сто тридцать четыре"))
    print(calc("один плюс два умножить на минус три", True))
    print(calc("десять остаток от деления на три", True))
    print(calc("синус от пи", True))
    print(calc("скобка открывается один плюс два скобка закрывается умножить на три", True))
    print(calc("двадцать и один десятых плюс один", True))
    print(calc("синус от скобка открывается пи умножить на два минус пи скобка закрывается", True))
if __name__ == "__main__":
    # testProgram()
    print(calc("размещений из четыре по два"))
