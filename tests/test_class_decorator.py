import pytest

from src.argteller.decorators.class_decorator import ArgtellerClassDecorator

sample_dsl1 = """
Topic1
-param1
-param2
"""

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass1():

	def __init__(self):

		pass

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass2():

    def __init__(self, a, b):

        self.a = a
        self.b = b

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass3():

    def __init__(self, a, param1):

        self.a = a
        self.param1 = param1

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass4():

    def __init__(self, a, *args):

        self.a = a
        
        self.args = args

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass5():

    def __init__(self, a, **kwargs):

        self.a = a
        
        self.kwargs = kwargs

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass6():

    def __init__(self, a, *args, **kwargs):

        self.a = a
        
        self.args = args
        self.kwargs = kwargs


def test_parameter_assignment():

	test = TestClass1()
	test.param1 = 1
	test.param2 = 2

	assert test.__access_object__().get_value('param1', 'Topic1')==str(test.param1)
	assert test.__access_object__().get_value('param2', 'Topic1')==str(test.param2)

def test_missing_POSITIONAL_OR_KEYWORD_args():

	with pytest.raises(Exception) as e:

		test = TestClass2()

	assert "__init__() missing 2 required positional arguments: 'a' and 'b'" in str(e.value)
	assert e.type == TypeError

def test_too_many_positional_args():

	with pytest.raises(Exception) as e:

		test = TestClass2(1, 2, 3)

	assert "__init__() takes 3 positional arguments but 4 were given" in str(e.value)
	assert e.type == TypeError

def test_positional_POSITIONAL_OR_KEYWORD_args():

	test = TestClass2(1, 2)

	assert test.a==1
	assert test.b==2

def test_keyword_POSITIONAL_OR_KEYWORD_args():

	test = TestClass2(a=1, b=2)

	assert test.a==1
	assert test.b==2

def test_positional_POSITIONAL_OR_KEYWORD_args_in_tree_not_in_signature():

	test = TestClass2(1, 2, param1=3)

	assert test.a==1
	assert test.b==2
	assert test.__access_object__().get_value('param1', 'Topic1')=='3'

def test_keyword_POSITIONAL_OR_KEYWORD_args_in_tree_not_in_signature():

	test = TestClass2(a=1, b=2, param1=3)

	assert test.a==1
	assert test.b==2
	assert test.__access_object__().get_value('param1', 'Topic1')=='3'

def test_positional_POSITIONAL_OR_KEYWORD_args_in_tree_in_signature():

	test = TestClass3(1, 2)

	assert test.a==1
	assert test.__access_object__().get_value('param1', 'Topic1')=='2'

def test_keyword_POSITIONAL_OR_KEYWORD_args_in_tree_in_signature():

	test = TestClass3(a=1, param1=2)

	assert test.a==1
	assert test.__access_object__().get_value('param1', 'Topic1')=='2'

def test_positional_VAR_POSITIONAL_args():

	test = TestClass4(1, 2, 3)

	assert test.a==1
	assert test.args==(2, 3)

def test_keyword_VAR_KEYWORD_args():

	test = TestClass5(1, param3=3, param1=3)

	assert test.a==1
	assert test.kwargs=={'param3': 3, 'param1': 3}
	assert test.__access_object__().get_value('param1', 'Topic1')=='3'

def test_keyword_VAR_POSITIONAL_and_VAR_KEYWORD_args():

	test = TestClass6(1, 2, 3, param3=6, param1=3)

	assert test.a==1
	assert test.args==(2, 3)
	assert test.kwargs=={'param3': 6, 'param1': 3}






