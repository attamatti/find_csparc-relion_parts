#!/usr/bin/env python
import sys

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile_new(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i:
            labelsdic[i.split()[0]] = labcount
            labcount +=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        elif len(i.split())>=1:
            data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

errmsg = '\nUSAGE: find_csparc-relion_particles.py <cryosparc star file> <relion star file>'


try:
    clabels,cheader,cdata = read_starfile_new(sys.argv[1])
except:
    sys.exit('ERROR: can not read cryosparc star file{0}'.format(errmsg))
try:
    rlabels,rheader,rdata = read_starfile_new(sys.argv[2])
except:
    sys.exit('ERROR: can not read realion star file{0}'.format(errmsg))
cs_parts=[]         #{xyimage}
print(clabels)
for i in cdata:
    partid = i[clabels['_rlnImageName']].split('@')[0]+i[clabels['_rlnImageName']].split('@')[-1].split('/')[-1]
    cs_parts.append(partid)

rln_parts = {}              # {partID:line} 
for i in rdata:
    partid = i[rlabels['_rlnImageName']].split('@')[0]+i[rlabels['_rlnImageName']].split('@')[-1].split('/')[-1]
    rln_parts[partid] = i

foundparts = list(set(cs_parts) &set(list(rln_parts)))

print list(rln_parts)

output = open('csparc-relion_fixed.star','w')
for i in rheader:
    output.write('{0}\n'.format(i))

count = 0
for i in foundparts:
    output.write('\n{0}'.format('    '.join(rln_parts[i])))
    count +=1
print('{0}/{1} particles found'.format(count,len(cs_parts)))
print('{0}/{1} total particles'.format(count,len(rln_parts)))