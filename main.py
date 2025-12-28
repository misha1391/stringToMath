from typing import List
from forExpressions import *
# Возращает позицию чисел/оператора в данном выражении
def separatorPos(expression: str) -> List[int]:
    for i in possibleOperators.keys():
        pos = expression.find(i)
        if pos > 0:
            return [pos, pos+len(i)+1]
    raise Exception("Ошибка, не найден оператор")
# Делит строку на числа и оператор и возвращает их в виде строки
def separateToVar(expression: str, positions: List[int]) -> List[str]:
    num1 = expression[:(positions[0]-1)]
    oper = expression[positions[0]:(positions[1]-1)]
    num2 = expression[positions[1]:]
    return [num1, oper, num2]
# Переводит строку в число
def strToInt(string: str) -> int:
    splitedString = string.split()
    if not (1 <= len(splitedString) <= 2):
        if len(splitedString) < 1:
            raise Exception("Ошибка, была введена пустая строка")
        else:
            raise Exception("Ошибка, числа в диапозоне 0-100 не могут содержать более 1 пробела")
    number = 0
    containUnits = False # Единицы
    containTens = False
    for i in splitedString:
        if possibleNumbers.get(i) != None and not containUnits:
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
def strToOperator(string: str) -> str:
    result = possibleOperators.get(string)
    if result == None:
        raise Exception("Ошибка, не найден оператор", string)
    return result
# Переводит число в строку
def intToStr(number: int) -> str:
    result = ""
    if number // 10 == 0 or number // 10 == 1:
        result = possibleNumbersRev[number]
    else:
        subTen = number // 10 * 10
        subUnit = number % 10
        result = possibleTensRev[subTen] + " " + possibleNumbersRev[subUnit]
    return result
def calc(expression: str) -> str:
    num1, oper, num2 = separateToVar(expression, separatorPos(expression))
    result = eval(str(strToInt(num1)) + strToOperator(oper) + str(strToInt(num2)))
    return intToStr(result)
def testProgram():
    exp = "один плюс два"
    print(separatorPos("Что-то плюс хрень"))
    print(separateToVar(exp, separatorPos(exp)))
    print(strToInt("двадцать один"))
if __name__ == "__main__":
    print(calc("десять разделить на ноль"))