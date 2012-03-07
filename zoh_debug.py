from pylab import *
from scipy import *


import controls

T = 50.0
dt = 1.0
step_time = dt
maxt = T

Gs = controls.TF(1,[1,1,0])
b,a = Gs.c2d(dt=1.0, method='zoh', maxt=50.0)#, step_time=step_time)


ystep = Gs.step_response(dt=dt, maxt=maxt, step_time=step_time)
myimp = Gs.create_impulse(dt=dt, maxt=maxt, imp_time=step_time)

num_order = Gs.den.order
den_order = Gs.den.order+1

nz, dz = controls.fit_discrete_response(ystep, myimp, \
                                        numorder=num_order, \
                                        denorder=den_order)#we want the numerator order to be one less than the denominator order - the denominator order +1 is the order of the denominator during a step response
            #multiply by (1-z^-1)
            
nz2 = r_[nz, [0.0]]
nzs = r_[[0.0],nz]
nz3 = nz2 - nzs
nzout, dzout = controls.polyfactor(nz3, dz)




# Test 2
k = 2.0
p = 5.0
dt2 = 1.0/500
T2 = 2.0
T2_hat = T2-dt2/2.0

G_RC = controls.TF(k,[1,p])
t2 = arange(0,T2,dt2)
u2 = G_RC.create_step_input(dt=dt2, maxt=T2_hat, indon=10)

y_RC = G_RC.lsim(u2,t2)

figure(1)
clf()
plot(t2,u2)
plot(t2,y_RC)

ylim([-0.01,1.2])

b2, a2 = G_RC.c2d(dt=dt2, method='zoh', maxt=T2_hat)

y_dig = zeros_like(u2)
Nden = len(a2)

for i in range(len(u2)):
    out = 0.0

    for n, bn in enumerate(b2):
        if (i-n) > 0:
            out += u2[i-n]*bn

    for n in range(1, Nden):
        if (i-n) > 0:
            out -= y_dig[i-n]*a2[n]

    out = out/a2[0]
    y_dig[i] = out


plot(t2, y_dig)

from scipy import signal

y_dig2 = signal.lfilter(b2,a2,u2)
plot(t2,y_dig2)

y_dig3 = zeros_like(u2)
Gz_plant = controls.Digital_Compensator(b2, a2, \
                                        input_vect=u2, \
                                        output_vect=y_dig3)

for i in range(len(u2)):
    y_i = Gz_plant.calc_out(i)
    y_dig3[i] = y_i

plot(t2, y_dig3)

test1 = y_dig - y_dig2
test2 = y_dig - y_RC
test3 = y_dig - y_dig3

i = 1
vect_list = [test1, test2, test3]

for vect in vect_list:
    cur_max = abs(vect).max()
    print('test%i = %0.4g' % (i, cur_max))
    i += 1
    
show()
