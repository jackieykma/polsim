'''
A script that piggy-backs on QU-fitting module of RM-Tools

Uses the defined model dictionaries to generate simulated data
'''



import RMtools_1D.do_QUfit_1D_mnest as qufit
import numpy as np



def iqu_sim(model_sel, pDict, freq_array, iDict, noise, seed):
   '''
   Main function of this script (see belew iqu_sim_test() for an example use case)
   
   model_sel: Selected model (e.g. 1, 5, 11... In integer)
   pDict: Dictionary of parameter defining the polarisation model
   freq_array: Array of frequency channels in Hz
   iDict: Define the Stokes I spectrum
   noise: Injected noise in Jy. Same noise injected for all Stokes and all frequencies
   seed: Randomisation seed for numpy RNG
   '''
   c = 299792458. ## Speed of light in m/s
   np.random.seed(seed) ## Choose seed for noise randomisation
   l2_array = (c/freq_array)**2 ## Convert to lambda2
   
   mod = qufit.load_model(model_sel) ## Load in the selected model
   qu_array = mod.model(pDict, l2_array) ## Generate Stokes qu spectra
   
   ## Generate Stokes IQU spectra
   i_array = iDict["flux"] * (freq_array/iDict["reffreq"])**iDict["alpha"] ## Noiseless, in Jy
   q_array = i_array * qu_array.real ## Noiseless, in Jy
   u_array = i_array * qu_array.imag ## Noiseless, in Jy
   
   ## Inject noise
   i_array = i_array + np.random.randn(len(freq_array))*noise
   q_array = q_array + np.random.randn(len(freq_array))*noise
   u_array = u_array + np.random.randn(len(freq_array))*noise
   
   return i_array, q_array, u_array



def iqu_sim_test():
   ## Test iqu_sim() with a default set of parameters
   ## Also can be seen as how one can set up and run iqu_sim()
   
   ## Array of frequency channels in Hz
   freq_array = np.arange(800.e6, 1089.e6, 1.e6)
   
   ## Selected model (e.g. '1', '2', '5', '11'... In integer)
   model_sel = 1
   
   ## Dictionary of parameter defining the polarisation model
   pDict = {
   "fracPol": 0.3,
   "psi0_deg": 25.,
   "RM_radm2": 170.,
   }
   
   ## Define the Stokes I spectrum
   iDict = {
   "reffreq": 944.e6, ## In Hz
   "flux": 500.e-6, ## In Jy
   "alpha": -0.7, ## S = S0 (nu/nu0)**alpha
   }
   
   ## Injected noise. Same noise injected for all Stokes and all frequencies. In unit of Jy
   noise = 20.e-6
   
   ## Choose randomisation seed?
   seed = 9999
   
   ## Generate the simulated data, and plot
   i_array, q_array, u_array = iqu_sim(model_sel, pDict, freq_array, iDict, noise, seed)
   
   import matplotlib.pyplot as plt
   plt.errorbar(freq_array, i_array, yerr=np.full(len(i_array), noise), fmt='ko', markersize=2, label='Stokes I')
   plt.errorbar(freq_array, q_array, yerr=np.full(len(q_array), noise), fmt='bo', markersize=2, label='Stokes Q')
   plt.errorbar(freq_array, u_array, yerr=np.full(len(u_array), noise), fmt='ro', markersize=2, label='Stokes U')
   
   ## Tidy things up
   plt.axhline(y=0., color='grey', ls=':')
   plt.xlabel('Frequency (Hz)')
   plt.ylabel('Flux Density (Jy)')
   plt.legend(loc='best')
   plt.tight_layout()
   plt.show()
   






