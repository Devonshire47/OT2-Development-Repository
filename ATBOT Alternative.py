# Author(s): Matt Burridge, Joshua Loh, Alex Laverick
# Last modified: 11:37, 06/08/18
# Python 3.6.4
# Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
# The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces
# SOB = Super Optimal Broth

from opentrons import labware, instruments, robot, modules  # Import Opentrons Api
from sqlite3 import IntegrityError                          # Import sqlite IntegrityError for any custom containers
from opentrons.drivers.temp_deck import TempDeck            # Import TempDeck driver for usable temp deck
from OT2_Functions import *

tiprack_3001 = labware.load("opentrons-tiprack-300ul", slot='8')  # Assigns a 300ul tip rack container to the variable tiprack_3001
tiprack_3002 = labware.load("opentrons-tiprack-300ul", slot='9')  # Assigns a 300ul tip rack to the variable tiprack_3002
tiprack_10 = labware.load("tiprack-10ul", slot='11')              # Assigns a 10ul tip rack to the variable tiprack_10
Buffers1 = labware.load("Universals_Cold_Box", slot='2')          # Assigns a custom container, universals cold box, to the variable Buffers1
Buffers2 = labware.load("Universals_Cold_Box", slot='5')          # Assigns a custom container, universals cold box, to the variable Buffers2
Buffers = labware.load("96-deep-well", slot='3', share=True)      # Assigns a 96 deep well plate to the variable Buffers, share allows a module in the slot as well, make sure to calibrate the deck accordingly
Compcells1 = labware.load('96-flat', slot='6')                    # Assigns a 96 well flat plate to the variable Compcells1
Culture = labware.load('duran_100', slot='4')                     # Assigns a custom container, Duran 100 to the variable Culture
DNA = labware.load('tube-rack-2ml', slot='10')                    # Assigns a tube rack 2ml container to the variable DNA
SOB = labware.load('duran_100', slot='7')                         # Assigns a custom duran 100 container to the variable SOB
tempdeck = modules.load('tempdeck', slot='3')                     # Connects the Tempdeck module to OT2 into a slot, the slot can be shared (share = True, only needs to be done on one declaration?)

trash = robot.fixed_trash                                         # Standard declaration of the trash area for the OT2

P300 = P300(200, 200, [tiprack_3001, tiprack_3002])               # Imports the P300() Function from the script OT2_Functions.py, setting the aspirate and dispense rate as well as tip racks respectively

P10 = P10(5, 5, tiprack_10)                                       # Imports the P10() function fromt he script OT2_Functions.py, setting the aspirate and dispense rate as well as tip racks respectively

#########################################################################################
#########################################################################################
reagents1 = [  # Input volumes, ul,  in list within a list must have no whitespaces
    [40, 0, 0, 40, 40, 40, 0, 40, 0, 0, 0, 40, 0, 40, 0, 40, 20, 40, 40, 0, 20, 40, 0, 20, 0],
    [40, 7.5, 7.5, 40, 7.5, 7.5, 7.5, 7.5, 40, 40, 23.75, 7.5, 7.5, 7.5, 40, 40, 23.75, 40, 23.75, 7.5, 7.5, 40, 40, 40,
     40],
    [5, 5, 5, 0, 0, 5, 0, 0, 5, 2.5, 0, 5, 5, 2.5, 0, 0, 2.5, 5, 5, 0, 0, 0, 5, 5, 0],
    [40, 20, 0, 0, 40, 0, 40, 0, 40, 0, 40, 40, 40, 40, 40, 20, 20, 0, 0, 0, 0, 40, 0, 40, 0],
    [0, 0, 0, 0, 0, 20, 40, 40, 0, 40, 0, 40, 40, 0, 20, 40, 20, 0, 40, 40, 0, 40, 40, 40, 0],
    [0, 40, 0, 40, 20, 40, 40, 0, 40, 0, 0, 0, 0, 40, 0, 0, 20, 0, 40, 40, 0, 40, 20, 40, 40],
    [0, 0, 12, 0, 12, 0, 0, 6, 6, 0, 0, 0, 12, 12, 12, 12, 6, 12, 12, 12, 0, 0, 0, 12, 12],
    [100, 0, 100, 50, 0, 100, 100, 100, 0, 0, 100, 0, 50, 100, 0, 100, 50, 0, 0, 0, 0, 0, 100, 100, 100]
]

reagent_pos1 = [Buffers1['A']['1':'6':2] + Buffers1['B']['2':'6':2] + Buffers1['C']['1':'6':2]]  # MgCl2, CaCl2, KOAc, MnCl2, RbCl2, NiCl2, Hexamine, KCl
#  Specify reagent positions, 1st list within list equates to first position in reagent_pos list

reagents2 = [  # Input volumes, ul, in list within a list must have no whitespaces
    [50, 50, 150, 150, 150, 150, 100, 50, 150, 150, 150, 150, 50, 50, 50, 150, 100, 100, 50, 150, 50, 50, 50, 150, 50],
    [25, 50, 0, 0, 50, 50, 0, 50, 0, 50, 50, 0, 50, 0, 0, 0, 25, 50, 0, 25, 0, 50, 0, 50, 50],
    [100, 100, 100, 100, 100, 0, 100, 100, 0, 100, 0, 50, 0, 0, 100, 0, 50, 0, 100, 0, 0, 0, 0, 100, 50],
    [100, 227.5, 125.5, 80, 80.5, 87.5, 72.5, 106.5, 219, 117.5, 136.25, 167.5, 245.5, 208, 238, 98, 162.75, 253,
     189.25, 225.5, 422.5, 200, 245, 0, 158]
]

reagent_pos2 = ['A1', 'A3', 'A5','B2']  # DMSO, HEPES, PEG8000, water. Specify reagent positions, 1st list within list equates to

Even_wells = [Compcells1.cols['B']['2':'11':2] + Compcells1.cols['C']['2':'11':2] + Compcells1.cols['D']['2':'11':2]       # Prevents the use of outside rows and columns
              + Compcells1.cols['D']['2':'11':2] + Compcells1.cols['E']['2':'11':2] + Compcells1.cols['F']['2':'11':2]]


Buffers_positions = Buffers.wells('A1', length=25)

TargetTemp = {"temp":4, "temp1": 4, "temp2": 42, "temp3": 37}  # Specifies the temperatures for heat sensitive processes such as heat shock


#########################################################################################
#########################################################################################

def sort(x, y, z, q):                               # This function determines which is the most accurate pipette to use based on the volume to be dispensed, it also tracks which reagent to use in which well
    if y == 0:                                      # Checks if it is the first position of a reagent list, if it is this is a new reagent and needs a new pipette
        global source                               # Calls the source variable from the global environment
        source = reagent_pos1[q]                    # Sets source as the location for the reagent to be dispensed, informing the pipettes where to aspirate from
        P300.pick_up_tip()                          # Equips the P300 with a new tip, if it does not have a tip
        P10.pick_up.tip()                           # Equips the P10 with a new tip, if it does not have a tip
    if x == float(0):                               # Checks if the volume to be dispensed is 0
        pass                                        # If the volume to be dispensed is 0 the step is skipped
    elif x < float(30):                             # Checks if the volume to be dispensed is less than 30 but greater than 0
        P10.distribute(                             # If the volume to be dispensed is less than 30, the P10 is selected for dispensing
            x,                                      # Sets the volume to be dispensed, in this case the value stored in x
            Buffers1(source),                       # Identifies which position in which container to aspirate from (container Stock1, position in the source variable)
            Buffers(y).top(0.5),                    # Sets which wells to dispense into, container well_buffers96 position stored in variable y, as well as the height to aspirate from
            blow_out=True,                          # After aspirating the Opentrons will aspirate a gust of air to clear out the pipette tip of fluid
            rate=1,                                 # Sets the rate for aspirating, if using viscous fluids lower this to 0.5 for accuracy
            new_tip='never')                        # If set to never, the same tip will be used to aspirate the reagent to every well
        P10.touch_tip(Buffers(y))                   # With this option declared the pipette tip will be touched to the top of each well after aspirating
        P10.blow_out(Buffers(y))                    # Sets another blow out of the pipette
    else:                                           # If the volume to be dispensed is greater than 30
        P300.distribute(                            # Sets the pipette to be used as the P300 instead of the P10
            x,                                      # Allocates X as the volume to be dispensed
            Buffers1(source),                       # Identifies the well position in the container to aspirate from (container Stock1 well position stored in source)
            Buffers(y).top(0.5),                    # Sets which wells to dispense to, container well_buffers96 well position stored in y, also sets the height to aspirate from
            blow_out=True,                          # Assigns a blow out after dispensing reagents to clear the pipette tip of fluid
            rate=1,                                 # Sets the dispensing rate of the pipette, set this to 0.5 if using a viscous fluid
            new_tip='never')                        # With this option declared the Opentron will not pick up a new pipette until explicitly instructed
        P300.touch_tip(Buffers(y))                  # With this option declared the pipette tip will be touched to the top of the wells after pipetting
        P300.blow_out(Buffers(y))                   # assigns another blow out, dispensing a gust of air after dispensing to clear the pipette tip of fluid
    if y == len(z) - 1:                             # Checks if the end of the reagent list has been reached, Python lists start at 0 so y will only ever reach 5 in a list fo 6 elements len(z) needs to have 1 subtracted
        P300.drop_tip()                             # Disposes of the tip on the P300
        P10.drop_tip()                              # Disposes of the tip on the P10


robot.home()                                        # Returns the Opentron pipette to the starting location
source = 0                                          # Source is declared as an empty variable so it can track reagent position from the sort() function

[[sort(values, well_counter, reagent, counter) for well_counter, values in enumerate(reagent)]for counter, reagent in enumerate(reagents1, 0)]  # Unless you change the name of reagents1, you will never need to alter this line
# The line above executes the entire protocol, iterating through the reagent lists and destinations, as such it shouldn't need to be adjusted unless the reagent list names change

#########################################################################################
#########################################################################################
# COMPETENT CELLS


if not robot.is_simulating():                     # If the OT2 is currently not heating something
    tempdeck.set_temperature(TargetTemp["temp"])  # Sets the temperature to the value in the TargetTemp dictionary with key temp
    tempdeck.wait_for_temp()                      # Pauses the protocol until the temperature deck reaches the desired temperature

target1 = Compcells1(Even_wells)                  # Assigns the wells of Compcells1 as the target1 variable

robot.home()                                                                                                              # Returns the OT2 to the starting position
robot.comment("Make sure that centrifuge has been chilled down to 4*C and all buffers are on ice.")                       # Produces a message on the OT2 display to inform the user of what the next step is
robot.comment(
    "All plates should be chilled at the beginning and culture should be incubated on ice for 15 minutes before start.")  # Produces a comment on the OT2 providing information for the next step
robot.comment("Once at set temperature, insert culture into slot 6 and plate onto TempDeck, then resume!")                # Produces a comment providing guidance to the user
robot.pause()                                                                                                             # Pauses the OT2 until the user resumes the process via the app


# bacterial culture								       # This is the first step of protocol, 200 uL bacterial culture at OD 0.4-0.6
for i in range(1):                                     # Added to 96 well plate in specified wells, Range 1 means the loop runs once. Why is this a loop????
    P300.pick_up_tip()                                 # Forces the OT2 to equip a new pipette tip to the P300
    P300.transfer(                                     # Transfers reagents from a well to destination wells
        200,                                           # Sets the volume, in ul, to be transferred by the OT2
        Culture('A1'),                                 # Sets the well to be aspirated from, the container stored in Culter, well A1
        target1(),                                     # Sets the wells to dispense to, the wells saved in target1
        blow_out=True)                                 # Activates the blow out feature, where after aspirating the OT2 dispenses an extra gust of air to ensure the pipette tip is free of fluid
    robot.comment("Time to centrifuge your cultures")  # Produces a comment in the OT2 interface informing the user of required action
    robot.pause()                                      # Pauses the OT2 until action is reactivated by the user via the OT2 app

# Wash Aliquot
for i in range(1):              # Wash step
    P300.pick_up_tip()          # Equips the P300 with a new pipette tip
    P300.transfer(              # Transfers reagents from a well to destination wells
        200,                    # Sets the volume, in ul, to be transferred
        target1(),              # Sets all the wells in target1 as the wells to be aspirated from
        Culture('A1').top(-27), # Sets the well in the container culture, well A1 as the destination well, -27 is the depth into the container dispensing occurs
        blow_out=True)          # Activates the blow out function
    P300.drop_tip()             # Forces the OT2 to unequip the tip on the P300

    P300.pick_up_tip()          # Wash buffer is added to each individual well and mixing occurs
    P300.transfer(              # to resuspend the pellet
        100,                    # Sets the volume to be transferred
        Buffers_positions,      # Sets the wells stored in Buffer_positions as the wells to aspirate from
        target1(),              # Sets the wells in target1 as the destination wells to be dispensed to
        mix_after=(5, 100),     # Mixes the well by pipetting, mixes 5 times by aspirating and dispensing 100ul
        new_tip='always')       # Equips a new tip after every well
    robot.comment(
        "Time to incubate your cultures")              # Produces a commont on the 0T2 interface to inform the user of the next step
    robot.comment("Time to centrifuge your cultures")  # See above
    robot.pause()                                      # Pauses the OT2 until reactivated by the user via the OT2 app
                                                       # Can be frozen or used immediately depending on your wash buffer


#########################################################################################
#########################################################################################
# COMPETENT CELLS

# Connects to and begins cooling
tempdeck.set_temperature(TargetTemp["temp1"])   # Sets the temperature of the temp deck to the value stored in the TargetTemp dictionary saved to the key Temp1
tempdeck.wait_for_temp()                        # Pauses the protocol until the temperature deck reaches the set temperature

target = Even_wells                             # Sets the target variable to the wells declared in Even_wells on the plate Compcells
SOB_wells = [well.top(1) for well in target()]  # Assigns the wells in target() and the distance of 1mm above them as the locations in SOB_wells

robot.pause()                                   # Pauses the OT2 until re-enabled by the user manually via the OT2 app

for i in range(1):               # Transfers plasmid DNA into competent cell aliquots
    P10.distribute(              # Sets the P10 as the pipette to distribute selected reagents
        3,                       # Dispense the volume specified, in ul
        DNA('A1'),               # Assigns the well to aspirate from, in this case the container declared as DNA, well A1
        Even_wells,              # Assigns the wells to dispense into, in this case container Compcells1, all the wells stored in Even_wells
        blow_out=True,           # After each dispension the OT2 dispenses a gust of air to ensure the pipette tip is clear of fluid
        new_tip='always'         # Sets the OT2 to equip a new tip after ever dispension to avoid decontamination
    )

robot.pause()                                  # Pauses the Opentrons until reactivated by the user via the Opentrons App
robot.home()                                   # Resets the Opentrons to the starting location
tempdeck.set_temperature(TargetTemp["temp2"])  # Sets the temperature of the temperature deck to the value in the dictionary TargetTemp, key temp2
tempdeck.wait_for_temp()                       # Pauses the protocol until the temperature deck reaches the target temperature
P10.delay(seconds=100)                         # Stops the P10 from pipetting for 100 seconds
tempdeck.set_temperature(TargetTemp["temp1"])  # Sets the temperature deck temperature to the value in the TargetTemp dictionary saved to key temp1
tempdeck.wait_for_temp()                       # Pauses the protocol until the temperature deck reaches the target protocol
robot.pause()                                  # Pauses the OT2 until re-enabled by the user through the OT2 app


for i in range(1):       # transferring in growth media for recovery, 1 because this is the total number of duran tubes we can make fit? Is there an alternative container?
    P300.pick_up_tip(),  # Forces the OT2 to equip a new tip to the P300
    P300.transfer(       # Sets the OT2 to transfer reagent material into the declared wells
        150,             # Assigns the volume, in ul, to be transferred to each well
        SOB('A1'),       # Declares which well to aspirate from, container SOB, well A1
        SOB_wells,       # Declares which wells to transfer the reagents into, Container SOB
        blow_out=True,   # Sets the OT2 to dispense an extra gust of air after each dispension to ensure no fluid is left in the tip
        new_tip='once'   # Equips a new pipette tip for each transfer refill but not each transfer
    )
tempdeck.set_temperature(TargetTemp["temp3"])  # Temperature for incubation, using the temperature saved in the TargetTemp dictionary to key temp3
tempdeck.wait_for_temp()                       # Pauses the protocol until the temperature deck reaches the set temperature
                                               # THE TEMPERATURE DECK DOES NOT DEACTIVATE UPON PROTOCOL END
robot.comment("Protocol Finished!")            # Informs the user that the protocol has completed by producing a comment in the Opentrons App

