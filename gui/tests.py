import unittest
from ImagePreProcessor import *

class tests(unittest.TestCase):
  
  def setUp(self):
    self.imgProcessor = ImagePreProcessor()
    
  def init_test(self):
    self.assertIsInstance(self.imgProcessor, ImagePreProcessor)
