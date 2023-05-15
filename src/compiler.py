import os,sys
import time
import dlex
import ply.yacc as yacc
import logging

tokens = dlex.tokens
data_size = {'int':4,'char':1,'float':4,'double':8,'long':8,'short':2 }
count = 0
states = 0
offset = 0
lineno = 1

class SymbolTable(object):
    def __init__(self, data):
        self.data = data
        self.father = None
        self.childTables = []
        self.attributes = {}

    def AppendNewTable(self, my_object):
        self.childTables.append(my_object)
        my_object.father = self

    def AppendNewVariable(self, my_object, data_type, size=0):
        if my_object in self.attributes:
            return False
        else:
            self.attributes[my_object] = {}
            self.attributes[my_object]['name'] = my_object
            self.attributes[my_object]['type'] = data_type
            self.attributes[my_object]['size'] = size
            self.attributes[my_object]['offset'] = ''
            return True


class NewNode(object):
    def __init__(self, Nodeinfo):
        self.data = Nodeinfo
        self.TAC = ""
        self.place = ""
        self.type = ""

tableNo = 1
globalScope = SymbolTable('Global_Vars')
currentScope = globalScope
i = 0

# def printTable(obj):

#     print("\nPrinting table", obj.data)
#     for j in obj.attributes:
#         print(j, ':', obj.attributes[j])
#     print("Children of", obj.data, ":",)
#     flag = False
#     for i in obj.childTables:
#         flag = True
#         print(i.data,)
#     if(not flag):
#         print("No child\n")
#     else:
#         print(" ")
#     for i in obj.childTables:
#         printTable(i)


#--------------------yacc grammer rule for d programming langugage-------#



def p_startProgram(p):
    ''' Program : LIST_OF_STATEMENTS
                '''
    p[0] = p[1]
    p[0].TAC = p[1].TAC
    print(p[0].TAC)
    # global globalScope
    # printTable(globalScope)
    
def p_LIST_OF_STATEMENTS(p):
    ''' LIST_OF_STATEMENTS : LIST_OF_STATEMENTS STATEMENT
                        | STATEMENT
                        '''
    if(len(p)== 3):
        p[0] = NewNode('STATEMENTS1')
        p[0].TAC = p[1].TAC + p[2].TAC
    else:
        p[0] = p[1]
        p[0].TAC = p[1].TAC

def p_STATEMENT(p):
    ''' STATEMENT : EXPRESSION_STATEMENT                    
                    | DECISION_STATEMENT
                    | LOOP_STATEMENT
                    | RETURN_STATEMENT
                    | BREAK_STATEMENT 
                    | VARIABLE_DECLARATION
                    | FUNCTION_DECL
                    | VARIABLE_DEF
                    | TEMPLATES
                                       
                    '''
    p[0] = p[1]
    p[0].TAC = p[1].TAC


#----------------------------------------------------------------
s = 0

def p_FUNCTION_DECL(p):
    ''' FUNCTION_DECL : VARIABLE_TYPE IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR  LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        | VARIABLE_TYPE IDENTIFIER LEFTPAR  RIGHTPAR  LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES                                                    
                        | VARIABLE_TYPE IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR NOTHROW STATEMENT  
                        | REF VARIABLE_TYPE IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR STATEMENT 
                        | AUTO IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR STATEMENT   
                        | VARIABLE_TYPE IDENTIFIER LEFTPAR VARIABLE_TYPE IDENTIFIER COMMA DOT DOT DOT RIGHTPAR STATEMENT  
                '''                
    if(len(p) == 9 ):
        p[0] = NewNode('FUNCTION_DECL')

        global globalScope, currentScope
        if not globalScope != currentScope:
                print("Error!! at line:", p.lexer.lineno," ", p[2] ," cant be declare here")
                sys.exit()
        else:
            new_var = currentScope.AppendNewVariable(p[2], p[1] ,-1)
            if not new_var:
                print("Error!! at line:",p.lexer.lineno," Multiple declaration for function ", p[2])
                sys.exit()
        # a = p[7].TAC
        # print('sasds', p[4].TAC)
        p[0].TAC = "\n" + p[2] + "_begin: " + "\n" + p[4].TAC + "\n" + p[7].TAC + "\nreturn;\n\n"


    elif(len(p)==8):
        if(1==2):
            i = 0
        elif(1==5):
            i = 0
        else:
            p[0] = NewNode('FUNCTION_DECL2')
            global globalScope, currentScope
            if not (globalScope == currentScope):
                print("Error!! : at line:", p.lexer.lineno, " ", p[2] ," can't be declared here")
                sys.exit()
            else:
                new_var = currentScope.AppendNewVariable(p[2], p[1].data,-1)
                if(not new_var):
                    print("Error!! at line:",p.lexer.lineno," Multiple declaration for function: ", p[2])
                    sys.exit()
            p[0].TAC = "\n" + p[2] + "_begin:\n" + p[6].TAC + "\nreturn;\n\n"

    elif(len(p) == 7 ):
        if(p[1]!= 'AUTO' ):
            i = 0
    else:
        i = 0

    global s
    s = 0

def p_FUNCTION_DECL2(p):
    ''' FUNCTION_DECL :  IDENTIFIER LEFTPAR LIST_OF_PARAMETERS RIGHTPAR  LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        | IDENTIFIER LEFTPAR RIGHTPAR  LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES                        
                    '''
    if(len(p)==8):                    
        p[0] = NewNode('FUNCTION_DECL')
        global globalScope, currentScope
        if not (currentScope == globalScope):
            print("Error!! : at line:", p.lexer.lineno," ", p[1], " cant be declare here")
        else:
            new_var = currentScope.AppendNewVariable(p[1], 'void',-1)
            if(not new_var):
                print("Error!! at line:",p.lexer.lineno," Multiple declaration for function ", p[1])
                sys.exit()
        p[0].TAC = "\n" + p[1] + "_begin:\n " + p[3].TAC + "\n" + p[6].TAC + "\nreturn;\n\n"
        global s
        s+=1
    else:
        p[0] = NewNode('FUNCTION_DECL3')
        global globalScope, currentScope
        if not (globalScope == currentScope):
            print("Error!! : at line:", p.lexer.lineno, " ", p[1], " cant be declare here" )
        else:
            new_var = currentScope.AppendNewVariable(p[1], 'void',-1)
            if(not new_var):
                print("Error!! at line:",p.lexer.lineno, " Multiple declaration for function: ", p[1])
                sys.exit()
        p[0].TAC = "\n" + p[1] + "_begin:\n" + p[5].TAC + "\nreturn;\n\n"

def p_LIST_OF_PARAMETERS (p):
    ''' LIST_OF_PARAMETERS : VARIABLE_TYPE IDENTIFIER COMMA LIST_OF_PARAMETERS
                    | VARIABLE_TYPE IDENTIFIER
                    '''
    if(len(p)==3):
        p[0] = NewNode('PARAMETERS1')
        global s
        s+=1
        p[0].TAC =  "_param"+ str(s) +" " + p[2]

    elif(len(p)==5):
        global s
        s+=1

        p[0] = NewNode('PARAMETERS2')
        p[0].TAC = "_param"+ str(s) +" " + p[2]  + " \n " + p[4].TAC             
 
# def p_PARAMETER_TYPE (p):
#     ''' PARAMETER_TYPE : VARIABLE_TYPE IDENTIFIER
#                         | VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER
#                         | REF VARIABLE_TYPE IDENTIFIER
#                         | REF VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
#                         | IMMUTABLE VARIABLE_TYPE IDENTIFIER
#                         | IMMUTABLE VARIABLE_TYPE LEFTBRACKET RIGHTBRACKET IDENTIFIER 
                        
#                         '''

def p_TEMPLATES(p):
    ''' TEMPLATES : VARIABLE_TYPE IDENTIFIER LEFTPAR TEMP_PARAMETERS_TYPE RIGHTPAR LEFTPAR LIST_OF_TEMP_PARAMETERS RIGHTPAR  STATEMENT
    '''

def p_TEMP_PARAMETERS_TYPE(p):
    ''' TEMP_PARAMETERS_TYPE : TEMP_PARAMETERS_TYPE COMMA IDENTIFIER
                    | IDENTIFIER
                    '''


def p_LIST_OF_TEMP_PARAMETERS(p):
    ''' LIST_OF_TEMP_PARAMETERS : LIST_OF_TEMP_PARAMETERS COMMA IDENTIFIER IDENTIFIER
                    | IDENTIFIER IDENTIFIER
    '''

########## RULE STILL REMAINING ########################

def p_EXPRESSION_STATEMENT(p):
    ''' EXPRESSION_STATEMENT : EXPRESSION SEMICOLON

                        '''
    p[0] = NewNode('EXPRESSION_STATEMENT')
    p[0].TAC = p[1].TAC                         



def p_DECISION_STATEMENT (p):
    '''DECISION_STATEMENT : IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        | IF LEFTPAR SIMPLE_EXPRESSION RIGHTPAR LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES ELSE LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        '''
# RIGHT NOW BRACES IS MUST FOR BOTH IF AND ELSE
    if(len(p)==8):

        p[0] =NewNode('DECISION_STATEMENT')
        global states
        states += 1
        p[0].TAC = p[3].TAC + "s = " + p[3].place + ";\n"
        p[0].TAC += "if s > 0 goto state_" + str(states) + ";" 
        p[0].TAC += "\nstate_" + str(states) + ":\n" + p[6].TAC + "\nstate_" + str(states+1) + ":\n"
        states += 1
        # p[0].next = 'state_' + str(states)

    elif(len(p)==12):

        p[0] =NewNode('DECISION_STATEMENT2')
        global states
        states += 1
        p[0].TAC = p[3].TAC + "s = " + p[3].place + ";\n"
        p[0].TAC += "if s > 0 goto state_" + str(states) + ";\n" 
        p[0].TAC += p[10].TAC + "\ngoto state_" + str(states+1) +";\n"
        p[0].TAC += "\nstate_" + str(states) + ":\n" + p[6].TAC + "\nstate_" + str(states+1) + ":\n"
        states += 1
        # p[0].next = 'state_' + str(states)

def p_LOOP_STATEMENT(p):
    '''LOOP_STATEMENT : FOR_LOOP
                        | WHILE_LOOP
                        '''
    p[0] = p[1]
    p[0].TAC = p[1].TAC

def p_FOR_LOOP(p):
    '''FOR_LOOP :       FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR STATEMENT
                        | FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES                        
                        '''                      
    global states                        
    if(len(p)==10):
        p[0] = NewNode('FOR_LOOP1')                 
        states += 1
        p[0].TAC = p[3].TAC + "\nstate_" + str(states) + ":\n" + p[5].TAC + "s = " + p[5].place + ";\n"
        p[0].TAC += "if s > 0 goto state_" + str(states+1) + ";\ngoto state_" + str(states+2) + ";\n" 
        states += 1
        p[0].TAC += "\nstate_" + str(states) + ":\n"+ p[9].TAC + "\n" + p[7].TAC + "\ngoto state_" + str(states-1) + ";\n"
        p[0].TAC += "\nstate_" + str(states+1) + ":\n"
        states += 1

    elif(len(p)==12):
        p[0] = NewNode('FOR_LOOP2')        
        states += 1
        p[0].TAC = p[3].TAC + "\nstate_" + str(states) + ":\n" + p[5].TAC + "s = " + p[5].place + ";\n"
        p[0].TAC += "if s > 0 goto state_" + str(states+1) + ";\ngoto state_" + str(states+2) + ";\n" 
        states += 1
        p[0].TAC += "\nstate_" + str(states) + ":\n"+ p[10].TAC + "\n" + p[7].TAC + "\ngoto state_" + str(states-1) + ";\n" 
        p[0].TAC += "\nstate_" + str(states+1) + ":\n"
        states += 1

# def p_FOR_LOOP2(p):
#     '''FOR_LOOP :  FOR LEFTPAR EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHTPAR SEMICOLON                                  
#                         '''                      
                          
#     p[0] = NewNode('FOR_LOOP3')
#     global states
#     states += 1
#     p[0].TAC = "\nstate_" + str(states) + ":\n" + p[7].TAC + "\ngoto state_" + str(states+1) + ";\n"
#     states += 1
#     p[0].TAC += p[3].TAC + "\ngoto state_"+ str(states) + ";\nstate_" + str(states) + ":\n"  + "\nif" + p[5].TAC + "\n" + "\ngoto state_" + str(states-1) + ";\ngoto " + str(p[3].next) + ";\n" 


def p_WHILE_LOOP(p):
    ''' WHILE_LOOP :     WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR STATEMENT
                        | WHILE LEFTPAR SIMPLE_EXPRESSION RIGHTPAR LEFTBRACES LIST_OF_STATEMENTS RIGHTBRACES
                        '''
    if(len(p)== 6):
        p[0] = NewNode('WHILE_LOOP1')
        global states
        states += 1
        p[0].TAC = "\nstate_" + str(states) +":" + p[3].TAC + "\ns = " + p[3].place + ";\n"
        p[0].TAC += "if s > 0 goto state_" + str(states+1) + ";\ngoto state_" + str(states+2) + ";\n"
        states += 1
        p[0].TAC += "\nstate_" + str(states) + ":" + p[5].TAC + "\ngoto state_" + str(states-1) + ";\n"
        p[0].TAC += "state_" + str(states+1) + ":\n"
        states += 1

    elif(len(p)== 8):
        p[0] = NewNode('WHILE_LOOP2')
        global states
        states += 1
        p[0].TAC = "\nstate_" + str(states) +":" + p[3].TAC + "\ns = " + p[3].place + ";\n"
        p[0].TAC += "if s > 0 goto state_" + str(states+1) + ";\ngoto state_" + str(states+2) + ";\n"
        states += 1
        p[0].TAC += "\nstate_" + str(states) + ":" + p[6].TAC + "\ngoto state_" + str(states-1) + ";"
        p[0].TAC += "\n" + "\nstate_" + str(states+1) + ":\n"
        states += 1



#---------------------------------------------------------------

def p_VARIABLE_DEF(p):
    ''' VARIABLE_DEF : ENUM ENUM_VARIABLE_TYPE LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES SEMICOLON
                            | ENUM COLON STRING_CONSTANT LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES 
                            | ENUM LEFTBRACES LISTOF_VAR_DECLARATIONS RIGHTBRACES
                        '''

def p_ENUM_VARIABLE_TYPE(p):
    ''' ENUM_VARIABLE_TYPE : ENUM
                        '''

def p_VARIABLE_DECLARATION(p):
    ''' VARIABLE_DECLARATION : VARIABLE_TYPE LISTOF_VAR_DECLARATIONS SEMICOLON
        '''
    p[0] = NewNode('VARIABLE_DECLARATION')    
    global currentScope
    global offset
    for i in currentScope.attributes:        
        if(currentScope.attributes[i]['type']==''):
            currentScope.attributes[i]['type'] = p[1].data
        if(currentScope.attributes[i]['offset']==''):
            currentScope.attributes[i]['offset'] = offset
            
            if(currentScope.attributes[i]['size']!= 0 and currentScope.attributes[i]['size'] != -1):
                offset += data_size[p[1].data] *   currentScope.attributes[i]['size']

            elif not currentScope.attributes[i]['size']==-1:
                offset += data_size[p[1].data]

            
        # print('ss ', currentScope.attributes[i])
    p[0].TAC =  p[2].TAC

    # p[0].type = p[1].type


def p_LISTOF_VAR_DECLARATIONS(p):
    ''' LISTOF_VAR_DECLARATIONS : VAR_DECLARATION_ID COMMA LISTOF_VAR_DECLARATIONS 
                    | VAR_DECLARATION_ID
                    '''
    if(len(p)==4):
        p[0] = NewNode('LISTOF_VAR_DECLARATIONS')
        p[0].TAC = p[3].TAC
  
    elif(len(p)==2):
        p[0] = p[1]
        p[0].TAC = p[1].TAC


def p_LISTOF_VAR_DECLARATIONS2(p):
    ''' LISTOF_VAR_DECLARATIONS : VAR_DECLARATION_ID EQUALS EXPRESSION COMMA LISTOF_VAR_DECLARATIONS
                    | VAR_DECLARATION_ID EQUALS EXPRESSION
                    '''
    if(len(p)==6):
        p[0] = NewNode('LISTOF_VAR_DECLARATIONS2')
        p[0].TAC = p[3].TAC + "\ns1 = " + p[3].place + ";\n" + p[1].place+ " = s1;\n" + p[5].TAC + "\n"

    elif(len(p)==4):
        p[0] = NewNode(p[2])
        p[0].TAC = p[3].TAC + "\ns1 = " + p[3].place + ";\n" + p[1].place+ " = s1;\n"


def p_VAR_DECLARATION_ID(p):
    ''' VAR_DECLARATION_ID : IDENTIFIER
                    | IDENTIFIER LEFTBRACKET INT_CONST RIGHTBRACKET
                    | IDENTIFIER LEFTBRACKET INT_CONST RIGHTBRACKET LEFTBRACKET INT_CONST RIGHTBRACKET
                    | LEFTBRACKET INT_CONST RIGHTBRACKET IDENTIFIER LEFTBRACKET INT_CONST RIGHTBRACKET   
                    | LEFTBRACKET INT_CONST RIGHTBRACKET LEFTBRACKET INT_CONST RIGHTBRACKET IDENTIFIER
                    
                    '''         #inp[string] array1;
#  SEE IF NEEED OF NewNode(VAR_DE)
    global currentScope
    if(len(p) == 2 ):
        # print('sahil  ', p[1])
        new_var = currentScope.AppendNewVariable(p[1], '')
        # print('sasadad ' , new_var )
        if(not new_var):
            print("Error!! at line:", p.lexer.lineno, "  Multiple declaration for variable ", p[1])
            sys.exit()
        p[0] = NewNode(p[1])
        p[0].TAC = ""
        p[0].place = p[1][0]

        #print(p[1])
    elif(len(p) == 5):
        p[0] = NewNode('VAR_DECLARATION_ID2')

        # print(p[3].data)
        new_var = currentScope.AppendNewVariable(p[1], '', int( p[3].data))
        if(not new_var):
            print("Error!! at line:", p.lexer.lineno, " Multiple declaration for variable ", p[1])
            sys.exit()
        global count
        count += 1
        new_var = "_t" + str(count)

        p[0].TAC = p[3].TAC + "\n"
        p[0].place = p[1] + "[" +  new_var + "]"


# DYNAMIC ARRAY NOT SUPPORTED
    else:
        p[0] = NewNode('VAR_DECLARATION_ID3')

        # elif(p[4]=='LEFTBRACKET'):      #a[1][1]  [1]a[2] [1][2]a

        # else:
            
                    
def p_VARIABLE_TYPE (p):
    ''' VARIABLE_TYPE : INT 
                      | FLOAT
                      | CHAR
                      | BOOL
                      | LONG                      
                      | DOUBLE
                      | VOID
                      | SHORT
                      '''
    p[0] = NewNode(p[1])
    p[0].TAC = ''
    p[0].place = p[1]

def p_RETURN_STATEMENT(p):
    '''RETURN_STATEMENT : RETURN EXPRESSION SEMICOLON
                    | RETURN SEMICOLON
                    '''
    if(len(p)==3):                    
        p[0] = NewNode('RETURN_STATEMENT1')    
        p[0].TAC = 'return ' + ";\n"                    
    else:
        p[0] = NewNode('RETURN_STATEMENT2')
        p[0].TAC = p[2].TAC + "\ns1 = " + p[2].place + ";\nreturn s1;\n"
   

def p_BREAK_STATEMENT(p):
    ''' BREAK_STATEMENT : BREAK SEMICOLON
                    '''
    p[0] = NewNode('BREAK_STATEMENT')
    p[0].TAC = 'break ' + ";\n"    


def p_EXPRESSION (p):
    ''' EXPRESSION : DATA_OBJECT EQUALS EXPRESSION
                    | DATA_OBJECT PLUS_EQUAL EXPRESSION
                    | DATA_OBJECT MINUS_EQUAL EXPRESSION
                    | DATA_OBJECT NOR_EQUAL EXPRESSION
                    | DATA_OBJECT OR_EQUAL EXPRESSION                     
                    | SIMPLE_EXPRESSION
                    | LEFTPAR EXPRESSION RIGHTPAR

                    '''
    global count                    
    if(len(p)==2):
        p[0] = p[1]
        p[0].TAC = p[1].TAC
        p[0].type = p[1].type

    elif(len(p)==4):
        p[0] = NewNode(p[2][0])
        if(p[1].type !=p[3].type):
            print("Error!! at line:", p.lexer.lineno, ' Type mismtach for ',p[2][1])
            sys.exit()
        else:
            p[0].type = p[1].type        
        if(p[2][1]=='EQUALS'):
            # print('sasadadafaaf')
            
            # p[0].TAC = p[1].TAC + p[3].TAC + "\n" + p[1].place + " = " + p[3].place + ";\n"
            p[0].TAC = p[3].TAC + "\ns1 = " + p[3].place + ";\n" + p[1].place+ " = s1;\n"
            p[0].place = p[1].place
        else:
            count += 1
            new_var = "_t" + str(count)
            p[0].TAC = p[1].TAC + p[3].TAC + "\ns1 = " + p[1].place + ";\n "
            p[0].TAC += "s2 = "+ p[3].place+ ";\n" 
            p[0].TAC += new_var + " = s1 +  s2;\n" 
            p[0].TAC += p[1].place + " = " + new_var + ";\n"
            p[0].place = new_var
    
    else:
        p[0] = NewNode(p[2])
        count += 1
        new_var = "_t" + str(count)
        p[0].TAC = p[1].TAC + p[3].TAC + "\ns1 = " + p[1].place + ";\n"
        p[0].TAC += "s2 = "+ p[3].place+ ";\n" + new_var + " = s1 +  s2;\n" 
        p[0].TAC += p[1].place + " = " + new_var + ";\n"
        p[0].place = new_var



def p_SIMPLE_EXPRESSION (p):
    ''' SIMPLE_EXPRESSION : SIMPLE_EXPRESSION AND RELATIONAL_EXPRESSION
                        | SIMPLE_EXPRESSION OR RELATIONAL_EXPRESSION   
                        | RELATIONAL_EXPRESSION
                        '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].TAC = p[1].TAC        
        p[0].type = p[1].type

    else:
        if(p[2][1]=='AND'):
            p[0] = NewNode(p[2])
            global states, count
            states += 1
            count += 1
            new_var = "_t" + str(count)
            false_cond = "\nstate_" + str(states) + ":\n" + new_var + " = 0;\n"
            p[0].TAC = p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n"
            p[0].TAC += "s2 = " + p[3].place + ";\n"
            p[0].TAC += "if s1 == 0 goto state_" + str(states) + ";\n"
            p[0].TAC += "if  s2 == 0 goto state_" + str(states) + ";\n"
            p[0].TAC += new_var + " = 1;\ngoto state_" + str(states+1) + ";\n"
            p[0].TAC += false_cond + "\nstate_" + str(states+1) + ":\n"
            states += 1
            p[0].place = new_var
            p[0].type = 'bool'
        else:
            p[0] = NewNode(p[2])
            global states, count
            states += 1
            count += 1
            new_var = "_t" + str(count)
            true_cond = "\nstate_" + str(states) + ":\n" + new_var + " = 1;\n"
            p[0].TAC = p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n s2 = " + p[3].place + ";\n"
            p[0].TAC += "if s1 > 0 goto state_" + str(states) + ";\n"
            p[0].TAC += " if  s2 > 0 goto state_" + str(states) + ";\n"
            p[0].TAC += new_var + " = 0;\ngoto state_" + str(states+1) + ";\n" 
            p[0].TAC += true_cond + "\nstate_" + str(states+1) + ":\n"
            states += 1
            p[0].place = new_var
            p[0].type = 'bool'

def p_RELATIONAL_EXPRESSION (p):
    ''' RELATIONAL_EXPRESSION : SUM_EXPRESSION LESSER SUM_EXPRESSION
                        | SUM_EXPRESSION GREATER SUM_EXPRESSION
                        | SUM_EXPRESSION LESSER_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION GREATER_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION NOT_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION EQUAL_EQUAL SUM_EXPRESSION
                        | SUM_EXPRESSION
                        '''
    global count
    if(len(p)==2):
        p[0] = p[1]
        p[0].TAC = p[1].TAC
        p[0].type = p[1].type
    else:
        # print('sumtype ',p[1].type , p[3].type)
        if(p[1].type!= p[3].type):
            print("Error!! at line:", p.lexer.lineno, ' Type mismatch for ',p[2][0]) #, 'at the line ',p.lexer.lineno
            sys.exit()

        # print('sahil22' , p[2]                       )
        if(p[2][1]=='LESSER'):
            p[0] = NewNode(p[2])            
            count += 1
            new_var = "_t" + str(count)
            p[0].TAC = "\n" + new_var + " = 0;\n" 
            p[0].TAC += p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n"
            p[0].TAC += "s2 = " + p[3].place + ";\n"
            p[0].TAC += "if s1 <  s2 " + new_var + " = 1;\n" 
            p[0].place = new_var


        elif(p[2][1]=='GREATER'):
            p[0] = NewNode(p[2])
            
            count += 1
            new_var = "_t" + str(count)
            p[0].TAC = "\n" + new_var + " = 0;\n" 
            p[0].TAC += p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n" 
            p[0].TAC += "s2 = " + p[3].place + ";\n"
            p[0].TAC += "if s1 >  s2 " + new_var + " = 1;\n" 
            p[0].place = new_var


        elif(p[2][1]=='LESSER_EQUAL'):
            p[0] = NewNode(p[2])
            
            count += 1
            new_var = "_t" + str(count)
            p[0].TAC = "\n" + new_var + " = 1;\n" 
            p[0].TAC += p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n"
            p[0].TAC += "s2 = " + p[3].place + ";\n"
            p[0].TAC += "if s1 >  s2 " + new_var + " = 0;\n" 
            p[0].place = new_var


        elif(p[2][1]=='GREATER_EQUAL'):
            p[0] = NewNode(p[2])
            
            count += 1
            new_var = "_t" + str(count)
            p[0].TAC = "\n" + new_var + " = 1;\n" 
            p[0].TAC += p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n "
            p[0].TAC += "s2 = " + p[3].place + ";\n"
            p[0].TAC += "if s1 <  s2 " + new_var + " = 0;\n" 
            p[0].place = new_var
    
        elif(p[2][1]=='NOT_EQUAL'):
            p[0] = NewNode(p[2])
            
            count += 1
            new_var = "_t" + str(count)
            p[0].TAC = "\n" + new_var + " = 1;\n" 
            p[0].TAC += p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n "
            p[0].TAC += "s2 = " + p[3].place + ";\n"
            p[0].TAC += "if s1 ==  s2 " + new_var + " = 0;\n" 
            p[0].place = new_var
            

        elif(p[2][1]=='EQUAL_EQUAL'):        
            p[0] = NewNode(p[2])
            count += 1
            new_var = "_t" + str(count)
            p[0].TAC = "\n" + new_var + " = 0;\n" 
            p[0].TAC += p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n "
            p[0].TAC += "s2 = " + p[3].place + ";\n"
            p[0].TAC += "if s1 ==  s2 " + new_var + " = 1;\n" 
            p[0].place = new_var

        p[0].type= p[1].type    
                
def p_SUM_EXPRESSION(p):
    ''' SUM_EXPRESSION : SUM_EXPRESSION PLUS UNARY_EXPRESSION
                        | SUM_EXPRESSION MINUS UNARY_EXPRESSION
                        | SUM_EXPRESSION STAR UNARY_EXPRESSION
                        | SUM_EXPRESSION DIVIDE UNARY_EXPRESSION
                        | SUM_EXPRESSION MOD UNARY_EXPRESSION                         
                        | UNARY_EXPRESSION
                        '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].TAC = p[1].TAC
        p[0].type = p[1].type

    else:                    
        p[0] = NewNode(p[2][0])
        global count
        count += 1
        new_var = "_t" + str(count)
        p[0].TAC = p[1].TAC + "\n" + p[3].TAC + "\ns1 = " + p[1].place + ";\n s2 = " + p[3].place + ";\n"
        if(p[2][1]=='PLUS'):
            p[0].TAC += new_var + " = s1 +  s2;\n"
        elif(p[2][1]=='MINUS'):
            p[0].TAC += new_var + " = s1 -  s2;\n"
        elif(p[2][1]=='STAR'):
            p[0].TAC += new_var + " = s1 *  s2;\n"
        elif(p[2][1]=='DIVIDE'):
            p[0].TAC += new_var + " = s1 /  s2;\n"
        elif(p[2][1]=='MOD'):
            p[0].TAC += new_var + " = s1 %  s2;\n"
 
        # print('sumtype ',p[1].type , p[3].type)
        if(p[1].type!= p[3].type):
            print("Error!! at line:", p.lexer.lineno,  ' Type mismatch for ',p[2][0])
            sys.exit()
        else:
            p[0].type = p[1].type

        p[0].place = new_var
 

            
def p_UNARY_EXPRESSION(p):
    ''' UNARY_EXPRESSION : UNARY_OPERATOR UNARY_EXPRESSION
                        | UNARY_EXPRESSION UNARY_OPERATOR 
                        | factor
                        '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].TAC = p[1].TAC
        p[0].type = p[1].type
    else:
        if(p[1].TAC == " + 1;\n" or p[1].TAC == " - 1;\n"):
            p[0] = NewNode('UNARY_EXPRESSION1')            
            p[0].TAC = p[2].place + " = " + p[2].place + p[1].TAC
            p[0].place = p[2]
            p[0].type = 'int'

        elif(p[2].TAC == " + 1;\n" or p[2].TAC == " - 1;\n"):  
            # print(p[1].place , "sada")
            p[0] = NewNode('UNARY_EXPRESSION2')
            p[0].TAC = p[1].place + " = " + p[1].place + p[2].TAC
            p[0].place = p[1].place + p[2].place
            p[0].type = 'int'
def p_UNARY_OPERATOR(p):
    '''UNARY_OPERATOR : PLUSPLUS
                | MINUSMINUS
                '''
    # print('PPPPPP'                )
    if(p[1][1]=='PLUSPLUS'):        
        p[0] = NewNode(p[1])
        p[0].TAC = " + 1;\n"
        p[0].place = ' - 1'    
    elif(p[1][1] == 'MINUSMINUS'):
        p[0] = NewNode(p[1])
        p[0].TAC = " - 1;\n"
        p[0].place = ' + 1'

def p_factor(p):
    ''' factor : DATA_OBJECT
                | OTHER_EXPR
                '''
    p[0] = p[1]
    p[0].TAC = p[1].TAC
    p[0].type = p[1].type
###### condition for data object is still remaining

def p_DATA_OBJECT(p):
    ''' DATA_OBJECT : IDENTIFIER
                | IDENTIFIER LEFTBRACKET EXPRESSION RIGHTBRACKET
                | IDENTIFIER LEFTBRACKET EXPRESSION RIGHTBRACKET LEFTBRACKET EXPRESSION RIGHTBRACKET                
                |  IDENTIFIER DOT IDENTIFIER
                '''
#  DOUBT
    global currentScope
    global count

    if(len(p)==2):
        p[0] = NewNode(p[1])
        p[0].TAC = ""
        p[0].place = p[1][0]                    
    elif(len(p)==5):
        p[0] = NewNode('DATA_OBJECT1')
        count += 1
        new_var = "_t" + str(count)
        p[0].TAC = p[3].TAC + "\n" + new_var + " = " + p[3].place + ";\n"
        p[0].place = p[1] + "[" + new_var + "]"
                                 
    elif(len(p)==8):
        i = 0
# DOUBLE ARRAY NOT HANDLED RIGHT NOW
    else:
        i = 0
# CLASS FUNCTIONS NOT HANDLED
    flag = 1
    for i in currentScope.attributes:        
        if(currentScope.attributes[i]['name']==p[1]):
            p[0].type = currentScope.attributes[i]['type']
            
            flag = 0
            break
    for i in currentScope.father.attributes:        
        if(currentScope.father.attributes[i]['name']==p[1]):
            p[0].type = currentScope.father.attributes[i]['type']

            flag = 0
            break

    if(flag):
        print("Error!! at line:", p.lexer.lineno,  ' variable ',p[1] ,'not declared before')
        sys.exit()    

def p_OTHER_EXPR(p):
    ''' OTHER_EXPR : LEFTBRACKET LIST_OF_CONSTANTS RIGHTBRACKET
                    | CONSTANT                    
                    | FUNCTION_INSTANCE                    
        '''                    
    if(len(p)==2):
        p[0] = p[1]
        p[0].TAC = p[1].TAC
        p[0].type = p[1].type        

def p_FUNCTION_INSTANCE (p):
    ''' FUNCTION_INSTANCE : IDENTIFIER LEFTPAR FUNC_ARGUMENTS RIGHTPAR
            '''

def p_FUNC_ARGUMENTS(p):
    ''' FUNC_ARGUMENTS : LIST_OF_FUNCTION_ARGUMENTS
            |
            '''    
        
def p_LIST_OF_FUNCTION_ARGUMENTS(p):
    ''' LIST_OF_FUNCTION_ARGUMENTS : LIST_OF_FUNCTION_ARGUMENTS COMMA EXPRESSION
                    | EXPRESSION
                    '''

def p_LIST_OF_CONSTANTS(p):
    ''' LIST_OF_CONSTANTS : STRING_CONSTANT COLON SIMPLE_EXPRESSION COMMA LIST_OF_CONSTANTS
                            | STRING_CONSTANT COLON SIMPLE_EXPRESSION
                    '''

def p_CONSTANT(p):
    ''' CONSTANT : INT_CONST
                    | FLOAT_CONST
                    | CHAR_CONST
                    | STR_CONST
                    '''
    if(len(p)==2):
        p[0] = p[1]
        p[0].TAC = p[1].TAC
        p[0].type = p[1].type

def p_INT_CONST(p):
    ''' INT_CONST : INT_CONSTANT
                '''
    p[0] = NewNode(p[1][0])
    p[0].TAC = ""
    p[0].place = p[1][0]
    p[0].type = "int"

def p_FLOAT_CONST (p):
    ''' FLOAT_CONST : FLOAT_CONSTANT
                '''
    p[0] = NewNode(p[1][0])
    p[0].TAC = ""
    p[0].place = p[1][0]
    p[0].type = "float"


def p_CHAR_CONST (p):
    ''' CHAR_CONST : CHAR_CONSTANT
                '''
    p[0] = NewNode(p[1][0])
    p[0].TAC = ""
    p[0].place = p[1][0]
    p[0].type = "char"

def p_STR_CONST (p):
    ''' STR_CONST : STRING_CONSTANT
                '''
    p[0] = NewNode(p[1][0])
    p[0].TAC = ""
    p[0].place = p[1][0]
    p[0].type = "string"

def p_LEFTBRACES(p):
    ''' LEFTBRACES : LEFTBRACE
                    '''
    # print('sasassasa' ,p[1]                    )
    p[0] = NewNode(p[1][0])
    p[0].TAC = ""
    global currentScope, tableNo
    new_scope = SymbolTable(tableNo)
    tableNo += 1
    currentScope.AppendNewTable(new_scope)
    currentScope = new_scope

def p_RIGHTBRACES(p):
    ''' RIGHTBRACES : RIGHTBRACE
                    '''
    p[0] = NewNode(p[1][0])
    p[0].TAC = ""
    global currentScope
    currentScope = currentScope.father

def p_error(p):
    print("Parse Time Error!! at line:", p.lexer.lineno)

logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)


parser = yacc.yacc()
data3 ='''int main(int c, int x, int k , int l) { int i ,c[2], j=1,k=0 ; k = 1 +j; k =  3 + 5  - 8 * 4 / 8%6;  if(i==j){ k = i*2;} else { j = j*2;}} '''
data1 = ' int main() { float  f = 7*5-5+4/5+5+5+5-5*6; }'
data2 = 'int main(){     int k=0;     float a=7.6;     int b=7;     x = a*b*b ; }'

data = open(sys.argv[1],'r').read()

print("input program is:")
print(data)
print("3-AC is")
print()

parser.parse(data, debug=logging.getLogger())

# print(parser.parse(data2, debug=logging.getLogger()))
# print(parser.parse(data, debug=logging.getLogger()))