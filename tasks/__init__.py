from invoke import Collection

from . import env
from . import format as format_
from . import test

ns = Collection()
ns.add_collection(env)
ns.add_collection(format_)
ns.add_collection(test)
