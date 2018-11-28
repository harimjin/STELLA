path = '/media/harim/ELEMENTARY/snIcm7/'
modelname = '/snIcm7'



import star
import matplotlib.pyplot as plt
from matplotlib import cm 

def chem():

 import star
 import matplotlib.pyplot as plt
 import numpy

 s = star.read_file('snIcm7.abn',0)
 f = star.read_file('snIcm7.hyd',1)

 plt.plot(f[:,6], s[:, 19], 'r', label='Ni')
 plt.plot(f[:,6], s[:, 14],'m', label='S')
 plt.plot(f[:,6], s[:, 13],'b',  label='Si')
 plt.plot(f[:,6], s[:, 9],'g', label='Ne')
 plt.plot(f[:,6], s[:, 8], 'c',  label='O')
 plt.plot(f[:,6], s[:, 6], 'Brown', label='C')
 plt.plot(f[:,6], s[:, 5], 'k', label='He')
 plt.plot(f[:,6], s[:, 4], 'k',label='H')

 plt.legend(loc=(0.9, 0.6), shadow = False)
 plt.show()

contents = dict(dir = [], data = [])

def lightcurve(dir): 

 import star
 import matplotlib.pyplot as plt

 s = star.read_file(path+dir+modelname+'.tt',85) 
 
 contents["dir"].append(dir)
 Vmaxtime=0
 Vmaxmag=0
 Bmaxtime=0
 UBVRI = []
 for i in range(len(s[:,0])):
  if s[i,6] == min(s[:,6]):
   Mbol = [s[i,0],s[i,6]]
   UBVRI.append(Mbol)
  if s[i,7] == min(s[:,7]):
   U = [s[i,0],s[i,7]]
   UBVRI.append(U)   
  if s[i,8] == min(s[:,8]):
   B = [s[i,0],s[i,8]]
   Bmaxtime+=s[i,0]
   UBVRI.append(B)  
  if s[i,9] == min(s[:,9]):
   V = [s[i,0],s[i,9]]
   Vmaxtime+=s[i,0]
   Vmaxmag+=s[i,9]
   UBVRI.append(V)  
  if s[i,11] == min(s[:,11]):
   R = [s[i,0],s[i,11]]
   UBVRI.append(R)  
  if s[i,10] == min(s[:,10]):
   I = [s[i,0],s[i,10]]
   UBVRI.append(I)  
 contents["data"].append(UBVRI)
 print dir
 print "Mbol", Mbol
 print "U", U
 print "B", B
 print "V", V
 print "R", R
 print "I", I 
 
 plt.plot(s[:,0], s[:,6], 'k', label = 'Mbol', linewidth = 3)
 plt.plot(s[:,0], s[:,7], 'm', label = 'U', linewidth = 3)
 plt.plot(s[:,0], s[:,8], 'b', label = 'B', linewidth = 3)
 plt.plot(s[:,0], s[:,9], 'g', label = 'V', linewidth = 3)
 plt.plot(s[:,0], s[:,10], 'c', label = 'I', linewidth = 3)
 plt.plot(s[:,0], s[:,11], 'r', label = 'R', linewidth = 3)
# plt.xlim(0,5)
 plt.ylim(-12,-23)
# plt.xlim(-23,10)
 plt.xlabel('Epoch (days)'), plt.ylabel('Absolute magnitude')
 plt.legend(loc=(0.9, 0.6), shadow = False)
# plt.savefig('/home/harim/Pictures/'+dir+'/lightcurve.png', format='png')
 plt.show()

lst = ['1e-1 13 10','1e-1 15 25','2e-1 13 15','5e-2 14 10','1e-1 13 15','1e-2 13 10','2e-1 13 20','5e-2 14 15','1e-1 13 20','1e-2 13 15','2e-1 13 25','5e-2 14 20','1e-1 13 25','1e-2 13 20','2e-1 14 10','5e-2 14 25','1e-1 14 10','1e-2 13 25','2e-1 14 15','5e-2 15 15','1e-1 14 15','1e-2 14 10','2e-1 14 20','5e-2 15 20','1e-1 14 20','1e-2 14 15','2e-1 14 25','5e-2 15 25','1e-1 14 25','1e-2 14 20','2e-1 15 10','1e-1 15 10','1e-2 14 25','2e-1 15 15','1e-1 15 15','1e-2 15 25','2e-1 15 20','1e-1 15 20','2e-1 13 10','2e-1 15 25']





#########################






def Mbol(lst): 

 for i in range(len(lst)):
  s = star.read_file(path+lst[i]+modelname+'.tt',85) 
  plt.plot(s[:,0], s[:,6], label=lst[i],linewidth = 2, color=cm.rainbow((len(lst)-i)*1.2/float(len(lst))))
  for j in range(len(s[:,0])):
   if s[j,6] == min(s[:,6]):
    Mbol = [s[j,0],s[j,6]]
  print "For ", lst[i], ", [tamx, Mbolamx] = ", Mbol
 plt.ylim(-12,-24)
 plt.legend(shadow = False)
# plt.savefig('/home/harim/Pictures/Mbol.png', format='png')
 plt.show()
 
 



#########################


#
#
#
#def U(lst): 
#
# for i in range(len(lst)):
#  s = star.read_file(path+lst[i]+modelname+'.tt',85) 
#  plt.plot(s[:,0], s[:,7], label=lst[i],linewidth = 2, color=cm.rainbow((len(lst)-i)*1.2/float(len(lst))))
#  for j in range(lFigure_en(s[:,0])):
#   if s[j,7] == min(s[:,7]):
#    U = [s[j,0],s[j,7]]
#  print "For ", lst[i], ", [tamx, Uamx] = ", U
# plt.ylim(-12,-24)
# plt.legend(shadow = False)
## plt.savefig('/home/harim/Pictures/U.png', format='png')
# plt.show()
# 
# 











#########################







def B(lst): 

 for i in range(len(lst)):
  s = star.read_file(path+lst[i]+modelname+'.tt',85) 
  plt.plot(s[:,0], s[:,8], label=lst[i],linewidth = 2, color=cm.rainbow((len(lst)-i)*1.2/float(len(lst))))
  for j in range(len(s[:,0])):
   if s[j,8] == min(s[:,8]):
    B = [s[j,0],s[j,8]]
  print "For ", lst[i], ", [tamx, Uamx] = ", B
 plt.ylim(-12,-24)
 plt.legend(shadow = False)
# plt.savefig('/home/harim/Pictures/B.png', format='png')
 plt.show()
 
 












#########################







import os


def V(lst): 

 for i in range(len(lst)):
  s = star.read_file(path+lst[i]+modelname+'.tt',85) 
  plt.plot(s[:,0], s[:,9], label=lst[i],linewidth = 2, color=cm.rainbow((len(lst)-i)*1.2/float(len(lst))))
  maxtime = 0
  maxmag = 0
  for i in range(len(s)):
   if s[i,9] == min(s[:,9]):
    maxtime = s[i,0]
    maxmag = s[i,9]

  for j in range(len(s[:,0])):
   if s[j,9] == min(s[:,9]):
    V = [s[j,0],s[j,9]]
# print "For ", lst[i], ", [tamx, Uamx] = ", V

 s = star.read_file(path+'observed/LSQ14efd.txt',1)
 time = s[:,0] -56900.7+maxtime
 #   +1.5 for 8M_0.6_0.07M_14_5B
 #   +0.7 for 4M_0.3-0.15M-14-1.5B (ni 0.25)
 band = s[:,1]
 mag = s[:,2] -18.88+maxmag
 #   +0.08 for 4M_0.3-0.15M-14-1.5B (ni 0.25)
 # col = np.where(band=='B','b',np.where(band=='R','r',np.where(band=='V','g',np.where(band=='U','k','m'))))
 col = []
 U = []
 B = []
 V = []
 R = []
 I = []
 Utime = []  
 Btime = [] 
 Vtime = [] 
 Rtime = [] 
 Itime = []    
 for i in range(0,len(band)):
    if band[i] == 1:
        col.append((0.0,0.0,1.0,1.0))
        Btime.append(time[i])
        B.append(mag[i])
    elif band[i]==3:
        col.append((1.0,0.0,0.0,1.0))     
        Rtime.append(time[i])
        R.append(mag[i])   
    elif band[i]==2:
        col.append((0.0,0.5,0.0,1.0))     
        Vtime.append(time[i])
        V.append(mag[i])   
    elif band[i]==0:
        col.append((0.0,0.75,0.75,1.0))    
        Utime.append(time[i])
        U.append(mag[i])   
#            magCorr[i] = mag[i] - UCorr
    elif band[i]==4:
        col.append((0.75,0.0,0.75,1.0))
        Itime.append(time[i])
        I.append(mag[i])   
    else:
        col.append((1.0,1.0,1.0,0.0))
 plt.plot(Vtime,V,color=(0.0,0.5,0.0,1.0),linewidth = 2,label='LSQ14efd')    
 plt.ylim(-12,-24)
 plt.legend(shadow = False)
 plt.savefig(path+'different fm.png', format='png')
 plt.show()
 








#########################








def R(lst): 

 for i in range(len(lst)):
  s = star.read_file(path+lst[i]+modelname+'.tt',85) 
  plt.plot(s[:,0], s[:,11], label=lst[i],linewidth = 2, color=cm.rainbow((len(lst)-i)*1.2/float(len(lst))))
  for j in range(len(s[:,0])):
   if s[j,11] == min(s[:,11]):
    R = [s[j,0],s[j,11]]
  print "For ", lst[i], ", [tamx, Uamx] = ", R
 plt.ylim(-12,-24)
 plt.legend(shadow = False)
# plt.savefig('/home/harim/Pictures/R.png', format='png')
 plt.show()
 
 












#########################








def I(lst): 

 for i in range(len(lst)):
  s = star.read_file(path+lst[i]+modelname+'.tt',85) 
  plt.plot(s[:,0], s[:,10], label=lst[i],linewidth = 2, color=cm.rainbow((len(lst)-i)*1.2/float(len(lst))))
  for j in range(len(s[:,0])):
   if s[j,10] == min(s[:,10]):
    I = [s[j,0],s[j,10]]
  print "For ", lst[i], ", [tamx, Uamx] = ", I
 plt.ylim(-12,-24)
 plt.legend(shadow = False)
# plt.savefig('/home/harim/Pictures/I.png', format='png')
 plt.show()
 
 












#########################

