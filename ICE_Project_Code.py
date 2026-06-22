import numpy as np
import matplotlib.pyplot as plt

gamma = 1.4
Cv = 0.718
Cp = 1.005

P1 = 100     
T1 = 300      
alpha = 1.7   
T_limit = 2500   

r_list = [12, 13, 14, 15, 16, 17, 18]

Qin_list = []
eff_list = []
T4_list = []
all_data = {}   

for r in r_list:
    rc = 1 + 0.05 * (r - 1)

    V1 = 1          
    V2 = V1 / r

    T2 = T1 * r**(gamma - 1)
    P2 = P1 * r**gamma

    P3 = alpha * P2
    T3 = alpha * T2
    V3 = V2

    P4 = P3
    T4 = T3 * rc
    V4 = rc * V3

    V5 = V1
    T5 = T4 * (V4 / V5)**(gamma - 1)
    P5 = P4 * (V4 / V5)**gamma

    Q23 = Cv * (T3 - T2)
    Q34 = Cp * (T4 - T3)
    Qin = Q23 + Q34
    Qout = Cv * (T5 - T1)
    Wnet = Qin - Qout
    eff = Wnet / Qin

    Qin_list.append(Qin)
    eff_list.append(eff * 100)
    T4_list.append(T4)

    all_data[r] = [rc, T2, T3, T4, T5, P2, P3, P4, P5, V2, V3, V4, V5, Qin, Qout, Wnet, eff]

    print("r =", r, " T4 =", round(T4, 1), " Qin =", round(Qin, 2), " eff =", round(eff * 100, 2))

print()

def get_T4(r):
    rc = 1 + 0.05 * (r - 1)
    T2 = T1 * r**(gamma - 1)
    T3 = alpha * T2
    T4 = T3 * rc
    return T4

r_low = 14
r_high = 15

for step in range(50):
    r_mid = (r_low + r_high) / 2
    T4_mid = get_T4(r_mid)
    if T4_mid > T_limit:
        r_high = r_mid
    else:
        r_low = r_mid

best_r = r_low  

print("exact best r =", round(best_r, 4))
print("T4 at this r =", round(get_T4(best_r), 2))

rc = 1 + 0.05 * (best_r - 1)
V2 = V1 / best_r
T2 = T1 * best_r**(gamma - 1)
P2 = P1 * best_r**gamma
P3 = alpha * P2
T3 = alpha * T2
V3 = V2
P4 = P3
T4 = T3 * rc
V4 = rc * V3
V5 = V1
T5 = T4 * (V4 / V5)**(gamma - 1)
P5 = P4 * (V4 / V5)**gamma
Q23 = Cv * (T3 - T2)
Q34 = Cp * (T4 - T3)
Qin = Q23 + Q34
Qout = Cv * (T5 - T1)
Wnet = Qin - Qout
eff = Wnet / Qin

Q_use = Qin   

print("Qin to use:", round(Q_use, 2))
print("dual eff:", round(eff * 100, 2))

V2o = V1 / best_r
T2o = T1 * best_r**(gamma - 1)
P2o = P1 * best_r**gamma
T3o = T2o + Q_use / Cv
P3o = P2o * (T3o / T2o)
V3o = V2o
V4o = V1
T4o = T3o * (V3o / V4o)**(gamma - 1)
P4o = P3o * (V3o / V4o)**gamma
Qouto = Cv * (T4o - T1)
Wneto = Q_use - Qouto
effo = 1 - 1 / best_r**(gamma - 1)   

print()
print("OTTO CYCLE")
print("T3 (Tmax):", round(T3o, 1))
print("eff:", round(effo * 100, 2))

V2d = V1 / best_r
T2d = T1 * best_r**(gamma - 1)
P2d = P1 * best_r**gamma
T3d = T2d + Q_use / Cp
P3d = P2d
rcd = T3d / T2d  
V3d = rcd * V2d
V4d = V1
T4d = T3d * (V3d / V4d)**(gamma - 1)
P4d = P3d * (V3d / V4d)**gamma
Qoutd = Cv * (T4d - T1)
Wnetd = Q_use - Qoutd
effd = Wnetd / Q_use

print()
print("DIESEL CYCLE")
print("T3 (Tmax):", round(T3d, 1))
print("eff:", round(effd * 100, 2))

print()
print("COMPARISON at r =", best_r)
print("Dual   eff:", round(eff * 100, 2))
print("Otto   eff:", round(effo * 100, 2))
print("Diesel eff:", round(effd * 100, 2))

def expand_curve(Va, Vb, Pa):
    V_arr = np.linspace(Va, Vb, 100)
    P_arr = Pa * (Va / V_arr)**gamma
    return V_arr, P_arr

plt.plot(r_list, Qin_list, marker='o')
plt.xlabel("compression ratio r")
plt.ylabel("Qin (kJ/kg)")
plt.title("Dual Cycle - Heat Input vs r")
plt.grid(True)
plt.show()

plt.plot(r_list, eff_list, marker='o', color='green')
plt.xlabel("compression ratio r")
plt.ylabel("efficiency (%)")
plt.title("Dual Cycle - Efficiency vs r")
plt.grid(True)
plt.show()

Vc, Pc = expand_curve(V1, V2, P1)
plt.plot(Vc, Pc, 'b')
plt.plot([V2, V3], [P2, P3], 'b')
plt.plot([V3, V4], [P3, P4], 'b')
Vc, Pc = expand_curve(V4, V5, P4)
plt.plot(Vc, Pc, 'b')
plt.plot([V5, V1], [P5, P1], 'b', label="Dual")

Vc, Pc = expand_curve(V1, V2o, P1)
plt.plot(Vc, Pc, 'r')
plt.plot([V2o, V3o], [P2o, P3o], 'r')
Vc, Pc = expand_curve(V3o, V4o, P3o)
plt.plot(Vc, Pc, 'r')
plt.plot([V4o, V1], [P4o, P1], 'r', label="Otto")

Vc, Pc = expand_curve(V1, V2d, P1)
plt.plot(Vc, Pc, 'g')
plt.plot([V2d, V3d], [P2d, P3d], 'g')
Vc, Pc = expand_curve(V3d, V4d, P3d)
plt.plot(Vc, Pc, 'g')
plt.plot([V4d, V1], [P4d, P1], 'g', label="Diesel")

plt.xlabel("V (m3/kg)")
plt.ylabel("P (kPa)")
plt.title("Dual vs Otto vs Diesel P-V Diagram")
plt.legend()
plt.grid(True)
plt.show()

re = 17   

V2a = V1 / best_r
V4a = re * V2a   

T2a = T1 * best_r**(gamma - 1)
P2a = P1 * best_r**gamma

T3a = T2a + Q_use / Cv
P3a = P2a * (T3a / T2a)
V3a = V2a

T4a = T3a * (V3a / V4a)**(gamma - 1)
P4a = P3a * (V3a / V4a)**gamma

Qouta = Cv * (T4a - T1)
Wneta = Q_use - Qouta
effa = Wneta / Q_use

print()
print("ATKINSON CYCLE")
print("rc =", best_r, " re =", re)
print("Tmax:", round(T3a, 1))
print("Wnet:", round(Wneta, 2))
print("eff:", round(effa * 100, 2))

print()
print("compare with Otto eff:", round(effo * 100, 2))
print("compare with Atkinson eff:", round(effa * 100, 2))

Vc, Pc = expand_curve(V1, V2a, P1)
plt.plot(Vc, Pc, color='orange')
plt.plot([V2a, V3a], [P2a, P3a], color='orange')
Vc, Pc = expand_curve(V3a, V4a, P3a)
plt.plot(Vc, Pc, color='orange')
plt.plot([V4a, V1], [P4a, P1], color='orange', linestyle='--')
plt.xlabel("V (m3/kg)")
plt.ylabel("P (kPa)")
plt.title("Atkinson Cycle P-V Diagram")
plt.grid(True)
plt.show()

Vd = 1.498e-3 
eta_v = 0.9     
P_in = 100000 
T_in = 300     
R_SI = 287  

rho_air = P_in / (R_SI * T_in)
print()
print("air density:", round(rho_air, 4), "kg/m3")

rpm_list = [1000, 2000, 3000, 4000, 5000, 6000, 6500]
for rpm in rpm_list:
    mdot = eta_v * rho_air * Vd * (rpm / 60) / 2
    print("rpm:", rpm, " mdot:", round(mdot * 1000, 3), "g/s")

final_drive = 3.9
tire_radius = 0.29   

gear_names = ["1st", "2nd", "3rd", "4th"]
gear_ratios = [2.785, 1.545, 1.000, 0.694]

print()
for i in range(len(gear_names)):
    name = gear_names[i]
    ratio = gear_ratios[i]
    speeds = []
    for rpm in [1000, 2000, 3000, 4000, 5000, 6000]:
        omega = 2 * np.pi * rpm / 60
        v = (omega * tire_radius) / (ratio * final_drive)
        v_kmh = v * 3.6
        speeds.append(round(v_kmh, 1))
    print(name, " ratio:", ratio, " speeds:", speeds)

rpm_range = np.linspace(500, 6500, 100)
mdot_range = eta_v * rho_air * Vd * (rpm_range / 60) / 2

plt.plot(rpm_range, mdot_range * 1000)
plt.xlabel("RPM")
plt.ylabel("mass flow rate (g/s)")
plt.title("Mass Flow Rate vs RPM (Nissan Sunny 1.5L)")
plt.grid(True)
plt.show()

rpm_range2 = np.linspace(500, 7000, 100)
for i in range(len(gear_names)):
    name = gear_names[i]
    ratio = gear_ratios[i]
    omega = 2 * np.pi * rpm_range2 / 60
    v_kmh = (omega * tire_radius) / (ratio * final_drive) * 3.6
    plt.plot(rpm_range2, v_kmh, label=name)

plt.xlabel("RPM")
plt.ylabel("speed (km/h)")
plt.title("Vehicle Speed vs RPM for Each Gear (Nissan Sunny)")
plt.legend()
plt.grid(True)
plt.show()

IVO = 350
IVC = 590
EVO = 490
EVC = 370

theta = np.linspace(0, 720, 2000)   


def get_lift(theta_array, open_angle, close_angle, max_lift):

    lift = np.zeros_like(theta_array)
    duration = close_angle - open_angle
    for i in range(len(theta_array)):
        th = theta_array[i]
        if open_angle <= th <= close_angle:
            lift[i] = max_lift * np.sin(np.pi * (th - open_angle) / duration)
    return lift


lift_intake = get_lift(theta, IVO, IVC, 8.5)
lift_exhaust = get_lift(theta, EVO, EVC + 360, 8.0)   

plt.plot(theta, lift_intake, color='blue', label='intake')
plt.plot(theta, lift_exhaust, color='red', label='exhaust')
plt.xlabel("crank angle (deg)")
plt.ylabel("lift (mm)")
plt.title("Valve Lift vs Crank Angle")
plt.legend()
plt.grid(True)
plt.show()


Pt = 105000
Tt = 300

Pratio_crit = (2 / (gamma + 1))**(gamma / (gamma - 1))
P_crit = Pratio_crit * Pt
print()
print("critical pressure ratio:", round(Pratio_crit, 4))
print("critical pressure:", round(P_crit / 1000, 2), "kPa")

P_up_values = np.linspace(20000, 105000, 300)
Vt_values = []
mdot_values = []

for Pu in P_up_values:
    ratio = Pu / Pt
    if ratio <= Pratio_crit:
        T_throat = Tt * 2 / (gamma + 1)
        Vt = np.sqrt(gamma * R_SI * T_throat)
        rho_throat = (Pratio_crit * Pt) / (R_SI * T_throat)
        mdot = rho_throat * Vt * 1e-4
    else:
        Ma = np.sqrt((2 / (gamma - 1)) * (ratio**(-(gamma - 1) / gamma) - 1))
        T_throat = Tt * ratio**((gamma - 1) / gamma)
        Vt = Ma * np.sqrt(gamma * R_SI * T_throat)
        rho_throat = Pu / (R_SI * T_throat)
        mdot = rho_throat * Vt * 1e-4

    Vt_values.append(Vt)
    mdot_values.append(mdot)

Vt_values = np.array(Vt_values)
mdot_values = np.array(mdot_values)



print("max throat velocity:", round(max(Vt_values), 1), "m/s")
print("max mass flow rate:", round(max(mdot_values) * 1000, 3), "g/s")

P_up_kpa = P_up_values / 1000

plt.plot(P_up_kpa, Vt_values, color='blue')
plt.axvline(P_crit / 1000, color='black', linestyle=':', label='critical pressure')
plt.xlabel("upstream pressure (kPa)")
plt.ylabel("throat velocity (m/s)")
plt.title("Throat Velocity vs Upstream Pressure")
plt.legend()
plt.grid(True)
plt.show()



Ru = 82.06    
tau = 0.002   



def k1_rate(T):

    A = 1.8e8
    Ea_R = 38370
    return A * np.exp(-Ea_R / T)


def O_concentration(T):

    return 3.97e5 * np.sqrt(1 / (Ru * T)) * np.exp(-31090 / T)


def N2_concentration(T):
    return 0.79 / (Ru * T)


def calc_NOx_ppm(T):
    O = O_concentration(T)
    N2 = N2_concentration(T)
    rate = 2 * k1_rate(T) * O * N2
    NO_conc = rate * tau
    total_conc = 1 / (Ru * T)
    ppm = (NO_conc / total_conc) * 1e6
    if ppm < 0:
        ppm = 0
    return ppm


cycle_names = ["Dual", "Otto", "Diesel", "Atkinson"]
Tmax_values = [T4, T3o, T3d, T3a]  

nox_values = []
print()
for i in range(len(cycle_names)):
    name = cycle_names[i]
    T = Tmax_values[i]
    ppm = calc_NOx_ppm(T)
    nox_values.append(ppm)
    print(name, " Tmax:", round(T, 1), " NOx:", round(ppm, 1), "ppm")

bar_colors = ['blue', 'red', 'green', 'orange']

plt.bar(cycle_names, nox_values, color=bar_colors)
plt.yscale('log')
plt.ylabel("NOx (ppm) - log scale")
plt.title("NOx Emissions Comparison")
plt.grid(True, axis='y', which='both')


for i in range(len(cycle_names)):
    plt.text(i, nox_values[i]*1.15, str(round(nox_values[i],1)), ha='center')

plt.show()
