import sys

function_name = ["ln", "sin", "cos", "tg", "ctg", "arcsin", "arctg"]
priority = [['+', '-'], ['*', '/'], ["**"], ['(', ')']]
right_associative = ["**"]
max_priority_val = len(priority)

ml = ["ln", "sin", "cos", "tg", "ctg", "arcsin", "arctg", '(', ')', '+', '-', '**', '/', "*"]


def to_list(in_str):
    if in_str == '':
        return list()
    for prt in ml:
        tmp = in_str.partition(prt)
        if tmp[1] != '':
            answer = list()
            answer.extend(to_list(tmp[0]))
            answer.append(tmp[1])
            answer.extend(to_list(tmp[2]))
            return answer
    return [in_str]


def get_priority(in_str):
    for i in range(0, max_priority_val):
        for t in priority[i]:
            if in_str == t:
                return i
    return -1


def is_right_associative(in_str):
    for t in right_associative:
        if in_str == t:
            return True
    return False


def is_function(in_str):
    for t in function_name:
        if in_str == t:
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
    instr = infile.readline().strip()
    while instr != "":
        in_list = instr.replace(' ', '')
        in_list = to_list(in_list)
        instr = infile.readline().strip()
        rpn_list = list()
        operation_stack = list()

        # to reverse Polish Notation
        for elem in in_list:
            if elem == '(':
                operation_stack.append('(')
            elif elem == ')':
                temp = operation_stack.pop()
                while temp != '(':
                    rpn_list.append(temp)
                    temp = operation_stack.pop()
                if len(operation_stack) != 0:
                    temp3 = operation_stack.pop()
                    if is_function(temp3):
                        rpn_list.append(temp3)
                    else:
                        operation_stack.append(temp3)
            elif is_number(elem):
                rpn_list.append(elem)
            elif elem == 'x' or elem == 'e':
                rpn_list.append(elem)
            elif is_function(elem):
                operation_stack.append(elem)
            else:
                if len(operation_stack) != 0:
                    temp2 = operation_stack.pop()
                    while((temp2 != 'none' and temp2 != '(')
                          and ((is_right_associative(temp2) and (get_priority(elem) < get_priority(temp2)))
                               or (not is_right_associative(temp2) and (get_priority(elem) <= get_priority(temp2))))):
                        rpn_list.append(temp2)
                        if len(operation_stack) == 0:
                            temp2 = 'none'
                        else:
                            temp2 = operation_stack.pop()
                    if temp2 != "none":
                        operation_stack.append(temp2)
                operation_stack.append(elem)
            # print(rpn_list)
            # print(operation_stack)
            # print("-" * 5)
        while len(operation_stack) != 0:
            rpn_list.append(operation_stack.pop())

        # print(rpn_list)

        # get Derivative
        work_stack = list()
        expressions = list()
        derivatives = list()
        expr = ""
        der = ""
        for elem in rpn_list:
            if is_number(elem) or elem == 'e':
                expressions.append(elem)
                derivatives.append("0")
                work_stack.append(len(expressions) - 1)
            elif elem == 'x':
                expressions.append(elem)
                derivatives.append("1")
                work_stack.append(len(expressions) - 1)
            else:
                if is_function(elem):
                    temp1 = work_stack.pop()
                    if elem == "ln":
                        expr = "ln(" + expressions[temp1] + ")"
                        der = "(1 / " + expressions[temp1] + ") * " + derivatives[temp1]
                    elif elem == "sin":
                        expr = "sin(" + expressions[temp1] + ")"
                        if derivatives[temp1] == "0":
                            der = "0"
                        else:
                            der = "cos(" + expressions[temp1] + ") * " + derivatives[temp1]
                    elif elem == "cos":
                        expr = "cos(" + expressions[temp1] + ")"
                        if derivatives[temp1] == "0":
                            der = "0"
                        else:
                            der = "-sin(" + expressions[temp1] + ") * " + derivatives[temp1]
                    elif elem == "tg":
                        expr = "tg(" + expressions[temp1] + ")"
                        der = "(1 / cos(" + expressions[temp1] + ") ** 2) * " + derivatives[temp1]
                    elif elem == "ctg":
                        expr = "ctg(" + expressions[temp1] + ")"
                        der = "(-1 / sin(" + expressions[temp1] + ") ** 2) * " + derivatives[temp1]
                    elif elem == "arcsin":
                        expr = "arcsin(" + expressions[temp1] + ")"
                        der = "(1 / (1 - " + expressions[temp1] + " ** 2) ** (1 / 2)) * " + derivatives[temp1]
                    elif elem == "arctg":
                        expr = "arcsin(" + expressions[temp1] + ")"
                        der = "(1 / 1 + " + expressions[temp1] + " ** 2) * " + derivatives[temp1]
                else:
                    temp2 = work_stack.pop()
                    temp1 = work_stack.pop()
                    if elem == '+' or elem == '-':
                        if is_number(expressions[temp1]) and is_number(expressions[temp2]):
                            der = str(0)
                            expr = str(float(expressions[temp1]) + (float(expressions[temp2]) if elem == "+"
                                                                    else -float(expressions[temp2])))
                        else:
                            expr = "(" + expressions[temp1] + " " + elem + " " + expressions[temp2] + ")"
                            der = "(" + derivatives[temp1] + " " + elem + " " + derivatives[temp2] + ")"
                    elif elem == '*':
                        expr = "(" + expressions[temp1] + " * " + expressions[temp2] + ")"
                        der = "(" + derivatives[temp1] + " * " + expressions[temp2] + " + " + expressions[temp1]\
                              + " * " + derivatives[temp2] + ")"
                    elif elem == '/':
                        if expressions[temp1] == '0':
                            expr = '0'
                            der = '0'
                        else:
                            expr = "(" + expressions[temp1] + " / " + expressions[temp2] + ")"
                            der = "(" + derivatives[temp1] + " * " + expressions[temp2] + " - " + expressions[temp1]\
                                  + " * " + derivatives[temp2] + ")" \
                                + " / (" + expressions[temp2] + " ** 2)"
                    elif elem == "**":
                        expr = "(" + expressions[temp1] + " ** " + expressions[temp2] + ")"
                        tmp = list()
                        if derivatives[temp1] != '0':
                            tmp.append(derivatives[temp1] + " / " + expressions[temp1] + " * " + expressions[temp2])
                        if derivatives[temp2] != '0':
                            tmp.append(derivatives[temp2] + " * ln(" + expressions[temp1] + ")")
                        if len(tmp) == 0:
                            der = '0'
                        else:
                            der = "(" + expressions[temp1] + " ** " + expressions[temp2] + ") * ("\
                                  + " + ".join(tmp) + ")"
                expressions.append(expr)
                derivatives.append(der)
                work_stack.append(len(expressions) - 1)

        outfile.write(derivatives[len(derivatives) - 1])
        outfile.write('\n')
    infile.close()
    outfile.close()

if __name__ == "__main__":
    main(sys.argv)

# (x ** 2 + (x ** 4 + 1) ** (1 / 3)) / ln(x ** (x + cos(x)) + 1)
