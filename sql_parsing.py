def parse_sql(in_str) :
    # pre-format string literals and comma-separated argument lists.
    in_str = in_str.replace('<', ' < ').replace('>', ' > ').replace('=', ' = ')
    in_list = in_str.replace(',', ' , ').replace('\'', ' \' ').replace('(', ' ( ').replace(')', ' ) ').split()
    str_formatted_list = []
    i = 0
    while i < len(in_list) :
        if in_list[i] == '\'' :
            str_list = []
            i += 1
            while i < len(in_list) and in_list[i] != '\'' :
                str_list.append(in_list[i])
                i += 1
            if i >= len(in_list) :
                return ['ERROR']
            str_formatted_list.append(' '.join(str_list))
        else :
            str_formatted_list.append(in_list[i])
        i += 1
    formatted_list = []
    i = 0
    while i < len(str_formatted_list) :
        if i+1 < len(str_formatted_list) and str_formatted_list[i+1] == ',' :
            param_list = []
            while i+1 < len(str_formatted_list) and str_formatted_list[i+1] == ',' :
                param_list.append(str_formatted_list[i])
                i += 2
            if i >= len(str_formatted_list) :
                return ['ERROR']
            param_list.append(str_formatted_list[i])
            formatted_list.append(param_list)
        else :
            formatted_list.append(str_formatted_list[i])
        i += 1

    # deal with each statement type separately.
    if formatted_list[0].upper() == 'SELECT' : # select:
        if type(formatted_list[1]) == list :
            p_params = formatted_list[1]
        else :
            p_params = [formatted_list[1]]
        if formatted_list[2].upper() != 'FROM' :
            return ['ERROR']
        if type(formatted_list[3]) == list :
            c_params = formatted_list[3]
        else :
            c_params = [formatted_list[3]]
        s_params = []
        if 'where' in formatted_list or 'WHERE' in formatted_list :
            if 'where' in formatted_list :
                i = formatted_list.index('where')
            else :
                i = formatted_list.index('WHERE')
            i += 1
            while i < len(formatted_list) and formatted_list[i].upper() != 'ORDER' :
                s_params.append(formatted_list[i])
                i += 1
        o_params = []
        if 'order' in formatted_list or 'ORDER' in formatted_list :
            if 'order' in formatted_list :
                i = formatted_list.index('order')
            else :
                i = formatted_list.index('ORDER')
            if i+1 >= len(formatted_list) or formatted_list[i+1].upper() != 'BY' :
                return ['ERROR']
            if i+3 < len(formatted_list) and formatted_list[i+3].upper() == 'DESC' :
                o_params.append('DESC')
            else :
                o_params.append('ASC')
            if i+2 >= len(formatted_list) :
                return ['ERROR']
            if type(formatted_list[i+2]) == list :
                o_params.append(formatted_list[i+2])
            else :
                o_params.append([formatted_list[i+2]])
        return ['SELECT', p_params, c_params, s_params, o_params]
    elif formatted_list[0].upper() == 'INSERT' : # insert into:
        if formatted_list[1].upper() != 'INTO' :
            return ['ERROR']
        c_params = formatted_list[2]
        p_params = []
        i = 3
        if formatted_list[3] == '(' and formatted_list[5] == ')':
            if type(formatted_list[4]) == list :
                p_params = formatted_list[4]
            else :
                p_params = [formatted_list[4]]
            i = 6
        if formatted_list[i].upper() != 'VALUES' or formatted_list[i+1] != '(' or formatted_list[i+3] != ')' :
            return ['ERROR']
        if type(formatted_list[i+2]) == list :
            in_params = formatted_list[i+2]
        else :
            in_params = [formatted_list[i+2]]
        if p_params and len(p_params) != len(in_params):
            return ['ERROR']
        return ['INSERT INTO', c_params, p_params, in_params]
    elif formatted_list[0].upper() == 'DELETE' : # delete:
        if formatted_list[1].upper() != 'FROM' :
            return ['ERROR']
        c_params = formatted_list[2]
        s_params = []
        if 'where' in formatted_list or 'WHERE' in formatted_list :
            if 'where' in formatted_list :
                i = formatted_list.index('where')
            else :
                i = formatted_list.index('WHERE')
            i += 1
            while i < len(formatted_list) :
                s_params.append(formatted_list[i])
                i += 1
        return ['DELETE', c_params, s_params]
    elif formatted_list[0].upper() == 'UPDATE' : # update:
        c_params = formatted_list[1]
        if formatted_list[2].upper() != 'SET' :
            return ['ERROR']
        p_params = []
        i = 3
        while i < len(str_formatted_list) and str_formatted_list[i].upper() != 'WHERE' :
            param_list = []
            while i < len(str_formatted_list) and str_formatted_list[i].upper() != 'WHERE' and str_formatted_list[i] != ',':
                param_list.append(str_formatted_list[i])
                i += 1
            p_params.append(param_list)
            if (str_formatted_list[i].upper() != 'WHERE') :
                i += 1
        s_params = []
        if 'where' in formatted_list or 'WHERE' in formatted_list :
            if 'where' in formatted_list :
                i = formatted_list.index('where')
            else :
                i = formatted_list.index('WHERE')
            i += 1
            while i < len(formatted_list) :
                s_params.append(formatted_list[i])
                i += 1
        return ['UPDATE', c_params, p_params, s_params]
    else :
        return ['ERROR']
