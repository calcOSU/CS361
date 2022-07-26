
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


## UML Diagram
A basic UML diagram for this microservice:

![uml diagram](https://github.com/calcOSU/CS361/blob/main/microservice/UML%20diagram.JPG)
