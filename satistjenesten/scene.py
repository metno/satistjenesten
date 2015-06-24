from satistjenesten.utils import load_area_def
from copy import deepcopy, copy
from pyresample import kd_tree, geometry
from osgeo import gdal, osr
from PIL import Image
import numpy
import pyresample as pr

class SatBand(object):
    def __init__(self):
        self.data = None
        self.long_name = None
        self.dtype    = None
        self.unit = None
        self.latitude = None
        self.longitude = None

class GenericScene(object):
    def __init__(self, filepath=None, configpath=None, **kwargs):
        self.file_path = filepath
        self.yaml_dict = configpath
        self.bands = None
        self.longitudes = None
        self.latitudes = None
        self.area_def = None
        self.timestamp = None
        self.kwargs = kwargs
        self._swath_area_def = None

    def get_filehandle(self):
        self.filehandle = open(self.file_path, 'r')

    @property
    def timestamp_string(self):
        return self.timestamp.strftime('%Y%m%d_%H%M')

    def get_area_def(self, area_name=None):
        if area_name:
            self.area_name = area_name
            self.area_def = load_area_def(self.area_name)
        else:
            pass

    @property
    def swath_area_def(self):
        return self._swath_area_def

    def get_swath_area_def(self, lons_name, lats_name):
        if self._swath_area_def is None:
            try:
                lons = self.filehandle.variables[lons_name][:]
                lats = self.filehandle.variables[lats_name][:]
            except:
                raise Exception('File does not contain latitude/longitude information')

        swath_area_def = geometry.SwathDefinition(lons, lats)
        self._swath_area_def = swath_area_def
        self.area_def = swath_area_def

    def load(self):
        self.get_filehandle()
        self.get_bands()

    def get_coordinates(self):
        """
        Retrieve lon/lat coordinates from the area definition object

        """
        if self.area_def is None:
            self.get_area_def()
        self.longitudes, self.latitudes = self.area_def.get_lonlats()

    def resample_to_area(self, target_area_def, resample_method=None):
        """
        Resample existing scene to the provided area definition

        """
        if resample_method not in ['nn', 'gaussian']:
            raise Exception('Resample method {} not known'.format(resample_method))

        attributes_list_to_pass = ['bands', 'timestamp']
        resampled_scene = GenericScene()
        resampled_scene.area_def = target_area_def
        copy_attributes(self, resampled_scene, attributes_list_to_pass)

        try:
            self.area_def = geometry.SwathDefinition(lons=self.longitudes, lats=self.latitudes)
        except:
            self.get_area_def()

        if resample_method is 'nn':
            neighbours = 1
        else:
            neighbours = 8

        valid_input_index, valid_output_index, index_array, distance_array = \
                kd_tree.get_neighbour_info(self.area_def, resampled_scene.area_def,
                                           resampled_scene.area_def.pixel_size_x*2.5, neighbours = neighbours, nprocs=1)

        bands_number = len(resampled_scene.bands)

        for i, band in enumerate(resampled_scene.bands.values()):

            print "Resampling band {0:d}/{1:d}".format(i+1, bands_number)
            swath_data = deepcopy(band.data)

            if resample_method == 'nn':
                band.data = kd_tree.get_sample_from_neighbour_info('nn', resampled_scene.area_def.shape,
                                                                   swath_data,
                                                                   valid_input_index,
                                                                   valid_output_index,
                                                                   index_array)

            elif resample_method == 'gaussian':

                radius_of_influence = resampled_scene.area_def.pixel_size_x * 2.5
                sigma = pr.utils.fwhm2sigma(radius_of_influence * 1.5)
                gauss = lambda r: numpy.exp(-r ** 2 / float(sigma) ** 2)

                band.data = kd_tree.get_sample_from_neighbour_info('custom', resampled_scene.area_def.shape,
                                                                    swath_data,
                                                                    valid_input_index,
                                                                    valid_output_index,
                                                                    index_array,
                                                                    distance_array=distance_array,
                                                                    weight_funcs=gauss,
                                                                    fill_value=0,
                                                                    with_uncert=False)

            else:
                raise Exception('Resampling method not known')
        return resampled_scene

    def save_geotiff(self, filepath, bands=None, cmap=None):
        """
        Export Scene in GeoTIFF format
        """

        # If we have a list of bands and it's smaller than the
        # original list, then exclude all of the bands we do not need
        bands_names = self.bands.keys()
        bands_dict = self.bands

        if bands is not None:
            for band_name in bands_names:
                if band_name not in bands:
                    bands_dict.pop(band_name)

        bands = bands_dict.values()

        self.export_path = filepath
        gtiff_driver = gdal.GetDriverByName('GTiff')
        gtiff_format = gdal.GDT_Byte
        bands_number = len(bands_dict)
        gtiff_options=["COMPRESS=LZW", "PREDICTOR=2", "TILED=YES"]
        gtiff_options = ["COMPRESS=DEFLATE", "PREDICTOR=2", "ZLEVEL=6", "INTERLEAVE=BAND"]
        gtiff_dataset = gtiff_driver.Create(self.export_path,
                                             int(self.area_def.x_size),
                                             int(self.area_def.y_size),
                                             bands_number,
                                             gtiff_format,
                                             gtiff_options)

        geometry_list = (self.area_def.area_extent[0],
                         self.area_def.pixel_size_x,
                         0,
                         self.area_def.area_extent[3],
                         0,
                         self.area_def.pixel_size_y * -1)

        gtiff_dataset.SetGeoTransform(geometry_list)
        srs = osr.SpatialReference()
        srs.ImportFromProj4(self.area_def.proj4_string.encode('ascii'))
        gtiff_dataset.SetProjection(srs.ExportToWkt())

        gtiff_colortable = None # by default we don't use any colortable 

        if cmap == 'istjenesten':

            # Gdal colortable
            gtiff_colortable=gdal.ColorTable()

            colors = { 'blue': (150, 200, 255), 
                    'green':   (140, 255, 160),
                    'yellow':  (255, 255, 0),
                    'orange':  (255, 127, 7),
                    'red':     (255, 0, 0) }

            cmap = istjenesten_colormap()
            for i in numpy.arange(0,255):
                gtiff_colortable.SetColorEntry(int(i), tuple(cmap[i].astype(numpy.int)))

        for i, band in enumerate(bands):
            raster_array = band.data.copy()
            gtiff_band = gtiff_dataset.GetRasterBand(i+1)
            if bands_number == 1: gtiff_band.SetColorTable(gtiff_colortable)
            gtiff_band.WriteArray(raster_array)

        gtiff_dataset = None


    def compose_rgb_image(self, rgb_list):
        """
        Save regular image with graphics
        """

        if rgb_list is not list:
            rgb_list = list(rgb_list)

        if len(rgb_list) is 1:
            rgb_list = [rgb_list[0],
                        rgb_list[0],
                        rgb_list[0]]


        red_band_name, green_band_name, blue_band_name = rgb_list

        red_band_array   = self.bands[red_band_name].data
        green_band_array = self.bands[green_band_name].data
        blue_band_array  = self.bands[blue_band_name].data

        rgb_array = numpy.dstack((red_band_array,
                                 green_band_array,
                                 blue_band_array)).astype(numpy.uint8)

        self.img = Image.fromarray(rgb_array)


    def save_rgb_image(self, output_filename, rgb_list):
        self.compose_rgb_image(rgb_list)
        self.img.save(output_filename)


def copy_attributes(object_from, object_to, attributes_list):
    for attribute_name in attributes_list:
        if hasattr(object_from, attribute_name):
            the_attribute = getattr(object_from, attribute_name)
            setattr(object_to, attribute_name, deepcopy(the_attribute))

def istjenesten_colormap():
    """
    """
    r = color((150, 140, 255, 255, 255, 255, 255), (0, 10, 30, 60,85, 99, 255))
    g = color((200, 255, 255, 125, 73, 0, 0), (0, 10, 30, 60,85, 99, 255))
    b = color((255, 160, 0, 7, 4, 0, 0), (0, 10, 30, 60, 85, 99, 255))
    return numpy.concatenate((r.reshape(255,1), g.reshape(255,1), b.reshape(255,1)), axis = 1)


def color(tie_points, intervals):
    ar = numpy.array([])
    for i in range(len(intervals)-1):
        tmp_ar = numpy.floor(numpy.linspace(tie_points[i], tie_points[i+1], intervals[i+1] - intervals[i], endpoint=False)).astype(numpy.int)
        ar = numpy.append(ar, tmp_ar)
    return ar
