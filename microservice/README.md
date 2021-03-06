
## Exercise Query
This Python program provides a sample exercises that match various attributes that a user may be trying to use for a workout.  It utilizes a JSON file as a 'mini database', to connect the specified attributes to various exercises, then returns a list consisting of exercises that match the given attributes.

## How to request and receive data
First, to request data, an instance of the server needs to be running.  This is done simply by navigating to the directory that contains the server file, then starting it by calling on python to run the file.
```
python server.py
```

Then, an instance of the client will need to be run to request data from the server.  This can be done in three different ways:
First, the client could simply be ran:
```
python client.py
```
By default, this will generate a series of user prompts to request exercise data.  You will receive data in the command line.

Second, the client could be called from the command line with input arguments describing the desired exercises.  For example:
```
python client.py 'shoulders' 'upper' 'compound'
```
Again, data will be received via the command line.
Returns:
```
['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']
```

Third, you could import the client file into another python file and call the functions to request data.  For example:
```
import client
exercise_attributes = ['shoulders', 'upper', 'compound']
resp = client.exercise_request(exercise_attributes)
print(resp)
```
Here, data will be received in the python file, where it could be manipulated.
will print:
```
['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']
```

You can put in 'demo' as a parameter from the command line to show a brief demonstration of how the data will be returned:
```
client.py 'demo'
```
Returns a number of different possibilities.  As you can see, if additional arguments are given that do not match an exercise, they will be ignored.  The arguments can be given in any order.  If not enough arguments are given, no exercises will be returned.
```
For the input list of: ['compound', 'upper', 'shoulders']
The result is: ['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']

For the input list of: ['shoulders', 'upper', 'compound']
The result is: ['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']

For the input list of: ['blank', 'blue']
The result is: False

For the input list of: ['shoulders', 'upper', 'compound', 'orange']
The result is: ['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']

For the input list of: ['blank', '', 'three', 3, 'four', 'orange']
The result is: False

For the input list of: [5, 3, 'compound', 'orange', 2, 'green', 1, 'upper', 'four', 'five', 3, 'shoulders', 'hey']
The result is: ['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']

For the input list of: ['hey', 'shoulders', 3, 'five', 'four', 'upper', 1, 'green', 2, 'orange', 'compound', 3, 5]
The result is: ['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']
```


## UML Diagram
A basic UML diagram for this microservice:

![uml diagram](https://github.com/calcOSU/CS361/blob/main/microservice/UML%20diagram.JPG)
