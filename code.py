import numpy as np
import matplotlib.pyplot as plt

dt = 0.001
t = np.arange(0, 1.6, dt)

G = np.zeros(len(t))

for k in range(len(t)):

    if t[k] < 0.4:
        G[k] = 1000

    elif t[k] < 0.8:
        G[k] = 800

    elif t[k] < 1.2:
        G[k] = 700

    else:
        G[k] = 1000

Voc = 40
Vmpp = 32
Pmax_nom = 10000

tau = 0.02

def pv_power(V, G):

    Pmax = Pmax_nom * (G / 1000)

    P = Pmax * (1 - ((V - Vmpp)/Vmpp)**2)

    return max(P,0)

Pideal = Pmax_nom * (G/1000)

# P&O

Vpo = np.zeros(len(t))
Ppo = np.zeros(len(t))

Vref = 25
deltaV = 0.5

Pold = 0
Vold = 0

for k in range(1, len(t)):

    # dinâmica do boost
    Vpo[k] = Vpo[k-1] + (dt/tau)*(Vref - Vpo[k-1])

    # ruído
    noise = np.random.normal(0,30)

    Ppo[k] = pv_power(Vpo[k], G[k]) + noise

    dP = Ppo[k] - Pold
    dV = Vpo[k] - Vold

    if dP > 0:

        if dV > 0:
            Vref += deltaV
        else:
            Vref -= deltaV

    else:

        if dV > 0:
            Vref -= deltaV
        else:
            Vref += deltaV

    Pold = Ppo[k]
    Vold = Vpo[k]

# INCOND

Vinc = np.zeros(len(t))
Pinc = np.zeros(len(t))

Vref = 25

Iold = 0
Vold = 0

for k in range(1, len(t)):

    Vinc[k] = Vinc[k-1] + (dt/tau)*(Vref - Vinc[k-1])

    noise = np.random.normal(0,30)

    Pinc[k] = pv_power(Vinc[k], G[k]) + noise

    Ipv = Pinc[k]/max(Vinc[k],0.1)

    dI = Ipv - Iold
    dV = Vinc[k] - Vold

    if abs(dV) > 1e-6:

        incCond = dI/dV
        cond = -Ipv/Vinc[k]

        if incCond > cond:
            Vref += deltaV

        elif incCond < cond:
            Vref -= deltaV

    Iold = Ipv
    Vold = Vinc[k]

# ERRO MPPT

Erro_PO = Pideal - Ppo
Erro_INC = Pideal - Pinc


# GRÁFICOS


plt.figure(figsize=(14,10))

plt.subplot(3,1,1)

plt.plot(t, Pideal, 'k--', linewidth=2, label='MPP Ideal')
plt.plot(t, Ppo, label='P&O')
plt.plot(t, Pinc, label='InCond')

plt.ylabel('Potência (W)')
plt.title('Comparação MPPT')
plt.legend()
plt.grid(True)

plt.subplot(3,1,2)

plt.plot(t, Erro_PO, label='Erro P&O')
plt.plot(t, Erro_INC, label='Erro InCond')

plt.ylabel('Erro (W)')
plt.legend()
plt.grid(True)

plt.subplot(3,1,3)

plt.plot(t, G)

plt.ylabel('Irradiância')
plt.xlabel('Tempo (s)')
plt.grid(True)

plt.tight_layout()
plt.show()

plt.figure(figsize=(10,5))

plt.plot(t, Pideal, 'k--', linewidth=2, label='MPP Ideal')
plt.plot(t, Ppo, 'b', linewidth=2, label='P&O')

plt.title('P&O MPPT')
plt.xlabel('Tempo (s)')
plt.ylabel('Potência (W)')
plt.grid(True)
plt.legend()

plt.figure(figsize=(10,5))

plt.plot(t, Pideal, 'k--', linewidth=2, label='MPP Ideal')
plt.plot(t, Pinc, 'r', linewidth=2, label='Incremental Conductance')

plt.title('Incremental Conductance MPPT')
plt.xlabel('Tempo (s)')
plt.ylabel('Potência (W)')
plt.grid(True)
plt.legend()

plt.figure(figsize=(12,5))

plt.plot(t, Ppo, linewidth=2, label='P&O')
plt.plot(t, Pinc, linewidth=2, label='InCond')

plt.title('Comparação de Potência')
plt.xlabel('Tempo (s)')
plt.ylabel('Potência (W)')
plt.grid(True)
plt.legend()

plt.figure(figsize=(12,5))

plt.plot(t, Pideal-Ppo, linewidth=2, label='Erro P&O')
plt.plot(t, Pideal-Pinc, linewidth=2, label='Erro InCond')

plt.title('Erro de Rastreamento MPPT')
plt.xlabel('Tempo (s)')
plt.ylabel('Erro (W)')
plt.grid(True)
plt.legend()

plt.figure(figsize=(12,4))

plt.plot(t, G, 'k', linewidth=2)

plt.title('Perfil de Irradiância')
plt.xlabel('Tempo (s)')
plt.ylabel('Irradiância (W/m²)')
plt.grid(True)
