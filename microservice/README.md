
## Exercise Query
This Python program provides a sample exercises that match various attributes that a user may be trying to use for a workout.  It utilizes a JSON file as a 'mini database', to connect the specified attributes to various exercises, then returns a list consisting of exercises that match the given attributes.

## How to request data
First, to request data, an instance of the server needs to be running.  This is done simply by navigating to the directory that contains the server file, then starting it by calling on python to run the file.
```
python server.py
```

Then, an instance of the client will need to be run to request data from the server.  This can be done in three different ways:
First, the client could simply be ran:
```
python client.py
```
By default, this will generate a series of user prompts to request exercise data.

Second, the client could be called from the command line with input arguments describing the desired exercises.  For example:
```
python client.py 'shoulders' 'upper' 'compound'
```
Returns:
```
['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']
```

Third, you could import the client file into another python file and call the functions to request data.  For example:
```
import client
exercise_attributes = ['shoulders', 'upper', 'compound']
client.exercise_request(exercise_attributes)
```
returns:
```
['Military Press', 'Seated Military Press', 'Upright Row', 'Arnold Press', 'Landmines']
```


## UML Diagram

![uml diagram](https://github.com/calcOSU/CS361/blob/main/microservice/UML%20diagram.JPG)
