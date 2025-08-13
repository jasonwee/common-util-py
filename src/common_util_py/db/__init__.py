# -*- coding: UTF-8 -*-
#
#   Copyright WeeTech Developer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""db module"""

from .mysql import Mysql as mysql
from .sql import (
    create_table,
    drop_table,
    insert,
    insert_statement,
    insert_rows,
    select_statement,
    delete,
    update,
    update_table,
    generic,
)

__all__ = [
    "mysql",
    "create_table",
    "drop_table",
    "insert",
    "insert_statement",
    "insert_rows",
    "select_statement",
    "delete",
    "update",
    "update_table",
    "generic",
]
