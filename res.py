from pathlib import Path
from io import StringIO
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import star
from matplotlib import cm 

#dir = raw_input("Mdot logRmax Eburst = ")
dir = "nowind-1B"
#home = Path('/home/harim')
#topdir = (home / 'stella' / 'stella_install' / 'sboproject' / 'run' / 'snIcm7' 
#         / '1e-1 13 10')
#fname = topdir / 'snIcm7.res'
#savename = topdir / 'snIcm7_contents.txt'

ff = open('/home/harim/stella/stella_install/sboproject/run/snIcm7/'+dir+'/snIcm7.res','r')
lines = ff.read().splitlines()
Mtot = float(lines[5][43:48])

#with open(fname, 'r') as ff:
#    lines = ff.read().splitlines()
    
starts = []
ends = []
contents = dict(obstime=[], data=[])
colspecs = ((0, 4), (4, 13), (13, 25), (25, 33), (33, 43), (43, 51), (51, 58),
            (58, 65), (65, 72), (72, 79), (79, 89), (89, 99), (99, 109),
            (109, 119), (119, 124), (124, 134), (134, 144), (144, 154), 
            (154, 164), (164, 174))

for i, line in enumerate(lines):
    if line.startswith('%H:'):
        starts.append(i)
    elif line.startswith('%B:'):
        ends.append(i)

for i, idx in enumerate(starts):
    obst = lines[idx+3].split(' D ')[0].split('= ')[-1].strip()
    contents["obstime"].append(float(obst))
    contents["data"].append(lines[idx+4:ends[i]])

for i, item in enumerate(contents["data"]):
    np.savetxt("tmp.txt", item, fmt='%s')
    contents["data"][i] = pd.read_fwf("tmp.txt", colspecs=colspecs)
    
for i, item in enumerate(contents["data"]):
    if len(item) == 0:
        del contents["obstime"][i]
        del contents["data"][i]



def values():
    for i in contents["obstime"]:
        print i,",",
    print "Column names ZON AM/SOL R14. V 8. T 5. Trad5 lgD-6. lgP 7. lgQv lgQRT XHI ENG LUM CAPPA ZON.1 n_bar n_e Fe II III"

values()

def get_data_by_obstime(contents, obstime):
    idx = np.argwhere(np.array(contents["obstime"]) == float(obstime))
    results = []
    for i in idx:
        results.append(contents["data"][i[0]])
#    print(len(results))
    return results

#res = get_data_by_obstime(contents, 63.71283)
#res = res[0]


#mass without wind = 3.92860048014




def curve(obstime,y):
    res = get_data_by_obstime(contents, obstime)
    res = res[0] 
    mass_coordinate = []
    for i in res["AM/SOL"]:
        if i > 1e-1:
            mass_coordinate.append(i)
        else:
            mass_coordinate.append(Mtot+i)
    index = min(range(len(mass_coordinate)), key=lambda i: abs(mass_coordinate[i]-3.92860048014))
    plt.plot(mass_coordinate,res[y])
    plt.plot(mass_coordinate[index], res[y][index], "|", markersize=10, color='r')
    
    nzone = len(res)
    tau = np.zeros((nzone), float)
    for i in range(nzone-2,0,-1):
        tau[i] = tau[i+1] + res["CAPPA"][i]*10.**res["lgD-6."][i]*(res["R14."][i+1]-res["R14."][i])*1e8
    for j in range(0,nzone-1):
        if tau[j] >= 0.67 and tau[j+1] < 0.67:
            ntau = j
    plt.plot(mass_coordinate[ntau], res[y][ntau], '*', markersize=5, color='b')    
    plt.xlabel('Mr/M0')
    plt.ylabel(y)
    plt.savefig('/home/harim/Pictures/'+dir+'/'+y+'.png', format='png')
    plt.show()






def curve2(obstimes, y):
    for i, obst in enumerate(obstimes):
        mass_coordinate = []
        res = get_data_by_obstime(contents, obst)
        res = res[0] 
        for r in res["AM/SOL"]:
            if r > 1e-1:
                mass_coordinate.append(r)
            else:
                mass_coordinate.append(Mtot+r)
        index = min(range(len(mass_coordinate)), key=lambda k: abs(mass_coordinate[k]-3.92860048014))
        plt.plot(mass_coordinate, res[y], label="obstime=%.5f" % obst, color=cm.rainbow((len(obstimes)-i)*1.2/float(len(obstimes))))
        plt.plot(mass_coordinate[index], res[y][index], "|", markersize=15 , color='k')
        plt.legend()

        nzone = len(res)
        tau = np.zeros((nzone), float)
        for i in range(nzone-2,0,-1):
            tau[i] = tau[i+1] + res["CAPPA"][i]*10.**res["lgD-6."][i]*(res["R14."][i+1]-res["R14."][i])*1e8
        for j in range(0,nzone-1):
            if tau[j] >= 0.67 and tau[j+1] < 0.67:
                ntau = j
        plt.plot(mass_coordinate[ntau], res[y][ntau], '*', markersize=8, color='r')           
    plt.xlabel('Mr/M0')
    plt.ylabel(y)    
#    plt.savefig('/home/harim/Pictures/'+dir+'/multiple'+y+'.png', format='png')
    plt.show()    







def ionization(obstimes):
    for i, obst in enumerate(obstimes):
        mass_coordinate = []
        res = get_data_by_obstime(contents, obst)
        res = res[0] 
        for r in res["AM/SOL"]:
            if r > 1e-1:
                mass_coordinate.append(r)
            else:
                mass_coordinate.append(Mtot+r)
        index = min(range(len(mass_coordinate)), key=lambda k: abs(mass_coordinate[k]-3.92860048014))
        plt.plot(mass_coordinate, res["n_e"]/res["n_bar"], label="obstime=%.5f" % obst, color=cm.rainbow((len(obstimes)-i)*1.2/float(len(obstimes))))
        plt.plot(mass_coordinate[index], res["n_e"][index]/res["n_bar"][index], "|", markersize=15 , color='k')
        plt.legend()

        nzone = len(res)
        tau = np.zeros((nzone), float)
        for i in range(nzone-2,0,-1):
            tau[i] = tau[i+1] + res["CAPPA"][i]*10.**res["lgD-6."][i]*(res["R14."][i+1]-res["R14."][i])*1e8
        for j in range(0,nzone-1):
            if tau[j] >= 0.67 and tau[j+1] < 0.67:
                ntau = j
        plt.plot(mass_coordinate[ntau], res["n_e"][ntau]/res["n_bar"][ntau], '*', markersize=8, color='r')           
    plt.xlabel('Mr/M0')
    plt.ylabel("n_e/n_bar")    
    plt.show()    



def curve4(obstimes):
    for i, obst in enumerate(obstimes):
        mass_coordinate = []
        res = get_data_by_obstime(contents, obst)
        res = res[0] 
        for r in res["AM/SOL"]:
            if r > 1e-1:
                mass_coordinate.append(r)
            else:
                mass_coordinate.append(Mtot+r)
        index = min(range(len(mass_coordinate)), key=lambda k: abs(mass_coordinate[k]-3.92860048014))


        nzone = len(res)
        tau = np.zeros((nzone), float)
        for i in range(nzone-2,0,-1):
            tau[i] = tau[i+1] + res["CAPPA"][i]*10.**res["lgD-6."][i]*(res["R14."][i+1]-res["R14."][i])*1e8
        for j in range(0,nzone-1):
            if tau[j] >= 0.67 and tau[j+1] < 0.67:
                ntau = j
        plt.plot(mass_coordinate, tau, label="obstime=%.5f" % obst, color=cm.rainbow((len(obstimes)-i)*1.2/float(len(obstimes))))
        plt.plot(mass_coordinate[index], tau[index], "|", markersize=15 , color='k')
        plt.legend()
        plt.plot(mass_coordinate[ntau], tau[ntau], '*', markersize=8, color='r')           
    plt.xlabel('Mr/M0')
    plt.ylabel("tau")    
    plt.show()    




def wind(obstimes, y):
    for i, obst in enumerate(obstimes):
        mass_coordinate = []
        res = get_data_by_obstime(contents, obst)
        res = res[0] 
        for r in res["AM/SOL"]:
            if r > 1e-1:
                mass_coordinate.append(r)
            else:
                mass_coordinate.append(Mtot+r)
        index = min(range(len(mass_coordinate)), key=lambda k: abs(mass_coordinate[k]-3.92860048014))
        plt.plot(mass_coordinate, res[y], label="obstime=%.5f" % obst)
        plt.plot(mass_coordinate[index], res[y][index], "|", markersize=10, color='r')
        plt.legend()
        
        nzone = len(res)
        tau = np.zeros((nzone), float)
        for i in range(nzone-2,0,-1):
            tau[i] = tau[i+1] + res["CAPPA"][i]*10.**res["lgD-6."][i]*(res["R14."][i+1]-res["R14."][i])*1e8
        for j in range(0,nzone-1):
            if tau[j] >= 0.67 and tau[j+1] < 0.67:
                ntau = j
        plt.plot(mass_coordinate[ntau], res[y][ntau], '*', markersize=5, color='b')   
    plt.xlabel('Mr/M0')
    plt.ylabel(y)      
    plt.xlim(3.92,Mtot)
    plt.show()    
    
    
    
    
    
    
    
    
def log2(obstimes, y):
    for i, obst in enumerate(obstimes):
        mass_coordinate = []
        res = get_data_by_obstime(contents, obst)
        res = res[0] 
        for r in res["AM/SOL"]:
            if r > 1e-1:
                mass_coordinate.append(r)
            else:
                mass_coordinate.append(Mtot+r)
        index = min(range(len(mass_coordinate)), key=lambda k: abs(mass_coordinate[k]-3.92860048014))
        plt.plot(mass_coordinate, res[y], label="obstime=%.5f" % obst, color=cm.rainbow((len(obstimes)-i)*1.2/float(len(obstimes))))
        plt.plot(mass_coordinate[index], res[y][index], "|", markersize=15 , color='k')
        plt.legend()

        nzone = len(res)
        tau = np.zeros((nzone), float)
        for i in range(nzone-2,0,-1):
            tau[i] = tau[i+1] + res["CAPPA"][i]*10.**res["lgD-6."][i]*(res["R14."][i+1]-res["R14."][i])*1e8
        for j in range(0,nzone-1):
            if tau[j] >= 0.67 and tau[j+1] < 0.67:
                ntau = j
        plt.plot(mass_coordinate[ntau], res[y][ntau], '*', markersize=8, color='r')           
    plt.xlabel('Mr/M0')
    plt.ylabel('log'+y)
    plt.yscale('log')    
    plt.savefig('/home/harim/Pictures/'+dir+'/log'+y+'.png', format='png')
    plt.show()   






#for i, data in enumerate(contents["data"][3:10]):
#    plt.plot(data["AM/SOL"], data["Fe"])
#plt.yscale('log')
#plt.legend()
