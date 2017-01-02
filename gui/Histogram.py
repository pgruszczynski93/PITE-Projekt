from PIL import Image
from PIL import ImageDraw
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

class Histogram(object):
	def __init__(self, image):
		self.hist_height = 180
		self.hist_width = 256
		self.show_stoplines = True    
		self.count_stoplines = 5
		self.multipler_value = 4
		self.x_marker = self.hist_width/self.count_stoplines

		self.background_color = (51,51,51)  
		self.line_color = (102,102,102)       
		self.red = (255,0,0)               
		self.green = (51,204,51)           
		self.blue = (0,102,255)     
		
		self.image = image
		self.hist_img = None
		self.drawer = None

		self.hist = self.image.histogram()
		self.hist_max = max(self.hist)
		self.x_scale = float(self.hist_width)/len(self.hist)
		self.y_scale = float((self.hist_height)*self.multipler_value)/self.hist_max

	def create_histogram(self):
		self.hist_img = Image.new("RGBA",(self.hist_width, self.hist_height),self.background_color)
		self.drawer = ImageDraw.Draw(self.hist_img)

	def draw_histogram(self):
		if self.show_stoplines:
			self.draw_stoplines()	

		x = 0; c = 0;
		for i in self.hist:
			if int(i)==0: pass
			else:
				color = self.red
				if c>255: color = self.green
				if c>511: color = self.blue			
				self.drawer.line((x, self.hist_height, x, self.hist_height-(i*self.y_scale)), fill=color)
			if x>255: x=0
			else: x+=1
			c+=1				     

		# self.hist_img.save('histogram.png', 'PNG')
		# self.hist_img.show()

	def draw_stoplines(self):
		x = 0
		for i in range(1,self.count_stoplines+1):
			self.drawer.line((x,0,x,self.hist_height), fill = self.line_color)
			x+=self.x_marker

		self.drawer.line((self.hist_width-1, 0, self.hist_width-1, 200), fill = self.line_color)
		self.drawer.line((0,0,0,self.hist_height),fill = self.line_color)

	def get_hist_img(self):
		return self.hist_img