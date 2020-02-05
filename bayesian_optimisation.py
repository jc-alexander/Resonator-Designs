from emukit.test_functions import branin_function
from emukit.core import ParameterSpace, ContinuousParameter
from emukit.experimental_design.model_free.random_design import RandomDesign
from GPy.models import GPRegression
from emukit.model_wrappers import GPyModelWrapper
from emukit.model_wrappers.gpy_quadrature_wrappers import BaseGaussianProcessGPy, RBFGPy
import numpy as np
import GPy
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import json

# Decision loops
from emukit.experimental_design.model_based import ExperimentalDesignLoop
from emukit.bayesian_optimization.loops import BayesianOptimizationLoop
from emukit.quadrature.loop import VanillaBayesianQuadratureLoop

# Acquisition functions
from emukit.bayesian_optimization.acquisitions import ExpectedImprovement
from emukit.experimental_design.model_based.acquisitions import ModelVariance
from emukit.quadrature.acquisitions import IntegralVarianceReduction

# Acquistions optimizers
from emukit.core.optimization import GradientAcquisitionOptimizer

# Stopping conditions
from emukit.core.loop import FixedIterationsStoppingCondition

# Point calculator
from emukit.core.loop import SequentialPointCalculator

# Bayesian quadrature kernel and model
from emukit.quadrature.kernels import QuadratureRBF
from emukit.quadrature.methods import VanillaBayesianQuadrature

# COMSOL simulation
from cap_wrapper import run_sim


# Define the input parameters for our function

#w = 1000
#l_arm = 450
#w_cap = 20
#gap = 30
#n = 5
#r = 25
#w_ind = 5
#o_gap = 20
y0 = 0
x0 = 0
h = 0.05

# Parameter space
# parameter_space = ParameterSpace([ContinuousParameter('l_ind', 10e-06, 50e-06), ContinuousParameter('gap_ind', 4e-07, 2e-06)])
parameter_space = ParameterSpace([\
    ContinuousParameter('w', 500, 2000), \
    ContinuousParameter('l_arm', 500, 1500), \
    ContinuousParameter('w_cap', 5, 50),\
    ContinuousParameter('gap', 5, 50), \
    # ContinuousParameter('t', 25e-09, 75e-09),
    ContinuousParameter('n', 2, 20),\
    ContinuousParameter('r', 10, 100), \
    ContinuousParameter('w_ind', 1, 50), \
    ContinuousParameter('o_gap', 1, 50), \
    # ContinuousParameter('l_cap', 150e-06, 750e-06)
    ])
"""
ContinuousParameter('gap_cap', 1e-06, 5e-06), \
ContinuousParameter('w_cap', 1e-06, 5e-06),\
ContinuousParameter('l_cap', 1e-05, 5e-05), \
ContinuousParameter('l', 7e-05, 1.1e-04),
ContinuousParameter('w', 3e-06, 7e-05),\
ContinuousParameter('gap_ind', 1e-06, 5e-06),\
"""
# Function to optimize
def q(X):
    w = X[:,0]
    l_arm = X[:, 1]
    w_cap = X[:, 2]
    gap = X[:,3]
    # t = X[:,3]
    n = X[:,4]
    r = X[:,5]
    w_ind = X[:,6]
    o_gap = X[:,7]
    # l_cap = X[:,5]
    out = np.zeros((len(l_arm),1))
    for g in range(len(l_arm)):
        out[g,0] = run_sim(w[g],l_arm[g],w_cap[g],gap[g],int(n[g]),r[g],w_ind[g],o_gap[g],y0,x0,h)
    return out

#f, space = branin_function()


num_data_points = 10
design = RandomDesign(parameter_space)
X = design.get_samples(num_data_points)
Y = q(X)
"""
num_data_points = 1000
design = RandomDesign(param_space)
X = design.get_samples(num_data_points)
Y = f(X)
plt.plot(X,Y)
plt.show()
"""
model_gpy = GPRegression(X,Y)
model_gpy.optimize()
model_emukit = GPyModelWrapper(model_gpy)
"""
model_emukit.model.plot()
model_emukit.model
plt.show()
"""
exp_imprv = ExpectedImprovement(model = model_emukit)
optimizer = GradientAcquisitionOptimizer(space = parameter_space)
point_calc = SequentialPointCalculator(exp_imprv,optimizer)
coords = []
min = []

bayesopt_loop = BayesianOptimizationLoop(model = model_emukit,
                                         space = parameter_space,
                                         acquisition=exp_imprv,
                                         batch_size=1)

stopping_condition = FixedIterationsStoppingCondition(i_max = 100)
bayesopt_loop.run_loop(q, stopping_condition)


coord_results  = bayesopt_loop.get_results().minimum_location
min_value = bayesopt_loop.get_results().minimum_value
step_results = bayesopt_loop.get_results().best_found_value_per_iteration
print(coord_results)
print(min_value)

"""
results = [coord_results,min_value]

results_file = open('results.txt','w')
results_file.write(str(results))
results_file.close()
"""
"""
data = model_emukit.model.to_dict()
with open('model_data.txt','w') as outfile:
    json.dump(data,outfile)

model_emukit.model.plot(levels=500,visible_dims=[1,2])
ax = plt.gca()
mappable = ax.collections[0]
plt.colorbar(mappable)
plt.savefig('model.png')
plt.show()

# Shelf
import shelve

filename='/tmp/shelve.out'
my_shelf = shelve.open(filename,'n') # 'n' for new
my_shelf['model_emukit'] = globals()['model_emukit']
# my_shelf['bayesopt_loop']= globals()['bayesopt_loop']
my_shelf.close()


model_emukit.model.plot()
model_emukit.model
plt.show()
print(point_calc)
a = bayesopt_loop.loop_state.X
print(f(a))
plt.scatter(a[:,0],f(a))
plt.show()
print(model_emukit.model)
"""
