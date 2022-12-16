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
import os
from operator import attrgetter, itemgetter

import pyproj as pyproj
import rasterio
from pyproj import Transformer


class FormationDB:
    def get_surface_elevation(self, x, y, path, as_utm=False):
        with rasterio.open(path) as dataset:
            if not as_utm:
                out = "epsg:4326"
                incrs = "epsg:{}".format(dataset.crs.to_epsg())
                transformer = Transformer.from_crs(out, incrs)
                lon, lat = transformer.transform(y, x)
            else:
                lon, lat = y, x
            py, px = dataset.index(lon, lat)

            arr = dataset.read(1)
            elevation = int(arr[py, px])
            if elevation != 65535:
                return elevation

    def search_rasters(self, x, y, z=None, as_utm=False):
        surface = self.get_surface_elevation(x, y, os.path.join('data', 'landsurface.tif'), as_utm)
        root = os.path.join('data', 'discrete')
        column = []
        for pname in os.listdir(root):
            name, ext = os.path.splitext(pname)
            if ext not in ('.tiff', '.tif'):
                continue
            p = os.path.join(root, pname)

            base_elevation = self.get_surface_elevation(x, y, p, as_utm)
            # print(name, base_elevation, surface)
            if base_elevation is not None:
                column.append((name, abs(base_elevation - surface)))

        cs = sorted(column, key=itemgetter(1))
        if z:
            min_depth = 0
            for name, depth in cs:
                if depth > z:
                    return name, min_depth, depth
                min_depth = depth
        else:
            return cs

    def get_formation(self, x, y, z, as_utm=False):
        f = self.search_rasters(x, y, z, as_utm)
        if f:
            name, min_depth, max_depth = f
            name = name.split('_')[1]
            f = {'name': name,
                 "depth_to_surface_top": min_depth,
                 "depth_to_surface_base": max_depth}

            return f

    def get_stratigraphy(self, x, y):
        return [dict(name="P Yeso", code="303YESO", zmin=10, zmax=20),
                dict(name="P San Andres", code='313SADR', zmin=20, zmax=1000)]


if __name__ == '__main__':
    fm = FormationDB()

    # frm = fm.get_formation(664655, 3658463, 10, True)
    frm = fm.get_formation(553108.095, 3700398.550, 125, True)
    print(frm)
    # fm.get_formation(-104.5824, 33.3186, 10)
    # fm.get_formation(545118, 3671007, 10)
# ============= EOF =============================================
