# EVB with GROMACS tutorial

In this tutorial we will go over how to perform EVB calculations using GROMACS <br/>
GROMACS can perform Free Energy perturbation calculations but not do EVB corrections, so, we will go through how to perform an FEP calculation in GROMACS for a very simple [reaction](reaction_evb.png) 

To get started let's go to prepare the system [here](Preparing.ipynb)

## Executable file with MPI

Once you have prepared all the `.txt` files I have created also an [MPI implementation](EVB_MPI.py) of the EVB driver that will print the activation free energy and reaction free energy in kcal/mol and in addition will generate a pdf plot of the profile called `evb.pdf`. This implementation can be advantageous when carrying many lambdas or long datafiles.
In order to execute the MPI implementation we need to have installed `mpi4py`.
To install it, execute in terminal the following line:
```
python -m pip install mpi4py
```
Once installed, the script can be executed as follows:
```
mpirun -np P python EVB_MPI.py H12 alpha num_lambdas
```
Where `P` is the number of processes that shall be used (it shall not exceed the number of cores of your computer). `H12` is the coupling term guess, `alpha` is the alpha shift guess and `num_lambdas` is the number of lambdas that you have from the FEP.
The plot generated can be seen in this file [evb.py](evb.pdf)
