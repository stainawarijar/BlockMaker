# Element monoisotopic masses (amu), taken from: https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl
# Rounded to 9 decimal places
CARBON_MASS = 12.000000000
HYDROGEN_MASS = 1.007825032
OXYGEN_MASS = 15.994914620
NITROGEN_MASS = 14.003074004
SULFUR_MASS = 31.972071174


# Mass differences for some heavier stable isotopes (compared to monoisotopic mass)
C13_MASS_DIFF = 13.003354835 - CARBON_MASS 
N15_MASS_DIFF = 15.000108899 - NITROGEN_MASS 


# H2O
WATER_MASS = 2 * HYDROGEN_MASS + OXYGEN_MASS  

# -CH2-CO-NH2 group, when treating cysteines with iodo/chloro-acetamide
ACETAMIDE_GROUP_MASS = 2 * CARBON_MASS + 4 * HYDROGEN_MASS + OXYGEN_MASS + NITROGEN_MASS

# -CH2-CO-OH group, when treating cysteines with iodo/chloro-acetic acid
ACETIC_ACID_GROUP_MASS = 2 * CARBON_MASS + 3 * HYDROGEN_MASS + 2 * OXYGEN_MASS

