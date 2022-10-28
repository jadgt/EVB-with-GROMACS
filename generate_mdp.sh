mkdir MDP
perl write_mdp.pl em_fep.mdp
mv em_fep_* MDP/
perl write_mdp.pl nvt_fep.mdp
mv nvt_fep_* MDP/
perl write_mdp.pl npt_fep.mdp
mv npt_fep_* MDP/
perl write_mdp.pl md_fep.mdp
mv md_fep_* MDP/