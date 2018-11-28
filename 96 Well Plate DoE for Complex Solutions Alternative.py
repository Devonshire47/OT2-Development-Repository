# Author(s): Matt Burridge, Joshua Loh, Alex Laverick, Alidivinas Prusokas
# Last modified: 14:00, 28/11/18
# Python 3.6.4
# Please keep the author(s) attached to the code segment for traceability, if changes are made please append the authour list and modify the timestamp

#####################################################################################################################################
# The input from the code must be in list within a list, the sublist must contain the appropriate float type value and no whitespaces


from opentrons import labware, instruments, robot                # Import Opentrons API
from sqlite3 import IntegrityError                               # Import sqlite IntegrityError for any custom containers

                                                                 # Slot refers to the position on the Opentrons workspace
tiprack_300 = labware.load("opentrons-tiprack-300ul", slot='1')  # Saves a 300ul tiprack to the variable tiprack_300
tiprack_10 = labware.load("tiprack-10ul", slot='3')              # Universals_Cold_Box = custom container for 30 mL universal tubes
Stock1 = labware.load("Universals_Cold_Box", slot='10')          # Universals_Cold_Box is a custom container, saved to the variable Stock1
Stock2 = labware.load("Universals_Cold_Box", slot='5')           # Another Universals cold box saved to the variable Stock2.
well_buffers96 = labware.load("96-flat", slot='2')               # 96 Flat well plate saved to the variable well_buffers96
trash = robot.fixed_trash                                        # Standard declaration of the trash container

P300 = instruments.P300_Single(																# Import pipette types 
	mount='right',																			# If using different pipette tips, modify float 
	aspirate_flow_rate=300,																	# and pipette commands in command block (see below)
	dispense_flow_rate=300,																	# Assign tiprack and trash, make sure aspirate/dispense speeds
	tip_racks=[tiprack_300],																# are suitable for reagent viscosity (can be further altered below)
	trash_container=trash 
)

P10 = instruments.P10_Single(                                                               # Imports the P10 command
	mount='left',                                                                           # Sets which mount the pipette is fixed to
	aspirate_flow_rate=10,                                                                  # sets the aspiration rate at ml per second
	dispense_flow_rate=10,                                                                  # Sets the dispense rate at ml per second
	tip_racks=[tiprack_10],                                                                 # Allocates where the pipette pulls tips from, the variable stores a tip rack location
	trash_container=trash                                                                   # Assigns the trash location
)

# IMPORTANT - DO NOT ASSIGN PIPETTE TIPS TO A PIPETTE THAT HAVE A SMALLER MAX VOLUME THAN PIPPET ie. P200 TIPS TO P300 PIPETTE
# WILL CAUSE CONTAMINATION AND/OR DAMAGE
# ALTER VALUES AND POSITIONS BELOW
#########################################################################################
#########################################################################################

reagents1 = [                                                                               # Input volumes in list within a list, must have no whitespaces
    	[40,7.5,40,40,7.5,40,7.5,40,7.5,40,7.5,40,0,40,0,40,20,40,40,0,20,40,0,20,0],
    	[40,7.5,7.5,40,7.5,7.5,7.5,7.5,40,40,23.75,7.5,7.5,7.5,40,40,23.75,40,23.75,7.5,7.5,40,40,40,40]
]

reagent_pos1 = [
    	'A1','A3'
]  # Specify reagent positions, 1st list within list equates to
# list sequence A1 = MgCl2 stock, A3 = CaCL2 stock											# first position in reagent_pos list

reagents2 = [                                                                               # Input volumes in list within a list must have no whitespaces
    []
]

reagent_pos2 = []  # Specify reagent positions, 1st list within list equates to
# first position in reagent_pos list

# all_reagents = [reagents1, reagents2]                                                     # Adds a randomizer that randomizers the reagent volumes with respect to the structure of the lists
# all_reagents = Randomizer(all_reagents)                                                   # This randomizer is commented out and will not run
# reagents1 = all_reagents[0]                                                               # To run the randomizer delete the # at the start of the lines so the text is no longer grey
# reagents2 = all_reagents[1]                                                               # If the randomizer is not wanted leave the # in
                                                                                            # If more than 2 reagents are being used, more lists can be added or expanded upon

#########################################################################################
#########################################################################################
# THE FOLLOWING ALLOWS FOR ALTERNATING PIPETTE USE AND THE USE OF UP TWO LABWARE CONTAINING STOCKS
# IF USING DIFFERENT LABWARE MAY NEED TO ALTER TOP/BOTTOM DISTANCE

def run(volume, well, source, num_steps):                               # This function determines which is the most accurate pipette to use based on the volume to be dispensed, it also tracks which reagent to use in which well
# source is the source location of the reagent to be dispensed, informing the pipettes where to aspirate from
    if well == 0:                                      # Checks if it is the first position of a reagent list, if it is this is a new reagent and needs a new pipette
        P300.pick_up_tip()                          # Equips the P300 with a new tip, if it does not have a tip
        P10.pick_up.tip()                           # Equips the P10 with a new tip, if it does not have a tip
    if volume == float(0):                               # Checks if the volume to be dispensed is 0
        pass                                        # If the volume to be dispensed is 0 the step is skipped
    elif volume <= float(30):                             # Checks if the volume to be dispensed is less than 30 but greater than 0
        P10.distribute(                             # If the volume to be dispensed is less than 30, the P10 is selected for dispensing
            volume,                                      # Sets the volume to be dispensed, in this case the value stored in x
            Stock1(source),                         # Identifies which position in which container to aspirate from (container Stock1, position in the source variable)
            well_buffers96(well).top(0.5),             # Sets which wells to dispense into, container well_buffers96 position stored in variable y, as well as the height to aspirate from
            blow_out=True,                          # After aspirating the Opentrons will aspirate a gust of air to clear out the pipette tip of fluid
            rate=1,                                 # Sets the rate for aspirating, if using viscous fluids lower this to 0.5 for accuracy
            new_tip='never')                        # If set to never, the same tip will be used to aspirate the reagent to every well
        P10.touch_tip(well_buffers96(well))            # With this option declared the pipette tip will be touched to the top of each well after aspirating
        P10.blow_out(well_buffers96(well))             # Sets another blow out of the pipette
    elif volume <= float(300):                                           # If the volume to be dispensed is greater than 30
        P300.distribute(                            # Sets the pipette to be used as the P300 instead of the P10
            volume,                                      # Allocates X as the volume to be dispensed
            Stock1(source),                         # Identifies the well position in the container to aspirate from (container Stock1 well position stored in source)
            well_buffers96(well).top(0.5),             # Sets which wells to dispense to, container well_buffers96 well position stored in y, also sets the height to aspirate from
            blow_out=True,                          # Assigns a blow out after dispensing reagents to clear the pipette tip of fluid
            rate=1,                                 # Sets the dispensing rate of the pipette, set this to 0.5 if using a viscous fluid
            new_tip='never')                        # With this option declared the Opentron will not pick up a new pipette until explicitly instructed
        P300.touch_tip(well_buffers96(well))           # With this option declared the pipette tip will be touched to the top of the wells after pipetting
        P300.blow_out(well_buffers96(well))            # assigns another blow out, dispensing a gust of air after dispensing to clear the pipette tip of fluid
    else:
	raise Exception('Volume should not exceed 300, the size of the largest tips. Volume was set to: {}'.format(volume))
    if well >= num_steps - 1:                             # Checks if the end of the reagent list has been reached, Python lists start at 0 so y will only ever reach 5 in a list fo 6 elements len(z) needs to have 1 subtracted
        P300.drop_tip()                             # Disposes of the tip on the P300
        P10.drop_tip()                              # Disposes of the tip on the P10


robot.home()                                        # Returns the Opentron pipette to the starting location

[[run(volume, well, reagent_pos1[reagent_num], len(reagent)) for well, volume in enumerate(reagent)] for reagent_num, reagent in enumerate(reagents1)]  # Unless you change the name of reagents1, you will never need to alter this line
# The line above executes the entire protocol, iterating through the reagent lists and destinations, as such it shouldn't need to be adjusted unless the reagent list names change

robot.comment("Protocol finished")                  # Informs the user that the protocol is complete via comment on the Opentrons
