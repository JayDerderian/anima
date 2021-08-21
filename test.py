'''
Simplified file for testing generative functions.
'''

# Imports
from modes.rando import newRandomComposition
from strqtet import newStrQtet

print("\nTest newRandomComposition (1) or newStrQtet(2) ? ")
choice = int(input("Selection (1 or 2): "))

if choice == 1:
    print("\ntesting rando.py...")
    if newRandomComposition() == -1:
        print("\nfurther testing is needed...\n")
    else:
        print("\nhooray!\n")
else:
    print("\ntesting strqtet.py...")
    if newStrQtet() == -1:
        print("\nfurther testing is needed...\n")
    else:
        print("\nhooray!\n")