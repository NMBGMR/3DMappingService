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

class FormationDB:
    def load_rasters(self):

        for code in ['303YESO', '313SADR']:
            p = os.path.join('data', 'rasters', f'{code}.tif')

            with rasterio.open(p) as dataset:
                self._rasters[code] = dataset

    def get_formation(self, x,y,z):
        return dict(code="303YESO", 
                    name="P Yeso",
                    zmin=0,
                    zmax=100)

    def get_stratigraphy(self, x, y):
        return [dict(name="P Yeso", code="303YESO", zmin=10, zmax=20),
                dict(name="P San Andres", code='313SADR', zmin=20, zmax=1000)]
                
# ============= EOF =============================================
