from osgeo import gdal, osr


class ElevationService:
    def __init__(self, tif_path):
        gdal.UseExceptions()
        self.dataset = gdal.Open(tif_path, gdal.GA_ReadOnly)
        proj = self.dataset.GetProjection()
        sr = osr.SpatialReference(wkt=proj)

    def get_elevation(self, lat: int, lon: int) -> int | None:
        if self.dataset is None:
            return None
        # 緯度と経度をピクセル座標に変換
        gt = self.dataset.GetGeoTransform()
        x = int((lon - gt[0]) / gt[1])
        y = int((lat - gt[3]) / gt[5])

        # ピクセル座標から標高を取得
        band = self.dataset.GetRasterBand(1)
        elevation = band.ReadAsArray(x, y, 1, 1)[0, 0]
        return elevation

    def __del__(self):
        self.dataset = None
