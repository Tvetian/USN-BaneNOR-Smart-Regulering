#Validering av simulering av jernbanenettet 

import numpy as np
import cmath

f = 50/3
resistans_tog_1 = 108 #ohm
induktans_tog_1 = 0.637*2*np.pi*f*1j #ohm
resistans_tog_2 = 150.5 #ohm
induktans_tog_2 = 0.17762*2*np.pi*f*1j #ohm


resistans_sektor_A = 0.718  #lengde_sektor_A*resistans_Kjoreledning #[ohm*km]
induktans_sektor_A = (2*np.pi*f*0.00724*1j)#lengde_sektor_A*Induktans_Kjoreledning #[H*km]

resistans_sektor_B =  9.28 #lengde_sektor_B*resistans_Kjoreledning #[ohm*km]
induktans_sektor_B = (2*np.pi*f*0.0936*1j) #lengde_sektor_B*Induktans_Kjoreledning #[H*km]


Z_tog_1 =  resistans_tog_1 + induktans_tog_1 #ohm
Z_tog_2 =  resistans_tog_2 + induktans_tog_2 #ohm
Z_L_A = resistans_sektor_A + induktans_sektor_A   #ohm
Z_L_B = resistans_sektor_B + induktans_sektor_B #resistans_sektor_B  + (induktans_sektor_B)*1j   #ohm
Z_L_C = 7.2 + 0.0726*2*np.pi*f*1j #resistans_Kjoreledning*lengde_sektor_C + (lengde_sektor_C*Induktans_Kjoreledning)*1j   #ohm
Z_L_D = 7.2 + 0.0726*2*np.pi*f*1j  #resistans_Kjoreledning*lengde_sektor_D + (lengde_sektor_D*Induktans_Kjoreledning)*1j   #ohm


G_1_spenning_RMS = 16000 #volt
G_2_spenning_RMS = 16000 #volt
G_3_spenning_RMS = 16000 #volt

G_1 = G_1_spenning_RMS*np.sqrt(2)*np.cos((-27)*(2*np.pi/360)) + G_1_spenning_RMS*np.sqrt(2)*np.sin((-27)*(2*np.pi/360))*1j
G_2 = G_2_spenning_RMS*np.sqrt(2)*np.cos((-27)*(2*np.pi/360)) + G_2_spenning_RMS*np.sqrt(2)*np.sin((-27)*(2*np.pi/360))*1j
G_3 = G_3_spenning_RMS*np.sqrt(2)*np.cos((-27)*(2*np.pi/360)) + G_3_spenning_RMS*np.sqrt(2)*np.sin((-27)*(2*np.pi/360))*1j


#Matrise 3x3:

matrise_A = np.array([[-(Z_L_A + Z_tog_1), Z_tog_1, 0,0],
                     [Z_tog_1,-(Z_tog_1+Z_L_B), 0,0],
                     [0,0,Z_L_C+Z_tog_2,-Z_tog_2],
                     [0,0,Z_tog_2,-(Z_tog_2 + Z_L_D)]])


matrise_b = np.array([[-G_1],[G_2],[G_2],[G_3]])

# Løsning I_1, I_2, I_3, I_4

løsning = np.linalg.solve(matrise_A, matrise_b)


# Løsning generator positiv retning oppover
I_generator_1 = (løsning[0])
I_generator_2 = (løsning[2])-(løsning[1])
I_generator_3 = -(løsning[3])

# Løsning last positiv retning nedover
I_last_1 =(løsning[0])-(løsning[1])
I_last_2 = (løsning[2])-(løsning[3])

# Aktiv og reaktiv effekt


# Polarform
I_generator_1 = abs(I_generator_1), cmath.phase(I_generator_1) #abs, rad
I_generator_2 = abs(I_generator_2), cmath.phase(I_generator_2) #abs, rad
I_generator_3 = abs(I_generator_3), cmath.phase(I_generator_3) #abs, rad
I_last_1  = abs(I_last_1 ), cmath.phase(I_last_1 ) #abs, rad 
I_last_2  = abs(I_last_2 ), cmath.phase(I_last_2 ) #abs, rad 

print("strøm i generator 1:", round(float(I_generator_1[0]), 2), "<", round(float(I_generator_1[1])*(360/(2*np.pi)), 2), "grader")
print("strøm i generator 2:", round(float(I_generator_2[0]), 2), "<", round(float(I_generator_2[1])*(360/(2*np.pi)), 2), "grader")
print("strøm i generator 3:", round(float(I_generator_3[0]), 2), "<", round(float(I_generator_3[1])*(360/(2*np.pi)), 2), "grader")
print("strøm i last 1:",        round(float(I_last_1[0])/np.sqrt(2), 2), "<",        round(float(I_last_1[1])*(360/2*np.pi), 2), "grader")
print("strøm i last 2:",        round(float(I_last_2[0])/np.sqrt(2), 2), "<",        round(float(I_last_2[1])*(360/2*np.pi), 2), "grader")

      
      
      