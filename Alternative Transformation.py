# Author(s): Matt Burridge, Alex Laverick, contact Alex for assistance
# Last modified: 8:45, 10/10/2018
# Python 3.6.4
# Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################

from opentrons import labware, robot, instruments, modules                                              # Import all opentrons API
from sqlite3 import IntegrityError                                                                      # Import sqlite3 for custom container support
from opentrons.drivers.temp_deck import TempDeck                                                        # Import TempDeck driver for usable temp deck, might be outdated now?
from OT2_Functions import *                                                                             # 0T2_Functions needs to be in the same working directory as the script that calls it (same folder)
import numpy

Tiprack10uL = labware.load('tiprack-10ul', slot='11')                                                   # Import all labware. Opentrons labware is imported from the Opentrons library
Tiprack200uL = labware.load('tiprack-200ul', slot='9')                                                  # The labware is defined from a list detailed in the Opentrons documentation
Compcells = labware.load('96-flat', slot='6')                                                           # Custom containers can be defined in the Labware.py script
trash = robot.fixed_trash                                                                               # Declare trash this way in every script otherwise OT2 Functions breaks
DNA = labware.load('tube-rack-2ml', slot='10')                                                          # Container rack that holds the Plasmids for transforming the chasis
SOB = labware.load('duran_100', slot='7')                                                               # Custom container: Super Optimal Broth

NumberofPlasmids = 1                                                                                    # Need to specify the number of plasmids being used in the experiment
PlasmidVolume = 3                                                                                       # Specify the volume of plasmid in ul to be added to each well
                                                                                                        # The code can be adjusted to accomodate multiple plasmids, but for now it would be better to run the protocol for 1 plasmid, swapping out and rerunning as needed

GrowthMediaVolume = 150                                                                                 # Specify the volume of growth media required in ul

P300 = P300(200, 200, Tiprack200uL)                                                                     # Pipette Function, imported from the OT2 Functions.py script
P10 = P10(10, 10, Tiprack10uL)                                                                          # Same as above, inputs are: Aspirate rate, Dispense rate and Tiprack respectively

#########################################################################################
#########################################################################################
                                                                                                                            # Variables are case sensitive
Plasmid1_wells = [Compcells.cols['B']['2':'11':2] + Compcells.cols['C']['2':'11':2] + Compcells.cols['D']['2':'11':2]       # Prevents the use of outside rows and columns, wells to add plasmid 1 to
              + Compcells.cols['D']['2':'11':2] + Compcells.cols['E']['2':'11':2] + Compcells.cols['F']['2':'11':2]]        # Specify the target wells that you want to have bacterial aliquots in
                                                                                                                            # Change Compcells to match whatever the container with the competent cells is called, Line 15
Plasmid2_wells = []                                                                                                         # The letter specifies the column, the numbers specify the range i.e 2 to 11, the third number specifies steps, 2 to 11 in steps of 2
                                                                                                                            # Additional List can be added, but these list need to be included in the All_wells array

All_wells = [Plasmid1_wells, Plasmid2_wells]                                                                                # Creates an array from the lists of wells. More lists can be declared and added to this array
                                                                                                                            # By adding in another variable to this section a second list for cells requiring a different plasmid can be used
                                                                                                                            # A third variable would be needed to house both lists and could be used to iterate through the loops with each smaller list being for each plasmid, biglist = [list1,list2], biglist[0]
#All_Wells = Randomizer(All_wells)                                                                                          # Randomizes the wells, delete the hashtag to allow this randomizer to run. Imported from OT2_Functions

#########################################################################################
#########################################################################################

tempdeck = TempDeck()                                                                                                       # Saves the temperature deck into a variable,

temperature = {"temp1": 4, "temp2": 42, "temp3": 37}                                                                        # Saves the temperatures for the protocol into a dictionary. Dictionaries have keys and values
                                                                                                                            # The value can be called by the key i.e temperature["temp1"] = 4
if not robot.is_simulating():                                                                                               # If the robot is inactive and the temperature deck isn't processing a command
    tempdeck.connect('/dev/ttyACM0')                                                                                        # Connects to and begins cooling the temperature deck
    tempdeck.set_temperature(temperature["temp1"])                                                                          # Initialization temperature for cooling
    tempdeck.wait_for_temp()                                                                                                # Pauses the protocol until the temperature deck reaches the set temperature

target = All_wells                                                                                                          # Adds the array of wells into a variable for easier readability during manipulation
SOB_wells = [well.top(1) for well in target]                                                                                # well.top moves the pipette to the top of the well, the number specifies the distance in mm

robot.pause()                                                                                                               # Opentron command that pauses whatever the robot is doing. The user can remove and centrifuge at this point, if the need is there. resumed via the OT app
                                                                                                                            # The code below handles distributing plasmid DNA
for i in range(NumberofPlasmids):                                                                                           # Transfers plasmid DNA into competent cell aliquots. The variable NumberofPlasmids controls how many times the loop is carried out, once for each plasmid
    P10.distribute(                                                                                                         # Presumes same plasmid for all cells, adds all doses to the pipette, wells specified later in the block
        PlasmidVolume,                                                                                                      # Specifies the volume in ul
        DNA(i),                                                                                                             # Selects which plasmid to pipette based on it's position on the container declared DNA. I increases with each loop, meaning the next plasmid is selected
        target,                                                                                                             # Target is the specified wells where the plasmid is then distributed (this will not work if multiple plasmids are being used)
        blow_out=True,                                                                                                      # Empties the pipette with an extra gust of air to ensure it is fluid free
        new_tip='always'                                                                                                    # Changes the pipette after every dispense to avoid contamination
    )

robot.pause()                                                                                                               # Pauses the robot until manually resumed in the OT app
robot.home()                                                                                                                # Homes the robot, setting the pipette to the starting position
tempdeck.set_temperature(temperature["temp2"])                                                                              # Sets the temperature of the temperature deck, temperature is pulled from the temperature dictionary
tempdeck.wait_for_temp()                                                                                                    # Pauses the protocol until the temperature deck reaches the target temperature
P10.delay(seconds=100)                                                                                                      # Delays further input for 100 seconds. This allows the heating to continue for 100 seconds before setting the temp deck back to a lower temp
tempdeck.set_temperature(temperature["temp1"])                                                                              # Sets the temperature deck according to the values in the temperature dictionary
tempdeck.wait_for_temp()                                                                                                    # Pauses the protocol until the temperature deck reaches the target temperature
robot.pause()                                                                                                               # Pauses the OT2 until resumed by the user via the OT app

# Transfer Growth media
for i in range(1):                                                                                                          # Transferring in growth media for recovery
    P300.pick_up_tip(),                                                                                                     # Picks up a new tick from the previously specified tip source
    P300.transfer(                                                                                                          # Transfer combines all the uptake into a single pipette and that is used to transfer the contents of a well
        GrowthMediaVolume,                                                                                                  # GrowthMediaVolume is specified towards the start of the script
        SOB('A1'),
        SOB_wells,                                                                                                          # Is 1mm above the top of the wells contained in target, which is every single well, as every well wants growth media
        blow_out=True,                                                                                                      # Blow out uses an extra gust of air to make sure that the pipette is empty
        new_tip='once'                                                                                                      # Picks up a new pipette tip for the run but then keeps the same one for each well
    )                                                                                                                       # The loop can eb adjusted to use multiple medias but it is probably better to run the protocol multiple times instead, substituting the medias for each run
tempdeck.set_temperature(temperature["temp3"])                                                                              # Temperature for incubation, taken from the temperature dictionary
tempdeck.wait_for_temp()                                                                                                    # Pauses the protocol until the temperature deck reaches the target temperature

robot.comment("Protocol Finished")                                                                                          # Informs the user the protocol has finished via a message on the Opentrons app