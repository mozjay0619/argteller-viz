Argteller
=========

The argteller package provides the class and method decorators for visual and interactive class object constructor. It frees the user from needing to constantly refer to documentations to figure out what arguments are required and what parameter values are valid inputs. It lists required arguments parsimoniously by only asking the parameters as needed, depending on the previously provided argument values. You can easily encode them in the custom DSL (domain specific language) script. 

Install
-------

::

	pip3 install argteller-viz

What does it do?
----------------

Let's say you have two classes ``Vehicle`` and ``Rider``. Each class has the following ``__init__`` signatures:

::

	class Vehicle():

	    def __init__(self, vehicle_type, num_doors=None, car_name=None, num_motors=None, boat_name=None):
	    	"""
	    	Parameters
	    	----------
	    	vehicle_type : str
	    	    Valid inputs: "car" or "boat"

	    	num_doors : int
	    	    Only used when vehicle_type is "car". Valid inputs: 2 or 4

	    	car_name : str
	    	    Only used when vehicle_type is "car". 

	    	num_motors : int
	    	    Only used when vehicle_type is "boar". Valid inputs: 1, 2, or 3

	    	boat_name : str
	    	    Only used when vehicle_type is "boar"
	    	"""

		# ...Vehicle class definition

::

	class Rider():

	    def __init__(self, rider_name, rider_height, rider_weight):
	    	"""
	    	Parameters
	    	----------
	    	rider_name : str

	    	rider_height : float

	    	rider_weight : float
	    	"""

		# ...Rider class definition

