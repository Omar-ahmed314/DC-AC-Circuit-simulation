import os
os.environ["LANG"]="en_US.UTF-8"
import ahkab
import math
from ahkab import circuit,printing,time_functions
import numpy as np











pi=np.pi
file=input("Enter the name of the file + .txt :")
cir=open(file,'r')  #opening the netlist file
out_put=open('out_put.txt','w')
ac_circuit=circuit.Circuit("Ac Circuit")
freq=int(input("Enter the frequency : "))
sympols=[]
impedence=[]
sn=[]
en=[]

for line in cir:
    words=line.split()
    if (words[0][0]=='V'):
        e_ip=words[0]

        n1=words[1]
        n2=words[2]
        ac_value=float(words[3])
        phase=float(words[4])*(pi/180)
        comx=complex(ac_value*np.math.cos(phase),ac_value*np.math.sin(phase))



        ac_circuit.add_vsource(e_ip,n1,n2,dc_value=0,ac_value=comx)
        sympols.append(e_ip)
        impedence.append(0)
        sn.append(n1)
        en.append(n2)

    elif (words[0][0]=='R'):
        e_ip=words[0]
        n1 = words[1]
        n2 = words[2]
        value=float(words[3])
        ac_circuit.add_resistor(e_ip,n1,n2,value)
        sympols.append(e_ip)
        impedence.append(value)
        sn.append(n1)
        en.append(n2)
    elif (words[0][0]=='C'):
        e_ip = words[0]
        n1 = words[1]
        n2 = words[2]
        value = float(words[3])
        ac_circuit.add_capacitor(e_ip, n1, n2,value)
        sympols.append(e_ip)
        impedence.append(complex(0,-1*(1/(freq*value))))
        sn.append(n1)
        en.append(n2)
    elif (words[0][0]=='L'):
        e_ip = words[0]
        n1 = words[1]
        n2 = words[2]
        value = float(words[3])
        ac_circuit.add_inductor(e_ip, n1, n2, value)
        sympols.append(e_ip)
        impedence.append(complex(0,freq*value))
        sn.append(n1)
        en.append(n2)
    elif (words[0][0]=='I'):
        e_ip = words[0]
        n1 = words[1]
        n2 = words[2]
        ac_value = float(words[3])
        phase = float(words[4])
        comx=complex(ac_value*np.math.cos(phase),ac_value*np.math.sin(phase))

        ac_circuit.add_isource(e_ip, n1, n2, dc_value=0, ac_value=comx)
        sympols.append(e_ip)
        impedence.append(0)
        sn.append(n1)
        en.append(n2)
    elif (words[0][0]=='E'):
        e_ip = words[0]
        n1 = words[1]
        n2 = words[2]
        ns1=words[3]
        ns2=words[4]
        value=float(words[5])
        ac_circuit.add_vcvs(e_ip, n1, n2, ns1, ns2,value)
        sympols.append(e_ip)
        impedence.append(0)
        sn.append(n1)
        en.append(n2)
    elif (words[0][0]=='G'):
        e_ip = words[0]
        n1 = words[1]
        n2 = words[2]
        ns1 = words[3]
        ns2 = words[4]
        value = float(words[5])
        ac_circuit.add_vccs(e_ip, n1, n2, ns1, ns2,value)
        sympols.append(e_ip)
        impedence.append(0)
        sn.append(n1)
        en.append(n2)
    elif (words[0][0]=='F'):
        e_ip = words[0]
        n1 = words[1]
        n2 = words[2]
        v= words[3]

        value = float(words[4])
        ac_circuit.add_cccs(e_ip, n1, n2, id(v),value)
        sympols.append(e_ip)
        impedence.append(0)
        sn.append(n1)
        en.append(n2)

ac = ahkab.new_ac(start=freq, stop=freq, points=0,x0=None)
res = ahkab.run(ac_circuit, ac)
print(res['ac'].keys())


def check_v(e,n):
    if(e[n]=='0'):

        return 0
    else:
        v = res['ac']['V{}'.format(e[n])]
        return v


for l in range(len(sympols)):
    if(sympols[l][0]=='R'):
        v=abs((check_v(en,l)-check_v(sn,l)))


        power=((pow(v,2))/(2*impedence[l]))
        print('p({})' .format(sympols[l]),power,'W')
        out_put.write('p({})' .format(sympols[l])+' '+'{}'.format(power)+' '+'W\n')
    elif(sympols[l][0]=='C') :
        v = abs(check_v(en, l) - check_v(sn, l))
        power = np.imag((pow(v, 2)) / (2 * impedence[l]))
        print('p({})' .format(sympols[l]), power, 'VAR')
        out_put.write('p({})'.format(sympols[l]) + ' ' + '{}'.format(power) + ' ' + 'VAR\n')
    elif(sympols[l][0]=='L') :
        v = abs((check_v(en, l) - check_v(sn, l)))
        power = np.imag((pow(v, 2)) / (2 * impedence[l]))
        print('p({})' .format(sympols[l]), power, 'VAR')
        out_put.write('p({})'.format(sympols[l]) + ' ' + '{}'.format(power) + ' ' + 'VAR\n')
    elif(sympols[l][0]=='V') :
        v=((check_v(sn,l)) - (check_v(en,l)))

        power=v*(np.conj(res['ac']['I({})'.format(sympols[l])]))/2
        print('p({})' .format(sympols[l]),power,'VA')
        out_put.write('p({})'.format(sympols[l]) + ' ' + '{}'.format(power) + ' ' + 'VA\n')


    elif(sympols[l][0]=='I'):
        v = ((check_v(sn, l)) - (check_v(en, l)))
        power = v*(np.conj(res['ac']['I({})'.format(sympols[l])])) / 2

        print('p({})' .format(sympols[l]) , power, 'VA')
        out_put.write('p({})'.format(sympols[l]) + ' ' + '{}'.format(power) + ' ' + 'VA\n')
    elif (sympols[l][0] == 'E'):
        v = ((check_v(sn, l)) - (check_v(en, l)))
        power = v * (np.conj(res['ac']['I({})'.format(sympols[l])])) / 2

        print('p({})'.format(sympols[l]), power, 'VA')
        out_put.write('p({})'.format(sympols[l]) + ' ' + '{}'.format(power) + ' ' + 'VA\n')
    elif (sympols[l][0] == 'G'):
        v = abs((check_v(sn, l)) - (check_v(en, l)))
        power = v * (np.conj(res['ac']['I({})'.format(sympols[l])])) / 2

        print('p({})'.format(sympols[l]), power, 'VA')
        out_put.write('p({})'.format(sympols[l]) + ' ' + '{}'.format(power) + ' ' + 'VA\n')
    elif (sympols[l][0] == 'F'):
        v = abs((check_v(sn, l)) - (check_v(en, l)))
        power = v * (np.conj(res['ac']['I({})'.format(sympols[l])])) / 2

        print('p({})'.format(sympols[l]), power, 'VA')
        out_put.write('p({})'.format(sympols[l]) + ' ' + '{}'.format(power) + ' ' + 'VA\n')

cir.close()
out_put.close()

