import pywincalc

# Path to the optical standard file.  All other files referenced by the standard file must be in the same directory
# Note:  While all optical standards packaged with WINDOW should work with optical calculations care should be
# taken to use NFRC standards if thermal results are desired.  This is because for thermal calculations currently
# only ISO 15099 is supported.  So while it is possible to use EN optical standards and create thermal results
# those results will not be based on EN 673
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

width = 1.0  # width of the glazing system in meters
height = 1.0  # height of the glazing system in meters

# Load solid layer measured values.  Solid layer information can come from either igsdb.lbl.gov or files generate
# by the Optics program.  Since igsdb.lbl.gov requires registration some optics files are provided for example
# purposes
clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3]
gaps = []  # single layer does not have any gaps

# Glazing_System environments defaults to the NFRC U environments
glazing_system_single_layer_u_environment = pywincalc.Glazing_System(solid_layers, gaps, optical_standard, width,
                                                                     height)
u_value = glazing_system_single_layer_u_environment.u()  # calculate U-value according to ISO15099
print("Single Layer U-value: {u}".format(u=u_value))

# To calculate SHGC use the NFRC SHGC environments for the glazing system instead
glazing_system_single_layer_shgc_environment = pywincalc.Glazing_System(solid_layers, gaps, optical_standard, width,
                                                                        height,
                                                                        pywincalc.nfrc_shgc_environments())
shgc_result = glazing_system_single_layer_shgc_environment.shgc()  # calculate SHGC according to ISO15099
print("Single Layer SHGC: {shgc}".format(shgc=shgc_result))

# It is possible to calculate U and SHGC for any environmental conditions.
# E.G. The SHGC for the NFRC U environmental conditions is
u_environment_shgc = glazing_system_single_layer_u_environment.shgc()
print("SHGC for the NFRC U-value environmental conditions: {shgc}".format(shgc=u_environment_shgc))
# And the u-value for the SHGC environment is
shgc_environment_u = glazing_system_single_layer_shgc_environment.u()
print("U for the NFRC SHGC environmental conditions: {u}".format(u=shgc_environment_u))

# Other thermal results available:

# Layer results can be calculated for two cases for each environment.  When U system is passed as a parameter
# the layer temperatures will be calculated for the given environments without taking solar radiation into account.
# When SHGC system is passed as a parameter solar ration is taken into account
shgc_layer_temperatures_with_solar_radiation = glazing_system_single_layer_shgc_environment.layer_temperatures(
    pywincalc.Tarcog_System_Type.SHGC)
shgc_layer_temperatures_without_solar_radiation = glazing_system_single_layer_shgc_environment.layer_temperatures(
    pywincalc.Tarcog_System_Type.U)

# Optical results are calculated based on methods defined by the optical standard loaded above.
# Get all solar results by
solar_results = glazing_system_single_layer_u_environment.optical_method_results(pywincalc.Optical_Method_Type.SOLAR)

# Optical results have two parts, results that apply to the entire system and results for each layer.
# System results and results for each layer are then divided by side (front, back).
# then by transmission type (transmittance, reflectance) and then by ____________ (direct_direct, direct_diffuse,
# direct_hemispherical, and diffuse_diffuse).  direct_diffuse does not include the direct_direct component while
# direct_hemispherical does.  In other words direct_direct + direct_diffuse = direct_hemispherical
#
# This prints out all available optical results for the solar method.  The same results are available
# for any other method in the optical standards file except for the color methods (method names starting with COLOR_)
system_solar_results = solar_results.system_results
print("Direct-direct front solar transmittance: {v}".format(
    v=system_solar_results.front.transmittance.direct_direct))
print("Direct-diffuse front solar transmittance: {v}".format(
    v=system_solar_results.front.transmittance.direct_direct))
print("Direct-hemispherical front solar transmittance: {v}".format(
    v=system_solar_results.front.transmittance.direct_hemispherical))
print("Diffuse-diffuse front solar transmittance: {v}".format(
    v=system_solar_results.front.transmittance.diffuse_diffuse))
print("Direct-direct front solar reflectance: {v}".format(
    v=system_solar_results.front.reflectance.direct_direct))
print("Direct-diffuse front solar reflectance: {v}".format(
    v=system_solar_results.front.reflectance.direct_direct))
print("Direct-hemispherical front solar reflectance: {v}".format(
    v=system_solar_results.front.reflectance.direct_hemispherical))
print("Diffuse-diffuse front solar reflectance: {v}".format(
    v=system_solar_results.front.reflectance.diffuse_diffuse))
print("Direct-direct back solar transmittance: {v}".format(
    v=system_solar_results.back.transmittance.direct_direct))
print("Direct-diffuse back solar transmittance: {v}".format(
    v=system_solar_results.back.transmittance.direct_direct))
print("Direct-hemispherical back solar transmittance: {v}".format(
    v=system_solar_results.back.transmittance.direct_hemispherical))
print("Diffuse-diffuse back solar transmittance: {v}".format(
    v=system_solar_results.back.transmittance.diffuse_diffuse))
print("Direct-direct back solar reflectance: {v}".format(
    v=system_solar_results.back.reflectance.direct_direct))
print("Direct-diffuse back solar reflectance: {v}".format(
    v=system_solar_results.back.reflectance.direct_direct))
print("Direct-hemispherical back solar reflectance: {v}".format(
    v=system_solar_results.back.reflectance.direct_hemispherical))
print("Diffuse-diffuse back solar reflectance: {v}".format(
    v=system_solar_results.back.reflectance.diffuse_diffuse))

# Currently only absorptance results are provided for each layer.  Direct and diffuse absportances are
# provided for each side of each layer.
solar_results_per_layer = solar_results.layer_results
print("Layer 1 front direct solar absorptance: {v}".format(v=solar_results_per_layer[0].front.absorptance.direct))
print("Layer 1 front diffuse solar absorptance: {v}".format(v=solar_results_per_layer[0].front.absorptance.diffuse))
print("Layer 1 back direct solar absorptance: {v}".format(v=solar_results_per_layer[0].back.absorptance.direct))
print("Layer 1 back diffuse solar absorptance: {v}".format(v=solar_results_per_layer[0].back.absorptance.diffuse))

# Similarly for visible results calculate using the Photopic method
visible_results = glazing_system_single_layer_u_environment.optical_method_results(
    pywincalc.Optical_Method_Type.PHOTOPIC)
print("Direct-direct front visible transmittance: {v}".format(
    v=visible_results.system_results.front.transmittance.direct_direct))
print("Direct-hemispheric back visible reflectance: {v}".format(
    v=visible_results.system_results.back.reflectance.direct_hemispherical))
print("Layer 1 front diffuse visible absorptance: {v}".format(
    v=visible_results.layer_results[0].front.absorptance.diffuse))
# etc...

# If the optical standard defines color methods those have a separate results set and function call
color_results = glazing_system_single_layer_u_environment.color()

# Currently color results only have system results.  Individual layer results are not yet supported.
# Color results follow the same layout as the other optical system results except each value is offered in
# the Trichromatic, Lab, and RGB color spaces.
direct_direct_front_transmittace_rgb_color = color_results.system_results.front.transmittance.direct_direct.rgb
print("Direct-direct front color transmittance in RGB: ({r}, {g}, {b})".format(
    r=direct_direct_front_transmittace_rgb_color.R, g=direct_direct_front_transmittace_rgb_color.G,
    b=direct_direct_front_transmittace_rgb_color.B))
direct_hemispherical_back_reflectance_lab_color = color_results.system_results.back.reflectance.direct_hemispherical.lab
print("Direct-hemispheric back color reflectance in Lab: ({l}, {a}, {b})".format(
    l=direct_hemispherical_back_reflectance_lab_color.L, a=direct_hemispherical_back_reflectance_lab_color.a,
    b=direct_hemispherical_back_reflectance_lab_color.b))
diffuse_diffuse_front_reflectance_trichromatic_color = color_results.system_results.front.reflectance.diffuse_diffuse.trichromatic
print("Diffuse-diffuse front color reflectance in trichromatic: ({x}, {y}, {z})".format(
    x=diffuse_diffuse_front_reflectance_trichromatic_color.X, y=diffuse_diffuse_front_reflectance_trichromatic_color.Y,
    z=diffuse_diffuse_front_reflectance_trichromatic_color.Z))
# etc...


# By default results are calculated at the normal angle of incidence but are avaialble for any given theta and phi
theta = 15
phi = 270

# Calculate SHGC at theta and phi
shgc_value = glazing_system_single_layer_shgc_environment.shgc(theta, phi)
print("SHGC at theta = {t} phi = {p}: {v}".format(t=theta, p=phi, v=shgc_value))

# Calculate solar optical results at theta and phi
solar_results = glazing_system_single_layer_u_environment.optical_method_results(pywincalc.Optical_Method_Type.SOLAR,
                                                                                 theta, phi)
direct_direct_front_transmittance = solar_results.system_results.front.transmittance.direct_direct
print("Direct-direct front solar transmittance at theta = {t} phi = {p}: {v}".format(t=theta, p=phi,
                                                                                     v=direct_direct_front_transmittance))
