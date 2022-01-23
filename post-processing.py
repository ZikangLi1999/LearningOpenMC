import openmc
import matplotlib.pyplot as plt
import numpy as np

# Get tally data from state point file
sp = openmc.StatePoint('statepoint.100.h5')
tally = sp.get_tally(scores=['flux'])
# print(tally)
# print("tally.sum = \n", tally.sum)
# print("tally.mean = \n", tally.mean)
# print("tally.std_dev = \n", tally.std_dev)
# print("tally.sum.shape = {}, tally.mean.shape = {}, tally.std_dev = {}".format(
#     tally.sum.shape, tally.mean.shape, tally.std_dev.shape))

# Seperate by score
flux = tally.get_slice(scores=['flux'])
fission = tally.get_slice(scores=['fission'])
flux.mean.shape = (100, 100)
fission.mean.shape = (100, 100)

# Plot Flux & Fission Reaction Rate
fig1 = plt.subplot(121)
fig1.imshow(flux.mean)
fig2 = plt.subplot(122)
fig2.imshow(fission.mean)
plt.title = "Flxu & Fission Reaction Rate"
plt.show()

# Hist Relative Error
flux.std_dev.shape = (100, 100)
relative_error = np.zeros_like(flux.std_dev)
nonzeros = flux.mean > 0
relative_error[nonzeros] = flux.std_dev[nonzeros] / flux.mean[nonzeros]
plt.hist(relative_error[nonzeros], bins=50)
plt.show()

# Source
source = sp.source
print("source.shape = {}".format(source.shape))
print("source.shape = ", format(source.shape))
spectrum = source['E']
print("source['E'] = \n", spectrum)

energy_bins = np.logspace(3, 7)
probabilities, bins_edges = np.histogram(spectrum, bins=energy_bins, density=True)
energy_steps = np.diff(energy_bins)
print(sum(probabilities * energy_steps), " == 1")
print("bins_edges.shape = ", format(bins_edges.shape))
plt.semilogx(energy_bins[:-1], probabilities * energy_steps, drawstyle='steps')
plt.title('Source Spectrum')
plt.xlabel('Energy / eV')
plt.ylabel('Probabilities')
plt.show()

plt.quiver(source['r']['x'], source['r']['y'], source['u']['x'], source['u']['y'], np.log(spectrum), cmap='hot')
plt.colorbar()
plt.title('Source Nuetron Distribution')
plt.xlim((-0.5, 0.5))
plt.ylim((-0.5, 0.5))
plt.show()
