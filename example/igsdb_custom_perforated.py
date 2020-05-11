import pywincalc
import requests

# Path to the optical standard file.  All other files referenced by the standard file must be in the same directory
# Note:  While all optical standards packaged with WINDOW should work with optical calculations care should be
# taken to use NFRC standards if thermal results are desired.  This is because for thermal calculations currently
# only ISO 15099 is supported.  So while it is possible to use EN optical standards and create thermal results
# those results will not be based on EN 673
optical_standard_path = "standards/W5_NFRC_2003.std"
optical_standard = pywincalc.load_standard(optical_standard_path)

glazing_system_width = 1.0  # width of the glazing system in meters
glazing_system_height = 1.0  # height of the glazing system in meters

# Define the gap between the shade and the glazing
gap_1 = pywincalc.Gap_Data(pywincalc.Predefined_Gas_Type.AIR, .0127)  # .0127 is gap thickness in meters

# A woven shade requires a BSDF hemisphere.  Create one based on a standard quarter basis for this test
bsdf_hemisphere = pywincalc.BSDF_Hemisphere.create(pywincalc.BSDF_Basis.Quarter)

# Download some product data from the IGSDB.  This example gets a generic single clear 3mm glazing (NFRC 102),
# and a material to use as part of the woven shade.
# For more information on getting data from the igsdb please see igsdb.lbl.gov/openapi
igsdb_api_token = "8ae3205081608099fe0261178ea571ecc3b01fc2"
url_single_product = "http://localhost:8000/api/v1/products/{id}"  # Template URL for single product

headers = {"Authorization": "Token {token}".format(token=igsdb_api_token)}  # Token authorization headers

generic_clear_3mm_glass_igsdb_id = 363

# This is the same material used in the venetian example but could be any material in the igsdb
shade_material_igsdb_id = 12852

generic_clear_3mm_glass_igsdb_response = requests.get(url_single_product.format(id=generic_clear_3mm_glass_igsdb_id),
                                                      headers=headers)
shade_material_igsdb_response = requests.get(
    url_single_product.format(id=shade_material_igsdb_id), headers=headers)

generic_clear_3mm_glass = pywincalc.parse_json(generic_clear_3mm_glass_igsdb_response.content)

shade_material = pywincalc.parse_json(shade_material_igsdb_response.content)

# Perforated screens need Perforated_Geometry.
# Make a rectangular perforation here.  Other options include circular and square
# Note: While using a string for perforation type is not ideal it is used here because this
# example is mostly using data from the IGSDB for the material and only adding a custom geometry
# For an example where the data is completely custom generated see custom_perforated.py
# TODO Do we really want to have both rectangular and square?  Seems redundant
perforation_type = "rectangular"
spacing_x = 0.01 # 10mm horizontal spacing
spacing_y = 0.02 # 20mm vertical spacing
dimension_x = 0.002 # 2mm perforation in the horizontal direction
dimension_y = 0.003 # 3mm perforation in the vertical direction
geometry = pywincalc.Perforated_Geometry(spacing_x, spacing_y, dimension_x, dimension_y, perforation_type)

# combine the shade_material and the geometry together into a Product_Composistion_Data
composition_data = pywincalc.Product_Composistion_Data(shade_material, geometry)

# create a layer from the product composition data.  No other information is required to create a layer in this case
woven_shade_layer = pywincalc.Composed_Product_Data(composition_data)

exterior_woven_u_environment = pywincalc.Glazing_System([woven_shade_layer, generic_clear_3mm_glass],
                                                           [gap_1],
                                                           optical_standard, glazing_system_width,
                                                           glazing_system_height,
                                                           pywincalc.nfrc_u_environments(), bsdf_hemisphere)

exterior_woven_shgc_environment = pywincalc.Glazing_System(
    [woven_shade_layer, generic_clear_3mm_glass], [gap_1],
    optical_standard, glazing_system_width, glazing_system_height,
    pywincalc.nfrc_shgc_environments(), bsdf_hemisphere)

exterior_woven_u = exterior_woven_u_environment.u()
print("Exterior venetian U: {v}".format(v=exterior_woven_u))
exterior_woven_shgc = exterior_woven_shgc_environment.shgc()
print("Exterior venetian SHGC: {v}".format(v=exterior_woven_shgc))
