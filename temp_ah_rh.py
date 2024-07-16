import numpy as np
import matplotlib.pyplot as plt

# Variablen
temp_grund = 9
temp_nutz = 14
temp_hoch = 26
rH_low = 45
rh_high = 65
temp_steps = 0.01

# Konstanten
temperatur_range = np.arange(-15, 46, temp_steps)  # Temperatur von -15 bis 45°C
absolute_humidity_range = np.linspace(0, 20, 100)  # Absolute Luftfeuchtigkeit von 0 bis 20 g/m³

# Funktion zur Berechnung des Sättigungsdampfdrucks (E_s) mit der Magnus-Formel
def magnus_formula(temp):
    temp = np.asarray(temp)  # Sicherstellen, dass temp ein Array ist
    es = np.where(temp > 0,
                   288.68 * (1.098 + temp / 100) ** 8.02 / 100,
                   4.689 * (1.486 + temp / 100) ** 12.3 / 100)
    return es

# Funktion zur Berechnung der relativen Luftfeuchtigkeit
def calculate_relative_humidity(temperature, absolute_humidity):
    es = magnus_formula(temperature)  # Sättigungsdampfdruck in hPa
    Mw = 18.016  # Molekulargewicht des Wasserdampfs in kg/kmol
    R = 8314.3  # Universelle Gaskonstante in J/(kmol·K)
    ea = absolute_humidity * (273.15 + temperature) * R / Mw / 1e5  # Tatsächlicher Dampfdruck in hPa
    RH = (ea / es) * 100  # Berechnung der relativen Luftfeuchtigkeit
    return RH

# Funktion zur Berechnung der absoluten Luftfeuchtigkeit
def calculate_absolute_humidity(temp, rel_humidity):
    E_s = magnus_formula(temp)
    E_a = (rel_humidity / 100.0) * E_s
    Mw = 18.016  # Molekulargewicht des Wasserdampfs in kg/kmol
    R = 8314.3  # Universelle Gaskonstante in J/(kmol·K)
    return 1e5 * Mw / R * E_a / (temp + 273.15)  # Absolute Luftfeuchtigkeit in g/m³

# Berechnung der absoluten Luftfeuchtigkeit für RH = 45% und 70%
absolute_humidity_low = calculate_absolute_humidity(temperatur_range, rH_low)
absolute_humidity_high = calculate_absolute_humidity(temperatur_range, rh_high)

# Plotting der Hauptgrafik
plt.figure(figsize=(8, 6))

# Berechnung der relativen Luftfeuchtigkeit für das Kontur-Plotting
relative_humidity_values = np.array([[calculate_relative_humidity(t, ah) for ah in absolute_humidity_range] for t in temperatur_range])

# Zeichnen der Konturen der relativen Luftfeuchtigkeit
RH_levels = [10, 20, 40, 50, 60, 80, 90, 100]
CS = plt.contour(absolute_humidity_range, temperatur_range, relative_humidity_values, levels=RH_levels, colors='lightgray', linestyles='dashed')
plt.clabel(CS, inline=True, fmt='%d%%', fontsize=10)  # % zu den Konturlabels hinzufügen

# Konturen für RH 45% und 70%
RH_levels = [rH_low, rh_high]
CS = plt.contour(absolute_humidity_range, temperatur_range, relative_humidity_values, levels=RH_levels, colors='gray', linestyles='dashed')
plt.clabel(CS, inline=True, fmt='%d%%', fontsize=10)

# Füllen des Bereichs zwischen RH 45% und RH 70%
plt.fill_betweenx(temperatur_range, absolute_humidity_low, absolute_humidity_high, 
                  where=(temperatur_range >= temp_grund) & (temperatur_range <= temp_hoch), 
                  color='lightgreen', alpha=0.5, edgecolor='black', linewidth=1.5)

# Festlegen der spezifischen x-Ticks
idx_temp_grund = np.argmin(np.abs(temperatur_range - temp_grund))
idx_temp_hoch = np.argmin(np.abs(temperatur_range - temp_hoch))

x_ticks = [
    absolute_humidity_low[idx_temp_grund],  # RH = 45% bei T = 9°C
    absolute_humidity_high[idx_temp_grund],  # RH = 65% bei T = 9°C
    absolute_humidity_high[idx_temp_hoch]  # RH = 65% bei T = 26°C
]
plt.xticks(x_ticks, [f"{x:.1f}" for x in x_ticks])  # Formatierung der x-Ticks

# Festlegen der y-Ticks
plt.yticks(np.arange(-15, 46, 5))

# Solid und gestrichelte Linien für spezifische Temperaturen
plt.axhline(y=temp_grund, color='black', linestyle='solid')   # T=9°C solid
plt.axhline(y=temp_hoch, color='black', linestyle='solid')  # T=26°C solid
plt.axhline(y=temp_nutz, color='black', linestyle='dashed')  # T=14°C gestrichelt

# Schalter für den zusätzlichen Punkt
winter_high_rH = True

if winter_high_rH:
    # Zielwert für die relative Luftfeuchtigkeit
    abs_point = 7
    T_point = 10

    # Berechnung des Schnittpunkts von abs_point bei RH = 65%
    crossing_temp = None
    for temp in temperatur_range:
        rh_values_at_temp = calculate_relative_humidity(temp, abs_point)
        if np.isclose(rh_values_at_temp, rh_high, atol=temp_steps):
            crossing_temp = temp
            break

    plt.plot(abs_point, T_point, 'ro')  # Punkt bei (x=7, T=10°C)
    plt.text(abs_point, T_point, f'({abs_point:.2f}, {T_point:.2f})', color='red', fontsize=12, verticalalignment='top')
    if crossing_temp is not None:
        plt.plot(abs_point, crossing_temp, 'bo')  # Punkt bei (abs_point=7, crossing_temp)
        plt.text(abs_point, crossing_temp, f'({abs_point:.2f}, {crossing_temp:.2f})', color='blue', fontsize=12, verticalalignment='bottom')
        plt.plot([abs_point, abs_point], [T_point, crossing_temp], 'g-')  # Linie zwischen beiden Punkten
    else:
        print("Kein Schnittpunkt bei RH=65%")

# Achsenbeschriftungen
plt.xlabel('Absolute Luftfeuchtigkeit (g/m³)')
plt.ylabel('Temperatur (°C)')
plt.grid(True)
plt.tight_layout()
plt.show()
