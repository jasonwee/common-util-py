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


class TransactionError(Exception):
    """Custom exception for transaction-related errors."""

# Sanitize table and column names
def sanitize_identifier(identifier: str) -> str:
    # Remove any characters that aren't alphanumeric or underscores
    return ''.join(c if c.isalnum() or c == '_' else '' for c in identifier)