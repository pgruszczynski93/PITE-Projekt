import PIL.ImageOps
import PIL.ImageDraw
import PIL.ImageFont
import math
import numpy
import datetime
import matplotlib
import random
from PIL import ImageFile
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter

from Modals import *
from Histogram import *

ImageFile.LOAD_TRUNCATED_IMAGES = True
class ImagePreProcessor(object):

	def __init__(self):
		self.image = None
		self.pixels = None
		self.modal_window = None
		self.contrast_mod_value = 0
		self.posterize_mod_value = 0
		self.solarization_mod_value = 0
		self.crop_opsborder_mod_value = 0
		self.frame_color_width = 0
		self.resize_mod_dim = (300, 200)
		self.rotate_mod_angle = 0
		self.brightness_mod_value = 100
		self.width = 0
		self.height = 0
		self.enhancer = None
		self.colbalance_mod_value = 100
		self.mouse_pos = (100, 100)
		self.input_text = ""
		self.drawer = None
		self.font = None
		self.hist = None
		self.gaussian_radius = 0
		self.modalfilter_size = 3
		self.minfilter_size = 3
		self.maxfilter_size = 3
		self.medianfilter_size = 3
		self.rankfilter_size = 3
		self.unsharp_mod_values = (10, 20, 30)
		self.kernel_vals = ()
		self.treshold_value = 20
		self.saturation_mod_value = 0
		self.gamma_mod_value = 0
		self.color_mod_value = 0
		self.noise_mod_value = 0
		self.marker_mod_values = (100, 100, 10, 1, 1, 255, 255, 255)
		self.save_message = ""

		self.ops_vals = {"contrast":self.contrast_mod_value,"posterize":self.posterize_mod_value,
		"solarization":self.solarization_mod_value,"cropborder":self.crop_opsborder_mod_value,
		"colorframewidth":self.frame_color_width,"rotate":self.rotate_mod_angle,"brightness":self.brightness_mod_value,
		"gauss":self.gaussian_radius,"modalfilter":self.modalfilter_size,"maxfilter":self.maxfilter_size,
		"medianfilter":self.medianfilter_size, "rankfilter":self.rankfilter_size,"treshold":self.treshold_value,
		"saturation":self.saturation_mod_value,"gamma":self.gamma_mod_value,"colormarker":self.color_mod_value,
		"noise":self.noise_mod_value,"fitscale":self.resize_mod_dim ,"resize":self.resize_mod_dim,"newfile":self.resize_mod_dim,"colorborder":self.frame_color_width,
		"minfilter":self.minfilter_size,"modefilter":self.modalfilter_size,
		"colorwheel":self.color_mod_value,"noisegen":self.noise_mod_value,"unsharp":self.unsharp_mod_values,"marker":self.marker_mod_values}

		self.preproc_methods = {"negative":self.negative,"contrast":self.auto_contrast_exec,"grayscale":self.auto_grayscale,
		"mirror":self.auto_mirror,"flip":self.auto_flip,"posterize":self.auto_posterize_exec,"solarization":self.auto_solarize_exec,
		"cropborder":self.auto_delete_border_exec,"equalize_hist":self.auto_equalize_histogram,"fitscale":self.auto_fitscale_exec,
		"rotate":self.auto_rotate_exec,"resize":self.auto_resize_exec,"newfile":self.auto_new_exec,
		"brightness":self.auto_brightness_exec,"gauss":self.auto_gaussianblur_exec,
		"colorize":self.auto_colorize_exec,"colorborder":self.auto_add_color_border_exec,
		"rankfilter":self.auto_rankfilter_exec,"medianfilter":self.auto_medianfilter_exec,"minfilter":self.auto_minfilter_exec,"maxfilter":self.auto_maxfilter_exec,
		"modefilter":self.auto_modefilter_exec,"treshold":self.treshold,"saturation":self.saturation_exec, "gamma":self.gamma_correction_exec,"colorwheel":self.color_change_exec,
		"noisegen":self.noise_generator_exec,"unsharp":self.auto_unsharpmask_exec,"marker":self.put_marker_exec}

	def image_close(self):
		self.image.close()

	def loadImage(self, imgFile, isGray=1):
		self.image = Image.open(imgFile)
		self.width, self.height = self.image.size
		self.pixels = self.image.load()

	def loadImageFromPIX(self, image):
		self.image = image

	def image_adjustment(self,operation, modal_state = None, title=None, window_opt=None,label_vals=None, slider_opts=None, test = None):
		if test == None:
			if modal_state==1:
				self.modal_window = Modal(title,window_opt)
				self.modal_window.init_modal(label_vals,slider_opts)
				self.modal_window.set_slider(self.modal_window.main_slider, slider_opts[0],slider_opts[1],self.ops_vals[operation],slider_opts[2])
				if self.modal_window.exec_():
					self.ops_vals[operation] = self.modal_window.button_confirm_exit()

			if modal_state==2:
				self.modal_window = Modal(title)
				self.modal_window.init_resize_modal(["Wysokość (pix)", "Szerokość (pix)"])
				if self.modal_window.exec_():
					self.ops_vals[operation] = self.modal_window.button_nonsignal_confirm_exit()

			if modal_state==3:
				self.modal_window = Modal()
				black = self.modal_window.init_color_picker()
				white = self.modal_window.init_color_picker()
				self.preproc_methods[operation](black, white)

			if modal_state==4:
				self.modal_window = Modal(title)
				if operation == "samplecolor" and (self.mouse_pos[0] <= self.width and self.mouse_pos[1] <= self.height):
					pix = self.image.getpixel((self.mouse_pos[0],self.mouse_pos[1]))
					self.modal_window.init_color_sampler(pix)
				elif operation == "histogram":
					self.get_hist()
					self.modal_window.init_histogram_drawer(self.hist.get_hist_img());
				self.modal_window.exec_()

			if modal_state == 5:
				value_changed = False
				self.modal_window = Modal(title)
				self.modal_window.init_unsharp_mask()
				self.modal_window.set_sliders(self.modal_window.sliders, self.unsharp_mod_values)
				if self.modal_window.exec_():
					self.unsharp_mod_values  = self.modal_window.button_confirm_exit()
					value_changed = True
					self.preproc_methods[operation](value_changed)

			if modal_state == 6:
				self.modal_window = Modal(title)
				self.modal_window.init_markers_modal()
				if self.modal_window.exec_():
					self.ops_vals["marker"] = self.modal_window.button_nonsignal_confirm_exit("marker")
				self.preproc_methods["marker"]()
			
			if modal_state == 7:
				pass

			if modal_state >= 0 and modal_state < 3:
				self.preproc_methods[operation]()

	def negative(self):
		self.image = PIL.ImageOps.invert(self.image)
		self.loadImageFromPIX(self.image)

	def auto_contrast_exec(self):
		self.image = PIL.ImageOps.autocontrast(self.image,int(self.ops_vals["contrast"]))
		self.loadImageFromPIX(self.image)

	def auto_grayscale(self):
		self.image = PIL.ImageOps.grayscale(self.image)
		self.loadImageFromPIX(self.image)

	def auto_colorize_exec(self, black, white):
		self.image = PIL.ImageOps.colorize(self.image, black, white)
		self.loadImageFromPIX(self.image)

	def auto_add_color_border_exec(self, test_mode=None):
		if test_mode == None:
			frame_color = self.modal_window.init_color_picker()
		else:
			frame_color = test_mode
		self.image = PIL.ImageOps.expand(self.image, self.ops_vals["colorborder"], frame_color)
		self.width, self.height = self.image.size
		self.loadImageFromPIX(self.image)

	def auto_mirror(self):
		self.image = PIL.ImageOps.mirror(self.image)
		self.loadImageFromPIX(self.image)

	def auto_flip(self):
		self.image = PIL.ImageOps.flip(self.image)
		self.loadImageFromPIX(self.image)

	def auto_posterize_exec(self):
		self.image = PIL.ImageOps.posterize(self.image, self.ops_vals["posterize"])
		self.loadImageFromPIX(self.image)

	def auto_solarize_exec(self):
		self.image = PIL.ImageOps.solarize(self.image, self.ops_vals["solarization"])
		self.loadImageFromPIX(self.image)

	def auto_delete_border_exec(self):
		self.image = PIL.ImageOps.crop(self.image, self.ops_vals["cropborder"])
		self.width, self.height = self.image.size
		self.loadImageFromPIX(self.image)
		
	def auto_equalize_histogram(self):
		self.image = PIL.ImageOps.equalize(self.image)
		self.loadImageFromPIX(self.image)

	def auto_fitscale_exec(self):
		self.image = PIL.ImageOps.fit(self.image, (int(self.ops_vals["fitscale"][0]), int(self.ops_vals["fitscale"][1])))
		self.width, self.height = self.image.size
		self.loadImageFromPIX(self.image)

	def auto_rotate_exec(self):
		self.width, self.height = (self.image.rotate(self.ops_vals["rotate"],0,1)).size
		self.loadImageFromPIX(self.image.rotate(self.ops_vals["rotate"],0,1))

	def auto_resize_exec(self):
		self.width, self.height = (self.image.resize((int(self.ops_vals["resize"][0]), int(self.ops_vals["resize"][1])))).size
		self.loadImageFromPIX(self.image.resize((int(self.ops_vals["resize"][0]), int(self.ops_vals["resize"][1]))))

	def auto_new_exec(self):
		self.image = Image.new("RGBA",(int(self.resize_mod_dim[0]), int(self.resize_mod_dim[1])),(255,255,255,255))
		self.width, self.height = self.image.size
		self.loadImageFromPIX(self.image)

	def auto_brightness_exec(self):
		self.enhancer = ImageEnhance.Brightness(self.image)			
		self.image = self.enhancer.enhance(self.ops_vals["brightness"]/100)
		self.loadImageFromPIX(self.image)

	def auto_filter(self, selected_filter):
		self.image = self.image.filter(selected_filter)
		self.loadImageFromPIX(self.image)

	def auto_gaussianblur_exec(self):
		self.image = self.image.filter(ImageFilter.GaussianBlur(self.ops_vals["gauss"]))
		self.loadImageFromPIX(self.image)

	def auto_unsharpmask_exec(self, value_changed):
		if value_changed:
			unsharp_img =self.image.filter(ImageFilter.UnsharpMask(self.unsharp_mod_values[0],self.unsharp_mod_values[1],self.unsharp_mod_values[2]))
			self.image = unsharp_img
			self.loadImageFromPIX(self.image)

	def auto_kernel(self,size):
		self.modal_window = Modal("Zdefiniuj maskę")
		self.modal_window.init_own_mask_modal(size)
		if self.modal_window.exec_():
			self.kernel_vals  = self.modal_window.button_nonsignal_confirm_exit("unsharp")
			kernel_img = self.image.filter(ImageFilter.Kernel(self.kernel_vals[0], self.kernel_vals[1]))
		self.image = kernel_img
		self.loadImageFromPIX(self.image)

	def auto_rankfilter_exec(self):
		self.image = self.image.filter(ImageFilter.RankFilter(self.ops_vals["rankfilter"],int(self.ops_vals["rankfilter"]*self.ops_vals["rankfilter"]/2)))
		self.loadImageFromPIX(self.image)

	def auto_medianfilter_exec(self):
		self.image = self.image.filter(ImageFilter.MedianFilter(self.ops_vals["medianfilter"]))
		self.loadImageFromPIX(self.image)

	def auto_minfilter_exec(self):
		self.image = self.image.filter(ImageFilter.MinFilter(self.ops_vals["minfilter"]))
		self.loadImageFromPIX(self.image)
		
	def auto_maxfilter_exec(self):
		self.image =  self.image.filter(ImageFilter.MaxFilter(self.ops_vals["maxfilter"]))
		self.loadImageFromPIX(self.image)

	def auto_modefilter_exec(self):
		modalfilter_img =self.image.filter(ImageFilter.ModeFilter(self.ops_vals["modefilter"]))
		self.image = modalfilter_img
		self.loadImageFromPIX(self.image)

	def treshold(self):
		value = self.ops_vals["treshold"]
		copy = self.image.copy()
		tup_value = (value,value,value)
		white = (255,255,255)
		black = (0,0,0)
		for w in range(self.width):
			for h in range(self.height):
				color = self.image.getpixel((w,h))
				red, green, blue = color
				red_lim, green_lim, blue_lim = tup_value
				if((red>red_lim) and (green>green_lim) and (blue>blue_lim)):
					copy.putpixel((w,h),white)
				else:
					copy.putpixel((w,h),black)
		self.image = copy
		self.loadImageFromPIX(self.image)

	def saturation_exec(self):
		in_data = numpy.asarray(self.image, dtype=numpy.uint8)
		in_data = in_data/255.
		hsv = matplotlib.colors.rgb_to_hsv(in_data)
		hsv[:,:,1] = hsv[:,:,1] - 1.0 + (self.ops_vals["saturation"]/100.)
		for y in range(self.height):
			for x in range(self.width):
				if hsv[y,x,1] < 0:
					hsv[y,x,1] = 0.0
				elif hsv[y,x,1] > 1:
					hsv[y,x,1] = 1.0
		rgb = matplotlib.colors.hsv_to_rgb(hsv)
		rgb = rgb*255.9999
		rgb = numpy.uint8(rgb)
		self.image = Image.fromarray(rgb)
		self.loadImageFromPIX(self.image)

	def gamma_correction_exec(self):
		in_data = numpy.asarray(self.image, dtype=numpy.uint8)
		in_data = in_data/255.
		in_data = in_data ** (self.ops_vals["gamma"]/100)
		in_data = in_data*255.9999
		in_data = numpy.uint8(in_data)
		self.image = Image.fromarray(in_data)
		self.loadImageFromPIX(self.image)
 
	def color_change_exec(self):
		in_data = numpy.asarray(self.image, dtype=numpy.uint8)
		in_data = in_data/255.
		hsv = matplotlib.colors.rgb_to_hsv(in_data)
		hsv[:,:,0] = hsv[:,:,0] + (self.ops_vals["colorwheel"]/360.)
		hsv[:,:,0] = ((hsv[:,:,0]*100) % 100) /100. 
		rgb = matplotlib.colors.hsv_to_rgb(hsv)
		rgb = rgb*255.9999
		rgb = numpy.uint8(rgb)
		self.image = Image.fromarray(rgb)
		self.loadImageFromPIX(self.image)

	def noise_generator_exec(self):
		in_data = numpy.asarray(self.image, dtype=numpy.uint8)
		in_data = in_data/255.
		for y in range(self.height):
			for x in range(self.width):
				if random.randint(0, 100) < self.ops_vals["noisegen"]:
					if random.randint(0,1) == 0:
						in_data[y,x,0] = 0.0
						in_data[y,x,1] = 0.0
						in_data[y,x,2] = 0.0
					else:
						in_data[y,x,0] = 1.0
						in_data[y,x,1] = 1.0
						in_data[y,x,2] = 1.0
		in_data = in_data*255.9999
		in_data = numpy.uint8(in_data)
		self.image = Image.fromarray(in_data)
		self.loadImageFromPIX(self.image)

	def get_hist(self):
		self.hist = Histogram(self.image)
		self.hist.create_histogram()
		self.hist.draw_histogram()

	def show_histogram(self):
		self.get_hist()
		self.modal_window = Modal("Histogram")
		self.modal_window.init_histogram_drawer(self.hist.get_hist_img());
		self.modal_window.exec_()

	def __in_marker_square(self, img, size, pos_width, pos_height, red, green, blue):
		for y in range(self.height):
			for x in range(self.width):
				if (abs(pos_width - x) < size) and \
				(abs(pos_height - y) < size):
					img[y,x,0] = red/255.
					img[y,x,1] = green/255.
					img[y,x,2] = blue/255.
		return img
					
	def __out_marker_square(self, img, size, pos_width, pos_height, red, green, blue):
		for y in range(self.height):
			for x in range(self.width):
				if (abs(pos_width - x) > size) or \
				(abs(pos_height - y) > size):
					img[y,x,0] = red/255.
					img[y,x,1] = green/255.
					img[y,x,2] = blue/255.
		return img
					
	def __in_marker_round(self, img, size, pos_width, pos_height, red, green, blue):
		for y in range(self.height):
			for x in range(self.width):
				if ((((x-pos_width)*(x-pos_width)) + ((y-pos_height)*(y-pos_height))) < (size*size)):
					img[y,x,0] = red/255.
					img[y,x,1] = green/255.
					img[y,x,2] = blue/255.
		return img
					
	def __out_marker_round(self, img, size, pos_width, pos_height, red, green, blue):
		for y in range(self.height):
			for x in range(self.width):
				if ((((x-pos_width)*(x-pos_width)) + ((y-pos_height)*(y-pos_height))) > (size*size)):
					img[y,x,0] = red/255.
					img[y,x,1] = green/255.
					img[y,x,2] = blue/255.
		return img
					
	def __in_marker_cross(self, img, size, pos_width, pos_height, red, green, blue):
		for y in range(self.height):
			for x in range(self.width):
				if ((abs(pos_width - x) < (size/3)) and \
				(abs(pos_height - y) < size)) or\
				((abs(pos_width - x) < size) and \
				(abs(pos_height - y) < (size/3))):
					img[y,x,0] = red/255.
					img[y,x,1] = green/255.
					img[y,x,2] = blue/255.
		return img
					
	def __out_marker_cross(self, img, size, pos_width, pos_height, red, green, blue):
		for y in range(self.height):
			for x in range(self.width):
				if ((abs(pos_width - x) > (size/3)) or \
				(abs(pos_height - y) > size)) and\
				((abs(pos_width - x) > size) or \
				(abs(pos_height - y) > (size/3))):
					img[y,x,0] = red/255.
					img[y,x,1] = green/255.
					img[y,x,2] = blue/255.
		return img

	def put_marker_exec(self):
		pos_width = int(self.ops_vals["marker"][0])
		pos_height = int(self.ops_vals["marker"][1])
		size = int(self.ops_vals["marker"][2])
		shape = int(self.ops_vals["marker"][3])
		kind = int(self.ops_vals["marker"][4])
		red = int(self.ops_vals["marker"][5])
		green = int(self.ops_vals["marker"][6])
		blue = int(self.ops_vals["marker"][7])
		in_data = numpy.asarray(self.image, dtype=numpy.uint8)
		in_data = in_data/255.
		if (pos_width - size < 0) or \
		(pos_width + size > self.width) or \
		(pos_height - size) < 0 or \
		(pos_height + size > self.height):
			self.modal_window.msg_box("Niewłaściwa pozycja markera bądź jego rozmiar.")
		else:
			if shape == 1:
				if kind == 1:
					in_data = self.__in_marker_square(in_data, size, pos_width, pos_height, red, green, blue)
				elif kind == 2:
					in_data = self.__out_marker_square(in_data, size, pos_width, pos_height, red, green, blue)
			elif shape == 2:
				if kind == 1:
					in_data = self.__in_marker_round(in_data, size, pos_width, pos_height, red, green, blue)
				elif kind == 2:
					in_data = self.__out_marker_round(in_data, size, pos_width, pos_height, red, green, blue)
			elif shape == 3:
				if kind == 1:
					in_data = self.__in_marker_cross(in_data, size, pos_width, pos_height, red, green, blue)
				elif kind == 2:
					in_data = self.__out_marker_cross(in_data, size, pos_width, pos_height, red, green, blue)

			in_data = in_data*255.9999
			in_data = numpy.uint8(in_data)
			self.image = Image.fromarray(in_data)
			self.loadImageFromPIX(self.image)

	def auto_clipping(self, clip_pos):
		cropped_img = self.image.crop(tuple(clip_pos))
		self.width, self.size = cropped_img.size
		self.image = cropped_img
		self.loadImageFromPIX(self.image)

	def save_photo_normal(self):
		if self.image:
			self.image.save(str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S"))+".jpg")
			self.save_message = "Zapisano pomyślnie w katalogu z programem"
		else:
			self.save_message = "Bład zapisu zdjęcia."

	def save_as(self, filepath):
		if self.image:
			self.image.save(filepath)
		else:
			self.save_message = "Bład zapisu zdjęcia."
