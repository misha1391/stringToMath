from typing import List, Any
from forExpressions import *
# Делит строку на числа и операторы и возвращает их в виде списка со списками(если число) и с строками(если оператор)
def separateToVar(expression: str) -> List[Any]:
    answer = []
    temp = []
    for i in expression.split():
        if i not in possibleOperators.keys():
            temp.append(i)
        else:
            answer.append(temp)
            answer.append(i)
            temp = []
    answer.append(temp)
    return answer
# Переводит строку в целое число
def strLsToInt(string: List[str]) -> int:
    if not (1 <= len(string) <= 2):
        if len(string) < 1:
            raise Exception("Ошибка, была введена пустая строка")
        else:
            raise Exception("Ошибка, числа в диапозоне 0-100 не могут содержать более 1 пробела")
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
        raise Exception("Ошибка, не найден оператор", string)
    return result
# Переводит целое число в строку
def intToStr(number: int) -> str:
    result = ""
    subUnit = number % 10
    subTen = (number - subUnit) % 100
    subHundred = number - subTen - subUnit
    if subTen != 10: # \ - Означает, что команда продолжается на следующей строке(к слову, после нее нельзя писать комментарии)
        result = (possibleHundredsRev[subHundred]+" " if subHundred != 0 else "")+ \
            (possibleTensRev[subTen]+" " if subTen != 0 else "")+ \
            (possibleNumbersRev[subUnit] if subUnit != 0 or subHundred == subTen == 0 else "")
    else:
        result = (possibleHundredsRev[subHundred]+" " if subHundred != 0 else "")+ \
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
def calc(expression: str) -> str:
    expLs = separateToVar(expression)
    evalStr = ""
    for i in expLs:
        evalStr += str(strToNum(i) if isinstance(i, List) else strToOperator(i))
    result = eval(evalStr)
    return numToStr(int(result) if int(result) == result else result)
def testProgram():
    # exp = "один плюс два"
    # print(separatorPos("Что-то плюс хрень"))
    # print(separateToVar(exp, separatorPos(exp)))
    print(strToNum("двадцать один"))
    print(strToNum("три и четырнадцать сотых"))
    print(intToStr(210))
    print(numToStr(3.14159))
    print(separateToVar("двадцать два плюс одиннадцать плюс сто тридцать четыре"))
if __name__ == "__main__":
    print(calc("один плюс два плюс три"))
    # print(calc("двадцать и один десятых плюс один"))