# ===============================================================================
# Copyright 2022 ross
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
# ===============================================================================

from three_d_model import FormationDB
from fastapi import FastAPI
from response_models import Formation
from typing import List


app = FastAPI()

fm = FormationDB()

@app.get("/stratigraphy/{x}/{y}", response_model=List[Formation])
async def read_stratigraphy(x: float,y: float):
    return fm.get_stratigraphy(x,y)


@app.get("/formation/{x}/{y}/{z}", response_model=Formation)
async def read_formation(x: float, y: float, z: float):
    return fm.get_formation(x,y,z)

if __name__ == '__main__':
    app.run()    
# ============= EOF =============================================
