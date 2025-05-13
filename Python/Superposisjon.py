# super posisjon

#Validering av simulering av jernbadenettet 

import numpy as np
import cmath

def parallel(Z1,Z2):
    Z_p = (Z1*Z2)/(Z1+Z2)
    return Z_p
def strømdeling(I,Z_ønsket,Z_p):
    I_delt = (I*Z_p)/(Z_ønsket+Z_p)
    return I_delt

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


#Løsning for G_1:
    
Z_t_1 = Z_L_A + parallel(Z_tog_1,Z_L_B)
I_1_1 = G_1/Z_t_1
I_tog_1_G1 = strømdeling(I_1_1,Z_tog_1,Z_L_B)

#Løsning for G_2:
Z_p1 = parallel(Z_L_A, Z_tog_1) 
Z_p2 = parallel(Z_tog_2, Z_L_D)
Z_p1_2 = Z_L_B + Z_p1
Z_p2_2 = Z_p2 + Z_L_C

Z_tot_2 = parallel(Z_p1_2,Z_p2_2)
I_G_2 = G_2/Z_tot_2
I_1_2 = strømdeling(I_G_2, Z_p1_2, Z_p2_2)
I_tog_1_G2 = strømdeling(I_1_2, Z_tog_1, Z_L_A)

I_2_2 = I_G_2 - I_1_2
I_tog_2_G2 = strømdeling(I_2_2, Z_tog_2, Z_L_D)

#Løsning for G_3 
Z_p1_3 = parallel(Z_tog_2, Z_L_C)
Z_tot_3 = Z_L_D + Z_p1_3
I_G_3 = G_3/Z_tot_3
I_tog_2_G3 = strømdeling(I_G_3,Z_tog_2, Z_L_C)

#Felles løsning for strøm til tog
I_tog_1 = I_tog_1_G1 + I_tog_1_G2
I_tog_2 = I_tog_2_G2 + I_tog_2_G3

# Aktiv og reaktiv effekt


# Polarform
I_tog_1 = abs(I_tog_1), cmath.phase(I_tog_1) #abs, rad
I_tog_2 = abs(I_tog_2), cmath.phase(I_tog_2) #abs, rad


print("strøm i last 1:",        round(float(I_tog_1[0])/np.sqrt(2), 2), "<",        round(float(I_tog_1[1])*(360/2*np.pi), 2), "grader")
print("strøm i last 2:",        round(float(I_tog_2[0])/np.sqrt(2), 2), "<",        round(float(I_tog_2[1])*(360/2*np.pi), 2), "grader")
      
      
