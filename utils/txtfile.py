"""
This module handles text file generation for new compositions.

Also see if we can reduce the number of times f.write() is called. It seems like... a lot, in
it's current state.
"""

from containers.chord import Chord
from containers.melody import Melody
from containers.composition import Composition


def gen_info_doc(file_name: str, comp: Composition, data=None):
    """
    Generates a new .txt file to save a new composition's data and meta-data to.
    Parameters:
        file_name: string
        data: any object
        comp: Composition
    """
    with open(file_name, "w+") as f:
        ### generate a header ###
        header = (
            "\n************************************************************* "
            "\n--------------------------COMPOSITION------------------------ "
            "\n************************************************************* "
        )
        f.write(header)

        ### add composition information ###
        info = (
            f"\n\nTitle: {comp.title} "
            f"\nComposer: {comp.composer} "
            f"\nInstruments: {', '.join(comp.instruments)} "
            f"\nDate: {comp.date} "
            f"\nDuration: {comp.duration()} "
        )
        f.write(info)

        ## add info about any data inputted to create the new composition ###
        if data is not None:
            data_str = (
                ", ".join([str(i) for i in range(len(data))])
                if type(data) == list
                else str(data)
            )
            data_info = f"\n\nData inputted: {data_str}"
            f.write(data_info)

        # iterate over composition part dictionary
        for part in comp.parts:
            ### add part information ###
            sub_header = (
                "\n\n\n---------------------------Part Info ---------------------------"
            )
            f.write(sub_header)
            # handle melody objects
            if isinstance(comp.parts[part], Melody):
                part = (
                    f"\n\nType: MELODY"
                    f"\nInstrument: {comp.parts[part].instrument}  "
                    f"\nTotal notes: {len(comp.parts[part].notes)}"
                    f"\nNotes: {comp.parts[part].notes}"
                    f"\nTotal rhythms: {len(comp.parts[part].rhythms)}"
                    f"\nRhythms: {comp.parts[part].rhythms}"
                    f"\nTotal dynamics: {len(comp.parts[part].dynamics)}"
                    f"\nDynamics: {comp.parts[part].dynamics}"
                    f"\n\n## --- Meta data --- ##"
                    f"\nInfo: {comp.parts[part].info}"
                    f"\nSource data: {comp.parts[part].source_data}"
                    f"\nSource scale: {comp.parts[part].source_notes}"
                    f"\nPitch classes: {comp.parts[part].pcs}"
                )
                f.write(part)
            # handle chord objects
            elif isinstance(comp.parts[part], Chord):
                part = (
                    f"\n\nType: HARMONY"
                    f"\nInstrument: {comp.parts[part].instrument}  "
                    f"\nType: Harmony (chord)"
                    f"\nTotal notes: {len(comp.parts[part].notes)}"
                    f"\nNotes: {comp.parts[part].notes}"
                    f"\nTotal rhythms: {len(comp.parts[part].rhythm)}"
                    f"\nRhythms: {comp.parts[part].rhythm}"
                    f"\nTotal dynamics: {len(comp.parts[part].dynamic)}"
                    f"\nDynamics: {comp.parts[part].dynamic}"
                    f"\n\n## --- Meta data --- ##"
                    f"\nInfo: {comp.parts[part].info}"
                    f"\nSource data: {comp.parts[part].source_data}"
                    f"\nSource scale: {comp.parts[part].source_notes}"
                    f"\nPitch classes: {comp.parts[part].pcs}"
                )
                f.write(part)
            # handle list of melody and/or chord objects
            elif isinstance(comp.parts[part], list):
                for item in comp.parts[part]:
                    # handle single melody or chord objects
                    if isinstance(item, Melody):
                        part = (
                            f"\n\nType: MELODY"
                            f"\nInstrument: {comp.parts[part].instrument}  "
                            f"\nTotal notes: {len(comp.parts[part].notes)}"
                            f"\nNotes: {comp.parts[part].notes}"
                            f"\nTotal rhythms: {len(comp.parts[part].rhythms)}"
                            f"\nRhythms: {comp.parts[part].rhythms}"
                            f"\nTotal dynamics: {len(comp.parts[part].dynamics)}"
                            f"\nDynamics: {comp.parts[part].dynamics}"
                            f"\n## --- Meta data --- ##"
                            f"\nInfo: {comp.parts[part].info}"
                            f"\nSource data: {comp.parts[part].source_data}"
                            f"\nSource scale: {comp.parts[part].source_notes}"
                            f"\nPitch classes: {comp.parts[part].pcs}"
                        )
                        f.write(part)
                    elif isinstance(item, Chord):
                        part = (
                            f"\n\nType: HARMONY"
                            f"\nInstrument: {comp.parts[part].instrument}  "
                            f"\nType: Harmony (chord)"
                            f"\nTotal notes: {len(comp.parts[part].notes)}"
                            f"\nNotes: {comp.parts[part].notes}"
                            f"\nTotal rhythms: {len(comp.parts[part].rhythm)}"
                            f"\nRhythms: {comp.parts[part].rhythm}"
                            f"\nTotal dynamics: {len(comp.parts[part].dynamic)}"
                            f"\nDynamics: {comp.parts[part].dynamic}"
                            f"\n## --- Meta data --- ##"
                            f"\nInfo: {comp.parts[part].info}"
                            f"\nSource data: {comp.parts[part].source_data}"
                            f"\nSource scale: {comp.parts[part].source_notes}"
                            f"\nPitch classes: {comp.parts[part].pcs}"
                        )
                        f.write(part)
                    else:
                        raise TypeError(
                            "Comp object has wrong type! "
                            "Should be a Melody, Chord object, or list of Melody or Chord objects "
                            f"Type was: {type(comp.parts[part])}"
                        )
            else:
                raise TypeError(
                    "Comp object has wrong type! "
                    "Should be a Melody, Chord object, or list of Melody or Chord objects "
                    f"Type was: {type(comp.parts[part])}"
                )
        # close file instance
        f.close()
