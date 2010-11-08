import functools
import os

L2_sharing = map(functools.partial(int,base=16),os.popen('cat /sys/devices/system/cpu/cpu?/cache/index2/shared_cpu_map'));
cpus= range(0,len(L2_sharing));
L2_sharing= set(L2_sharing)
nb=0
aff=''
for b in cpus:
    #cpu ok iff no bit is set below it's bit on a bitmap with it's bit is set
    # -> we take the highest cpu of a set sharing L2
    ok=True;
    for bitmap in L2_sharing:
        v= 1<<(b+1);
        if( (bitmap & v) and (bitmap &(v-1))):
            ok=False;
            break;
    if(ok):
        aff+=' %d'%b
        nb+=1
print("export OMP_NUM_THREADS=%d ; GOMP_CPU_AFFINITY=%s;"%(nb, aff))
