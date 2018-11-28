#path = 'D:/snIcm7/'
#modelname = '/snIcm7'
path = '/media/harim/ELEMENTARY/snIcm7/'
modelname = '/snIcm7'

import star
import matplotlib.pyplot as plt
from matplotlib import cm 

lst15 = ['13/0.6-0.05M-13-5B','13/0.6-0.07M-13-5B','13/0.6-0.3M-13-5B','14/0.6-0.05M-14-5B','14/0.6-0.07M-14-5B','14/0.6-0.3M-14-5B','14/0.3-0.07M-14-5B','14/1.2-0.07M-14-5B','14/0.6-0.07M-14-4B','14/0.6-0.07M-14-6B','14.5/0.6-0.05M-14.5-5B','14.5/0.6-0.07M-14.5-5B','14.5/0.6-0.3M-14.5-5B']
lst7 = ['13/0.3-0.05M-13-1.5B','13/0.3-0.15M-13-1.5B','13/0.3-0.3M-13-1.5B','14/0.3-0.05M-14-1.5B','14/0.3-0.15M-14-1.5B','14/0.3-0.3M-14-1.5B','14/0.15-0.15M-14-1.5B','14/0.6-0.15M-14-1.5B','14/0.3-0.15M-14-1B','14/0.3-0.15M-14-2B','15/0.3-0.05M-15-1.5B','15/0.3-0.15M-15-1.5B','15/0.3-0.3M-15-1.5B']
    

def color(dir):

    import star
    import matplotlib.pyplot as plt
    import numpy as np
    import json
    from scipy.interpolate import interp1d
    
    obs_rawdata = star.read_file(path+'observed/LSQ14efd.txt',1)
    datastore = json.load(open(path+'observed/LSQ14efd.json'))    
    time_U,obs_U,time_B,obs_B,time_V,obs_V,time_R,obs_R,time_I,obs_I=[],[],[],[],[],[],[],[],[],[]
    for i in range(0,len(obs_rawdata[:,0])):
        if obs_rawdata[i,1]==0:
            time_U.append(obs_rawdata[i,0])
            obs_U.append(obs_rawdata[i,2])
        elif obs_rawdata[i,1]==1:
            time_B.append(obs_rawdata[i,0])
            obs_B.append(obs_rawdata[i,2])
        elif obs_rawdata[i,1]==2:
            time_V.append(obs_rawdata[i,0])
            obs_V.append(obs_rawdata[i,2])
        elif obs_rawdata[i,1]==3:
            time_R.append(obs_rawdata[i,0])
            obs_R.append(obs_rawdata[i,2])
        elif obs_rawdata[i,1]==4:
            time_I.append(obs_rawdata[i,0])
            obs_I.append(obs_rawdata[i,2])        
    model_data = star.read_file(path+dir+modelname+'.tt',85)
    
    #            for j, mag in enumerate(s[:,9]):
    #                if mag == min(s[:,9]):
    #                    maxtime = s[j,0]
    #                    maxmag = mag
    #    h = star.read_file(path+'observed/LSQ14efd.txt',1)
    ##########################change below line for every iteration
    #    time = h[:,0] -56900.7+maxtime+1.2
    #    #   +1.2 for 8M-0.6-0.07M-14-5B
    #    #   +0.7 for 4M-0.3-0.15M-14-1.5B
    ##########################change below line for every iteration
    #    mag = h[:,2] -18.88+maxmag
    #    #   +0.08 for 4M-0.3-0.15M-14-1.5B
    #    band = h[:,1]
    
    timemodel = model_data[:,0]
    Bolmodel = model_data[:,6]
    Umodel = model_data[:,7]
    Bmodel = model_data[:,8]
    Vmodel = model_data[:,9]
    Rmodel = model_data[:,11]
    Imodel = model_data[:,10]
    maxtime = timemodel[np.argmin(Vmodel)]
    
    
    #####BV#####
    comtimeBV = []
    comBV = []
    for time in time_B:
        if time in time_V:
            comtimeBV.append(time-56900.7+maxtime)
            comB = obs_B[time_B.index(time)]
            comV = obs_V[time_V.index(time)]
            comBV.append(comB-comV)
    
    #####VR#####
    comtimeVR = []
    comVR = []
    for time in time_V:
        if time in time_R:
            comtimeVR.append(time-56900.7+maxtime)
            comV = obs_V[time_V.index(time)]
            comR = obs_R[time_R.index(time)]
            comVR.append(comV-comR)
    
    #####RI#####
    comtimeRI = []
    comRI = []
    for time in time_R:
        if time in time_I:
            comtimeRI.append(time-56900.7+maxtime)
            comR = obs_R[time_R.index(time)]
            comI = obs_I[time_I.index(time)]
            comRI.append(comR-comI)        
            
    ###plot
    plt.plot(comtimeBV,comBV,color='blue')   
    plt.plot(comtimeVR,comVR,color='green')   
    plt.plot(comtimeRI,comRI,color='red')   
    plt.scatter(comtimeBV,comBV,s=20,label='B-V',color='blue')
    plt.scatter(comtimeVR,comVR,s=20,label='V-R',color='green')
    plt.scatter(comtimeRI,comRI,s=20,label='R-I',color='red')
    plt.plot(timemodel,Bmodel-Vmodel,color='blue')
    plt.plot(timemodel,Vmodel-Rmodel,color='green')
    plt.plot(timemodel,Rmodel-Imodel,color='red')

    
    #B = interp1d(time_B, obs_B)
    #V = interp1d(time_V, obs_V)
    #R = interp1d(time_R, obs_R)
    #I = interp1d(time_I, obs_I)
    #
    #minBV = max(min(time_B),min(time_V))
    #maxBV = min(max(time_B),max(time_V))
    #timeBV = np.linspace(minBV, maxBV, num=100, endpoint=True)
    #
    #minVR = max(min(time_V),min(time_R))
    #maxVR = min(max(time_V),max(time_R))
    #timeVR = np.linspace(minVR, maxVR, num=100, endpoint=True)
    #
    #minRI = max(min(time_R),min(time_I))
    #maxRI = min(max(time_R),max(time_I))
    #timeRI = np.linspace(minRI, maxRI, num=100, endpoint=True)
    
    #plt.plot(timeBV-56900.7+maxtime, B(timeBV)-V(timeBV),color='blue')
    #plt.plot(timeVR-56900.7+maxtime, V(timeVR)-R(timeVR),color='green')
    #plt.plot(timeRI-56900.7+maxtime, R(timeRI)-I(timeRI),color='red')
    plt.legend(loc='best')
    plt.xlim(0,100)
    plt.ylim(-0.5,2.0)
    plt.savefig(path+dir+'color.png', format='png')  
    plt.show()




def v(lst):
    maxtime = 0
    maxmag = 0
    for i,item in enumerate(lst):
        s = star.read_file(path+item+modelname+'.tt',85)
        if i == 0 :
            plt.plot(s[:,0],s[:,9],label=item, linewidth = 2, color='purple')
        if i == 1 :
            plt.plot(s[:,0],s[:,9],label=item, linewidth = 2, color='blue')
        if i == 2:
            plt.plot(s[:,0],s[:,9],label=item, linewidth = 2, color='lightblue')
        if i == 3:
            plt.plot(s[:,0],s[:,9],label=item, linewidth = 2, color='red')
            
#########################change below line for every iteration
        if i == 1:
            for j, mag in enumerate(s[:,9]):
                if mag == min(s[:,9]):
                    maxtime = s[j,0]
                    maxmag = mag
    h = star.read_file(path+'observed/LSQ14efd.txt',1)
#########################change below line for every iteration
    time = h[:,0] -56900.7+maxtime+1.2
    #   +1.2 for 8M-0.6-0.07M-14-5B
    #   +0.7 for 4M-0.3-0.15M-14-1.5B
#########################change below line for every iteration
    mag = h[:,2] -18.88+maxmag
    #   +0.08 for 4M-0.3-0.15M-14-1.5B
    band = h[:,1]

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
    plt.scatter(Vtime,V,s=5,c=(0.0,0.5,0.0,1.0),linewidth=1,label='LSQ14efd',zorder=3)
#    plt.plot(Vtime,V,color=(0.0,0.5,0.0,1.0),label='LSQ14efd',zorder=3)
#    plt.xlim(0,100)
    plt.ylim(-15,-19)   
    plt.legend(loc = 'best',shadow = False)
    plt.axvline(x=2.87,color='k')
#   x=3.60 for 4M-0.3-0.15M-14-1.5B
#   x=2.87 for 8M-0.6-0.07M-14-5B
    plt.savefig(path+'cadencecheck15.png', format='png')
    plt.show()    



#v(['13/0.3-0.05M-13-1.5B','13/0.3-0.15M-13-1.5B','13/0.3-0.3M-13-1.5B'])    
#v(['14/0.3-0.05M-14-1.5B','14/0.3-0.15M-14-1.5B','14/0.3-0.3M-14-1.5B'])    
#v(['15/0.3-0.05M-15-1.5B','15/0.3-0.15M-15-1.5B','15/0.3-0.3M-15-1.5B'])    
#v(['14/0.15-0.15M-14-1.5B','14/0.3-0.15M-14-1.5B','14/0.6-0.15M-14-1.5B'])    
#v(['14/0.3-0.15M-14-1B','14/0.3-0.15M-14-1.5B','14/0.3-0.15M-14-2B'])    

#v(['13/0.6-0.05M-13-5B','13/0.6-0.07M-13-5B','13/0.6-0.3M-13-5B'])    
#v(['14/0.6-0.05M-14-5B','14/0.6-0.07M-14-5B','14/0.6-0.3M-14-5B'])   
#v(['14.5/0.6-0.05M-14.5-5B','14.5/0.6-0.07M-14.5-5B','14.5/0.6-0.3M-14.5-5B'])   
#v(['14/0.3-0.07M-14-5B','14/0.6-0.07M-14-5B','14/1.2-0.07M-14-5B'])   
#v(['14/0.6-0.07M-14-4B','14/0.6-0.07M-14-5B','14/0.6-0.07M-14-6B']) 
    
def all(dirname):
    
     import sys
     import numpy as np
     import matplotlib.pyplot as plt
     import matplotlib as mpl
     import star
     import json


################################
     
     h = star.read_file(path+dirname+modelname+'.tt',85) 
     maxtime = 0
     maxmag = 0
     for i in range(len(h)):
         if h[i,9] == min(h[:,9]):
             maxtime = h[i,0]
             maxmag = h[i,9]

##############################-18.88+maxmag

#     datastore = json.load(open('/home/harim/stella/stella_install/sboproject/run/snIcm15/observed/LSQ14efd.json'))
     
#     dist = datastore['LSQ14efd']["lumdist"][0]["value"]
    # print dist, float(dist)
     s = star.read_file(path+'observed/LSQ14efd.txt',1)
     time = s[:,0] -56900.7+maxtime
     #   +0.7 for fm0.3-0.15M-14-1.5B (ni0.25)
     #   +1.9 for 0.15M-13-1B (ni0.14)
     band = s[:,1]
     mag = s[:,2] -18.88+maxmag
     #   +0.08 for fm0.3-0.15M-14-1.5B (ni0.25)
     magCorr = mag 
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
      
#     print col
#     print len(band), len(col)

#     plt.plot(h[:,0], h[:,6], color='k', label = 'Mbol')
#     plt.plot(h[:,0], h[:,7], color=(0.0,0.75,0.75,1.0), label = 'U')
#     plt.plot(h[:,0], h[:,8], color=(0.0,0.0,1.0,1.0), label = 'B')
#     plt.plot(h[:,0], h[:,9], color=(0.0,0.5,0.0,1.0), label = 'V')
#     plt.plot(h[:,0], h[:,10], color=(0.75,0.0,0.75,1.0), label = 'I')
#     plt.plot(h[:,0], h[:,11], color=(1.0,0.0,0.0,1.0), label = 'R')

     plt.scatter(time,magCorr,s=20,c=col,label='LSQ14efd',zorder=3)     
     plt.plot(Utime,U, color=(0.0,0.75,0.75,1.0), label = 'U',linewidth=0.5)
     plt.plot(Btime,B, color=(0.0,0.0,1.0,1.0), label = 'B',linewidth=0.5)
     plt.plot(Vtime,V, color=(0.0,0.5,0.0,1.0), label = 'V',linewidth=0.5)
     plt.plot(Rtime,R, color=(0.75,0.0,0.75,1.0), label = 'I',linewidth=0.5)
     plt.plot(Itime,I, color=(1.0,0.0,0.0,1.0), label = 'R',linewidth=0.5)
     plt.xlim(0,100)
     plt.ylim(-15,-19)
     plt.legend(loc = 'best',shadow = False)
     plt.savefig(path+dirname+'lsq.png', format='png')
     plt.show()    
