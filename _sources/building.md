# building NGSolve with CUDA




```
git clone --recurse-submodules https://github.com/NGSolve/ngsolve.git src/ngsolve
mkdir -p build/ngsolve
cd build/ngsolve
cmake ../../src/ngsolve -DUSE_SUPERBUILD=ON -DUSE_CCACHE=ON -DCMAKE_INSTALL_PREFIX=~/install -DUSE_CUDA=ON
```




## build on the musica cluster:

* now working exactly with gcc 13 and Python 3.14
* importing ngsolve.ngscuda still not working

```
module purge --force
module load EESSI/2025.06 ASC/2025.06
module load GCC/13 OpenBLAS/0.3.27-GCC-13.3.0  CUDA

python3.14 -m venv ngs
source ngs/bin/activate
pip install --upgrade netgen-occt-devel cmake numpy pybind11 pip


git clone --recurse-submodules https://github.com/NGSolve/ngsolve.git src/ngsolve

# rm -rf build/ngsolve
mkdir -p build/ngsolve
cd build/ngsolve

cmake ~/src/ngsolve \
  -DUSE_SUPERBUILD=ON \
  -DUSE_CCACHE=ON \
  -DCMAKE_INSTALL_PREFIX=~/install \
  -DUSE_CUDA=ON \
  -DUSE_GUI=OFF \
  -DCMAKE_CUDA_ARCHITECTURES="90" \
  -DUSE_UMFPACK=OFF \
  -DBUILD_STUB_FILES=OFF

make -j 8 install
```


### the slurm script `submit_slurm.sh`:
```
#!/bin/bash
#SBATCH --job-name "myjob"
#SBATCH --gres=gpu:1
#SBATCH -p zen4_0768_h100x4
#SBATCH --qos zen4_0768_h100x4
#SBATCH --threads-per-core=1
#SBATCH --time=01:00:00

# Optional: load modules (adjust to your environment)

module purge --force
module load EESSI/2025.06 ASC/2025.06
module load GCC/13 OpenBLAS/0.3.27-GCC-13.3.0  CUDA

source /home/js65943/ngs/bin/activate

export LD_LIBRARY_PATH="/cvmfs/software.eessi.io/versions/2025.06/software/linux
/x86_64/amd/zen4/software/OpenBLAS/0.3.27-GCC-13.3.0/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="/cvmfs/software.asc.ac.at/versions/2025.06/software/linu
x/x86_64/amd/zen4/software/CUDA/12.9.0/lib:$LD_LIBRARY_PATH"


which python
nvidia-smi

# Run from the directory you submitted from
# cd "${SLURM_SUBMIT_DIR:-$PWD}"
cd ~/submit

# Example commands: replace with your job's commands
echo "Job started at $(date)"
echo "Running on host $(hostname)"
python test.py 
echo "Job finished at $(date)"
```

and a python file `test.py` in the submit directory:
```
import sys
sys.path.append('/home/js65943/install/lib/python3.14/site-packages')

import ngsolve
print ("have ngsolve")

import ngsolve.ngscuda
```


which you submit as
```
sbatch --partition=zen4_0768_h100x4 submit_slurm.sh
```