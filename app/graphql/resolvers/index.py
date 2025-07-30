from .user.query_resolvers import query_resolvers
from .user.mutation_resolvers import mutation_resolvers

resolvers = [query_resolvers, mutation_resolvers]

# 동적으로 resolver loading
# import importlib
# import pkgutil
# import os

# resolvers = []

# def load_resolvers():
#     base_path = os.path.dirname(__file__)
#     for _, module_name, _ in pkgutil.iter_modules([base_path]):
#         if module_name == "index":
#             continue  # exclude index.py
#         module = importlib.import_module(f"app.resolvers.{module_name}")
#         if hasattr(module, "query"):
#             resolvers.append(module.query)
#         if hasattr(module, "mutation"):
#             resolvers.append(module.mutation)

# load_resolvers()