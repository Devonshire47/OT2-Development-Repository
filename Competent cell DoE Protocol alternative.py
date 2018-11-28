# Author(s): Matt Burridge, Alex Laverick
# Last modified: 11:35, 22/10/18
# Python 3.6.4
# Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp #

#####################################################################################################################################
# The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces


from opentrons import labware, instruments, robot, modules  # Import all Opentrons API
from sqlite3 import IntegrityError                          # Import sqlite3 for custom container support


tiprack200_1 = labware.load('tiprack-200ul', slot='9')      # Import labware
tempdeck = modules.load('tempdeck', slot='7')               # Saves the temperature deck as a variable
Compcells1 = labware.load('96-flat', slot='7', share=True)  # Declares a 96 well flat container as a variable, share allows a module to share the slot
trash = robot.fixed_trash                                   # Declares the trash container on the fixed trash position of the work surface in the OT2
Culture = labware.load('duran_100', slot='4')               # Declares a custom duran_100 container from the Labware
Buffers = labware.load('96-deep-well', slot='3')            # Declares a 96 deep well plate as a variable

P300 = instruments.P300_Single(																# Import Pipette, set aspiration/dispense rates and equip with rack 
    mount='right',
    aspirate_flow_rate=200,
    dispense_flow_rate=200,
    tip_racks=[tiprack200_1],
    trash_container=trash
)

NumberofCultures = 1                                        # Declares the number of cultures being used in the protocol
CultureVolume = 200                                         # Sets the volume of the cultures
NumberofWashes = 1                                          # Sets the number of wash steps to be used in the protocol
VolumeofWashBuffer = 100                                    # Sets the volume of wash buffer to be used in the wash steps


#########################################################################################
#########################################################################################


target_temperature = 4  # Specifies TempDeck temperature, 4 degrees is best for this protocol

Even_wells = [Compcells1.rows['B']['2':'11':2] + Compcells1.rows['C']['2':'11':2] + Compcells1.rows['D']['2':'11':2]       # Prevents the use of outside rows and columns, wells to add plasmid 1 to
              + Compcells1.rows['D']['2':'11':2] + Compcells1.rows['E']['2':'11':2] + Compcells1.rows['F']['2':'11':2]]    # Specify the target wells that you want to have bacterial aliquots in

Buffers_positions = Buffers.wells('A1', length=25)                                                                      # Specify the buffer positions, change length=25 to whatever the number of buffers you have, eg if 15 buffers length=15


#########################################################################################
#########################################################################################
# BELOW IS CODE FOR THE PROTOCOL
# IF WORKING WITH E. COLI, BELOW IS A OPTIMAL PROTOCOL THAT ONLY REQUIRES 1 WASH STEP
# IF INVESTINGATING DIFFERENT INCUBATION TIMES, ALTER P300 DELAYS
# IF WANTING TO CHANGE TEMPDECK ON CONSTANTLY, REMOVE ALL tempdeck.disengage() AND PLACE BEFORE
# FINAL ROBOT COMMENT

if not robot.is_simulating():                                                                                               # Cannot use while simulating, the OT2 needs to be inactive for this statement to be carried out
    tempdeck.set_temperature(target_temperature)                                                                            # Sets the temperature to whats specified as target_temperature
    tempdeck.wait_for_temp()                                                                                                # Pauses the protocol until the temperature deck reaches the target temperature

target1 = Even_wells                                                                                                        # Saves the wells specified earlier, in the array, as a variable

robot.home()                                                                                                                # Resets the position of the pipette to the starting location
robot.pause()                                                                                                               # Pauses the OT2 untiled resumed via the OT app
robot.comment("Make sure that centrifuge has been chilled down to 4*C and all buffers are on ice.")                         # Causes the Opentron to produce a message, statin what is in the brackets
robot.comment(
    "All plates should be chilled at the beginning and culture should be incubated on ice for 15 minutes before start.")    # Sames as above
robot.comment("Once at set temperature, insert culture into slot 6 and plate onto TempDeck, then resume!")                  # Same as above

# bacterial culture							           # This is the first step of protocol, 200 uL bacterial culture at OD 0.4-0.6
for i in range(NumberofCultures):                      # Iterates through the number of cultures, dispensing reagents to specified wells
    P300.pick_up_tip()                                 # The Opentron picks up a new tip for each culture
    P300.transfer(                                     # The Opentron transfers the culture media via a single pipette
        CultureVolume,                                 # Uses the variable declared earlier as the source of the volume to be dispensed to each well
        Culture(i),                                    # Declares the container where the culture is located (and by extension what is to be dispensed)
        target1,                                       # Sets the wells to be dispensed to
        blow_out=True)                                 # After each dispensing of fluid, The Opentron uses an extra gust of air to clear out the pipette
    robot.comment("Time to centrifuge your cultures")  # Pause to allow time for bacteria to be pelleted via centrifuge
    robot.pause()                                      # Pauses the Opentrons until the process is resumed manually via the OT2 app

# Wash Aliquot
for i in range(NumberofCultures):                      # Loops through the cultures again
    P300.pick_up_tip()                                 # The Opentron picks up a new tip for each culture application
    P300.transfer(                                     # Transfers the culture to each well
        CultureVolume,                                 # Sets the volume for the culture using the variable declared earlier
        target1,                                     # Sets the target wells for the culture using the variable where the array is stored
        Culture('A1').top(-27),                        # Allocates the container where the culture is pulled from. .top sets the distance of the pipette tip from the top of the well before dispensing
        blow_out=True)                                 # After dispensing the Opentron blows an extra gust of air to clear out the pipette tip
    P300.drop_tip()                                    # Drops the pipette tip after dispensing to a well, picking up a new tip after due to the loop

    P300.pick_up_tip()                                 # The Opentrons picks up a new pipette tip
    P300.transfer(                                     # Specified reagents are transferred to the target wells, specified earlier in the array
        VolumeofWashBuffer,                            # The volume of the wash buffer to be added to the wells, declared earlier
        Buffers_positions,                             # Positions of the wash buffers to be used, specified earleir in the script
        target1,                                     # Target wells to receive the wash buffer
        mix_after=(5, 100),                            # Mix the well after pippetting. The fist number indicates the number of mixes the second represents the volume i.e. mix 5 times, aspirating and dispensing 100ul
        new_tip='always')                              # Always equip a new tip after mixing
    robot.comment(
        "Time to incubate your cultures")              # Produces a comment from the Opentron providing instruction to the user
    robot.comment("Time to centrifuge your cultures")  # same as above
    robot.pause()                                      # Pauses the Opentron until resumed by the user via the Opentron app
                                                       # Can be frozen or used immediately depending on your wash buffer

tempdeck.deactivate()                                  # Deactivates the temperature deck at the end of the protocol
robot.comment("Protocol Finished")                     # Produces a comment that informs the user that the protocol has been completed
