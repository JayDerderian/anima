'''
-------------------------------------------ABOUT---------------------------------------------------

``AnimA`` contains a number of generative methods used to automatically create a music
composition, it's sheet music, and a MIDI file as well as a .txt file containing data about
how that piece was composed and the raw materials used during its generation. 

Example usage for generating a single melody using a person's name

.. code-block:: python
    
    from utils.mid import midi
    from utils.txtfile import saveInfo
    from core.generate import Generate

    # create a generate object
    create = Generate()

    # get the user's name
    name = input("Enter your name:" )

    # generate a melody() object
    m = create.newMelody(data=name, dataType=3)

    # generate title and export to a MIDI file
    title = create.newTitle()
    midiFileName = title + ".mid"
    midi.saveMelody(midiFileName, new_melody)

    # create a text file name and save melody info 
    # to a .txt file
    txtFileName = title + ".txt"
    create.saveInfo(txtFileName, mid)
'''
__version__ = '1.0'