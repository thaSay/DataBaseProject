table_dict = {}


def print_table(table) :
    max_width = [0 for i in range(len(table[0]))]
    for row in table[1:] :
        for i, value in enumerate(row) :
            max_width[i] = max(max_width[i], len(str(value)))
    table_str = ''
    for row in table[1:] :
        table_str += '| '
        for i, value in enumerate(row) :
            if value == None :
                value = 'NULL'
            table_str += '{0: <{1}} |{2}'.format(value, max_width[i], ' ' if i != len(row)-1 else '\n')
    print(table_str, end='')


def cartesian_product(tables) :
    if len(tables) == 1 :
        return tables[0]
    recursive_table = cartesian_product(tables[1:])
    table = [tables[0][0]+recursive_table[0], tables[0][1]+recursive_table[1]]
    for row_l in tables[0][2:] :
        for row_r in recursive_table[2:] :
            table.append(row_l+row_r)
    return table


def parse_expression(clause) :
    if '<' in clause :
        i = clause.index('<')
        if clause[i+1] == '=' :
            return ['<=', clause[i-1], clause[i+2]]
        elif clause[i+1] == '>' :
            return ['<>', clause[i-1], clause[i+2]]
        else :
            return ['<', clause[i-1], clause[i+1]]
    elif '>' in clause :
        i = clause.index('>')
        if clause[i+1] == '=' :
            return ['>=', clause[i-1], clause[i+2]]
        else :
            return ['>', clause[i-1], clause[i+1]]
    elif '=' in clause :
        i = clause.index('=')
        return ['=', clause[i-1], clause[i+1]]
    else :
        return []

def verify_expression(table_keys, row, parsed_expression) :
    if parsed_expression[1] in table_keys :
        var_l = row[table_keys.index(parsed_expression[1])]
        if var_l == None :
            return False
        if parsed_expression[2] in table_keys :
            var_r = row[table_keys.index(parsed_expression[2])]
            if var_r == None :
                return False
        else :
            var_r = type(var_l)(parsed_expression[2])
    elif parsed_expression[2] in table_keys :
        var_r = row[table_keys.index(parsed_expression[2])]
        if var_r == None :
            return False
        var_l = type(var_r)(parsed_expression[1])
        if var_l == None :
            return False
    else :
        return False
    if parsed_expression[0] == '<=' :
        return var_l <= var_r
    elif parsed_expression[0] == '<>' :
        return var_l != var_r
    elif parsed_expression[0] == '<' :
        return var_l < var_r
    elif parsed_expression[0] == '>=' :
        return var_l >= var_r
    elif parsed_expression[0] == '>' :
        return var_l > var_r
    elif parsed_expression[0] == '=' :
        return var_l == var_r
    else :
        return False

def selection(table, clauses) :
    rows = []
    if 'or' in clauses :
        j = clauses.index('or')
        expression_l = parse_expression(clauses[:j])
        expression_r = parse_expression(clauses[j+1:])
        for i, row in enumerate(table[2:], 2) :
            if (verify_expression(table[1], row, expression_l) or verify_expression(table[1], row, expression_r)) :
                rows.append(i)
    elif 'and' in clauses :
        j = clauses.index('and')
        expression_l = parse_expression(clauses[:j])
        expression_r = parse_expression(clauses[j+1:])
        for i, row in enumerate(table[2:], 2) :
            if (verify_expression(table[1], row, expression_l) and verify_expression(table[1], row, expression_r)) :
                rows.append(i)
    elif clauses :
        expression = parse_expression(clauses)
        for i, row in enumerate(table[2:], 2) :
            if (verify_expression(table[1], row, expression)) :
                rows.append(i)
    else :
        for i, row in enumerate(table[2:], 2) :
            rows.append(i)
    return rows


def select(projection_list, table_list, selection_list, order) :
    table = cartesian_product(table_list)
    rows = selection(table, selection_list)
    if order :
        key_priority = []
        for key in order[1] :
            key_priority.append(table[1].index(key))
        sorting_table = []
        for row in rows :
            sorting_row = []
            for key in key_priority :
                sorting_row.append(table[row][key])
            sorting_row.append(row)
            sorting_table.append(sorting_row)
        sorting_table.sort()
        if order[0] == 'DESC' :
            sorting_table.reverse()
        row_order = []
        for row in sorting_table :
            row_order.append(row[-1])
    else :
        row_order = rows
    if projection_list[0] == '*' :
        ans = [[], table[1]]
    else :
        ans = [[], projection_list]
    key_order = []
    for key in ans[1] :
        i = table[1].index(key)
        ans[0].append(table[0][i])
        key_order.append(i)
    for row in row_order :
        ans_row = []
        for key in key_order :
            ans_row.append(table[row][key])
        ans.append(ans_row)
    print_table(ans)


def insert_into(table, key_list, value_list) :
    key_order = []
    for key in key_list :
        key_order.append(table[1].index(key))
    i = 0
    while len(key_order) < len(table[0]) :
        if (i not in key_order) :
            key_order.append(i)
        i += 1
    while len(value_list) < len(table[0]) :
        value_list.append(None)
    row = [None for i in range(len(table[0]))]
    i = 0
    while i < len(table[0]) :
        row[key_order[i]] = value_list[i]
        i += 1
    table.append(row)


def delete(table, selection_list) :
    rows = selection(table, selection_list)
    for i, row in enumerate(rows) :
        del table[row-i]


def execute_statement(parsed_statement) :
    if parsed_statement[0] == 'SELECT' :
        tables = []
        for table_key in parsed_statement[2] :
            tables.append(table_dict[table_key])
        select(parsed_statement[1], tables, parsed_statement[3], parsed_statement[4])
    if parsed_statement[0] == 'INSERT INTO' :
        insert_into(table_dict[parsed_statement[1]], parsed_statement[2], parsed_statement[3])
    if parsed_statement[0] == 'DELETE' :
        delete(table_dict[parsed_statement[1]], parsed_statement[2])
