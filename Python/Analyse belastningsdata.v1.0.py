# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 10:17:17 2025

Program for å gjennomgå spesifikke CSV-filer fra Bane Nor med data fra omformerstasjoner.

@author: Johannes Børte, Håkon Tveitan, Kim Norborg
"""
import time
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()

#Lese inn filer direkte
fil_etter = r""#Lim inn filbane
fil_før = r""#Lim inn filbane
omformerstasjons_nummer = "" #Sett inn egenvalgt stasjonsnummer
utskrifts_navn = "Omf_st_"+str(omformerstasjons_nummer)

#Opprette dataframe
def opprette_dataFrame(fil):
    belastningsdata = pd.read_csv(fil,
                     header = 0,
                     names = ["tid", "UTC","Generator_1", "Generator_2", "Trafo_1", "Trafo_2"],
                     usecols = [0, 2, 3, 4, 5],
                     dtype = {
                         'Generator_1':'float32',
                         'Generator_2':'float32',
                         'Trafo_1': 'float32',
                         'Trafo_2': 'float32'})

    #Nye kolonner i tabell
    belastningsdata["Drift generator_1"] = False
    belastningsdata["Tomgang generator_1"] = False
    belastningsdata["Start generator_1"] = False

    belastningsdata["Drift generator_2"] = False
    belastningsdata["Tomgang generator_2"] = False
    belastningsdata["Start generator_2"] = False
    """belastningsdata_etter = np.loadtext()"""
    belastningsdata = belastningsdata.sort_values(by = 'tid')

    #lage kolonne med ukenummer for fremtidig plott
    belastningsdata['tid'] = pd.to_datetime(belastningsdata['tid'], errors='coerce')
    belastningsdata['ukenummer'] = belastningsdata['tid'].dt.isocalendar().week
    belastningsdata['årstall'] = belastningsdata['tid'].dt.isocalendar().year
    return belastningsdata

belastningsdata_før = opprette_dataFrame(fil_før)
belastningsdata_etter = opprette_dataFrame(fil_etter)


#lengde av dataframe
lengde_belastningsdata_før = len(belastningsdata_før)
lengde_belastningsdata_etter = len(belastningsdata_etter)


#simuleringsparameter
ts = 60 #tidsskritt i sekunder fra CSV


#Driftsparameter

tomgang = 0.2 # Kriterie for å være i tomgang
av = 0.02 # Kriterie for å være av

#Opptellingsparamenter før
tomgang_tid_generator_1_før = 0
drift_tid_generator_1_før = 0
av_tid_generator_1_før = 0
antall_starter_generator_1_før = 0
tomgang_tid_generator_2_før = 0
drift_tid_generator_2_før = 0
av_tid_generator_2_før = 0
antall_starter_generator_2_før = 0

#Opptellingsparamenter etter
tomgang_tid_generator_1_etter = 0
drift_tid_generator_1_etter = 0
av_tid_generator_1_etter = 0
antall_starter_generator_1_etter = 0
tomgang_tid_generator_2_etter = 0
drift_tid_generator_2_etter = 0
av_tid_generator_2_etter = 0
antall_starter_generator_2_etter = 0

#Omformersystem 
#Sjekk om status er av, på eller tomgang

def status_omformere(dataFrame, lengde_dataFrame, tidskritt, systemnummer):
    tomgang_tid_generator = 0
    drift_tid_generator = 0
    av_tid_generator = 0
    for i in range(0, lengde_dataFrame):
        
        if((abs(dataFrame.at[i,"Trafo_"+str( systemnummer)])< tomgang) and (abs(dataFrame.at[i,"Trafo_"+str( systemnummer)]) > av)):
            
            tomgang_tid_generator = tomgang_tid_generator + tidskritt
            dataFrame.at[i,"Tomgang generator_"+str( systemnummer)] = True
            
            drift_tid_generator= drift_tid_generator+ tidskritt
            dataFrame.at[i,"Drift generator_"+str( systemnummer)] = True
            
        elif(abs(dataFrame.at[i,"Trafo_"+str( systemnummer)]) < av):
            
            av_tid_generator = av_tid_generator + tidskritt
            
        else:
            drift_tid_generator= drift_tid_generator+ tidskritt
            dataFrame.at[i,"Drift generator_"+str( systemnummer)] = True
        
    return tomgang_tid_generator, drift_tid_generator, av_tid_generator

tomgang_tid_generator_1_før, drift_tid_generator_1_før, av_tid_generator_1_før =status_omformere(belastningsdata_før, lengde_belastningsdata_før, ts,1)
tomgang_tid_generator_2_før, drift_tid_generator_2_før, av_tid_generator_2_før =status_omformere(belastningsdata_før, lengde_belastningsdata_før, ts,2)

tomgang_tid_generator_1_etter, drift_tid_generator_1_etter, av_tid_generator_1_etter =status_omformere(belastningsdata_etter, lengde_belastningsdata_etter, ts,1)
tomgang_tid_generator_2_etter, drift_tid_generator_2_etter, av_tid_generator_2_etter =status_omformere(belastningsdata_etter, lengde_belastningsdata_etter, ts,2)





#Antall starter generatorer 
def antall_starter_omformere(dataFrame, lengde_dataFrame,  systemnummer):  
    antall_starter = 0     
    for i in range(5,lengde_dataFrame):
        if ((dataFrame.at[i,"Drift generator_"+str( systemnummer)] == True) and
            (dataFrame.at[i-1, "Drift generator_"+str( systemnummer)] == False) and
            (dataFrame.at[i-2, "Drift generator_"+str( systemnummer)] == False) and
            (dataFrame.at[i-3, "Drift generator_"+str( systemnummer)] == False) and
            (dataFrame.at[i-4, "Drift generator_"+str( systemnummer)] == False) and
            (dataFrame.at[i-5, "Drift generator_"+str( systemnummer)] == False) 
            ):
            antall_starter =  antall_starter +1
            dataFrame.at[i,"Start generator_"+str( systemnummer)] = True
    
    return antall_starter

antall_starter_generator_1_før = antall_starter_omformere(belastningsdata_før, lengde_belastningsdata_før, 1)
antall_starter_generator_2_før = antall_starter_omformere(belastningsdata_før, lengde_belastningsdata_før, 2)

antall_starter_generator_1_etter = antall_starter_omformere(belastningsdata_etter, lengde_belastningsdata_etter, 1)
antall_starter_generator_2_etter = antall_starter_omformere(belastningsdata_etter, lengde_belastningsdata_etter, 2)





#Totalforbruk
totalforbruk_før = belastningsdata_før.groupby("ukenummer")[["Trafo_1", "Trafo_2"]].sum().sum(axis=1).sum()
forbruk_MWh_før = (totalforbruk_før/60)
totalforbruk_etter = belastningsdata_etter.groupby("ukenummer")[["Trafo_1", "Trafo_2"]].sum().sum(axis=1).sum()
forbruk_MWh_etter = (totalforbruk_etter/60)

generator_før = belastningsdata_før.groupby("ukenummer")[["Generator_1", "Generator_2"]].sum().sum(axis=1).sum()
generator_etter = belastningsdata_etter.groupby("ukenummer")[["Generator_1", "Generator_2"]].sum().sum(axis=1).sum()

#Skriving av variabler til txt-fil
def save_variable_explorer(filename="variables.txt"):
    import datetime
    currentDate = datetime.datetime.now()
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Variable Explorer Dump - {currentDate}\n")
        file.write("=" * 50 + "\n\n")
        
        for var_name, var_value in globals().items():
            # Hopp over innebygde variabler/moduler
            if var_name.startswith("__") or callable(var_value) or isinstance(var_value, type):
                continue
            
            file.write(f"Variable: {var_name}\n")
            file.write(f"Type: {type(var_value)}\n")
            
            if isinstance(var_value, pd.DataFrame):
                file.write(f"Shape: {var_value.shape}\n")
                
                # Hvis DataFrame har en TIMESTAMP-kolonne, skriv ut tidsrommet
                if "tid" in var_value.columns:
                    min_time = var_value["tid"].min()
                    max_time = var_value["tid"].max()
                    file.write(f"Time Range: {min_time} - {max_time}\n")
                
                file.write(f"Columns: {list(var_value.columns)}\n")
                file.write(f"Head:\n{var_value.head()}\n")

            elif isinstance(var_value, (dict, list, set, tuple)):
                file.write(f"Length: {len(var_value)}\n")
                file.write(f"Content (preview): {str(var_value)[:500]}\n")  # Begrens lengde
                
            else:
                file.write(f"Value: {var_value}\n")
            
            file.write("\n" + "-" * 50 + "\n\n")
    

    print(f"Variabler lagret til {filename}")

# Lagrer variablene i txt-fil.    
save_variable_explorer(utskrifts_navn)    

#Summering av ukentlige effektforbruk MWh for plotting, axis=1 :summerer radvis 
ukentlig_forbruk_før = belastningsdata_før.groupby("ukenummer", sort=False)[["Trafo_1", "Trafo_2"]].sum().sum(axis=1)
ukentlig_forbruk_før = (ukentlig_forbruk_før/60) # Dele opp i MWA

ukentlig_forbruk_etter = belastningsdata_etter.groupby("ukenummer",sort=False)[["Trafo_1", "Trafo_2"]].sum().sum(axis=1)
ukentlig_forbruk_etter = (ukentlig_forbruk_etter/60) # Dele opp i MWA


#Plot av effekt trafo
plt.close ('all')
plt.figure (figsize=(12,6)) # Størrelse plot


plt.plot (ukentlig_forbruk_før.values, label = 'Forbruk før', color = 'red', linestyle='-', linewidth=2) 
plt.plot (ukentlig_forbruk_etter.values, label = 'Forbruk etter', color = 'blue', linestyle='-', linewidth=2) 

plt.title('Ukentlig forbruk')
plt.grid()
plt.legend()
plt.xlabel ('uke')
plt.ylabel ('MWh')
plt.xticks(range(0,len(ukentlig_forbruk_før))) # Inndeling av X-aksen
plt.savefig('Ukentlig forbruk.pdf')
plt.show ()

print(f"Driftstimer generatorer etter:{(drift_tid_generator_1_etter+ drift_tid_generator_2_etter)/3600}timer")
print(f"Driftstimer generatorer før:{(drift_tid_generator_1_før+ drift_tid_generator_2_før)/3600}timer")
print(tomgang_tid_generator_1_etter/3600)
print(tomgang_tid_generator_1_før/3600)

print(f"Tomgang generatorer:{(tomgang_tid_generator_1_etter+tomgang_tid_generator_2_etter)/3600}timer")

end_time = time.time()
print(f"Tid brukt: {end_time - start_time:.4f} sekunder")

# Skriv ut resultatet
print(ukentlig_forbruk_før)
print(ukentlig_forbruk_etter)


