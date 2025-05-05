import numpy as np
import matplotlib.pyplot as plt

R=0.14*80# Resistanse i kabelen
X=0.20*80#induktanse i kabelen 
U_A=15
U_B=15
s_A=0
s_B=0
n=18


x = np.arange(13,n+1)

q=[]
p=[]



for i in range (13,n+1):
    
    P=( R*(i**2-i*U_B*np.cos(s_A-s_B))  +X*i*U_B*np.sin(s_A-s_B) ) / (R**2+X**2)
    
    Q=( X*(i**2-i*U_B*np.cos(s_A-s_B))  -R*i*U_B*np.sin(s_A-s_B) ) / (R**2+X**2)
    
    q.append(Q)
    
    p.append(P)


plt.title("Effektoverføring A til B")
plt.plot(x,p,label ="P")
plt.plot(x,q,label ="Q")
plt.xlabel('Spenning Generator A [kV]')
plt.ylabel('Effekt overført [MW]/]MVAr]')
plt.grid()
plt.legend()