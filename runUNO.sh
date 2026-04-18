#!/bin/bash
#SBATCH --job-name=vesiculaDOS_dppc
#SBATCH --output=v2_resultado_simulacion.log
#SBATCH --error=errores.log
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=12            
#SBATCH --gres=gpu:1                  
#SBATCH --time=24:00:00               
#SBATCH --mail-type=END,FAIL         
#SBATCH --mail-user=alejandro.eadr06@gmail.com

# Configuración de hilos
export OMP_NUM_THREADS=12

# Comando de ejecución
mpirun -np 1 /apps/bin/lammps.cuda -in inTRES.lmp -sf gpu -pk gpu 1
