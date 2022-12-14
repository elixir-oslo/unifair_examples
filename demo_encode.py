from omnipy import runtime
from omnipy.compute.flow import FuncFlowTemplate
from omnipy.modules.fairtracks.tasks import import_dataset_from_encode
from omnipy.modules.general.tasks import cast_dataset
from omnipy.modules.json.models import JsonDictOfAnyModel
from omnipy.modules.json.util import serialize_to_tarpacked_json_files
from omnipy.modules.pandas.util import serialize_to_tarpacked_csv_files
from omnipy.modules.tables.tasks import flatten_nested_json_to_list_of_dicts, remove_columns
import omnipy.modules.json.util
import omnipy.modules.pandas.util
import omnipy.modules.raw.util
omnipy.modules.json.util.ROOT_DIR = './input/bif'
omnipy.modules.pandas.util.ROOT_DIR = './input/bif'
omnipy.modules.raw.util.ROOT_DIR = './input/bif'



runtime.config.engine = 'local'
runtime.config.prefect.use_cached_results = False

# cast_to_dict_on_top = cast_dataset.refine(
#     name='cast_to_dict_on_top',
#     fixed_params=dict(cast_model=JsonDictOfAnyModel),
# )

encode_json = import_dataset_from_encode.run(
    endpoints=[
        'experiment',
        'biosample',
    ],
    max_data_item_count=25,
)
# encode_json_pruned = remove_columns.run(
#     encode_json, column_keys_for_data_items=dict(
#         experiment=['audit'],
#         biosample=['audit'],
#     ))
# encode_json_dict = cast_to_dict_on_top.run(encode_json)
splitted_encode_json = flatten_nested_json_to_list_of_dicts.run(encode_json)

serialize_to_tarpacked_json_files('encode_json', encode_json)
serialize_to_tarpacked_json_files('splitted_encode_json', splitted_encode_json)
# serialize_to_tarpacked_csv_files('encode_json', encode_json)
serialize_to_tarpacked_csv_files('splitted_encode_csv', splitted_encode_json)
# serialize_to_tarpacked_csv_files('encode_json_pruned', encode_json_pruned)

# runtime = Runtime()
# runtime.config.engine = 'prefect'
# runtime.config.prefect.use_cached_results = True
#
#
# @FuncFlowTemplate
# def import_encode_data_tmpl():
#     encode_json = import_dataset_from_encode(
#         endpoints=[
#             'experiment',
#             'biosample',
#         ],
#         max_data_item_count=25,
#         serialize_as='csv',
#     )
#     encode_json_pruned = remove_columns(
#         encode_json,
#         column_keys_for_data_items=dict(
#             experiment=['audit'],
#             biosample=['audit'],
#         ),
#         serialize_as='csv',
#     )
#     return encode_json_pruned
#
#
# import_encode_data.run()
