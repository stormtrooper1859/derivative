import sys

function_name = ["ln", "sin", "cos", "tg", "ctg", "arcsin", "arctg"]
priority = [['(', ')'], ['+', '-'], ['*', '/'], ["**"]]
right_associative = ["**"]
max_priority_val = len(priority)

def getPriority(str):
    for i in range(0, max_priority_val):
        for t in priority[i]:
            if(str == t):
                return i
    return -1

def isRightAssociative(str):
    for t in right_associative:
        if(str == t):
            return True
    return False

def isFunction(str):
    for t in function_name:
        if (str == t):
            return True
    return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def main(argv):
    infile = open(argv[1], 'r')
    outfile = open(argv[2], 'w')
    instrstr = infile.readline()
    while(instrstr != ""):
        #instrstr = input()
        instr = instrstr.split()
        instrstr = infile.readline()

        outstr = list()
        operationstack = list()
        #toreversePolishNotation
        for elem in instr:
            #print(elem)
            while (elem[0] == '('):
                elem = elem[1:]
                operationstack.append('(')
            flag = True
            while(flag):
                flag = False
                flagName = ""
                for t1 in function_name:
                    if (elem.find(t1) == 0):
                        flag = True
                        flagName = t1
                if(flag):
                    operationstack.append(flagName)
                    elem.replace(flagName, "")
                    elem = elem[(len(flagName)):]
                while (elem[0] == '('):
                    elem = elem[1:]
                    operationstack.append('(')
            closebracket_count = 0
            while(elem[0] == '('):
                elem = elem[1:]
                operationstack.append('(')
            while(elem[len(elem) - 1] == ')'):
                elem = elem[:len(elem) - 1]
                closebracket_count += 1
            if(is_number(elem)):
                outstr.append(elem)
            elif(elem == 'x' or elem == 'e'):
                outstr.append(elem)
            else:
                if(len(operationstack) != 0):
                    temp = operationstack.pop()
                    while((temp != "none") and (isRightAssociative(temp) and (getPriority(elem) < getPriority(temp)))
                          or (not isRightAssociative(str) and (getPriority(elem) <= getPriority(temp)))):
                        outstr.append(temp)
                        if(len(operationstack) == 0):
                            temp = "none"
                        else:
                            temp = operationstack.pop()
                    if(temp != "none"):
                        operationstack.append(temp)
                operationstack.append(elem)
            for i in range(0, closebracket_count):
                temp = operationstack.pop()
                while (temp != '('):
                    outstr.append(temp)
                    if(len(operationstack) == 0):
                        temp = '('
                    else:
                        temp = operationstack.pop()
                        if(isFunction(temp)):
                            outstr.append(temp)
                            if (len(operationstack) == 0):
                                temp = '('
                            else:
                                temp = operationstack.pop()
                if(len(operationstack) != 0):
                    temp3 = operationstack.pop()
                    if(isFunction(temp3)):
                        outstr.append(temp3)
                    else:
                        operationstack.append(temp3)
        while(len(operationstack) != 0):
            outstr.append(operationstack.pop())

        #print(outstr)

        #getDerivative
        workStack = list()
        expressions = list()
        derivatives = list()

        expr = ""
        der = ""
        temp2 = 0
        temp1 = 0

        for elem in outstr:
            if(is_number(elem) or elem == 'e'):
                expressions.append(elem)
                derivatives.append("0")
                workStack.append(len(expressions) - 1)
            elif(elem == 'x'):
                expressions.append(elem)
                derivatives.append("1")
                workStack.append(len(expressions) - 1)
            else:
                if(isFunction(elem)):
                    if(elem == "ln"):
                        temp1 = workStack.pop()
                        expr = "ln(" + expressions[temp1] + ")"
                        der = "(1 / " + expressions[temp1] + ") * " + derivatives[temp1]
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif(elem == "sin"):
                        temp1 = workStack.pop()
                        expr = "sin(" + expressions[temp1] + ")"
                        der = "cos(" + expressions[temp1] + ") * " + derivatives[temp1]
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif (elem == "cos"):
                        temp1 = workStack.pop()
                        expr = "cos(" + expressions[temp1] + ")"
                        der = "-sin(" + expressions[temp1] + ") * " + derivatives[temp1]
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif (elem == "tg"):
                        temp1 = workStack.pop()
                        expr = "tg(" + expressions[temp1] + ")"
                        der = "(1 / cos(" + expressions[temp1] + ") ** 2) * " + derivatives[temp1]
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif (elem == "ctg"):
                        temp1 = workStack.pop()
                        expr = "ctg(" + expressions[temp1] + ")"
                        der = "(-1 / sin(" + expressions[temp1] + ") ** 2) * " + derivatives[temp1]
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif (elem == "arcsin"):
                        temp1 = workStack.pop()
                        expr = "arcsin(" + expressions[temp1] + ")"
                        der = "(1 / (1 - " + expressions[temp1] + " ** 2) ** (1 / 2)) * " + derivatives[temp1]
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif (elem == "arctg"):
                        temp1 = workStack.pop()
                        expr = "arcsin(" + expressions[temp1] + ")"
                        der = "(1 / 1 + " + expressions[temp1] + " ** 2) * " + derivatives[temp1]
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                else:
                    if(elem == '+' or elem == '-'):
                        temp2 = workStack.pop()
                        temp1 = workStack.pop()
                        expr = "(" + expressions[temp1] + " " + elem + " " + expressions[temp2] + ")"
                        der = "(" + derivatives[temp1] + " " + elem + " " + derivatives[temp2] + ")"
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif(elem == '*'):
                        temp2 = workStack.pop()
                        temp1 = workStack.pop()
                        expr = "(" + expressions[temp1] + " * " + expressions[temp2] + ")" # ?
                        der = "(" + derivatives[temp1] + " * " + expressions[temp2] + " + " + expressions[temp1] + " * " + derivatives[temp2] + ")"
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif(elem == '/'):
                        temp2 = workStack.pop()
                        temp1 = workStack.pop()
                        if(expressions[temp1] == '0'):
                            expr = 0
                            der = 0
                        else:
                            expr = "(" + expressions[temp1] + " / " + expressions[temp2] + ")"
                            der = "(" + derivatives[temp1] + " * " + expressions[temp2] + " - " + expressions[temp1] + " * " + derivatives[temp2] + ")" \
                                + " / (" + expressions[temp2] + " ** 2)"
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)
                    elif(elem == "**"):
                        temp2 = workStack.pop()
                        temp1 = workStack.pop()
                        expr = "(" + expressions[temp1] + " ** " + expressions[temp2] + ")"
                        der = "(" + expressions[temp1] + " ** " + expressions[temp2] + ") * (" + derivatives[temp1] + " / " + expressions[temp1] \
                            + " * " + expressions[temp2] + " + " + derivatives[temp2] + " * ln(" + expressions[temp1] + "))"
                        expressions.append(expr)
                        derivatives.append(der)
                        workStack.append(len(expressions) - 1)

        #print("in:")
        #print(instrstr)
        #print("answer:")
        #print(derivatives[len(derivatives) - 1])
        outfile.write(derivatives[len(derivatives) - 1])
        outfile.write('\n')
    infile.close()
    outfile.close()

if __name__ == "__main__":
    main(sys.argv)

# (x ** 2 + (x ** 4 + 1) ** (1 / 3)) / ln(x ** (x + cos(x)) + 1)