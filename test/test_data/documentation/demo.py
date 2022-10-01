# FILE HEADER DOCUMENTATION
# This file and folder is not documentation about test_data, but test data for documentation
#
# This is an example of the types of python documentation. In general this can serve as an example of how
# code should/could look like in the project.
#                                                    
#     ____Expected Totals____                                           
#     Classes . . . . . . . 3                                        
#     Class docstring . . . 2
#     File import lines . . 7     
#     Functions . . . . . . 3
#     Function docstring. . 3
#     Function nested def . 1
#     Methods inc. init . . 12 
#     Method nested def . . 2                                                
#     Method docstring. . . 10 
#     Method returns. . . . 11                                               
#     Super class lines . . 2
#     Super classes . . . . 3 
#     Todo. . . . . . . . . 2                                              
#                                           
from datetime import datetime as dt, time
from config.modules import Documentation, \
Logging 
from datetime import timedelta
import decimal as dec
import numbers

# Start classes 
class Class1:
    ''' This is an example superclass

        Usage aka code block:

            ```
            example code block
            line 2 should line up with above
                and this should in tabbed in one
                    and this indented 2
            ```

            ```example code block
            line 2 should line up with above
                and this should in tabbed in one
                    and this indented 2```

        Params:
            - param1: description with `code in it` 
            - param2: this is a longer description than normal. Try to keep lines within 100 char
              if you have to go over. align it with the block above to be included. 
            - param3:False to do this, True to do that

        Notes:
            This is a set of notes they may have `code` withing and that code may have `a: colon`
            and should still be rendered correctly. In fact any : in anything other than a header 
            should be ignored. 

        There can also be other paragraph blocks inside of this one. 

        Lists:
            - there should
            - be multiple levels of indent
                - like this
                    - and this
                - and back to here
            - it should work to have : in a list
            - as well as inline code
    '''
    class_var1 = ''
    class_var2 = ['List']

    def __init__(self, param1:str, param2:dict, param3:False) -> None:
        ''' Heres a docstring in an __init__ '''
        self.param1 = param1


    @classmethod
    def c1func1(cls, param1:str) -> list:
        ''' Example one line docstring. Also a class method'''
        return []


    @staticmethod
    def c1func2(param1:dict, param2=False):
        ''' Example one string with closing tag on new line. Also a static method
        '''
        def nestedDef1(param1):
            return 1

        def nestedDef2(param2):
            return 2

        return ''

    def c3func3(
        self,
        param1:list,
        param2:str,
        param3:dict
    ) -> dict:
        ''' Example multi line docstring with the preferred formatting style
            This is the second line 
        '''
        pass

class Class2(Class1):
    ''' This is an example class with a super class '''
    class_var1 = ''
    class_var2 = ['List']

    def __init__(self, param1: str, param2: dict, param3: False, param4=False) -> None:
        self.param4 = param4
        super().__init__(param1, param2, param3)

    def c1func1(self, param1:str) -> list:
        ''' Example one line docstring'''
        return []

    def c1func2(self, param1:dict, param2=False) -> str:
        ''' Example one string with closing tag on new line
        '''
        return ''

    def c3func3(
        self,
        param1:list,
        param2:str,
        param3:dict
    ) -> dict:
        ''' Example multi line docstring with the preferred formatting style
            This is the second line 
        '''
        return {}


def testImportInFunction(param1, param2:str, param3=None):
    ''' A single line docstring  '''
    from datetime import timezone
    


class Class3(Class1, Class1):
    def __init__(self, param1:str, param2:dict, param3:False) -> None:
        self.param1 = param1

    def c1func1(self, param1:str) -> list:
        ''' Example one line docstring'''
        return []

    def c1func2(self, param1:dict, param2=False) -> str:
        ''' Example one string with closing tag on new line
        '''
        return ''

    def c3func3(
        self,
        param1:list,
        param2:str,
        param3:dict
    ) -> dict:
        ''' Example multi line docstring with the preferred formatting style
            This is the second line 
        '''
        return {}


def testNestedDefInFunction(param1, param2: str):
    ''' Example one string with closing tag on new line
    ''' 
    # todo: example of todo 2
    def returns1():
        return 1
    pass



def func3(
    param1,
    param2:str,
    param3={}
) -> str:        
    ''' Example multi line docstring with the preferred formatting style
            This is the second line 
    '''
    # TODO example of a todo
    return ''
