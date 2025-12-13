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

export LD_LIBRARY_PATH="/cvmfs/software.eessi.io/versions/2025.06/software/linux/x86_64/amd/zen4/software/OpenBLAS/0.3.27-GCC-13.3.0/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="/cvmfs/software.asc.ac.at/versions/2025.06/software/linux/x86_64/amd/zen4/software/CUDA/12.9.0/lib:$LD_LIBRARY_PATH"

export PYTHONPATH="/home/js65943/install/lib/python3.14/site-packages:$PYTHONPATH"


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
import ngsolve
print ("have ngsolve")

import ngsolve.ngscuda
```


which you submit as
```
sbatch --partition=zen4_0768_h100x4 submit_slurm.sh
```



### remaining problem

the output gives
```
/home/js65943/ngs/bin/python
Sat Dec 13 15:07:26 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.95.05              Driver Version: 580.95.05      CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA H100                    On  |   00000000:C6:00.0 Off |                    0 |
| N/A   41C    P0             68W /  700W |       0MiB /  95830MiB |      0%      Default |
|                                         |                        |             Disabled |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
Job started at Sat Dec 13 15:07:26 CET 2025
Running on host n3015-020
cudaGetDeviceCount() failed: CUDA driver version is insufficient for CUDA runtime version
CUDA Device Query...
Initializing cublas and cusparse.
 ** On entry to cusparseCreate(): CUDA context cannot be initialized

have ngsolve
```