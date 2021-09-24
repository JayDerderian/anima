'''
-------------------------------------------ABOUT---------------------------------------------------

``anima`` contains a number of generative methods used to automatically create a music
composition, it's sheet music, and a MIDI file as well as a .txt file containing data about
how that piece was composed and the raw materials used during its generation. 

Example usage for generating a single melody using a person's name

.. code-block:: python
    
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
    name = input("Enter your name:" )

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

'''
__version__ = '1.0'