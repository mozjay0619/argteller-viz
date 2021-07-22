import pytest

from argteller.decorators.class_decorator import ArgtellerClassDecorator

sample_dsl1 = """
Topic1
-param1
-param2
"""

@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass1():

	def __init__(self):

		pass


def test_parameter_assignment():

	test = TestClass1()
	test.param1 = 1
	test.param2 = 2

	print(test.__access_object__)

	assert test.__access_object__().get_value('param1', 'Topic1')==str(test.param1)
	assert test.__access_object__().get_value('param2', 'Topic1')==str(test.param2)

	


@ArgtellerClassDecorator(dsl=sample_dsl1)
class TestClass2():

    def __init__(self, a):

        self.a = a



# def test_raises_exception():
#     data = {"extra": 1, "y": 2}
#     with pytest.raises(Exception) as exc:
#         1/0
#     assert "division by zero" in str(exc.value)
#     assert exc.type == ZeroDivisionError