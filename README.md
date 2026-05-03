# Andromeda

A bullet hell engine.
Enjoy :)

Code released under Mozilla Public License by Iron Lotus Software.
The latest binary builds are available at www.ironlotussoftware.com/andromeda.

## Controls
Space - shoot  
Arrow keys - move a given direction


## To install dependencies
Set up a virtual environment with:  
```$ make venv```

## Running
Note that the code does not include assets.  You must download the asset pack and extract it in 
the same directory as `andromeda.py` or `andromeda.bin`.

### Run from source
```
$ unzip assets.zip
$ make venv
$ make run
```

### Run from binary
```
$ unzip andromeda-linux.zip
$ cd andromeda-linux
$ unzip assets.zip
$ ./andromeda.bin
```

## Compilation

You don't need to compile to run the game if you have Python installed.  However, there is the option to compile
to binary with Nuitka, a Python compiler.

You must have the chrpath package installed.  On Ubuntu 18.04:
```$ sudo apt install chrpath```

### Build
```$ make```

### Package
```$ make zip```

### Remove all artifacts
```$ make clean```

## Run unit tests
```$ make test```

## Contribution Credits
Art for level 1 and player ship created by MagykalMystique.

Music provided by NoCopyrightSounds:  
Jarico - Island  
Jarico - Landscape  
https://www.youtube.com/watch?v=Srqs4CitU2U  
https://www.youtube.com/watch?v=kcNpXMxOo48
