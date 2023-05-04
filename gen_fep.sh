
for (( i=0; i<11; i++ ))
do
    LAMBDA=$i

    # A new directory will be created for each value of lambda and
    # at each step in the workflow for maximum organization.

    mkdir Lambda_$LAMBDA
    cd Lambda_$LAMBDA

    ##############################
    # ENERGY MINIMIZATION STEEP  #
    ##############################
    echo "Starting minimization for lambda = $LAMBDA..." 

    mkdir EM
    cd EM

    # Iterative calls to grompp and mdrun to run the simulations

    gmx grompp -f ../../MDP/em_fep_$LAMBDA.mdp -c ../../init.gro -p ../../topol.top -o min$LAMBDA.tpr -maxwarn 1

    gmx mdrun -v -ntomp 4 -deffnm min$LAMBDA

    sleep 10

    #####################
    # NVT EQUILIBRATION #
    #####################
    echo "Starting constant volume equilibration..."

    cd ../
    mkdir NVT
    cd NVT

    gmx grompp -f ../../MDP/nvt_fep_$LAMBDA.mdp -c ../EM/min$LAMBDA.gro -p ../../topol.top -o nvt$LAMBDA.tpr -maxwarn 1

    gmx mdrun -v -ntomp 4 -deffnm nvt$LAMBDA

    echo "Constant volume equilibration complete."

    sleep 10

    #####################
    # NPT EQUILIBRATION #
    #####################
    echo "Starting constant pressure equilibration..."

    cd ../
    mkdir NPT
    cd NPT

    gmx grompp -f ../../MDP/npt_fep_$LAMBDA.mdp -c ../NVT/nvt$LAMBDA.gro -p ../../topol.top -t ../NVT/nvt$LAMBDA.cpt -o npt$LAMBDA.tpr -maxwarn 1

    gmx mdrun -v -ntomp 4 -deffnm npt$LAMBDA

    echo "Constant pressure equilibration complete."

    sleep 10

    #################
    # PRODUCTION MD #
    #################
    echo "Starting production MD simulation..."

    cd ../
    mkdir Production_MD
    cd Production_MD

    gmx grompp -f ../../MDP/md_fep_$LAMBDA.mdp -c ../NPT/npt$LAMBDA.gro -p ../../topol.top -t ../NPT/npt$LAMBDA.cpt -o md$LAMBDA.tpr -maxwarn 1

    gmx mdrun -v -ntomp 4 -deffnm md$LAMBDA

    echo "Production MD complete."

    # End
    echo "Ending. Job completed for lambda = $LAMBDA"

    cd ../../
done

exit;
