"""
This module handles text file generation for new compositions.

Also see if we can reduce the number of times f.write() is called. It seems like... a lot, in
it's current state.
"""

from containers.melody import Melody
from containers.chord import Chord
from containers.composition import Composition


def gen_info_doc(file_name: str, data, comp: Composition):
    """
    Generates a new .txt file to save a new composition's data and meta-data to.
    Parameters:
        file_name: string
        data: any object
        comp: Composition
    """
    with open(file_name, "w+") as f:
        ### generate a header ###
        header = '\n\n************************************************************* ' \
                 '\n--------------------------COMPOSITION------------------------ ' \
                 '\n*************************************************************\n'
        f.write(header)

        ### add composition information ###
        info = f"\n\nTitle: {comp.title} " \
               f"\n\nFor {comp.ensemble}" \
               f"\n\nComposer: {comp.composer} " \
               f"\n\nDate: {comp.date} "
        f.write(info)

        ## add info about any data inputted to create the new composition ###
        data_str = "".join([str(i) for i in range(len(data))])
        data_info = f"\n\n\nData inputted: {data_str}"
        f.write(data_info)

        ### add part information ###
        f.write("\n\n----------------------- Part Info --------------------------------\n\n")
        for part in comp.parts:
            # handle single melody or chord objects
            if isinstance(comp.parts[part], Melody) or isinstance(comp.parts[part], Chord):
                part = f"\n\nInstrument: {comp.parts[part].instrument}  " \
                       f"\n\nTotal notes: {len(comp.parts[part].notes)}" \
                       f"\n\nNotes: {comp.parts[part].notes}" \
                       f"\n\nTotal rhythms: {len(comp.parts[part].rhythms)}" \
                       f"\n\nRhythms: {comp.parts[part].rhythms}" \
                       f"\n\nTotal dynamics: {len(comp.parts[part].dynamics)}" \
                       f"\n\nDynamics: {comp.parts[part].dynamics}" \
                       f"\n\nInfo: {comp.parts[part].info}" \
                       f"\n\nSource data: {comp.parts[part].source_data}" \
                       f"\n\nSource scale: {comp.parts[part].source_scale}"
                f.write(part)
            # handle list of melody or chord objects
            elif isinstance(comp.parts[part], list):
                for item in comp.parts[part]:
                    # handle single melody or chord objects
                    if isinstance(comp.parts[part], Melody) or isinstance(comp.parts[part], Chord):
                        part = f"\n\nInstrument: {comp.parts[part].instrument}  " \
                               f"\n\nTotal notes: {len(comp.parts[part].notes)}" \
                               f"\n\nNotes: {comp.parts[part].notes}" \
                               f"\n\nTotal rhythms: {len(comp.parts[part].rhythms)}" \
                               f"\n\nRhythms: {comp.parts[part].rhythms}" \
                               f"\n\nTotal dynamics: {len(comp.parts[part].dynamics)}" \
                               f"\n\nDynamics: {comp.parts[part].dynamics}" \
                               f"\n\nInfo: {comp.parts[part].info}" \
                               f"\n\nSource data: {comp.parts[part].source_data}" \
                               f"\n\nSource scale: {comp.parts[part].source_scale}"
                        f.write(part)
            else:
                raise TypeError("Comp object has wrong type! "
                                "Should be a Melody, Chord object, or list of Melody or Chord objects "
                                f"Type was: {type(comp.parts[part])}")
        # close file instance
        f.close()
