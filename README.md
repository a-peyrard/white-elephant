## White elephant

This is not really for white elephant, but to make a random draw for Xmas gift (I do like the name white elephant :)). 

This is a dummy script quickly written, but it works, and this is what we are asking for... 

The script takes a json input containing the participants and some constraints (we usually don't want to do a gift for our spouse, nor children, ...).
Here is an example of a valid input:
```json
{
    "Augustin": ["Anna"],
    "Anna": ["Augustin"],
    "Sam": [],
    "Elo": ["Arnaud"],
    "Arnaud": ["Elo"]
}
```

Then one can launch the draw like this:
```bash
python we/main.py my_input.json
```
