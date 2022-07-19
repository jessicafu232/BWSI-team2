# r = tc/2
def basic_radar_eq(t):
    c = 299792458 #m/s
    R = (t*c) / 2
    return R

def basic_radar_eq_mk2(r):
    c = 299792458 #m/s
    T = (2*r) / c
    return T

