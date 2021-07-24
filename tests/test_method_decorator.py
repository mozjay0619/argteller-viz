import pytest

from src.argteller.decorators.class_decorator import ArgtellerClassDecorator
from src.argteller.decorators.method_decorator import ArgtellerMethodDecorator

sample_dsl1 = """
Topic1
-param1
-param2
"""

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass():

    def __init__(self):

        pass

class TestMethod1():
    
    @ArgtellerMethodDecorator(source_name='my_helper', topic='Topic1')
    def __init__(self, param1, param2):
        
        self.param1 = param1
        self.param2 = param2

class TestMethod2():
    
    @ArgtellerMethodDecorator(source_name='my_helper', topic='Topic1')
    def __init__(self, param1, param2, *args):
        
        self.param1 = param1
        self.param2 = param2
        
        self.args = args


def test_source_assignment():

	helper = TestClass(param1 = 'a', param2 = 'b')

	assert helper.param1 == 'a'
	assert helper.param2 == 'b'
	assert helper.__access_object__().get_value('param1', 'Topic1')==str(helper.param1)
	assert helper.__access_object__().get_value('param2', 'Topic1')==str(helper.param2)

	test = TestMethod1(my_helper=helper)

	assert test.param1 == 'a'
	assert test.param2 == 'b'

def test_positional_arg_assignment():

	test = TestMethod1('a', 'b')

	assert test.param1 == 'a'
	assert test.param2 == 'b'

def test_keyword_arg_assignment():

	test = TestMethod1(param1='a', param2='b')

	assert test.param1 == 'a'
	assert test.param2 == 'b'

def test_positional_and_keyword_arg_assignment():

	test = TestMethod1('a', param2='b')

	assert test.param1 == 'a'
	assert test.param2 == 'b'

# def test_keyword_before_positional_error():

# 	with pytest.raises(Exception) as e:

# 		test = TestMethod1(param1='a', 'b')

# 	assert "positional argument follows keyword argument" in str(e.value)
# 	assert e.type == SyntaxError

def test_positional_arg_override_source_assignment():

	helper = TestClass(param1='a', param2='b')

	test = TestMethod1(1, 2, my_helper=helper)

	assert test.param1 == 1
	assert test.param2 == 2

def test_keyword_arg_override_source_assignment():

	helper = TestClass(param1='a', param2='b')

	test = TestMethod1(param1=1, param2=2, my_helper=helper)

	assert test.param1 == 1
	assert test.param2 == 2

def test_positional_arg_partial_override_source_assignment():

	helper = TestClass(param1='a', param2='b')

	test = TestMethod1(1, my_helper=helper)

	assert test.param1 == 1
	assert test.param2 == 'b'

def test_keyword_arg_partial_override_source_assignment():

	helper = TestClass(param1='a', param2='b')

	test = TestMethod1(param1=1, my_helper=helper)

	assert test.param1 == 1
	assert test.param2 == 'b'

def test_positional_VAR_POSITIONAL_args():

	helper = TestClass(param1='a', param2='b')

	test = TestMethod2(1, 2, 3, 4, my_helper=helper)

	assert test.param1 == 1
	assert test.param2 == 2
	assert test.args == (3, 4)








