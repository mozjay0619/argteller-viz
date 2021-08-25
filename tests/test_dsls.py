import pytest

from src.argteller.decorators.class_decorator import ArgtellerClassDecorator

sample_dsl1="""
Topic_1
-param1:option1
    =option1
        -paramA:a
    =option2
        -paramB:b

Topic_2
-param2:asdf

Topic_3
-param3:A
    =A
        -Topic_1/param1:option1
        -Topic_1/paramA:value1
        -Topic_2/param2:value1
    =B
        -Topic_1/param1:option2
        -Topic_1/paramB:value2
        -Topic_2/param2:value2
"""

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass1():

	def __init__(self):

		pass

def test_sample_dsl1():

	test = TestClass1()

	assert test.param1=='option1'
	assert test.paramA=='value1'
	assert test.param2=='value1'


sample_dsl2="""

Topic_1

-param1:option1
    =option1
        -paramA:a
    =option2
        -paramB:b

Topic_2
-param2:1/5

Topic_3
-param3:A
    =A
        -Topic_1/param1:option1
        -Topic_1/paramA:1/5
    =B
        -Topic_1/param1:option2
        -Topic_1/paramB:value2

"""

@ArgtellerClassDecorator(dsl=sample_dsl2)
class TestClass2():

	def __init__(self):

		pass

def test_sample_dsl2():

	test = TestClass2()

	assert test.paramA==0.2
	assert test.param2==0.2





