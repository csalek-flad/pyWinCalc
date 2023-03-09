import pywincalc

# Path to the optical standard file.  All other files referenced by the standard file must be in the same directory
# Note:  While all optical standards packaged with WINDOW should work with optical calculations care should be
# taken to use NFRC standards if NFRC thermal results are desired.  This is because for thermal calculations currently
# only ISO 15099 is supported.  While it is possible to use EN optical standards and create thermal results
# those results will not be based on EN 673
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

width = 1.0  # width of the glazing system in meters
height = 1.0  # height of the glazing system in meters

# Define the gap between the shade and the glazing.  In this case use a default air gap
# that is 12.7mm thick.  For more on creating gases and gaps see the gases.py example
gap_1 = pywincalc.Layers.gap(thickness=.0127)

# Load solid layer measured values.  Solid layer information can come from either igsdb.lbl.gov or files generate
# by the Optics program.  Since igsdb.lbl.gov requires registration some optics files are provided for example
# purposes
clear_3_path = "products/CLEAR_3.DAT"
clear_3 = pywincalc.parse_optics_file(clear_3_path)

clear_6_path = "products/CLEAR_6.DAT"
clear_6 = pywincalc.parse_optics_file(clear_3_path)

solid_layers = [clear_3, clear_6]
gaps = [gap_1]

# Using a small basis here to make printing out the matrix results managable
# Small should probably not be used for actual simulation
bsdf_hemisphere = pywincalc.BSDFHemisphere.create(pywincalc.BSDFBasisType.SMALL)

# By default a glazing system is created using the environmental conditions defined by
# the NFRC U-value calculations
glazing_system_u_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                       solid_layers=solid_layers,
                                                       gap_layers=gaps,
                                                       width_meters=width,
                                                       height_meters=height,
                                                       bsdf_hemisphere=bsdf_hemisphere)

# To calculate SHGC use the NFRC SHGC environments for the glazing system instead.
# These are provided by calling pywincalc.nfrc_shgc_environments().
# U-value conditions are also available with pywincalc.nfrc_u_environments().
glazing_system_shgc_environment = pywincalc.GlazingSystem(optical_standard=optical_standard,
                                                          solid_layers=solid_layers,
                                                          gap_layers=gaps,
                                                          width_meters=width,
                                                          height_meters=height,
                                                          environment=pywincalc.nfrc_shgc_environments(),
                                                          bsdf_hemisphere=bsdf_hemisphere)

# In general there are two types of results: optical and thermal.  Here optical and thermal
# refer to the calculation methods and not the wavelengths.  Environmental conditions can only affect thermal results.
#
# All calculations default to calculating results from radiation at a normal angle of incidence but
# support off-normal calculations by allowing users to pass theta and phi values.
#
# So any result can be calculated for any incidence angle this way.
# e.g. to calculate SHGC results at incidence angle theta = 15 and phi = 25 call
# glazing_system.shgc(theta=15, phi=25)
#
# ------------------------------------Optical Results--------------------------------------------
#
# Since optical results do not depend on environmental conditions all examples below will use the
# same glazing system for uniformity.  The choice to alias glazing_system to glazing_system_u_environment
# is arbitrary and just to save on space
#
glazing_system = glazing_system_u_environment

# The types of optical results depend on which methods are defined in the optical standards file.
# Below are examples of every optical results defined in the W5_NFRC_2003.std file

# ------------------All mathods except Thermal IR and Colors------------------
#
# Methods are defined by name in the standards file.  To calculate results for
# all methods except Thermal IR and Colors (see below) pass the method name to the 
# GlazingSystem.optical_method_results function.
#
# The below enumerates the results available from the W5_NFRC_2003.std file.
# Since the standards files are free to name the methods as they like if you are using
# some other standard some knowledge about what the various methods represent may be required.

# -------------------------------------Solar-------------------------------------
solar_results = glazing_system.optical_method_results("SOLAR")

print("System solar front transmittance direct-direct: {v}".format(
    v=solar_results.system_results.front.transmittance.direct_direct))
print("System solar front transmittance direct-diffuse: {v}".format(
    v=solar_results.system_results.front.transmittance.direct_diffuse))
print("System solar front transmittance direct-hemispherical: {v}".format(
    v=solar_results.system_results.front.transmittance.direct_hemispherical))
print("System solar front transmittance diffuse-diffuse: {v}".format(
    v=solar_results.system_results.front.transmittance.diffuse_diffuse))
print(
    "System solar front transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=solar_results.system_results.front.transmittance.matrix))

print("System solar front reflectance direct-direct: {v}".format(
    v=solar_results.system_results.front.reflectance.direct_direct))
print("System solar front reflectance direct-diffuse: {v}".format(
    v=solar_results.system_results.front.reflectance.direct_diffuse))
print("System solar front reflectance direct-hemispherical: {v}".format(
    v=solar_results.system_results.front.reflectance.direct_hemispherical))
print("System solar front reflectance diffuse-diffuse: {v}".format(
    v=solar_results.system_results.front.reflectance.diffuse_diffuse))
print(
    "System solar front reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=solar_results.system_results.front.reflectance.matrix))

print("System solar back transmittance direct-direct: {v}".format(
    v=solar_results.system_results.back.transmittance.direct_direct))
print("System solar back transmittance direct-diffuse: {v}".format(
    v=solar_results.system_results.back.transmittance.direct_diffuse))
print("System solar back transmittance direct-hemispherical: {v}".format(
    v=solar_results.system_results.back.transmittance.direct_hemispherical))
print("System solar back transmittance diffuse-diffuse: {v}".format(
    v=solar_results.system_results.back.transmittance.diffuse_diffuse))
print(
    "System solar back transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=solar_results.system_results.back.transmittance.matrix))

print("System solar back reflectance direct-direct: {v}".format(
    v=solar_results.system_results.back.reflectance.direct_direct))
print("System solar back reflectance direct-diffuse: {v}".format(
    v=solar_results.system_results.back.reflectance.direct_diffuse))
print("System solar back reflectance direct-hemispherical: {v}".format(
    v=solar_results.system_results.back.reflectance.direct_hemispherical))
print("System solar back reflectance diffuse-diffuse: {v}".format(
    v=solar_results.system_results.back.reflectance.diffuse_diffuse))
print("System solar back reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
    v=solar_results.system_results.back.reflectance.matrix))

for i in range(len(solid_layers)):
    print("Layer {idx} solar front total direct absorptance: {v}".format(idx=i + 1,
                                                                         v=solar_results.layer_results[
                                                                             i].front.absorptance.total_direct))
    print("Layer {idx} solar front total diffuse absorptance: {v}".format(idx=i + 1,
                                                                          v=solar_results.layer_results[
                                                                              i].front.absorptance.total_diffuse))
    print("Layer {idx} solar front heat direct absorptance: {v}".format(idx=i + 1,
                                                                        v=solar_results.layer_results[
                                                                            i].front.absorptance.heat_direct))
    print("Layer {idx} solar front heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                         v=solar_results.layer_results[
                                                                             i].front.absorptance.heat_diffuse))
    print("Layer {idx} solar front electricity direct absorptance: {v}".format(idx=i + 1,
                                                                               v=solar_results.layer_results[
                                                                                   i].front.absorptance.electricity_direct))
    print("Layer {idx} solar front electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                                v=solar_results.layer_results[
                                                                                    i].front.absorptance.electricity_diffuse))
    print(
        "Layer {idx} solar back total direct absorptance: {v}".format(idx=i + 1,
                                                                      v=solar_results.layer_results[
                                                                          i].back.absorptance.total_direct))
    print("Layer {idx} solar back total diffuse absorptance: {v}".format(idx=i + 1,
                                                                         v=solar_results.layer_results[
                                                                             i].back.absorptance.total_diffuse))
    print("Layer {idx} solar back heat direct absorptance: {v}".format(idx=i + 1,
                                                                       v=solar_results.layer_results[
                                                                           i].back.absorptance.heat_direct))
    print("Layer {idx} solar back heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                        v=solar_results.layer_results[
                                                                            i].back.absorptance.heat_diffuse))
    print("Layer {idx} solar back electricity direct absorptance: {v}".format(idx=i + 1,
                                                                              v=solar_results.layer_results[
                                                                                  i].back.absorptance.electricity_direct))
    print("Layer {idx} solar back electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                               v=solar_results.layer_results[
                                                                                   i].back.absorptance.electricity_diffuse))

# ---------------------------------Photopic (aka Visible)-----------------------
photopic_results = glazing_system.optical_method_results("PHOTOPIC")

print("System photopic front transmittance direct-direct: {v}".format(
    v=photopic_results.system_results.front.transmittance.direct_direct))
print("System photopic front transmittance direct-diffuse: {v}".format(
    v=photopic_results.system_results.front.transmittance.direct_diffuse))
print("System photopic front transmittance direct-hemispherical: {v}".format(
    v=photopic_results.system_results.front.transmittance.direct_hemispherical))
print("System photopic front transmittance diffuse-diffuse: {v}".format(
    v=photopic_results.system_results.front.transmittance.diffuse_diffuse))
print(
    "System photopic front transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=photopic_results.system_results.front.transmittance.matrix))

print("System photopic front reflectance direct-direct: {v}".format(
    v=photopic_results.system_results.front.reflectance.direct_direct))
print("System photopic front reflectance direct-diffuse: {v}".format(
    v=photopic_results.system_results.front.reflectance.direct_diffuse))
print("System photopic front reflectance direct-hemispherical: {v}".format(
    v=photopic_results.system_results.front.reflectance.direct_hemispherical))
print("System photopic front reflectance diffuse-diffuse: {v}".format(
    v=photopic_results.system_results.front.reflectance.diffuse_diffuse))
print(
    "System photopic front reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=photopic_results.system_results.front.reflectance.matrix))

print("System photopic back transmittance direct-direct: {v}".format(
    v=photopic_results.system_results.back.transmittance.direct_direct))
print("System photopic back transmittance direct-diffuse: {v}".format(
    v=photopic_results.system_results.back.transmittance.direct_diffuse))
print("System photopic back transmittance direct-hemispherical: {v}".format(
    v=photopic_results.system_results.back.transmittance.direct_hemispherical))
print("System photopic back transmittance diffuse-diffuse: {v}".format(
    v=photopic_results.system_results.back.transmittance.diffuse_diffuse))
print(
    "System photopic back transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=photopic_results.system_results.back.transmittance.matrix))

print("System photopic back reflectance direct-direct: {v}".format(
    v=photopic_results.system_results.back.reflectance.direct_direct))
print("System photopic back reflectance direct-diffuse: {v}".format(
    v=photopic_results.system_results.back.reflectance.direct_diffuse))
print("System photopic back reflectance direct-hemispherical: {v}".format(
    v=photopic_results.system_results.back.reflectance.direct_hemispherical))
print("System photopic back reflectance diffuse-diffuse: {v}".format(
    v=photopic_results.system_results.back.reflectance.diffuse_diffuse))
print(
    "System photopic back reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=photopic_results.system_results.back.reflectance.matrix))

for i in range(len(solid_layers)):
    print("Layer {idx} photopic front total direct absorptance: {v}".format(idx=i + 1,
                                                                            v=photopic_results.layer_results[
                                                                                i].front.absorptance.total_direct))
    print("Layer {idx} photopic front total diffuse absorptance: {v}".format(idx=i + 1,
                                                                             v=photopic_results.layer_results[
                                                                                 i].front.absorptance.total_diffuse))
    print("Layer {idx} photopic front heat direct absorptance: {v}".format(idx=i + 1,
                                                                           v=photopic_results.layer_results[
                                                                               i].front.absorptance.heat_direct))
    print("Layer {idx} photopic front heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                            v=photopic_results.layer_results[
                                                                                i].front.absorptance.heat_diffuse))
    print("Layer {idx} photopic front electricity direct absorptance: {v}".format(idx=i + 1,
                                                                                  v=photopic_results.layer_results[
                                                                                      i].front.absorptance.electricity_direct))
    print("Layer {idx} photopic front electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                                   v=photopic_results.layer_results[
                                                                                       i].front.absorptance.electricity_diffuse))
    print(
        "Layer {idx} photopic back total direct absorptance: {v}".format(idx=i + 1,
                                                                         v=photopic_results.layer_results[
                                                                             i].back.absorptance.total_direct))
    print("Layer {idx} photopic back total diffuse absorptance: {v}".format(idx=i + 1,
                                                                            v=photopic_results.layer_results[
                                                                                i].back.absorptance.total_diffuse))
    print("Layer {idx} photopic back heat direct absorptance: {v}".format(idx=i + 1,
                                                                          v=photopic_results.layer_results[
                                                                              i].back.absorptance.heat_direct))
    print("Layer {idx} photopic back heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                           v=photopic_results.layer_results[
                                                                               i].back.absorptance.heat_diffuse))
    print("Layer {idx} photopic back electricity direct absorptance: {v}".format(idx=i + 1,
                                                                                 v=photopic_results.layer_results[
                                                                                     i].back.absorptance.electricity_direct))
    print("Layer {idx} photopic back electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                                  v=photopic_results.layer_results[
                                                                                      i].back.absorptance.electricity_diffuse))

# -------------------------------SPF-------------------------
# Unlike the other methods the layers in the glazing system do not contain
# measured values for that cover the range defined by the SPF method in the standards file
# pywincalc will throw an exception in such circumstances

try:
    spf_results = glazing_system.optical_method_results("SPF")
except Exception as e:
    print("Error trying to calculate results for SPF method: {e}".format(e=e))

# ---------------------------------TUV-----------------------
tuv_results = glazing_system.optical_method_results("TUV")

print("System TUV front transmittance direct-direct: {v}".format(
    v=tuv_results.system_results.front.transmittance.direct_direct))
print("System TUV front transmittance direct-diffuse: {v}".format(
    v=tuv_results.system_results.front.transmittance.direct_diffuse))
print("System TUV front transmittance direct-hemispherical: {v}".format(
    v=tuv_results.system_results.front.transmittance.direct_hemispherical))
print("System TUV front transmittance diffuse-diffuse: {v}".format(
    v=tuv_results.system_results.front.transmittance.diffuse_diffuse))
print(
    "System TUV front transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tuv_results.system_results.front.transmittance.matrix))

print("System TUV front reflectance direct-direct: {v}".format(
    v=tuv_results.system_results.front.reflectance.direct_direct))
print("System TUV front reflectance direct-diffuse: {v}".format(
    v=tuv_results.system_results.front.reflectance.direct_diffuse))
print("System TUV front reflectance direct-hemispherical: {v}".format(
    v=tuv_results.system_results.front.reflectance.direct_hemispherical))
print("System TUV front reflectance diffuse-diffuse: {v}".format(
    v=tuv_results.system_results.front.reflectance.diffuse_diffuse))
print(
    "System TUV front reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tuv_results.system_results.front.reflectance.matrix))

print("System TUV back transmittance direct-direct: {v}".format(
    v=tuv_results.system_results.back.transmittance.direct_direct))
print("System TUV back transmittance direct-diffuse: {v}".format(
    v=tuv_results.system_results.back.transmittance.direct_diffuse))
print("System TUV back transmittance direct-hemispherical: {v}".format(
    v=tuv_results.system_results.back.transmittance.direct_hemispherical))
print("System TUV back transmittance diffuse-diffuse: {v}".format(
    v=tuv_results.system_results.back.transmittance.diffuse_diffuse))
print(
    "System TUV back transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tuv_results.system_results.back.transmittance.matrix))

print("System TUV back reflectance direct-direct: {v}".format(
    v=tuv_results.system_results.back.reflectance.direct_direct))
print("System TUV back reflectance direct-diffuse: {v}".format(
    v=tuv_results.system_results.back.reflectance.direct_diffuse))
print("System TUV back reflectance direct-hemispherical: {v}".format(
    v=tuv_results.system_results.back.reflectance.direct_hemispherical))
print("System TUV back reflectance diffuse-diffuse: {v}".format(
    v=tuv_results.system_results.back.reflectance.diffuse_diffuse))
print("System TUV back reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
    v=tuv_results.system_results.back.reflectance.matrix))

for i in range(len(solid_layers)):
    print("Layer {idx} TUV front total direct absorptance: {v}".format(idx=i + 1,
                                                                       v=tuv_results.layer_results[
                                                                           i].front.absorptance.total_direct))
    print("Layer {idx} TUV front total diffuse absorptance: {v}".format(idx=i + 1,
                                                                        v=tuv_results.layer_results[
                                                                            i].front.absorptance.total_diffuse))
    print("Layer {idx} TUV front heat direct absorptance: {v}".format(idx=i + 1,
                                                                      v=tuv_results.layer_results[
                                                                          i].front.absorptance.heat_direct))
    print("Layer {idx} TUV front heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                       v=tuv_results.layer_results[
                                                                           i].front.absorptance.heat_diffuse))
    print("Layer {idx} TUV front electricity direct absorptance: {v}".format(idx=i + 1,
                                                                             v=tuv_results.layer_results[
                                                                                 i].front.absorptance.electricity_direct))
    print("Layer {idx} TUV front electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                              v=tuv_results.layer_results[
                                                                                  i].front.absorptance.electricity_diffuse))
    print(
        "Layer {idx} TUV back total direct absorptance: {v}".format(idx=i + 1,
                                                                    v=tuv_results.layer_results[
                                                                        i].back.absorptance.total_direct))
    print("Layer {idx} TUV back total diffuse absorptance: {v}".format(idx=i + 1,
                                                                       v=tuv_results.layer_results[
                                                                           i].back.absorptance.total_diffuse))
    print("Layer {idx} TUV back heat direct absorptance: {v}".format(idx=i + 1,
                                                                     v=tuv_results.layer_results[
                                                                         i].back.absorptance.heat_direct))
    print("Layer {idx} TUV back heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                      v=tuv_results.layer_results[
                                                                          i].back.absorptance.heat_diffuse))
    print("Layer {idx} TUV back electricity direct absorptance: {v}".format(idx=i + 1,
                                                                            v=tuv_results.layer_results[
                                                                                i].back.absorptance.electricity_direct))
    print("Layer {idx} TUV back electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                             v=tuv_results.layer_results[
                                                                                 i].back.absorptance.electricity_diffuse))

# ---------------------------------TDW-----------------------
tdw_results = glazing_system.optical_method_results("TDW")

print("System TDW front transmittance direct-direct: {v}".format(
    v=tdw_results.system_results.front.transmittance.direct_direct))
print("System TDW front transmittance direct-diffuse: {v}".format(
    v=tdw_results.system_results.front.transmittance.direct_diffuse))
print("System TDW front transmittance direct-hemispherical: {v}".format(
    v=tdw_results.system_results.front.transmittance.direct_hemispherical))
print("System TDW front transmittance diffuse-diffuse: {v}".format(
    v=tdw_results.system_results.front.transmittance.diffuse_diffuse))
print(
    "System TDW front transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tdw_results.system_results.front.transmittance.matrix))

print("System TDW front reflectance direct-direct: {v}".format(
    v=tdw_results.system_results.front.reflectance.direct_direct))
print("System TDW front reflectance direct-diffuse: {v}".format(
    v=tdw_results.system_results.front.reflectance.direct_diffuse))
print("System TDW front reflectance direct-hemispherical: {v}".format(
    v=tdw_results.system_results.front.reflectance.direct_hemispherical))
print("System TDW front reflectance diffuse-diffuse: {v}".format(
    v=tdw_results.system_results.front.reflectance.diffuse_diffuse))
print(
    "System TDW front reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tdw_results.system_results.front.reflectance.matrix))

print("System TDW back transmittance direct-direct: {v}".format(
    v=tdw_results.system_results.back.transmittance.direct_direct))
print("System TDW back transmittance direct-diffuse: {v}".format(
    v=tdw_results.system_results.back.transmittance.direct_diffuse))
print("System TDW back transmittance direct-hemispherical: {v}".format(
    v=tdw_results.system_results.back.transmittance.direct_hemispherical))
print("System TDW back transmittance diffuse-diffuse: {v}".format(
    v=tdw_results.system_results.back.transmittance.diffuse_diffuse))
print(
    "System TDW back transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tdw_results.system_results.back.transmittance.matrix))

print("System TDW back reflectance direct-direct: {v}".format(
    v=tdw_results.system_results.back.reflectance.direct_direct))
print("System TDW back reflectance direct-diffuse: {v}".format(
    v=tdw_results.system_results.back.reflectance.direct_diffuse))
print("System TDW back reflectance direct-hemispherical: {v}".format(
    v=tdw_results.system_results.back.reflectance.direct_hemispherical))
print("System TDW back reflectance diffuse-diffuse: {v}".format(
    v=tdw_results.system_results.back.reflectance.diffuse_diffuse))
print("System TDW back reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
    v=tdw_results.system_results.back.reflectance.matrix))

for i in range(len(solid_layers)):
    print("Layer {idx} TDW front total direct absorptance: {v}".format(idx=i + 1,
                                                                       v=tdw_results.layer_results[
                                                                           i].front.absorptance.total_direct))
    print("Layer {idx} TDW front total diffuse absorptance: {v}".format(idx=i + 1,
                                                                        v=tdw_results.layer_results[
                                                                            i].front.absorptance.total_diffuse))
    print("Layer {idx} TDW front heat direct absorptance: {v}".format(idx=i + 1,
                                                                      v=tdw_results.layer_results[
                                                                          i].front.absorptance.heat_direct))
    print("Layer {idx} TDW front heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                       v=tdw_results.layer_results[
                                                                           i].front.absorptance.heat_diffuse))
    print("Layer {idx} TDW front electricity direct absorptance: {v}".format(idx=i + 1,
                                                                             v=tdw_results.layer_results[
                                                                                 i].front.absorptance.electricity_direct))
    print("Layer {idx} TDW front electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                              v=tdw_results.layer_results[
                                                                                  i].front.absorptance.electricity_diffuse))
    print(
        "Layer {idx} TDW back total direct absorptance: {v}".format(idx=i + 1,
                                                                    v=tdw_results.layer_results[
                                                                        i].back.absorptance.total_direct))
    print("Layer {idx} TDW back total diffuse absorptance: {v}".format(idx=i + 1,
                                                                       v=tdw_results.layer_results[
                                                                           i].back.absorptance.total_diffuse))
    print("Layer {idx} TDW back heat direct absorptance: {v}".format(idx=i + 1,
                                                                     v=tdw_results.layer_results[
                                                                         i].back.absorptance.heat_direct))
    print("Layer {idx} TDW back heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                      v=tdw_results.layer_results[
                                                                          i].back.absorptance.heat_diffuse))
    print("Layer {idx} TDW back electricity direct absorptance: {v}".format(idx=i + 1,
                                                                            v=tdw_results.layer_results[
                                                                                i].back.absorptance.electricity_direct))
    print("Layer {idx} TDW back electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                             v=tdw_results.layer_results[
                                                                                 i].back.absorptance.electricity_diffuse))

# ---------------------------------TKR-----------------------
tkr_results = glazing_system.optical_method_results("TKR")

print("System TKR front transmittance direct-direct: {v}".format(
    v=tkr_results.system_results.front.transmittance.direct_direct))
print("System TKR front transmittance direct-diffuse: {v}".format(
    v=tkr_results.system_results.front.transmittance.direct_diffuse))
print("System TKR front transmittance direct-hemispherical: {v}".format(
    v=tkr_results.system_results.front.transmittance.direct_hemispherical))
print("System TKR front transmittance diffuse-diffuse: {v}".format(
    v=tkr_results.system_results.front.transmittance.diffuse_diffuse))
print(
    "System TKR front transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tkr_results.system_results.front.transmittance.matrix))

print("System TKR front reflectance direct-direct: {v}".format(
    v=tkr_results.system_results.front.reflectance.direct_direct))
print("System TKR front reflectance direct-diffuse: {v}".format(
    v=tkr_results.system_results.front.reflectance.direct_diffuse))
print("System TKR front reflectance direct-hemispherical: {v}".format(
    v=tkr_results.system_results.front.reflectance.direct_hemispherical))
print("System TKR front reflectance diffuse-diffuse: {v}".format(
    v=tkr_results.system_results.front.reflectance.diffuse_diffuse))
print(
    "System TKR front reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tkr_results.system_results.front.reflectance.matrix))

print("System TKR back transmittance direct-direct: {v}".format(
    v=tkr_results.system_results.back.transmittance.direct_direct))
print("System TKR back transmittance direct-diffuse: {v}".format(
    v=tkr_results.system_results.back.transmittance.direct_diffuse))
print("System TKR back transmittance direct-hemispherical: {v}".format(
    v=tkr_results.system_results.back.transmittance.direct_hemispherical))
print("System TKR back transmittance diffuse-diffuse: {v}".format(
    v=tkr_results.system_results.back.transmittance.diffuse_diffuse))
print(
    "System TKR back transmittance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
        v=tkr_results.system_results.back.transmittance.matrix))

print("System TKR back reflectance direct-direct: {v}".format(
    v=tkr_results.system_results.back.reflectance.direct_direct))
print("System TKR back reflectance direct-diffuse: {v}".format(
    v=tkr_results.system_results.back.reflectance.direct_diffuse))
print("System TKR back reflectance direct-hemispherical: {v}".format(
    v=tkr_results.system_results.back.reflectance.direct_hemispherical))
print("System TKR back reflectance diffuse-diffuse: {v}".format(
    v=tkr_results.system_results.back.reflectance.diffuse_diffuse))
print("System TKR back reflectance matrix (only available for systems calculated with a BSDF hemisphere): {v}".format(
    v=tkr_results.system_results.back.reflectance.matrix))

for i in range(len(solid_layers)):
    print("Layer {idx} TKR front total direct absorptance: {v}".format(idx=i + 1,
                                                                       v=tkr_results.layer_results[
                                                                           i].front.absorptance.total_direct))
    print("Layer {idx} TKR front total diffuse absorptance: {v}".format(idx=i + 1,
                                                                        v=tkr_results.layer_results[
                                                                            i].front.absorptance.total_diffuse))
    print("Layer {idx} TKR front heat direct absorptance: {v}".format(idx=i + 1,
                                                                      v=tkr_results.layer_results[
                                                                          i].front.absorptance.heat_direct))
    print("Layer {idx} TKR front heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                       v=tkr_results.layer_results[
                                                                           i].front.absorptance.heat_diffuse))
    print("Layer {idx} TKR front electricity direct absorptance: {v}".format(idx=i + 1,
                                                                             v=tkr_results.layer_results[
                                                                                 i].front.absorptance.electricity_direct))
    print("Layer {idx} TKR front electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                              v=tkr_results.layer_results[
                                                                                  i].front.absorptance.electricity_diffuse))
    print(
        "Layer {idx} TKR back total direct absorptance: {v}".format(idx=i + 1,
                                                                    v=tkr_results.layer_results[
                                                                        i].back.absorptance.total_direct))
    print("Layer {idx} TKR back total diffuse absorptance: {v}".format(idx=i + 1,
                                                                       v=tkr_results.layer_results[
                                                                           i].back.absorptance.total_diffuse))
    print("Layer {idx} TKR back heat direct absorptance: {v}".format(idx=i + 1,
                                                                     v=tkr_results.layer_results[
                                                                         i].back.absorptance.heat_direct))
    print("Layer {idx} TKR back heat diffuse absorptance: {v}".format(idx=i + 1,
                                                                      v=tkr_results.layer_results[
                                                                          i].back.absorptance.heat_diffuse))
    print("Layer {idx} TKR back electricity direct absorptance: {v}".format(idx=i + 1,
                                                                            v=tkr_results.layer_results[
                                                                                i].back.absorptance.electricity_direct))
    print("Layer {idx} TKR back electricity diffuse absorptance: {v}".format(idx=i + 1,
                                                                             v=tkr_results.layer_results[
                                                                                 i].back.absorptance.electricity_diffuse))

# ------------------------------------Color------------------------------------  
# Color results have a different calculation method and so require a different call to calculate
# Also color results do not have results for each layer.  Only system results exist for color
color_results = glazing_system.color()
# Front transmittance direct-direct
print("Color front transmittance direct-direct RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.front.transmittance.direct_direct.rgb.R,
    g=color_results.system_results.front.transmittance.direct_direct.rgb.G,
    b=color_results.system_results.front.transmittance.direct_direct.rgb.B))
print("Color front transmittance direct-direct Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.front.transmittance.direct_direct.lab.L,
    a=color_results.system_results.front.transmittance.direct_direct.lab.a,
    b=color_results.system_results.front.transmittance.direct_direct.lab.b))
print("Color front transmittance direct-direct Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.front.transmittance.direct_direct.trichromatic.X,
    y=color_results.system_results.front.transmittance.direct_direct.trichromatic.Y,
    z=color_results.system_results.front.transmittance.direct_direct.trichromatic.Z))

# Front transmittance direct-diffuse.
print("Color front transmittance direct-diffuse RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.front.transmittance.direct_diffuse.rgb.R,
    g=color_results.system_results.front.transmittance.direct_diffuse.rgb.G,
    b=color_results.system_results.front.transmittance.direct_diffuse.rgb.B))
print("Color front transmittance direct-diffuse Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.front.transmittance.direct_diffuse.lab.L,
    a=color_results.system_results.front.transmittance.direct_diffuse.lab.a,
    b=color_results.system_results.front.transmittance.direct_diffuse.lab.b))
print("Color front transmittance direct-diffuse Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.front.transmittance.direct_diffuse.trichromatic.X,
    y=color_results.system_results.front.transmittance.direct_diffuse.trichromatic.Y,
    z=color_results.system_results.front.transmittance.direct_diffuse.trichromatic.Z))

# Front transmittance direct-hemispherical.
print("Color front transmittance direct-hemispherical RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.front.transmittance.direct_hemispherical.rgb.R,
    g=color_results.system_results.front.transmittance.direct_hemispherical.rgb.G,
    b=color_results.system_results.front.transmittance.direct_hemispherical.rgb.B))
print("Color front transmittance direct-hemispherical Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.front.transmittance.direct_hemispherical.lab.L,
    a=color_results.system_results.front.transmittance.direct_hemispherical.lab.a,
    b=color_results.system_results.front.transmittance.direct_hemispherical.lab.b))
print("Color front transmittance direct-hemispherical Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.front.transmittance.direct_hemispherical.trichromatic.X,
    y=color_results.system_results.front.transmittance.direct_hemispherical.trichromatic.Y,
    z=color_results.system_results.front.transmittance.direct_hemispherical.trichromatic.Z))

# Front transmittance diffuse-diffuse
print("Color front transmittance diffuse-diffuse RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.front.transmittance.diffuse_diffuse.rgb.R,
    g=color_results.system_results.front.transmittance.diffuse_diffuse.rgb.G,
    b=color_results.system_results.front.transmittance.diffuse_diffuse.rgb.B))
print("Color front transmittance diffuse-diffuse Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.front.transmittance.diffuse_diffuse.lab.L,
    a=color_results.system_results.front.transmittance.diffuse_diffuse.lab.a,
    b=color_results.system_results.front.transmittance.diffuse_diffuse.lab.b))
print("Color front transmittance diffuse-diffuse Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.front.transmittance.diffuse_diffuse.trichromatic.X,
    y=color_results.system_results.front.transmittance.diffuse_diffuse.trichromatic.Y,
    z=color_results.system_results.front.transmittance.diffuse_diffuse.trichromatic.Z))

# Front reflectance direct-direct
print("Color front reflectance direct-direct RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.front.reflectance.direct_direct.rgb.R,
    g=color_results.system_results.front.reflectance.direct_direct.rgb.G,
    b=color_results.system_results.front.reflectance.direct_direct.rgb.B))
print("Color front reflectance direct-direct Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.front.reflectance.direct_direct.lab.L,
    a=color_results.system_results.front.reflectance.direct_direct.lab.a,
    b=color_results.system_results.front.reflectance.direct_direct.lab.b))
print("Color front reflectance direct-direct Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.front.reflectance.direct_direct.trichromatic.X,
    y=color_results.system_results.front.reflectance.direct_direct.trichromatic.Y,
    z=color_results.system_results.front.reflectance.direct_direct.trichromatic.Z))

# Front reflectance direct-diffuse.
print("Color front reflectance direct-diffuse RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.front.reflectance.direct_diffuse.rgb.R,
    g=color_results.system_results.front.reflectance.direct_diffuse.rgb.G,
    b=color_results.system_results.front.reflectance.direct_diffuse.rgb.B))
print("Color front reflectance direct-diffuse Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.front.reflectance.direct_diffuse.lab.L,
    a=color_results.system_results.front.reflectance.direct_diffuse.lab.a,
    b=color_results.system_results.front.reflectance.direct_diffuse.lab.b))
print("Color front reflectance direct-diffuse Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.front.reflectance.direct_diffuse.trichromatic.X,
    y=color_results.system_results.front.reflectance.direct_diffuse.trichromatic.Y,
    z=color_results.system_results.front.reflectance.direct_diffuse.trichromatic.Z))

# Front reflectance direct-hemispherical.
print("Color front reflectance direct-hemispherical RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.front.reflectance.direct_hemispherical.rgb.R,
    g=color_results.system_results.front.reflectance.direct_hemispherical.rgb.G,
    b=color_results.system_results.front.reflectance.direct_hemispherical.rgb.B))
print("Color front reflectance direct-hemispherical Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.front.reflectance.direct_hemispherical.lab.L,
    a=color_results.system_results.front.reflectance.direct_hemispherical.lab.a,
    b=color_results.system_results.front.reflectance.direct_hemispherical.lab.b))
print("Color front reflectance direct-hemispherical Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.front.reflectance.direct_hemispherical.trichromatic.X,
    y=color_results.system_results.front.reflectance.direct_hemispherical.trichromatic.Y,
    z=color_results.system_results.front.reflectance.direct_hemispherical.trichromatic.Z))

# Front reflectance diffuse-diffuse
print("Color front reflectance diffuse-diffuse RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.front.reflectance.diffuse_diffuse.rgb.R,
    g=color_results.system_results.front.reflectance.diffuse_diffuse.rgb.G,
    b=color_results.system_results.front.reflectance.diffuse_diffuse.rgb.B))
print("Color front reflectance diffuse-diffuse Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.front.reflectance.diffuse_diffuse.lab.L,
    a=color_results.system_results.front.reflectance.diffuse_diffuse.lab.a,
    b=color_results.system_results.front.reflectance.diffuse_diffuse.lab.b))
print("Color front reflectance diffuse-diffuse Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.front.reflectance.diffuse_diffuse.trichromatic.X,
    y=color_results.system_results.front.reflectance.diffuse_diffuse.trichromatic.Y,
    z=color_results.system_results.front.reflectance.diffuse_diffuse.trichromatic.Z))

print("Color back transmittance direct-direct RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.back.transmittance.direct_direct.rgb.R,
    g=color_results.system_results.back.transmittance.direct_direct.rgb.G,
    b=color_results.system_results.back.transmittance.direct_direct.rgb.B))
print("Color back transmittance direct-direct Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.back.transmittance.direct_direct.lab.L,
    a=color_results.system_results.back.transmittance.direct_direct.lab.a,
    b=color_results.system_results.back.transmittance.direct_direct.lab.b))
print("Color back transmittance direct-direct Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.back.transmittance.direct_direct.trichromatic.X,
    y=color_results.system_results.back.transmittance.direct_direct.trichromatic.Y,
    z=color_results.system_results.back.transmittance.direct_direct.trichromatic.Z))

# back transmittance direct-diffuse.
print("Color back transmittance direct-diffuse RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.back.transmittance.direct_diffuse.rgb.R,
    g=color_results.system_results.back.transmittance.direct_diffuse.rgb.G,
    b=color_results.system_results.back.transmittance.direct_diffuse.rgb.B))
print("Color back transmittance direct-diffuse Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.back.transmittance.direct_diffuse.lab.L,
    a=color_results.system_results.back.transmittance.direct_diffuse.lab.a,
    b=color_results.system_results.back.transmittance.direct_diffuse.lab.b))
print("Color back transmittance direct-diffuse Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.back.transmittance.direct_diffuse.trichromatic.X,
    y=color_results.system_results.back.transmittance.direct_diffuse.trichromatic.Y,
    z=color_results.system_results.back.transmittance.direct_diffuse.trichromatic.Z))

# back transmittance direct-hemispherical.
print("Color back transmittance direct-hemispherical RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.back.transmittance.direct_hemispherical.rgb.R,
    g=color_results.system_results.back.transmittance.direct_hemispherical.rgb.G,
    b=color_results.system_results.back.transmittance.direct_hemispherical.rgb.B))
print("Color back transmittance direct-hemispherical Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.back.transmittance.direct_hemispherical.lab.L,
    a=color_results.system_results.back.transmittance.direct_hemispherical.lab.a,
    b=color_results.system_results.back.transmittance.direct_hemispherical.lab.b))
print("Color back transmittance direct-hemispherical Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.back.transmittance.direct_hemispherical.trichromatic.X,
    y=color_results.system_results.back.transmittance.direct_hemispherical.trichromatic.Y,
    z=color_results.system_results.back.transmittance.direct_hemispherical.trichromatic.Z))

# back transmittance diffuse-diffuse
print("Color back transmittance diffuse-diffuse RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.back.transmittance.diffuse_diffuse.rgb.R,
    g=color_results.system_results.back.transmittance.diffuse_diffuse.rgb.G,
    b=color_results.system_results.back.transmittance.diffuse_diffuse.rgb.B))
print("Color back transmittance diffuse-diffuse Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.back.transmittance.diffuse_diffuse.lab.L,
    a=color_results.system_results.back.transmittance.diffuse_diffuse.lab.a,
    b=color_results.system_results.back.transmittance.diffuse_diffuse.lab.b))
print("Color back transmittance diffuse-diffuse Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.back.transmittance.diffuse_diffuse.trichromatic.X,
    y=color_results.system_results.back.transmittance.diffuse_diffuse.trichromatic.Y,
    z=color_results.system_results.back.transmittance.diffuse_diffuse.trichromatic.Z))

# back reflectance direct-direct
print("Color back reflectance direct-direct RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.back.reflectance.direct_direct.rgb.R,
    g=color_results.system_results.back.reflectance.direct_direct.rgb.G,
    b=color_results.system_results.back.reflectance.direct_direct.rgb.B))
print("Color back reflectance direct-direct Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.back.reflectance.direct_direct.lab.L,
    a=color_results.system_results.back.reflectance.direct_direct.lab.a,
    b=color_results.system_results.back.reflectance.direct_direct.lab.b))
print("Color back reflectance direct-direct Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.back.reflectance.direct_direct.trichromatic.X,
    y=color_results.system_results.back.reflectance.direct_direct.trichromatic.Y,
    z=color_results.system_results.back.reflectance.direct_direct.trichromatic.Z))

# back reflectance direct-diffuse.
print("Color back reflectance direct-diffuse RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.back.reflectance.direct_diffuse.rgb.R,
    g=color_results.system_results.back.reflectance.direct_diffuse.rgb.G,
    b=color_results.system_results.back.reflectance.direct_diffuse.rgb.B))
print("Color back reflectance direct-diffuse Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.back.reflectance.direct_diffuse.lab.L,
    a=color_results.system_results.back.reflectance.direct_diffuse.lab.a,
    b=color_results.system_results.back.reflectance.direct_diffuse.lab.b))
print("Color back reflectance direct-diffuse Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.back.reflectance.direct_diffuse.trichromatic.X,
    y=color_results.system_results.back.reflectance.direct_diffuse.trichromatic.Y,
    z=color_results.system_results.back.reflectance.direct_diffuse.trichromatic.Z))

# back reflectance direct-hemispherical.
print("Color back reflectance direct-hemispherical RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.back.reflectance.direct_hemispherical.rgb.R,
    g=color_results.system_results.back.reflectance.direct_hemispherical.rgb.G,
    b=color_results.system_results.back.reflectance.direct_hemispherical.rgb.B))
print("Color back reflectance direct-hemispherical Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.back.reflectance.direct_hemispherical.lab.L,
    a=color_results.system_results.back.reflectance.direct_hemispherical.lab.a,
    b=color_results.system_results.back.reflectance.direct_hemispherical.lab.b))
print("Color back reflectance direct-hemispherical Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.back.reflectance.direct_hemispherical.trichromatic.X,
    y=color_results.system_results.back.reflectance.direct_hemispherical.trichromatic.Y,
    z=color_results.system_results.back.reflectance.direct_hemispherical.trichromatic.Z))

# back reflectance diffuse-diffuse
print("Color back reflectance diffuse-diffuse RGB: ({r}, {g}, {b})".format(
    r=color_results.system_results.back.reflectance.diffuse_diffuse.rgb.R,
    g=color_results.system_results.back.reflectance.diffuse_diffuse.rgb.G,
    b=color_results.system_results.back.reflectance.diffuse_diffuse.rgb.B))
print("Color back reflectance diffuse-diffuse Lab: ({l}, {a}, {b})".format(
    l=color_results.system_results.back.reflectance.diffuse_diffuse.lab.L,
    a=color_results.system_results.back.reflectance.diffuse_diffuse.lab.a,
    b=color_results.system_results.back.reflectance.diffuse_diffuse.lab.b))
print("Color back reflectance diffuse-diffuse Trichromatic: ({x}, {y}, {z})".format(
    x=color_results.system_results.back.reflectance.diffuse_diffuse.trichromatic.X,
    y=color_results.system_results.back.reflectance.diffuse_diffuse.trichromatic.Y,
    z=color_results.system_results.back.reflectance.diffuse_diffuse.trichromatic.Z))

# Thermal IR:  Thermal IR results are not available for a system.  They are only available for a solid layer
# See thermal_ir.py

# ------------------------------------Thermal Results--------------------------------------------
# Since thermal results depend on environmental conditions the below examples will show
# results for the two most common values (U and SHGC) using both sets of standard NFRC environmental conditions
# to demonstrate the difference environmental conditions can make
#
# However any system created with any environmental conditions has all results available to it.
# For more on creating user-defined environmental conditions see custom_environmental_conditions.py

u_value_NFRC_u_conditions = glazing_system_u_environment.u()
u_value_NFRC_shgc_conditions = glazing_system_shgc_environment.u()
print(
    "U-Value.  Based on NFRC U-value environmental conditions: {u}.  Based on NFRC SHGC environmnetal conditions: {shgc}".format(
        u=u_value_NFRC_u_conditions, shgc=u_value_NFRC_shgc_conditions))

shgc_NFRC_u_conditions = glazing_system_u_environment.shgc()
shgc_NFRC_shgc_conditions = glazing_system_shgc_environment.shgc()
print(
    "SHGC.  Based on NFRC U-value environmental conditions: {u}.  Based on NFRC SHGC environmnetal conditions: {shgc}".format(
        u=shgc_NFRC_u_conditions, shgc=shgc_NFRC_shgc_conditions))

#----------------------------Other thermal results-----------------------------
# Most other thermal can be calculated for two cases for each environment.  When U system is passed as a parameter
# the layer temperatures will be calculated for the given environments without taking solar radiation into account.
# When SHGC system is passed as a parameter solar ration is taken into account
#
# The exception is relative_heat_gain which does not take a system type.
#
# Since the NFRC U-value conditions have 0 solar radiation the below will all use the SHGC conditions
# as examples.
shgc_layer_temperatures_with_solar_radiation = glazing_system_shgc_environment.layer_temperatures(
    pywincalc.TarcogSystemType.SHGC)
print("Layer temperatures in SHGC environment with solar radiation: {v}".format(
    v=shgc_layer_temperatures_with_solar_radiation))
shgc_layer_temperatures_without_solar_radiation = glazing_system_shgc_environment.layer_temperatures(
    pywincalc.TarcogSystemType.U)
print("Layer temperatures in SHGC environment without solar radiation: {v}".format(
    v=shgc_layer_temperatures_without_solar_radiation))

shgc_environment_solid_layer_effective_conductivities_with_solar_radiation = glazing_system_shgc_environment.solid_layers_effective_conductivities(
    (pywincalc.TarcogSystemType.SHGC))
print("Solid layer effective conductivities in SHGC environment with solar radiation: {v}".format(
    v=shgc_environment_solid_layer_effective_conductivities_with_solar_radiation))
shgc_environment_solid_layer_effective_conductivities_without_solar_radiation = glazing_system_shgc_environment.solid_layers_effective_conductivities(
    (pywincalc.TarcogSystemType.U))
print("Solid layer effective conductivities in SHGC environment without solar radiation: {v}".format(
    v=shgc_environment_solid_layer_effective_conductivities_without_solar_radiation))

shgc_environment_gap_layer_effective_conductivities_with_solar_radiation = glazing_system_shgc_environment.gap_layers_effective_conductivities(
    (pywincalc.TarcogSystemType.SHGC))
print("Gap layer effective conductivities in SHGC environment with solar radiation: {v}".format(
    v=shgc_environment_gap_layer_effective_conductivities_with_solar_radiation))
shgc_environment_gap_layer_effective_conductivities_without_solar_radiation = glazing_system_shgc_environment.gap_layers_effective_conductivities(
    (pywincalc.TarcogSystemType.U))
print("Gap layer effective conductivities in SHGC environment without solar radiation: {v}".format(
    v=shgc_environment_gap_layer_effective_conductivities_without_solar_radiation))

system_effective_conductivity_with_solar_radiation = glazing_system_shgc_environment.system_effective_conductivity(
    pywincalc.TarcogSystemType.SHGC)
print("System effective conductivity with solar radiation: {v}".format(
    v=system_effective_conductivity_with_solar_radiation))
system_effective_conductivity_without_solar_radiation = glazing_system_shgc_environment.system_effective_conductivity(
    pywincalc.TarcogSystemType.U)
print("System effective conductivity without solar radiation: {v}".format(
    v=system_effective_conductivity_without_solar_radiation))

# Relative heat gain is an exception and does not take a system type as a parameter
relative_heat_gain = glazing_system_shgc_environment.relative_heat_gain()
print("Relative heat gain: {v}".format(v=relative_heat_gain))

# Deflection calculation and results are also available.  See deflection.py in examples