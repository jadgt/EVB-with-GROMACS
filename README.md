# EVB_gromacs_tutorial

The EVB arises to aid the exploration of chemical reactivity in complex environments, where quantum mechanical methods are too expensive and molecular mechanics are too inaccurate to describe a high-quality potential energy surface\cite{warshel1980empirical}. In this regard, EVB is an intermediate approach between quantum and molecular mechanics where the environment and unactive parts of a molecule can be effectively treated by molecular mechanics but, the reactive region will be corrected by means of \textbf{empirical} (or quantum mechanical) references. In consequence, EVB is, in practice, a molecular mechanics method which introduces correction from empirical (or higher-level calculations) values for a reaction of interest. The major advantage of EVB is its capacity to describe changes in reactivity when the environment is changed. 

Let us consider a bond formation reaction defined by a reactant state 1 and a product state 2. The lowest energy eigenvalue will be given by the solution of the secular equation:$$\left|\begin{matrix}H_{11}-E_g&H_{12}-E_gS_{12}\\H_{21}-E_gS_{21}&H_{22}-E_g\\\end{matrix}\right|=0$$

Where $H_{11}$ and $H_{22}$ are the potential energy surfaces of reactant and products and are usually called diabatic potential surfaces.  $E_g$ is the adiabatic potential surface corresponding to the transformation from 1 to 2 and $S_{12}=S_{21}$ are the overlap between states which, in practice, are neglected and incorporated into the off-diagonal terms $H_{12}$ and $H_{21}$. In the framework of molecular mechanics, the diabatics will be defined as:
$$H_{11}=\mathcal{M}\left(r_1\right)+U_{active}^{(1)}+U_{inactive}^{(1)}$$
$$H_{22}=\mathcal{M}\left(r_2\right)+U_{active}^{(2)}+U_{inactive}^{(2)}+\alpha_{12}$$

Where $\mathcal{M}\left(r_i\right)$ denotes the Morse potential respect to the equilibrium in state $i$, $U_{active}^{(i)}$ is the force field energy of the active region (rest of bonds, angles and dihedrals affected by the bond formation), $U_{inactive}^{(i)}$ is the force field potential of the inactive part of the molecule and $\alpha_{12}$ is the energy difference between $H_{11}$ and $H_{22}$ at infinite separation. The treatment of the off-diagonal terms is purely empirical, and its mathematical description categorize the EVB methods in different formalisms. In this thesis the original formalism by Warshel \cite{warshel1980empirical}, where $H_{12}=H_{21}$ and equal to an exponential function, will be used.

Once obtained all the determinantal elements, the adiabatic $E_g$ will be given by the solution of 2.81:
$$E_g=\frac{1}{2}\left[\left(H_{11}+H_{22}\right)-\sqrt{\left(H_{11}-H_{22}\right)^2+4H_{12}^2}\right]$$
 
Which is the canonical equation of the EVB approach. 

*EVB free energy*

Once the adiabatic potential $E_g$ is obtained, the interest for a computational chemist in many cases will be obtaining the Gibbs free energy. One can use a \textbf{\gls{FEP}} molecular dynamics simulation in the isothermal-isobaric ensemble (NPT) and correct it with the EVB approach. The free energy perturbation is mathematically defined by the \textbf{Zwanzig equation} \cite{zwanzig1954high}:
$$\Delta G_{1\rightarrow 2}=-k_b T \ln \left\langle e^{\frac{H_{22}-H{11}}{k_B T}} \right\rangle_1$$
Where $\langle \rangle _1$ denotes the average over the ensemble of the state 1. This equation, besides its exactitude, computationally converges very slowly. To accelerate the convergence it is customary to use a \textbf{mapping potential} that slowly moves from state 1 to state 2 by dividing the reaction coordinate into symmetrical fragments. Introducing a coupling parameter $\lambda\ \in[0,1]$  the mapping potential will read as:
$$ \varepsilon_m(\lambda_m)=\ H_{11}(1-\lambda_m)+H_{22}\lambda_m $$

The free energy associated with an incremental change in the coupling parameter will be obtained applying 2.85:
$$\Delta G({\lambda_m \rightarrow \lambda_{m+1}})= -k_b T \ln \langle e^{(-\varepsilon_{m+1}-\varepsilon_m) / k_bT} \rangle_{\lambda_m}$$
And the total reaction free energy will be obtained by integrating the incremental variations given by 2.87. Finally, to introduce the EVB potential energy correction in the mapping potential, one can combine 2.84, 2.86 and 2.87 in the following way:
$$ \Delta G_{EVB}(\lambda_m \rightarrow \lambda_{m+1})=\log\left(\frac{e^{(-E_g(\lambda_m)-\varepsilon_m(\lambda_m)/RT} e^{(- \Delta G({\lambda_m \rightarrow \lambda_{m+1}})/RT}} {RT}\right) $$
And the summation of 2.88 over all $\lambda$ will give the *EVB corrected free energy* profile of reaction.

