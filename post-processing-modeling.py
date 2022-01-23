import openmc

# Materials
# 1.6% Fuel
uo2 = openmc.Material(name='1.6% Fuel', temperature=718.0)
uo2.add_nuclide('U235', 3.7503e-4)
uo2.add_nuclide('U238', 2.2625e-2)
uo2.add_nuclide('O16', 4.6007e-2)
uo2.set_density('g/cm3', 10.31341)
# Zircaloy
zircaloy = openmc.Material(name='zircaloy', temperature=718.0)
zircaloy.add_nuclide('Zr90', 7.2758e-3)
zircaloy.set_density('g/cm3', 6.55)
# Borated Water
water = openmc.Material(name='water', temperature=718.0)
water.add_nuclide('H1', 4.9457e-2)
water.add_nuclide('O16', 2.4732e-2)
water.add_nuclide('B10', 8.0042e-6)
water.set_density('g/cm3', 0.470582)
materials = openmc.Materials(materials=[uo2, zircaloy, water])
materials.export_to_xml()

# Geometry
fuel_outer_surface = openmc.ZCylinder(r=0.39218)
clad_outer_surface = openmc.ZCylinder(r=0.45720)
xmin = openmc.XPlane(-0.63, boundary_type='reflective')
xmax = openmc.XPlane(0.63, boundary_type='reflective')
ymin = openmc.YPlane(-0.63, boundary_type='reflective')
ymax = openmc.YPlane(0.63, boundary_type='reflective')
zmin = openmc.ZPlane(-0.63, boundary_type='reflective')
zmax = openmc.ZPlane(0.63, boundary_type='reflective')
cell_region = +zmin & -zmax & +ymin & -ymax & +xmin & -xmax

fuel = openmc.Cell(name='fuel', fill=uo2, region=-fuel_outer_surface)
clad = openmc.Cell(name='clad', fill=zircaloy, region=+fuel_outer_surface & -clad_outer_surface)
moderator = openmc.Cell(name='moderator', fill=water, region=+clad_outer_surface)

pin_cell_universe = openmc.Universe(cells=[fuel, clad, moderator])
root_cell = openmc.Cell(name='root', fill=pin_cell_universe, region=cell_region)
root_universe = openmc.Universe(name='root', cells=[root_cell])

geometry = openmc.Geometry(root=root_universe)
geometry.export_to_xml()

# Settings
setting = openmc.Settings()
setting.batches = 100
setting.inactive = 10
setting.particles = 5000

box_boundary = [-0.63, -0.63, -0.63, 0.63, 0.63, 0.63]
box = openmc.stats.Box(box_boundary[:3], box_boundary[3:])
uniform_distribution = openmc.stats.Box(box_boundary[:3], box_boundary[3:], only_fissionable=True)
source = openmc.Source(space=uniform_distribution)
setting.export_to_xml()

# Plot
plot = openmc.Plot.from_geometry(geometry)
plot.filename = 'post processing'
plot.pixels = [400, 400]
# plots = openmc.Plots(plots=[plot])
# plots.export_to_xml()
openmc.plot_geometry()

# Tallies
mesh = openmc.RegularMesh()
mesh.dimension = [100, 100]
mesh.lower_left = [-0.63, -0.63]
mesh.upper_right = [0.63, 0.63]
mesh_filter = openmc.MeshFilter(mesh)

tally = openmc.Tally(name='flux')
tally.filters = [mesh_filter]
tally.scores = ['flux', 'fission']

tallies = openmc.Tallies(tallies=[tally])
tallies.export_to_xml()

# Run
openmc.run()
