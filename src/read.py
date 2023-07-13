# -------------- Required packages
import numpy as np
import h5py
import pycstruct
from scipy.interpolate import NearestNDInterpolator

# -------------- Read file functions

def read_hdf5(file):
    # Read hdf5-file:
    h = h5py.File(file, 'r')

    # Internal units:
    ulength = h['Header'].attrs['UnitLength_in_cm']
    umass   = h['Header'].attrs['UnitMass_in_g']
    uvel    = h['Header'].attrs['UnitVelocity_in_cm_per_s']
    utime   = ulength/uvel
    udens   = umass/(ulength**3)
    uaccel  = uvel/utime
    uinterg = uvel**2
    uangmom = ulength * uvel * umass
    iu = {
        'ulength' : ulength,
        'umass'   : umass,
        'uvel'    : uvel,
        'utime'   : utime,
        'udens'   : udens,
        'uaccel'  : uaccel,
        'uinterg' : uinterg,
        'uangmom' : uangmom
    }

    return h, iu

def read_dump(file, spin=False, bh=False, hm=False, rcirc=False):
    f = open(file, 'rb')
    
    time = np.fromfile(f, np.float64, 1)
    NSinksAllTasks = np.fromfile(f, np.uint32, 1)
    sinks = {}
    
    fields = ['Pos', 'Vel', 'Accel', 'Mass', 'FormationMass', 'FormationTime', 
              'ID', 'HomeTask', 'Index', 'FormationOrder']
    
    if spin == True:
        fields += ['AngularMomentum']
        
    if bh == True:
        fields += ['BlackHole'] 
        if hm == True:
            fields += ['BlackHoleHotMode']
        fields += ['BlackHoleAccRadius', 'BlackHoleMass', 'BlackHoleDiskMass', 'BlackHoleReservoir', 'BlackHoleSinkAccRate', 'CellsTotalMassBuffer']
        if rcirc == True:
            fields += ['BlackHoleCircRadius']
    
    for i in fields:
        sinks[i] = []
        
    for i in range(NSinksAllTasks[0]):
        struct = pycstruct.StructDef(alignment = 8)
        struct.add('float64', 'Pos', shape=3)
        struct.add('float64', 'Vel', shape=3)
        struct.add('float64', 'Accel', shape=3)
        struct.add('float64', 'Mass')
        struct.add('float64', 'FormationMass')
        struct.add('float64', 'FormationTime')
        struct.add('uint64', 'ID')
        struct.add('uint32', 'HomeTask')
        struct.add('uint32', 'Index')
        struct.add('uint32', 'FormationOrder')
        if spin == True:
            struct.add('float64', 'AngularMomentum', shape=3)
        if bh == True:
            struct.add('uint32', 'BlackHole')
            if hm == True:
                struct.add('uint32', 'BlackHoleHotMode')
            struct.add('float64', 'BlackHoleAccRadius')
            struct.add('float64', 'BlackHoleMass')
            struct.add('float64', 'BlackHoleDiskMass')
            struct.add('float64', 'BlackHoleReservoir')
            struct.add('float64', 'BlackHoleSinkAccRate')
            struct.add('float64', 'CellsTotalMassBuffer')
            if rcirc == True:
                struct.add('float64', 'BlackHoleCircRadius')

        inbytes = f.read(struct.size())
        data = struct.deserialize(inbytes)
        for field in fields:
            sinks[field] += [data[field]]
    
    for field in fields:
        sinks[field] = np.array(sinks[field])
    
    f.close()
    
    return time, NSinksAllTasks, sinks


