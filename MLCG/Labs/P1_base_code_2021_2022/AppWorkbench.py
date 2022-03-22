from PyRT_Common import *
import matplotlib.pyplot as plt

# ############################################################################################## #
# Given a list of hemispherical functions (function_list) and a set of sample positions over the #
#  hemisphere (sample_pos_), return the corresponding sample values. Each sample value results   #
#  from evaluating the product of all the functions in function_list for a particular sample     #
#  position.                                                                                     #
# ############################################################################################## #
def collect_samples(function_list, sample_pos_):
    sample_values = []
    for i in range(len(sample_pos_)):
        val = 1
        for j in range(len(function_list)):
            val *= function_list[j].eval(sample_pos_[i])
        sample_values.append(RGBColor(val, 0, 0))  # for convenience, we'll only use the red channel
    return sample_values


# ########################################################################################### #
# Given a set of sample values of an integrand, as well as their corresponding probabilities, #
# this function returns the classic Monte Carlo (cmc) estimate of the integral.               #
# ########################################################################################### #
def compute_estimate_cmc(sample_prob_, sample_values_):
    # TODO: PUT YOUR CODE HERE
    return 0



# ----------------------------- #
# ---- Main Script Section ---- #
# ----------------------------- #


# #################################################################### #
# STEP 0                                                               #
# Set-up the name of the used methods, and their marker (for plotting) #
# #################################################################### #
methods_label = [('MC', 'o')]
# methods_label = [('MC', 'o'), ('MC IS', 'v'), ('BMC', 'x'), ('BMC IS', '1')] # for later practices
n_methods = len(methods_label) # number of tested monte carlo methods

# ######################################################## #
#                   STEP 1                                 #
# Set up the function we wish to integrate                 #
# We will consider integrals of the form: L_i * brdf * cos #
# ######################################################## #
#l_i = ArchEnvMap()
l_i = Constant(1)
kd = 1
brdf = Constant(kd)
cosine_term = CosineLobe(1)
integrand = [l_i, brdf, cosine_term]  # l_i * brdf * cos

# ############################################ #
#                 STEP 2                       #
# Set-up the pdf used to sample the hemisphere #
# ############################################ #
uniform_pdf = UniformPDF()
#exponent = 1
#cosine_pdf = CosinePDF(exponent)


# ###################################################################### #
# Compute/set the ground truth value of the integral we want to estimate #
# NOTE: in practice, when computing an image, this value is unknown      #
# ###################################################################### #
ground_truth = cosine_term.get_integral()  # Assuming that L_i = 1 and BRDF = 1
print('Ground truth: ' + str(ground_truth))


# ################### #
#     STEP 3          #
# Experimental set-up #
# ################### #
ns_min = 20  # minimum number of samples (ns) used for the Monte Carlo estimate
ns_max = 101  # maximum number of samples (ns) used for the Monte Carlo estimate
ns_step = 20  # step for the number of samples
ns_vector = np.arange(start=ns_min, stop=ns_max, step=ns_step)  # the number of samples to use per estimate
n_estimates = 1  # the number of estimates to perform for each value in ns_vector
n_samples_count = len(ns_vector)

# Initialize a matrix of estimate error at zero
results = np.zeros((n_samples_count, n_methods))  # Matrix of average error


# ################################# #
#          MAIN LOOP                #
# ################################# #

# for each sample count considered
for k, ns in enumerate(ns_vector):

    print(f'Computing estimates using {ns} samples')

    # TODO: Estimate the value of the integral using CMC
    estimate_cmc = 0
    abs_error = abs(ground_truth - estimate_cmc)

    results[k, 0] = abs_error


# ################################################################################################# #
# Create a plot with the average error for each method, as a function of the number of used samples #
# ################################################################################################# #
for k in range(len(methods_label)):
    method = methods_label[k]
    plt.plot(ns_vector, results[:, k], label=method[0], marker=method[1])

plt.legend()
plt.show()
