import yeelight

smart_software_tuples = (
    (None, '---'),
    ('yeelight_bulb', 'Yeelight Bulb')
)

yeelight_models_tuple = tuple((x, x) for x in yeelight.main._MODEL_SPECS)