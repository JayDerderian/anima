# About
`anima` is a generative music application and mini python library.

`anima` contains a number of [generative](https://en.wikipedia.org/wiki/Generative_music) methods used to automatically create raw material for music composition. `anima` can assemble this material and export it as a MIDI file which can be used in MIDI sequencing and sheet music generation. It can also generate a text file containing information about how that piece was composed and the raw elements used during creation (for example, a pitch-class set that was selected as a 'seed' to build material off of). 

`anima` also contains two additional utility classes. The `Modify` class can be used to create variations on any generated material, and the `Analyze` class can be used to analyze the material. Analysis is done through the lense of pitch class set analysis.

## Installation

This package requires `python` (3.6+) in order to run and install all dependencies.

Run `pip install -r requirements.txt` in order to install dependencies.

## Using the Generate library

Example usage for generating a single melody using a person's name:

<!-- .. code-block:: python -->
    
    from utils.midi import export_midi
    from core.generate import Generate

    name = input("Enter your name:")                          # get the user's name
    create = Generate()                                       # create a generate object
    comp = create.init_comp(tempo=60.0, composer=name)        # intialize a new composition object

    melody = create.new_melody(tempo=comp.tempo, 
                          data=name, data_type=3)             # generate a melody() object
    melody.instrument = create.new_instrument()               # pick an instrument for this melody
    comp.add_part(part=melody, instr=melody.instrument)       # save to comp object 
    export_midi(comp)                                         # generate MIDI file           

This will export a new MIDI file with the title of the composition into the directory 
where this script was executed. 

## Example Compositions

There are several example compositions under the "composition" directory. Each module
has a description of the underlying process governing the composition's generation.