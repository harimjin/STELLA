#path = '/home/harim/stella/stella_install/sboproject/run/snIcm7/'
#path = '/home/harim/stella/stella_install/sboproject/run/snIcm15/'
path = 'D:/snIcm7/'
modelname = '/snIcm7'

def lumm(title):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 import matplotlib as mpl
 import matplotlib.ticker as ticker
 import matplotlib.patches as patches
 import os
 import physcons
 import matplotlib.colors as colors
 from matplotlib import cm 

 def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
#
# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
# # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)

 nlines = len(s[:,0])
 print nlines

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"

 
 ss = star.read_file(path+title+modelname+'.tt', 85) 

 V_max = min(ss[:,9])
 tss = ss[:,0]
 t_vmax = tss[ss[:,9] == V_max]
 t_vmax = min(t_vmax)

 print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
 header1 = f.readline()
 hh = header1.split()
 nzone = hh[1]
 Mcut = hh[2]
 nzone = int(nzone)
 Mcut = float(Mcut)

 f = star.read_file(path+title+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 print 'Mtot = ', Mtot
 print 'Mejeta = ', Mtot - Mcut

 x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 print 'Nblock = ', nblock, nlines, nzone

 time = np.zeros((nblock), float)
 time2 = np.zeros((nblock), float)
 Mphotosphere = np.zeros((nblock), float)
 Tphotosphere = np.zeros((nblock), float)
 TRphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Vphotosphere = np.zeros((nblock), float)
 Lphotosphere = np.zeros((nblock), float)
 Xphotosphere = np.zeros((nblock,14), float)
 Kphotosphere = np.zeros((nblock), float)
 Rphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 velocity = np.zeros((nzone), float)



# k = 0
# for i in range(0, nblock):
#   print i, ' time = ', s[k, 0], 'day'
#   time[i] = s[k,0]
#   k = k + nzone
 
 
 iout = 22

 tau = np.zeros((nzone), float)


 k = 0
# for i in range(0, nblock):
 for i in range(0, nblock):
    if i == iout: 
        velocity = ff[:, 4]
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Tphotosphere[i] = ff[ntau,5]
    TRphotosphere[i] = ff[ntau,6]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
    Vphotosphere[i] = ff[ntau,4]
    Kphotosphere[i] = ff[ntau,12]
    Rphotosphere[i] = ff[ntau,3]
    Lphotosphere[i] = ff[ntau,11]
    Xphotosphere[i,1] = x[ntau,4]  #H
    Xphotosphere[i,2] = x[ntau,5]  #He
    Xphotosphere[i,3] = x[ntau,6]  #C
    Xphotosphere[i,4] = x[ntau,7]  #N
    Xphotosphere[i,5] = x[ntau,8]  #O
    Xphotosphere[i,6] = x[ntau,9]  #Ne
    Xphotosphere[i,7] = x[ntau,11] #Mg
    Xphotosphere[i,8] = x[ntau,13] #Si
    Xphotosphere[i,9] = x[ntau,14] #S
    Xphotosphere[i,10] = x[ntau,15]#Ar
    Xphotosphere[i,11] = x[ntau,16]#Ca
    Xphotosphere[i,12] = x[ntau,17]#Fe
    Xphotosphere[i,13] = x[ntau,19]#Ni
#    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
    if 0 <= i <= nblock:
     plt.plot(Mtot - 10.**ff[:,2], ff[:,11], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
     plt.plot(Mphotosphere[i], Lphotosphere[i], '*', markersize=15, color='r')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
     plt.plot(Mtot - 10.**ff[index,2],ff[index,11],'|',markersize=15,color='k')
     
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
 plt.xlim(1.4, 4.2)
 plt.ylim(-11000, 80000)
 plt.xlabel('$M_r/M_\odot$')
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
# plt.xlabel('$logR$',fontsize=30)
# plt.ylabel('$V8$', fontsize=30)
 plt.ylabel('$L$$(10^{40}$ $\mathrm{erg}$ $\mathrm{s}^{-1})$')
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)

# plt.savefig('/home/harim/Pictures/'+title+'/lumm.png', format='png')

 plt.show()



###################################################
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
def lumr(title):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 import matplotlib as mpl
 import matplotlib.ticker as ticker
 import matplotlib.patches as patches
 import os
 import physcons
 import matplotlib.colors as colors
 from matplotlib import cm 

 def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
#
# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
# # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)

 nlines = len(s[:,0])
 print nlines

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"

 
 ss = star.read_file(path+title+modelname+'.tt', 85) 

 V_max = min(ss[:,9])
 tss = ss[:,0]
 t_vmax = tss[ss[:,9] == V_max]
 t_vmax = min(t_vmax)

 print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
 header1 = f.readline()
 hh = header1.split()
 nzone = hh[1]
 Mcut = hh[2]
 nzone = int(nzone)
 Mcut = float(Mcut)

 f = star.read_file(path+title+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 print 'Mtot = ', Mtot
 print 'Mejeta = ', Mtot - Mcut

 x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 print 'Nblock = ', nblock, nlines, nzone

 time = np.zeros((nblock), float)
 time2 = np.zeros((nblock), float)
 Mphotosphere = np.zeros((nblock), float)
 Tphotosphere = np.zeros((nblock), float)
 TRphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Vphotosphere = np.zeros((nblock), float)
 Lphotosphere = np.zeros((nblock), float)
 Xphotosphere = np.zeros((nblock,14), float)
 Kphotosphere = np.zeros((nblock), float)
 Rphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 velocity = np.zeros((nzone), float)



# k = 0
# for i in range(0, nblock):
#   print 'k = ', k, 'time = ', s[k, 0], 'day', '', i
#   time[i] = s[k,0]
#   k = k + nzone
 
 
 iout = 22

 tau = np.zeros((nzone), float)


 k = 0
# for i in range(0, nblock):
 for i in range(0, nblock):
    if i == iout: 
        velocity = ff[:, 4]
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Tphotosphere[i] = ff[ntau,5]
    TRphotosphere[i] = ff[ntau,6]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
    Vphotosphere[i] = ff[ntau,4]
    Kphotosphere[i] = ff[ntau,12]
    Rphotosphere[i] = ff[ntau,3]
    Lphotosphere[i] = ff[ntau,11]
    Xphotosphere[i,1] = x[ntau,4]  #H
    Xphotosphere[i,2] = x[ntau,5]  #He
    Xphotosphere[i,3] = x[ntau,6]  #C
    Xphotosphere[i,4] = x[ntau,7]  #N
    Xphotosphere[i,5] = x[ntau,8]  #O
    Xphotosphere[i,6] = x[ntau,9]  #Ne
    Xphotosphere[i,7] = x[ntau,11] #Mg
    Xphotosphere[i,8] = x[ntau,13] #Si
    Xphotosphere[i,9] = x[ntau,14] #S
    Xphotosphere[i,10] = x[ntau,15]#Ar
    Xphotosphere[i,11] = x[ntau,16]#Ca
    Xphotosphere[i,12] = x[ntau,17]#Fe
    Xphotosphere[i,13] = x[ntau,19]#Ni
#    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
    if 0 <= i <= nblock:
     plt.plot(ff[:,3], ff[:,11], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
     plt.plot(Rphotosphere[i], Lphotosphere[i], '*', markersize=15, color='r')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
     plt.plot(ff[index,3],ff[index,11],'|',markersize=15,color='k')
    
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
 plt.xlim(1.4, 4.2)
 plt.ylim(-11000, 80000)
 plt.xlabel('$logR$')
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
# plt.xlabel('$logR$',fontsize=30)
# plt.ylabel('$V8$', fontsize=30)
 plt.ylabel('$L$$(10^{40}$ $\mathrm{erg}$ $\mathrm{s}^{-1})$')
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)

# plt.savefig('/home/harim/Pictures/'+title+'/lumr.png', format='png')
# plt.yscale('log10')
 plt.show()






 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 













################################################
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
def velm(title):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 import matplotlib as mpl
 import matplotlib.ticker as ticker
 import matplotlib.patches as patches
 import os
 import physcons
 import matplotlib.colors as colors
 from matplotlib import cm 

 def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
#
# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
 # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)

 nlines = len(s[:,0])
 print nlines

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"

 
 ss = star.read_file(path+title+modelname+'.tt', 85) 

 V_max = min(ss[:,9])
 tss = ss[:,0]
 t_vmax = tss[ss[:,9] == V_max]
 t_vmax = min(t_vmax)

 print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
 header1 = f.readline()
 hh = header1.split()
 nzone = hh[1]
 Mcut = hh[2]
 nzone = int(nzone)
 Mcut = float(Mcut)

 f = star.read_file(path+title+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 print 'Mtot = ', Mtot
 print 'Mejeta = ', Mtot - Mcut

 x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 print 'Nblock = ', nblock, nlines, nzone

 time = np.zeros((nblock), float)
 time2 = np.zeros((nblock), float)
 Mphotosphere = np.zeros((nblock), float)
 Tphotosphere = np.zeros((nblock), float)
 TRphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Vphotosphere = np.zeros((nblock), float)
 Lphotosphere = np.zeros((nblock), float)
 Xphotosphere = np.zeros((nblock,14), float)
 Kphotosphere = np.zeros((nblock), float)
 Rphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 velocity = np.zeros((nzone), float)



# k = 0
# for i in range(0, nblock):
#   print 'k = ', k, 'time = ', s[k, 0], 'day', '', i
#   time[i] = s[k,0]
#   k = k + nzone
 
 
 iout = 22

 tau = np.zeros((nzone), float)


 k = 0
# for i in range(0, nblock):
 for i in range(0, nblock):
    if i == iout: 
        velocity = ff[:, 4]
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Tphotosphere[i] = ff[ntau,5]
    TRphotosphere[i] = ff[ntau,6]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
    Vphotosphere[i] = ff[ntau,4]
    Kphotosphere[i] = ff[ntau,12]
    Rphotosphere[i] = ff[ntau,3]
    Lphotosphere[i] = ff[ntau,11]
    Xphotosphere[i,1] = x[ntau,4]  #H
    Xphotosphere[i,2] = x[ntau,5]  #He
    Xphotosphere[i,3] = x[ntau,6]  #C
    Xphotosphere[i,4] = x[ntau,7]  #N
    Xphotosphere[i,5] = x[ntau,8]  #O
    Xphotosphere[i,6] = x[ntau,9]  #Ne
    Xphotosphere[i,7] = x[ntau,11] #Mg
    Xphotosphere[i,8] = x[ntau,13] #Si
    Xphotosphere[i,9] = x[ntau,14] #S
    Xphotosphere[i,10] = x[ntau,15]#Ar
    Xphotosphere[i,11] = x[ntau,16]#Ca
    Xphotosphere[i,12] = x[ntau,17]#Fe
    Xphotosphere[i,13] = x[ntau,19]#Ni
#    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
    if 0 <= i <= nblock :
     plt.plot(Mtot - 10.**ff[:,2], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
     plt.plot(Mphotosphere[i], Vphotosphere[i], '*', markersize=15, color='r')
     plt.plot(Mtot - 10.**ff[index,2],ff[index,4],'|',markersize=15,color='k')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
#     plt.plot(ff[index,3],ff[index,4],'|',markersize=15,color='k')
#    
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
 plt.xlim(1.4, 4.2)
 plt.ylim(0, 20)
 plt.xlabel('$M_r/M_\odot$')
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
# plt.xlabel('$logR$',fontsize=30)
 plt.ylabel('$V8$')
# plt.ylabel('$L$$(10^{40}$ $\mathrm{erg}$ $\mathrm{s}^{-1})$', fontsize=30)
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)

# plt.savefig('/home/harim/Pictures/'+title+'/velm.png', format='png')

 plt.show()
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
###################################3
 
 
 
 
 
 
 
 
  
def velr(title):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 import matplotlib as mpl
 import matplotlib.ticker as ticker
 import matplotlib.patches as patches
 import os
 import physcons
 import matplotlib.colors as colors
 from matplotlib import cm 

 def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
# # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)

 nlines = len(s[:,0])
 print nlines

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"

 
 ss = star.read_file(path+title+modelname+'.tt', 85) 

 V_max = min(ss[:,9])
 tss = ss[:,0]
 t_vmax = tss[ss[:,9] == V_max]
 t_vmax = min(t_vmax)

 print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
 header1 = f.readline()
 hh = header1.split()
 nzone = hh[1]
 Mcut = hh[2]
 nzone = int(nzone)
 Mcut = float(Mcut)

 f = star.read_file(path+title+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 print 'Mtot = ', Mtot
 print 'Mejeta = ', Mtot - Mcut

 x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 print 'Nblock = ', nblock, nlines, nzone

 time = np.zeros((nblock), float)
 time2 = np.zeros((nblock), float)
 Mphotosphere = np.zeros((nblock), float)
 Tphotosphere = np.zeros((nblock), float)
 TRphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Vphotosphere = np.zeros((nblock), float)
 Lphotosphere = np.zeros((nblock), float)
 Xphotosphere = np.zeros((nblock,14), float)
 Kphotosphere = np.zeros((nblock), float)
 Rphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 velocity = np.zeros((nzone), float)



# k = 0
# for i in range(0, nblock):
#   print 'k = ', k, 'time = ', s[k, 0], 'day', '', i
#   time[i] = s[k,0]
#   k = k + nzone
 
 
 iout = 22

 tau = np.zeros((nzone), float)


 k = 0
# for i in range(0, nblock):
 for i in range(0, nblock):
    if i == iout: 
        velocity = ff[:, 4]
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Tphotosphere[i] = ff[ntau,5]
    TRphotosphere[i] = ff[ntau,6]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
    Vphotosphere[i] = ff[ntau,4]
    Kphotosphere[i] = ff[ntau,12]
    Rphotosphere[i] = ff[ntau,3]
    Lphotosphere[i] = ff[ntau,11]
    Xphotosphere[i,1] = x[ntau,4]  #H
    Xphotosphere[i,2] = x[ntau,5]  #He
    Xphotosphere[i,3] = x[ntau,6]  #C
    Xphotosphere[i,4] = x[ntau,7]  #N
    Xphotosphere[i,5] = x[ntau,8]  #O
    Xphotosphere[i,6] = x[ntau,9]  #Ne
    Xphotosphere[i,7] = x[ntau,11] #Mg
    Xphotosphere[i,8] = x[ntau,13] #Si
    Xphotosphere[i,9] = x[ntau,14] #S
    Xphotosphere[i,10] = x[ntau,15]#Ar
    Xphotosphere[i,11] = x[ntau,16]#Ca
    Xphotosphere[i,12] = x[ntau,17]#Fe
    Xphotosphere[i,13] = x[ntau,19]#Ni
#    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
    if 0 <= i <= nblock+1:
#     plt.plot(Mtot - 10.**ff[:,2], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Mphotosphere[i], Vphotosphere[i], '*', markersize=15, color='r')
#     plt.plot(Mtot - 10.**ff[index,2],ff[index,4],'|',markersize=15,color='k')
     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
     plt.plot(ff[index,3],ff[index,4],'|',markersize=15,color='k')
    
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
 plt.xlim(1.4, 4.2)
 plt.ylim(0, 20)
# plt.xlabel('$M_r/M_\odot$', fontsize=30)
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
 plt.xlabel('$logR$')
 plt.ylabel('$V8$')
# plt.ylabel('$L$$(10^{40}$ $\mathrm{erg}$ $\mathrm{s}^{-1})$', fontsize=30)
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)

# plt.savefig('/home/harim/Pictures/'+title+'/velr.png', format='png')
 
 plt.show()


 
 
 
 
 
 
###################################3
 
 
 
 
 
 
 
 
  
def pr(title,pindex):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 import matplotlib as mpl
 import matplotlib.ticker as ticker
 import matplotlib.patches as patches
 import os
 import physcons
 import matplotlib.colors as colors
 from matplotlib import cm 

 def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
# # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)

 nlines = len(s[:,0])
 print nlines

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"

 
 ss = star.read_file(path+title+modelname+'.tt', 85) 

 V_max = min(ss[:,9])# plt.xlim(1.4, 4.2)
# plt.ylim(-20, 400)
 tss = ss[:,0]
 t_vmax = tss[ss[:,9] == V_max]
 t_vmax = min(t_vmax)

 print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
 header1 = f.readline()
 hh = header1.split()
 nzone = hh[1]
 Mcut = hh[2]
 nzone = int(nzone)
 Mcut = float(Mcut)

 f = star.read_file(path+title+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 print 'Mtot = ', Mtot
 print 'Mejeta = ', Mtot - Mcut

 x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 print 'Nblock = ', nblock, nlines, nzone

 time = np.zeros((nblock), float)
 time2 = np.zeros((nblock), float)
 Mphotosphere = np.zeros((nblock), float)
 Tphotosphere = np.zeros((nblock), float)
 Pphotosphere = np.zeros((nblock), float)
 TRphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Vphotosphere = np.zeros((nblock), float)
 Lphotosphere = np.zeros((nblock), float)
 Xphotosphere = np.zeros((nblock,14), float)
 Kphotosphere = np.zeros((nblock), float)
 Rphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 velocity = np.zeros((nzone), float)



# k = 0
# for i in range(0, nblock):
#   print 'k = ', k, 'time = ', s[k, 0], 'day', '', i
#   time[i] = s[k,0]
#   k = k + nzone
 
 
 iout = 22

 tau = np.zeros((nzone), float)


 k = 0
# for i in range(0, nbloc# plt.xlim(1.4, 4.2)
# plt.ylim(-20, 400)k):
 for i in range(0, nblock):
    if i == iout: 
        velocity = ff[:, 4]
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Tphotosphere[i] = ff[ntau,5]
    TRphotosphere[i] = ff[ntau,6]
    Pphotosphere[i] = ff[ntau,8]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
    Vphotosphere[i] = ff[ntau,4]
    Kphotosphere[i] = ff[ntau,12]
    Rphotosphere[i] = ff[ntau,3]
    Lphotosphere[i] = ff[ntau,11]
    Xphotosphere[i,1] = x[ntau,4]  #H
    Xphotosphere[i,2] = x[ntau,5]  #He
    Xphotosphere[i,3] = x[ntau,6]  #C
    Xphotosphere[i,4] = x[ntau,7]  #N
    Xphotosphere[i,5] = x[ntau,8]  #O
    Xphotosphere[i,6] = x[ntau,9]  #Ne
    Xphotosphere[i,7] = x[ntau,11] #Mg
    Xphotosphere[i,8] = x[ntau,13] #Si
    Xphotosphere[i,9] = x[ntau,14] #S
    Xphotosphere[i,10] = x[ntau,15]#Ar
    Xphotosphere[i,11] = x[ntau,16]#Ca
    Xphotosphere[i,12] = x[ntau,17]#Fe
    Xphotosphere[i,13] = x[ntau,19]#Ni
#    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
#    if i == pindex:
    if 0<=i<=nblock:       
#     plt.plot(Mtot - 10.**ff[:,2], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Mphotosphere[i], Vphotosphere[i], '*', markersize=15, color='r')
#     plt.plot(Mtot - 10.**ff[index,2],ff[index,4],'|',markersize=15,color='k')
     plt.plot(10**ff[:,3], 10**ff[:,8], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
     plt.plot(10**Rphotosphere[i],10**Pphotosphere[i],'*',markersize=15,color='r')   
     plt.plot(10**ff[index,3],10**ff[index,8],'|',markersize=15,color='k')
    
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
# plt.xlim(1.4, 4.2)
# plt.ylim(-20, 400)
# plt.xlabel('$M_r/M_\odot$', fontsize=30)
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
 plt.xlabel('$R$')
 plt.ylabel('$P$')
# plt.ylabel('$L$$(10^{40}$ $\mathrm{erg}$ $\mathrm{s}^{-1})$', fontsize=30)
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)

# plt.savefig('/home/harim/Desktop/0.6_0.07M_14_5B/Pr/pr'+str(pindex)+'.png', format='png')
 
 plt.show()




##########################################################################################################



 

 
 
 
def T(title):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 import matplotlib as mpl
 import matplotlib.ticker as ticker
 import matplotlib.patches as patches
 import os
 import physcons
 import matplotlib.colors as colors
 from matplotlib import cm 

 def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
#
# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
 # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)
# s = star.read_file(path+title+modelname+'.swd',0)

 nlines = len(s[:,0])
 print nlines

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"

 ss = star.read_file(path+title+modelname+'.tt', 85)  
# ss = star.read_file(path+title+modelname+'.tt', 85) 

 V_max = min(ss[:,9])
 tss = ss[:,0]
 t_vmax = tss[ss[:,9] == V_max]
 t_vmax = min(t_vmax)

 print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
# f = open(path+title+modelname+'.hyd', 'r')
 header1 = f.readline()
 hh = header1.split()
 nzone = hh[1]
 Mcut = hh[2]
 nzone = int(nzone)
 Mcut = float(Mcut)

 f = star.read_file(path+title+modelname+'.hyd', 1) 
# f = star.read_file(path+title+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 print 'Mtot = ', Mtot
 print 'Mejeta = ', Mtot - Mcut

 x = star.read_file(path+title+modelname+'.abn', 0) 
# x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 print 'Nblock = ', nblock, nlines, nzone

 time = np.zeros((nblock), float)
 time2 = np.zeros((nblock), float)
 Mphotosphere = np.zeros((nblock), float)
 Tphotosphere = np.zeros((nblock), float)
 TRphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Vphotosphere = np.zeros((nblock), float)
 Lphotosphere = np.zeros((nblock), float)
 Xphotosphere = np.zeros((nblock,14), float)
 Kphotosphere = np.zeros((nblock), float)
 Rphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 velocity = np.zeros((nzone), float)



# k = 0
# for i in range(0, nblock):
#   print 'k = ', k, 'time = ', s[k, 0], 'day', '', i
#   time[i] = s[k,0]
#   k = k + nzone
 
 
 iout = 22

 tau = np.zeros((nzone), float)


 k = 0
# for i in range(0, nblock):
 for i in range(0, nblock):
    if i == iout: 
        velocity = ff[:, 4]
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Tphotosphere[i] = ff[ntau,5]
    TRphotosphere[i] = ff[ntau,6]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
    Vphotosphere[i] = ff[ntau,4]
    Kphotosphere[i] = ff[ntau,12]
    Rphotosphere[i] = ff[ntau,3]
    Lphotosphere[i] = ff[ntau,11]
    Xphotosphere[i,1] = x[ntau,4]  #H
    Xphotosphere[i,2] = x[ntau,5]  #He
    Xphotosphere[i,3] = x[ntau,6]  #C
    Xphotosphere[i,4] = x[ntau,7]  #N
    Xphotosphere[i,5] = x[ntau,8]  #O
    Xphotosphere[i,6] = x[ntau,9]  #Ne
    Xphotosphere[i,7] = x[ntau,11] #Mg
    Xphotosphere[i,8] = x[ntau,13] #Si
    Xphotosphere[i,9] = x[ntau,14] #S
    Xphotosphere[i,10] = x[ntau,15]#Ar
    Xphotosphere[i,11] = x[ntau,16]#Ca
    Xphotosphere[i,12] = x[ntau,17]#Fe
    Xphotosphere[i,13] = x[ntau,19]#Ni
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
#    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
    if 0 <= i <= nblock :
#    if 15 <= i <= nblock :
     plt.plot(Mtot - 10.**ff[:,2], ff[:,5], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
     plt.plot(Mphotosphere[i], Tphotosphere[i], '*', markersize=15, color='r')
     plt.plot(Mtot - 10.**ff[index,2],ff[index,5],'|',markersize=15,color='k')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
#     plt.plot(ff[index,3],ff[index,4],'|',markersize=15,color='k')
#    
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
 plt.xlim(1.4, 4.2)
 plt.ylim(3, 6)
# plt.ylim(3.4,4.7)
 plt.xlabel('$M_r/M_\odot$')
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
# plt.xlabel('$logR$',fontsize=30)
 plt.ylabel('$logT$')
# plt.ylabel('$L$$(10^{40}$ $\mathrm{erg}$ $\mathrm{s}^{-1})$', fontsize=30)
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)

# plt.savefig('/home/harim/Pictures/'+title+'/Tm.png', format='png')

 plt.show()
 
 
 
 
 
 
 
 


 


##########################################################################################################

 
 
  
def kappa(title):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 import matplotlib as mpl
 import matplotlib.ticker as ticker
 import matplotlib.patches as patches
 import os
 import physcons
 import matplotlib.colors as colors
 from matplotlib import cm 

 def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
#
# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
# # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)

 nlines = len(s[:,0])
 print nlines

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"

 
 ss = star.read_file(path+title+modelname+'.tt', 85) 

 V_max = min(ss[:,9])
 tss = ss[:,0]
 t_vmax = tss[ss[:,9] == V_max]
 t_vmax = min(t_vmax)

 print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
 header1 = f.readline()
 hh = header1.split()
 nzone = hh[1]
 Mcut = hh[2]
 nzone = int(nzone)
 Mcut = float(Mcut)

 f = star.read_file(path+title+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 print 'Mtot = ', Mtot
 print 'Mejeta = ', Mtot - Mcut

 x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 print 'Nblock = ', nblock, nlines, nzone

 time = np.zeros((nblock), float)
 time2 = np.zeros((nblock), float)
 Mphotosphere = np.zeros((nblock), float)
 Tphotosphere = np.zeros((nblock), float)
 TRphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Vphotosphere = np.zeros((nblock), float)
 Lphotosphere = np.zeros((nblock), float)
 Xphotosphere = np.zeros((nblock,14), float)
 Kphotosphere = np.zeros((nblock), float)
 Rphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 velocity = np.zeros((nzone), float)



# k = 0
# for i in range(0, nblock):
#   print i, ' time = ', s[k, 0], 'day'
#   time[i] = s[k,0]
#   k = k + nzone
 
 
 iout = 22

 tau = np.zeros((nzone), float)


 k = 0
# for i in range(0, nblock):
 for i in range(0, nblock):
    if i == iout: 
        velocity = ff[:, 4]
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Tphotosphere[i] = ff[ntau,5]
    TRphotosphere[i] = ff[ntau,6]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
    Vphotosphere[i] = ff[ntau,4]
    Kphotosphere[i] = ff[ntau,12]
    Rphotosphere[i] = ff[ntau,3]
    Lphotosphere[i] = ff[ntau,11]
    Xphotosphere[i,1] = x[ntau,4]  #H
    Xphotosphere[i,2] = x[ntau,5]  #He
    Xphotosphere[i,3] = x[ntau,6]  #C
    Xphotosphere[i,4] = x[ntau,7]  #N
    Xphotosphere[i,5] = x[ntau,8]  #O
    Xphotosphere[i,6] = x[ntau,9]  #Ne
    Xphotosphere[i,7] = x[ntau,11] #Mg
    Xphotosphere[i,8] = x[ntau,13] #Si
    Xphotosphere[i,9] = x[ntau,14] #S
    Xphotosphere[i,10] = x[ntau,15]#Ar
    Xphotosphere[i,11] = x[ntau,16]#Ca
    Xphotosphere[i,12] = x[ntau,17]#Fe
    Xphotosphere[i,13] = x[ntau,19]#Ni
#    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
    if 0 <= i <= nblock:
     plt.plot(Mtot - 10.**ff[:,2], ff[:,12], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
     plt.plot(Mphotosphere[i], Kphotosphere[i], '*', markersize=15, color='r')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
     plt.plot(Mtot - 10.**ff[index,2],ff[index,12],'|',markersize=15,color='k')
     
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
# plt.xlim(1.4, 4.2)
# plt.ylim(-20, 400)
 plt.xlabel('$M_r/M_\odot$')
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
# plt.xlabel('$logR$',fontsize=30)
# plt.ylabel('$V8$', fontsize=30)
 plt.ylabel('kappa')
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)

# plt.savefig('/home/harim/Pictures/'+title+'/kappa.png', format='png')

 plt.show()







 
 
 
 


 


##########################################################################################################

 
 
  
def rho(title):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 import matplotlib as mpl
 import matplotlib.ticker as ticker
 import matplotlib.patches as patches
 import os
 import physcons
 import matplotlib.colors as colors
 from matplotlib import cm 

 def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")
#
# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
# # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)

 nlines = len(s[:,0])
 print nlines

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"

 
 ss = star.read_file(path+title+modelname+'.tt', 85) 

 V_max = min(ss[:,9])
 tss = ss[:,0]
 t_vmax = tss[ss[:,9] == V_max]
 t_vmax = min(t_vmax)

 print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
 header1 = f.readline()
 hh = header1.split()
 nzone = hh[1]
 Mcut = hh[2]
 nzone = int(nzone)
 Mcut = float(Mcut)

 f = star.read_file(path+title+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 print 'Mtot = ', Mtot
 print 'Mejeta = ', Mtot - Mcut

 x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 print 'Nblock = ', nblock, nlines, nzone

 time = np.zeros((nblock), float)
 time2 = np.zeros((nblock), float)
 Mphotosphere = np.zeros((nblock), float)
 Tphotosphere = np.zeros((nblock), float)
 TRphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Vphotosphere = np.zeros((nblock), float)
 Lphotosphere = np.zeros((nblock), float)
 Xphotosphere = np.zeros((nblock,14), float)
 Kphotosphere = np.zeros((nblock), float)
 Rphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 velocity = np.zeros((nzone), float)



# k = 0
# for i in range(0, nblock):
#   print i, ' time = ', s[k, 0], 'day'
#   time[i] = s[k,0]
#   k = k + nzone
 
 
 iout = 22

 tau = np.zeros((nzone), float)


 k = 0
# for i in range(0, nblock):
 for i in range(0, nblock):
    if i == iout: 
        velocity = ff[:, 4]
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Tphotosphere[i] = ff[ntau,5]
    TRphotosphere[i] = ff[ntau,6]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
    Vphotosphere[i] = ff[ntau,4]
    Kphotosphere[i] = ff[ntau,12]
    Rphotosphere[i] = ff[ntau,3]
    Lphotosphere[i] = ff[ntau,11]
    Xphotosphere[i,1] = x[ntau,4]  #H
    Xphotosphere[i,2] = x[ntau,5]  #He
    Xphotosphere[i,3] = x[ntau,6]  #C
    Xphotosphere[i,4] = x[ntau,7]  #N
    Xphotosphere[i,5] = x[ntau,8]  #O
    Xphotosphere[i,6] = x[ntau,9]  #Ne
    Xphotosphere[i,7] = x[ntau,11] #Mg
    Xphotosphere[i,8] = x[ntau,13] #Si
    Xphotosphere[i,9] = x[ntau,14] #S
    Xphotosphere[i,10] = x[ntau,15]#Ar
    Xphotosphere[i,11] = x[ntau,16]#Ca
    Xphotosphere[i,12] = x[ntau,17]#Fe
    Xphotosphere[i,13] = x[ntau,19]#Ni
    #    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
    if 0 <= i <= nblock:
     plt.plot(Mtot - 10.**ff[:,2], ff[:,7], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
     plt.plot(Mphotosphere[i], ff[ntau,7], '*', markersize=15, color='r')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
     plt.plot(Mtot - 10.**ff[index,2],ff[index,7],'|',markersize=15,color='k')
     
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
 plt.xlim(1.4, 4.2)
 plt.ylim(-10, 1)
 plt.xlabel('$M_r/M_\odot$')
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
# plt.xlabel('$logR$',fontsize=30)
# plt.ylabel('$V8$', fontsize=30)
 plt.ylabel('logrho-6')
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)

# plt.savefig('/home/harim/Pictures/'+title+'/rho.png', format='png')

 plt.show()




















###########################################################################################################
 
 
 
 
 
 
 
 
 
 
 
 
 
 
def curve(title,title2,iindex, iindex2, integer):
 import star
 import matplotlib.pyplot as plt
 import numpy as np
 from matplotlib import cm 
 

#
# # set tick width
# mpl.rcParams['xtick.labelsize'] = 28
# mpl.rcParams['ytick.labelsize'] = 28
# mpl.rcParams['xtick.major.size'] = 11
# mpl.rcParams['xtick.major.width'] = 3
# mpl.rcParams['xtick.minor.size'] = 8
# mpl.rcParams['xtick.minor.width'] = 2 
# mpl.rcParams['ytick.major.size'] = 11
# mpl.rcParams['ytick.major.width'] = 3
# mpl.rcParams['ytick.minor.size'] = 8
# mpl.rcParams['ytick.minor.width'] = 2 
# mpl.rcParams['ytick.major.pad'] = '8'
# mpl.rcParams['xtick.major.pad'] = '8'
# #mpl.rcParams['legend.labelspacing'] = '20'
# #mpl.rcParams['legend.borderpad'] = '100'
# mpl.rcParams['axes.linewidth'] = 3
# mpl.rcParams["figure.figsize"] = [15, 10]
# # mpl.rcParams['pdf.fonttype'] = 42
# # mpl.rcParams['ps.fonttype'] = 42


##########################################################################################################
#   Data            #####################################################################################
##########################################################################################################

 s = star.read_file(path+title+modelname+'.swd',0)
 s2 = star.read_file(path+title2+modelname+'.swd',0)
 nlines = len(s[:,0])
 nlines2 = len(s2[:,0])

 print " 0     1     2     3     4     5     6        7       8   9     10     11   12   "
 print " t   zone   lgM   lgR    v8   lgT   lgTrad  lgRho   lgP  lgqv  eng12   L   Cap_ross"
 indexnumber = range(0,13)
 indexname = ['t','zone','lgM','lgR','v8','lgT','lgTrad','lgRho','lgP','lgqv','eng12','L','Cap_ross']
#
# 
# ss = star.read_file(path+title+modelname+'.tt', 85) 
# ss2 = star.read_file(path+title2+modelname+'.tt', 85) 
# 
# V_max = min(ss[:,9])
# tss = ss[:,0]
# t_vmax = tss[ss[:,9] == V_max]
# t_vmax = min(t_vmax)
#
# print 't_vmax = ', t_vmax

 f = open(path+title+modelname+'.hyd', 'r')
 f2 = open(path+title2+modelname+'.hyd', 'r')
 header1 = f.readline()
 header2 = f2.readline()
 hh = header1.split()
 hh2 = header2.split()
 nzone = hh[1]
 nzone2 = hh2[1]
# Mcut = hh[2]
 nzone = int(nzone)
 nzone2 = int(nzone2)
# Mcut = float(Mcut)
#
 f = star.read_file(path+title+modelname+'.hyd', 1) 
 f2 = star.read_file(path+title2+modelname+'.hyd', 1) 
 Mtot = max(f[:,6])
 Mtot2 = max(f2[:,6])
# print 'Mtot = ', Mtot
# print 'Mejeta = ', Mtot - Mcut
#
# x = star.read_file(path+title+modelname+'.abn', 0) 

 nblock = nlines/nzone
 nblock2 = nlines2/nzone2
# print 'Nblock = ', nblock, nlines, nzone

 Mphotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 Rhophotosphere = np.zeros((nblock), float)
 tau = np.zeros((nzone), float)

 Mphotosphere2 = np.zeros((nblock2), float)
 Rhophotosphere2 = np.zeros((nblock2), float)
 Rhophotosphere2 = np.zeros((nblock2), float)
 tau2 = np.zeros((nzone2), float)
 
# k = 0
# for i in range(0, nblock):
#   print i, ' time = ', s[k, 0], 'day'
#   time[i] = s[k,0]
#   k = k + nzone
 
 k = 0
# for i in range(0, nblock):
 for i in range(0, nblock):
    ff = s[k:k+nzone,:]
    tau[nzone-1] = 0.0
    for j in range(nzone-2,0,-1):
      tau[j] = tau[j+1] + ff[j,12]*10.**ff[j,7]*(10.**ff[j+1,3] - 10.**ff[j,3])*1e-6
    k = k+nzone
    mr = Mtot - 10**ff[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau[0] = tau[1]
    for j in range(0, nzone-1):
          if tau[j] >= 0.67 and tau[j+1] < 0.67:  
                ntau = j
    Mphotosphere[i] = mr[ntau]
    Rhophotosphere[i] = np.log10(1e-6*10.**ff[ntau,7])
#    index = min(range(len(mr)), key=lambda k: abs(mr[k]-3.92860048014))
    index = min(range(len(mr)), key=lambda k: abs(mr[k]-8.25749374296))
    if i == integer:
     if iindex == 11:
      plt.plot(Mtot - 10.**ff[:,2], np.log10(ff[:,iindex]), 'k', linewidth = 3)
      plt.plot(Mphotosphere[i], np.log10(ff[ntau,iindex]), '*', markersize=15, color='r')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
      plt.plot(Mtot - 10.**ff[index,2],np.log10(ff[index,iindex]),'|',markersize=15,color='k')         
     else:
      plt.plot(Mtot - 10.**ff[:,2], ff[:,iindex], 'k', linewidth = 3)
      plt.plot(Mphotosphere[i], ff[ntau,iindex], '*', markersize=15, color='r')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
      plt.plot(Mtot - 10.**ff[index,2],ff[index,iindex],'|',markersize=15,color='k')

 k = 0

 for i in range(0, nblock2):
    ff2 = s2[k:k+nzone2,:]
    tau2[nzone2-1] = 0.0
    for j in range(nzone2-2,0,-1):
      tau2[j] = tau2[j+1] + ff2[j,12]*10.**ff2[j,7]*(10.**ff2[j+1,3] - 10.**ff2[j,3])*1e-6
    k = k+nzone2
    mr2 = Mtot2 - 10**ff2[:,2]  
#    plt.plot(mr[:], ff[:,12], linewidth=3)
    tau2[0] = tau2[1]
    for j in range(0, nzone2-1):
          if tau2[j] >= 0.67 and tau2[j+1] < 0.67:  
                ntau2 = j
    Mphotosphere2[i] = mr2[ntau2]
    Rhophotosphere2[i] = np.log10(1e-6*10.**ff2[ntau2,7])
#    index = min(range(len(mr2)), key=lambda k: abs(mr2[k]-3.92860048014))
    index = min(range(len(mr2)), key=lambda k: abs(mr2[k]-8.25749374296))
    if i == integer:
     if iindex2 == 11:
      plt.plot(Mtot2 - 10.**ff2[:,2], np.log10(ff2[:,iindex2]), 'gray', linewidth = 3)
      plt.plot(Mphotosphere2[i], np.log10(ff2[ntau2,iindex2]), '*', markersize=15, color='r')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
      plt.plot(Mtot2 - 10.**ff2[index,2],np.log10(ff2[index,iindex2]),'|',markersize=15,color='k')         
     else:
      plt.plot(Mtot2 - 10.**ff2[:,2], ff2[:,iindex2], 'gray', linewidth = 3)
      plt.plot(Mphotosphere2[i], ff2[ntau2,iindex2], '*', markersize=15, color='r')
#     plt.plot(ff[:,3], ff[:,4], linewidth = 3, color=cm.rainbow(i*1.2/float(nblock)))
#     plt.plot(Rphotosphere[i],Vphotosphere[i],'*',markersize=15,color='r')   
      plt.plot(Mtot2 - 10.**ff2[index,2],ff2[index,iindex2],'|',markersize=15,color='k')     
# ax = plt.gca()
## ax.xaxis.set_ticks_position('bottom')
## ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# plt.title('HE3.87, $E_\mathrm{exp} = 1.5\mathrm{B}$, $M_\mathrm{Ni} = 0.07M_\odot$', fontsize=30, y=1.01)
# plt.xlim(1.4, 4.2)
# plt.ylim(-20, 400)
 plt.xlabel('$M_r/M_\odot$')
# plt.ylabel('$L$ $(10^{40})$ $\rm{erg~s^{-1}}$', fontsize=20)
# plt.xlabel('$logR$',fontsize=30)
# plt.ylabel('$V8$', fontsize=30)
 plt.ylabel('black---'+indexname[iindex]+'   '+'gray---'+indexname[iindex2])
# plt.ylabel('black---'+'ni0.14'+'   '+'gray---'+'ni0.25')
# plt.text(1.75, -6,'0.5d',fontsize=20)
# plt.text(1.81, 40,'3d',fontsize=20)
# plt.text(1.85, 70,'5d',fontsize=20)
# plt.text(1.9, 95,'7d',fontsize=20)
# plt.text(1.9, 120,'10d',fontsize=20)
# plt.text(2.22, 145,'13d',fontsize=20)
# plt.text(2.55, 162,'18d',fontsize=20)
 lst = [0.01,0.1,0.2,0.3,0.5,0.75,1,2,3,4,5,6,7,8,9,10,11,12,14,16,18,20,22,24,28,34,40,50,60]
# plt.savefig('/home/harim/Desktop/0.6_0.07M_14_5B/V-rho/'+str(integer+1)+'V-rho'+str(lst[integer])+'day.png', format='png')
 plt.show() 
 
 

    
 
 
 
 
 
 
 
 


