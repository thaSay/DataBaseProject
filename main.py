from db_importing import import_from_db
from sql_parsing import parse_sql
from table_management import execute_statement


project_name = 'Prime SGBD'

print('Running {0}...'.format(project_name))
print('Type \'help\' for command options.\n')

in_str = input('> ')
while in_str :
    in_list = in_str.split()
    if in_list[0] == 'help' :
        print('help *: List all available commands.')
        print('quit *: Quit the application.')
        print('import <server> <user> <password> <database>: Import tables from database.')
        print('sql <statement>: Execute SQL statement.')
    elif in_list[0] == 'quit' :
        break
    elif in_list[0] == 'import' :
        try :
            import_from_db(in_list[1], in_list[2], in_list[3], in_list[4])
        except Exception :
            print('Error: could not import!')
    elif in_list[0] == 'sql' :
        try :
            parsed_statement = parse_sql(in_str[4:])
            if parsed_statement[0] == 'ERROR' :
                print('Error: could not parse!')
            else :
                try :
                    execute_statement(parsed_statement)
                except Exception :
                    print('Error: could not execute!')
        except Exception :
            print('Error: could not parse!')
    else :
        print('Unknown command.')

    print()
    in_str = input('> ')

print('Shutting {0}...\n'.format(project_name))
