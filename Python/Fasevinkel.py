import numpy as np
import matplotlib.pyplot as plt

R=0.14*80
X=0.20*80
U_A=15
U_B=15
s_A=0
s_B=0

start=-15
n=21

"P1=( R*(U_A**2-U_A*U_B*np.cos(s_A-s_B))   +X*U_A*U_B*np.sin(s_A-s_B))/(R**2+X**2)"
"Q=(X*(U_A**2-U_A*U_B*np.cos(s_A-s_B)+R*U_A*U_B*np.sin(s_A-s_B)))/(R**2+X**2)"


x = np.arange(start,n)

q=[]
p=[]

valor=0.01745329 #radianes
for i in range (start,n):
    
    P=( R*(U_A**2-U_A*U_B*np.cos(i*valor-s_B))  +X*U_A*U_B*np.sin(i*valor-s_B) ) / (R**2+X**2)
    Q=( X*(U_A**2-U_A*U_B*np.cos(i*valor-s_B))  -R*U_A*U_B*np.sin(i*valor-s_B) ) / (R**2+X**2)
    
    q.append(Q)
    p.append(P)


plt.title("Fasevinkel mellom omformere")
plt.plot(x,p,label ="P")
plt.plot(x,q,label ="Q")
plt.xlabel('Vinkelforskjell mellom A og B i grader')
plt.ylabel('Effekt overført MW/MVAr')
plt.grid()
plt.legend()