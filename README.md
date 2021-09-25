# About
`anima` is a generative music application and python library. The program can be used in the terminal, or in the browser
using the app.js script. 

`anima` contains a number of [generative](https://en.wikipedia.org/wiki/Generative_music) methods used to automatically create a music composition.
New compositions are exported as a MIDI file, sheet music in a PDF, anda .txt file containing data about how that piece was composed and the raw
elements used during creation (for example, a pitch-class set that was selected as a 'seed' to build material off of). 

## Installation

This package requires `python` (3.6+) and `npm` in order to run and install all dependencies.

For the frontend, simply run `npm install` in the main directory, and finally

To set up the backend, run `pip install -r requirements.txt` in order to install Flask and its dependencies.
## Using the program in the browser

## Using the libary directly

Example usage for generating a single melody using a person's name:

<!-- .. code-block:: python -->
    
    from containers.composition import Composition
    from utils.mid import midi
    from utils.txtfile import saveInfo
    from core.generate import Generate

    # create a generate object
    create = Generate()
    # create a composition object
    comp = Composition()
    # pick a tempo
    comp.tempo= create.newTempo()
    # pick a title
    comp.title = create.newTitle()
    
    # get the user's name
    name = input("Enter your name:")

    # generate a melody() object
    m = create.newMelody(tempo=comp.tempo, 
                         data=name, 
                         dataType=3)
    # pick an instrument for this melody
    m.instrument = create.newInstrument()
    # save to comp object to write out a MIDI file with
    comp.melodies.append(m)

    # create file names and write out
    comp.midiFileName = comp.title + ".mid"
    comp.txtFileName = compt.title + ".txt"
    midi.save(comp)