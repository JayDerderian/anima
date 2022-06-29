# About
`anima` is a generative music application and python library. The program can be used in the terminal using a CLI (forthcoming)

`anima` contains a number of [generative](https://en.wikipedia.org/wiki/Generative_music) methods used to automatically create a music composition.
New compositions are exported as a MIDI file, sheet music in a PDF, anda .txt file containing data about how that piece was composed and the raw
elements used during creation (for example, a pitch-class set that was selected as a 'seed' to build material off of). 

## Installation

This package requires `python` (3.6+) in order to run and install all dependencies.

Run `pip install -r requirements.txt` in order to install dependencies.

## Using the Generate library

Example usage for generating a single melody using a person's name:

<!-- .. code-block:: python -->
    
    from utils.midi import save
    from core.generate import Generate

    name = input("Enter your name:")                          # get the user's name
    create = Generate()                                       # create a generate object
    comp = create.init_comp(tempo=60.0, composer=name)        # intialize a new composition object

    m = create.new_melody(tempo=comp.tempo, data=name, dt=3)  # generate a melody() object
    m.instrument = create.new_instrument()                    # pick an instrument for this melody
    comp.melodies.append(m)                                   # save to comp object 
    save(comp)                                                # generate MIDI file           

This will export a new MIDI file with the title of the composition into the directory 
where this script was executed. 

There will also be a .txt file with the same name with information about how the piece was generated,
what kinds of (if any) source material were used, as well as some music theory-adjacent data.

## Example Compositions

There are several example compositions under the "ensembles" directory. Each module
has a description of the underlying process governing the composition's generation.

Included compositions:
    - bloom
    - mixedqtet
    - strqtet
    - pnoduet
    - rando

Each of these has a description in the file about the underlying process governing
how each composition is created.