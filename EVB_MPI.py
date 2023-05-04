import numpy as np
import matplotlib.pyplot as plt
import sys
from mpi4py import MPI
from scipy import interpolate

RT = 2.479
H12 = float(sys.argv[1])
alpha = float(sys.argv[2])
#H12 = 67.5
#alpha = 29.8
num_lam = int(sys.argv[3])
l = np.linspace(0, num_lam-1, num_lam+1)

def evb_driver(lambda_0, lambda_1, l_val):
    state0_av = np.average(lambda_0)
    state1_av = np.average(lambda_1) + alpha
    e_g = 0.5*(state1_av+state0_av)-0.5*np.sqrt((state1_av-state0_av)**2+4*H12**2)
    vi = state0_av + state1_av
    evb = np.exp(-(e_g-vi)/RT)
    dG_EVB = -RT*np.log(evb)
    print(f"Done for lambda: {l_val}")
    return dG_EVB

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

files = [f"{i}.txt" for i in range(num_lam)]
files_per_process = len(files) // size
if rank < len(files) % size:
    files_per_process += 1
my_files = files[rank * files_per_process:(rank + 1) * files_per_process]

evb_dG = []
lambdas = []
for fil in my_files:
    l_val = int(fil.split(".")[0])
    with open(fil) as f:
        lambda_0, lambda_1 = np.loadtxt(f, unpack=True)
    dg_evb = evb_driver(lambda_0, lambda_1, l_val)
    evb_dG.append(dg_evb)
    lambdas.append(l_val)

all_evb_dG = comm.gather(evb_dG, root=0)
all_lambdas = comm.gather(lambdas, root=0)

if rank == 0:
    evb_dG = [item for sublist in all_evb_dG for item in sublist]
    lambdas = [item for sublist in all_lambdas for item in sublist]
    EVB_lam = np.column_stack((lambdas, evb_dG))
    EVB_lambdas = EVB_lam[EVB_lam[:, 0].argsort()]
    en = EVB_lambdas.T[1]
    min_energy = min(en)
    EVB_integral = [(en[i]-min_energy) for i in range(1, len(en))]
    r_coord = [i for i in range(1, len(en))]

    f = interpolate.interp1d(r_coord, EVB_integral, kind='cubic')
    xnew = np.linspace(1, len(en)-1, 1000)
    ynew = f(xnew)

    # Find the minimum and maximum points
    max_point = (xnew[np.argmax(ynew)], ynew.max())
    min_points = [(xnew[np.argmin(ynew[:len(ynew)//2])], ynew[:len(ynew)//2].min()), 
                (xnew[len(ynew)//2+np.argmin(ynew[len(ynew)//2:])], ynew[len(ynew)//2:].min())]

    # Calculate the activation and reaction free energies
    act_free_energy = max_point[1] - min_points[0][1]
    react_free_energy = min_points[1][1] - min_points[0][1]

    # Print Activation and Reaction free energies
    print(f"Activation free energy: {act_free_energy:.2f} kcal/mol")
    print(f"Reaction free energy: {react_free_energy:.2f} kcal/mol")

    plt.plot(xnew, ynew, label='EVB')
    plt.ylabel('$\Delta G\;[kcal/mol]$', fontsize=20)
    plt.xlabel('$\lambda$', fontsize=20)
    plt.legend(loc='upper center')
    plt.savefig("evb.pdf", format="pdf")




