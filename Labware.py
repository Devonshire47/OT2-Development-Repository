
from opentrons import labware, instruments, robot
from sqlite3 import IntegrityError

###################################################################################
# CREATE YOUR LABWARE BELOW
# TO LOAD LABWARE, RUN THIS CODE WITH YOUR SPECIFICATIONS
# ONCE LOADED, LABWARE WILL BE SAVED TO THE OT-2
# LOAD YOUR PROTOCOL AND THE CUSTOM LABWARE WILL BE RECOGNISED
###################################################################################
try:
    Universals_Cold_Box = labware.create(
	'Universals_Cold_Box',
	grid=(5,3),
	spacing=(25,25),
	diameter=20,
	depth=105,
	volume=20000
)

except IntegrityError:
    pass
###################################################################################

###################################################################################
# PASTE YOUR CREATED LABWARE BELOW
###################################################################################
# This did not work when I tried, may work again with update (Matt)

# Temp_96flat = Tempdeck + standard 96 well plate 
	# TempDeck_96-flat = labware.create(
	#'TempDeck_96-flat',
	#grid=(8,12),
	#spacing=(9,9),
	#diameter=6.4,
	#depth=10.5,
	#volume=400

###################################################################################
# No details, works perfectly well, just line the pipette tip a few cm above the rim
# Postion = top right corner of slot, up against ridges so stable and reproducible position

duran_100 = 100 mL duran

###################################################################################
# No details, not recommened to use apart from as microbial waste. 
# Bottle too large for pipette to reach the bottom, TEST WITHOUT IT IN PLACE BEFORE USE
# Postion = top right corner of slot, up against ridges so stable and reproducible postion 

#duran_250 = 250 mL duran

####################################################################################
# No details, 100 mL flask in a 200 mL pyrex beaker, worked well to keep microbial cultures on ice 
# During pipetting
# Postion = top right corner of slot, up against ridges so stable and reproducible position

#chilledflask_100 = 100 ml flask in 200 ml pyrex beaker for cooling


####################################################################################
# This is for 20 mL universal tubes, would recommend redoing this as the spacings are a bit off, 
# However it does work

#Universals_Cold_Box =  Universals_Cold_Box - A1 bottom left, A1, A3, A5, B2, B4, C1, C3, C5
#Universals_Cold_Box = labware.create(
	#'Universals_Cold_Box',
	#grid=(5,3),
	#spacing=(25,25),
	#diameter=20,
	#depth=105,
	#volume=20000
###################################################################################


