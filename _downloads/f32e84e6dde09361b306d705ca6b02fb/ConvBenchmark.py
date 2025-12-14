# ssh cerbsim 'source ~/.bashrc; nsys profile --trace=cuda python -' < ConvBenchmark.py
# scp cerbsim:gpu.trace .
from ngsolve import *
from time import time, sleep



mesh = Mesh(unit_cube.GenerateMesh(maxh=0.05))
for k in range(0):
    mesh.Refine()


fes = VectorL2(mesh, order=1)
u,v = fes.TnT()
wind = CF((1,0,0))


with TaskManager():
    A = BilinearForm(Grad(v)*wind*u*dx).Assemble()

Amat = A.mat # .DeleteZeroElements(1e-10)

    
vx = Amat.CreateRowVector()
vy = Amat.CreateColVector()

vx.SetRandom()

print ("ndof =", fes.ndof, ", nze = ", Amat.nze)
runs = 10

ts = time()
for k in range(runs):
    vy.data = Amat * vx
print (Norm(vy))
te = time()

# print ("t op = ", (te-ts)/runs)
print ("GFlops =", Amat.nze*runs / (te-ts)*1e-9)





A2 = BilinearForm(Grad(v)*wind*u*dx, nonlinear_matrix_free_bdb=True).Assemble()
print (A2.mat.GetOperatorInfo())


ts = time()
for k in range(runs):
    vy.data = A2.mat * vx
print (Norm(vy))
te = time()

# print ("t op = ", (te-ts)/runs)
print ("GFlops =", Amat.nze*runs / (te-ts)*1e-9)


# ################### both ops on device ######################


import ngsolve.ngscuda
ngsolve.ngscuda.SetSyncKernels(False)

# Adev = Amat.CreateDeviceMatrix()
A2dev = A2.mat.CreateDeviceMatrix()
xdev = vx.CreateDeviceVector(copy=True)
ydev = vy.CreateDeviceVector(copy=False)

# ydev.data = Adev * xdev  # warmup
ts = time()
# for k in range(runs):
#    ydev.data = Adev * xdev
norm = Norm(ydev)    
te = time()

# print ("t op = ", (te-ts)/runs)
print ("GPU-sparse, GFlops =", Amat.nze*runs / (te-ts)*1e-9, ", norm=", norm)




ydev.data = A2dev * xdev  # warmup
with PajeTrace("gpu"):
    ts = time()
    for k in range(runs):
        ydev.data = A2dev * xdev
    norm = Norm(ydev)
    te = time()
print ("writing 'gpu.trace'")

# print ("t op = ", (te-ts)/runs)
print ("GPU-operator, GFlops =", Amat.nze*runs / (te-ts)*1e-9, ", norm=", norm)



# ################### Capture ########################

# print (A2dev.GetOperatorInfo())

graph = ngsolve.ngscuda.CudaGraph()

graph.BeginCapture()
ydev.data = A2dev * xdev
graph.EndCapture()
graph.Launch() # warmup
norm = Norm(ydev)

ydev[:] = 0
 
ts = time()
for k in range(runs):
    graph.Launch()
norm = Norm(ydev) 
te = time()
    
print ("GPU-graph, GFlops =", Amat.nze*runs / (te-ts)*1e-9, ", norm=", norm)


