import unittest
from MainWindow import *


class tests(unittest.TestCase):
  
	def setUp(self):
		self.imgProcessor = ImagePreProcessor()

	def test_windows_creation(self):
		print("Sprawdzenie, czy poprawnie tworzy się okno główne programu i ustawione są właściwe parametry oraz wywołanie jego metod")
		app = QtGui.QApplication(sys.argv)
		MainWindow = QtGui.QMainWindow()
		ui = Ui_MainWindow()
		ui.setupUi(MainWindow)

		print("Sprawdzanie ImageWidget")
		image_widget = ImageWidget(QtGui.QWidget())
		QtGui.QWidget().paintEvent=ui.paint_clipping_frame
		print("Sprawdzenie czy obiekt jest instancją klasy ImageWidget")
		self.assertIsInstance(image_widget,ImageWidget)

		print("Sprawdzenie poprawności parametrów")
		self.assertEqual(ui.in_clipping_mode, False)
		self.assertEqual(ui.clipping_not_done, True)
		self.assertEqual(ui.border_rect, None)
		self.assertEqual(ui.clip_rect, None)
		self.assertEqual(ui.dragging, None)
		self.assertEqual(ui.drag_offset, QPoint())
		self.assertEqual(ui.handle_offsets, (QPoint(8, 8), QPoint(-1, 8), QPoint(8, -1), QPoint(-1, -1)))
		self.assertEqual(ui.clipping_pos, None)

		print("Sprawdzenie metody otwierającej obraz")
		ui.open_image("./gui/image.jpg")

		print("Sprawdzenie poprawnej konwersji JPG do QImage - klasa Histogram")
		self.imgProcessor.loadImage("./gui/image.jpg")
		modal_window = Modal()
		self.assertIsInstance(modal_window.pil2pixmap(self.imgProcessor.image), QtGui.QPixmap)

		print("Sprawdzanie glownej metody do przetwarzajacej obrazy - Process_Image")
		ui.process_image(self.imgProcessor.auto_filter, ui.pred_filters[1])
		ui.process_image(self.imgProcessor.image_adjustment, "negative", 0, None, None,None,None)

		print("Zamykanie aplikacji")
		ui.close_application()

		print("Sprawdzenie zmiany rozmiaru ramki kadrowania")
		ui.self_dragging = None
		ui.resize_clipping_frame(QtGui.QMouseEvent)
		ui.self_dragging = 0
		ui.resize_clipping_frame(QtGui.QMouseEvent)
		ui.self_dragging = 1
		ui.resize_clipping_frame(QtGui.QMouseEvent)
		ui.self_dragging = 2
		ui.resize_clipping_frame(QtGui.QMouseEvent)
		ui.self_dragging = 3
		ui.resize_clipping_frame(QtGui.QMouseEvent)

		print("Rogi kadrowania")
		ui.corner(0)
		ui.corner(1)
		ui.corner(2)
		ui.corner(3)

		print("Wejscie do trybu kadrowania")
		ui.clipping_mode()

		print("Sprawdzenie właściwego tworzenia się okien modalnych - klasa Modals")
		modal = Modal()
		modal.sliders.append(QSlider(Qt.Horizontal))
		modal.sliders.append(QSlider(Qt.Horizontal))
		modal.sliders.append(QSlider(Qt.Horizontal))
		modal.set_current_label_val(50, QLabel(),"test")
		print("Sprawdzenie ustawienia wartości zwracanej przez Modal")
		modal.set_modal_return_value(50)
		print("Srawdzenie poprawnej inicjalizacji sliderów")
		modal.set_sliders(modal.sliders, [50,50,50])
		print("Sprawdzenie przycisku Potwierdź modala")
		modal.button_confirm_exit()
		print("Sprawdzenie przycisku Anuluj modala")
		modal.button_cancel_exit()
		print("Sprawdzenie przycisku Potwierdź nie opartego na sygnałach")
		modal.button_nonsignal_confirm_exit()
		modal.textfields.append(QLineEdit())
		modal.textfields.append(QLineEdit())
		modal.textfields.append(QLineEdit())
		modal.comboboxes.append(QComboBox())
		modal.comboboxes.append(QComboBox())
		modal.text_tf.setText("test")
		modal.textfields[0].setText("2")
		modal.textfields[1].setText("3")
		modal.textfields[2].setText("4")
		modal.mask_size = 3
		modal.colorpicker_color = QtGui.QColor(244,232,124,255)
		modal.button_nonsignal_confirm_exit("unsharp")
		modal.button_nonsignal_confirm_exit("text")
		modal.button_nonsignal_confirm_exit("marker")
		print("Sprawdzenie wartosci glownego slidera")
		modal.main_slider_value = 50
		modal.current_value_label.setText("test")
		modal.set_modal_return_value(50)
		modal.get_mainslider_value("test")

		print("Modal")
		modal_window = Modal("Zmiana kontrastu","Kontrast: ")
		modal_window.init_modal([0,50],[0,50,1])
		modal_window.set_slider(modal_window.main_slider, 0,50,self.imgProcessor.contrast_mod_value,1)

		print("Histogram Drawer")
		modal_window = Modal()
		hist = Histogram(self.imgProcessor.image)
		hist.create_histogram()
		modal_window.init_histogram_drawer(hist.hist_img)

		print("Sprawdzenie ustawienia akutalnej etykiety (CURRENT_LABEL)")
		modal_window = Modal()

		print("Resize Modal")
		modal_window = Modal("Skalowanie i dopasowanie")
		modal_window.init_resize_modal(["Wysokość (pix)", "Szerokość (pix)"])

		print("Color Sampler")
		modal_window = Modal()
		modal_window.init_color_sampler((255, 255, 255))

		print("Text Modal")
		modal_window = Modal("Wprowadź tekst do wstawienia ")
		modal_window.init_text_modal()

		print("Unsharp Mask")
		modal_window = Modal("Maska wyostrzająca")
		modal_window.init_unsharp_mask()

		print("Ownmask")
		modal_window = Modal("Zdefiniuj maskę")
		modal_window.init_own_mask_modal(3)

		print("Markers Modal")
		modal_window = Modal("Wstawianie markera")
		modal_window.init_markers_modal()

		print("Message Box")
		modal_window = Modal()
		modal_window.msg_box("Testy","simulate")
		
	
	def test_init(self):
		print("Sprawdzenie, czy utworzony obiekt jest instancją klasy ImagePreProcessor")
		self.assertIsInstance(self.imgProcessor, ImagePreProcessor)

	def test_parameters(self):
		print("Sprawdzenie, czy domyślne parametry instancji klasy ImagePreProcessor są prawidłowe")
		self.assertEqual(self.imgProcessor.image, None)
		self.assertEqual(self.imgProcessor.pixels, None)
		self.assertEqual(self.imgProcessor.modal_window, None)
		self.assertEqual(self.imgProcessor.contrast_mod_value, 0)
		self.assertEqual(self.imgProcessor.posterize_mod_value, 0)
		self.assertEqual(self.imgProcessor.solarization_mod_value, 0)
		self.assertEqual(self.imgProcessor.crop_opsborder_mod_value, 0)
		self.assertEqual(self.imgProcessor.frame_color_width, 0)
		self.assertEqual(self.imgProcessor.resize_mod_dim, (300, 200))
		self.assertEqual(self.imgProcessor.rotate_mod_angle, 0)
		self.assertEqual(self.imgProcessor.brightness_mod_value, 100)
		self.assertEqual(self.imgProcessor.width, 0)
		self.assertEqual(self.imgProcessor.height, 0)
		self.assertEqual(self.imgProcessor.enhancer, None)
		self.assertEqual(self.imgProcessor.colbalance_mod_value, 100)
		self.assertEqual(self.imgProcessor.mouse_pos, (100,100))
		self.assertEqual(self.imgProcessor.input_text, "")
		self.assertEqual(self.imgProcessor.drawer, None)
		self.assertEqual(self.imgProcessor.font, None)
		self.assertEqual(self.imgProcessor.hist, None)
		self.assertEqual(self.imgProcessor.gaussian_radius, 0)
		self.assertEqual(self.imgProcessor.modalfilter_size, 3)
		self.assertEqual(self.imgProcessor.minfilter_size, 3)
		self.assertEqual(self.imgProcessor.maxfilter_size, 3)
		self.assertEqual(self.imgProcessor.medianfilter_size, 3)
		self.assertEqual(self.imgProcessor.rankfilter_size, 3)
		self.assertEqual(self.imgProcessor.unsharp_mod_values, (10, 20, 30))
		self.assertEqual(self.imgProcessor.kernel_vals, ())
		self.assertEqual(self.imgProcessor.treshold_value, 20)
		self.assertEqual(self.imgProcessor.saturation_mod_value, 0)
		self.assertEqual(self.imgProcessor.gamma_mod_value, 0)
		self.assertEqual(self.imgProcessor.color_mod_value, 0)
		self.assertEqual(self.imgProcessor.noise_mod_value, 50)
		self.assertEqual(self.imgProcessor.marker_mod_values, (100, 100, 10, 1, 1, 255, 255, 255))

		# for key in self.imgProcessor.ops_vals.keys():
			# self.assertEqual(key, self.imgProcessor.ops_vals[key])

	def test_imgpreproc_dicts(self):
		print("Sprawdzenie poprawności utworzenia słowników")
		self.assertTrue(self.imgProcessor.ops_vals) 
		self.assertTrue(self.imgProcessor.preproc_methods)
		print("Sprawdzenie czy nie wyrzuca KeyError")
		self.assertRaises(KeyError, lambda: self.imgProcessor.ops_vals['errorkey']) 

	def test_image_operations(self):
		print("Sprawdzenie funkcji wczytującej obraz wejściowy")
		self.imgProcessor.loadImage("./gui/image.jpg")
		print("Sprawdzenie działania progowania")
		self.imgProcessor.treshold()
		print("Sprawdzenie operacji nasycenia")
		self.imgProcessor.saturation_exec()
		self.imgProcessor.ops_vals["saturation"] = 200
		self.imgProcessor.saturation_exec()
		print("Sprawdzenie operacji korekcji gamma")
		self.imgProcessor.gamma_correction_exec()
		print("Sprawdzenie operacji zmiany koloru")
		self.imgProcessor.color_change_exec()
		print("Sprawdzenie operacji generowania szumu")
		self.imgProcessor.noise_generator_exec()
		print("Sprawdzenie operacji wstawiania markera")
		self.imgProcessor.put_marker_exec()
		self.imgProcessor.ops_vals["marker"] = (100, 100, 10, 2, 1, 255, 255, 255)
		self.imgProcessor.put_marker_exec()
		self.imgProcessor.ops_vals["marker"] = (100, 100, 10, 3, 1, 255, 255, 255)
		self.imgProcessor.put_marker_exec()
		self.imgProcessor.ops_vals["marker"] = (100, 100, 10, 1, 2, 255, 255, 255)
		self.imgProcessor.put_marker_exec()
		self.imgProcessor.ops_vals["marker"] = (100, 100, 10, 2, 2, 255, 255, 255)
		self.imgProcessor.put_marker_exec()
		self.imgProcessor.ops_vals["marker"] = (100, 100, 10, 3, 2, 255, 255, 255)
		self.imgProcessor.put_marker_exec()
		print("Sprawdzenie operacji tworzenia histogramu")
		self.imgProcessor.get_hist()
		print("Sprawdzenie operacji pobierania zdjecia histogramu")
		self.imgProcessor.hist.get_hist_img()
		print("Sprawdzenie operacji tworzenia negatywu")
		self.imgProcessor.negative()
		print("Sprawdzenie operacji zmiany kontrastu")
		self.imgProcessor.auto_contrast_exec()
		print("Sprawdzenie operacji konwersji do skali szarości")
		self.imgProcessor.auto_grayscale()
		print("Sprawdzenie operacji koloryzacji")
		self.imgProcessor.auto_colorize_exec((0,0,0), (255,255,255))
		print("Sprawdzenie operacji lustra")
		self.imgProcessor.auto_mirror()
		print("Sprawdzenie operacji przerzucania")
		self.imgProcessor.auto_flip()
		print("Sprawdzenie operacji posteryzacji")  #nic nie robi!!!
		self.imgProcessor.auto_posterize_exec()
		print("Sprawdzenie operacji solaryzacji")
		self.imgProcessor.auto_solarize_exec()
		print("Sprawdzenie operacji usunięcia obramowania")
		self.imgProcessor.auto_delete_border_exec()
		print("Sprawdzenie operacji normalizacji histogramu")
		self.imgProcessor.auto_equalize_histogram()
		print("Sprawdzenie operacji dodawania obramowania")
		self.imgProcessor.auto_add_color_border_exec(Qt.black)
		print("Sprawdzenie operacji skalowania")
		self.imgProcessor.auto_fitscale_exec()
		print("Sprawdzenie operacji rotacji")
		self.imgProcessor.auto_rotate_exec()
		print("Sprawdzenie operacji zmiany rozmiaru")
		self.imgProcessor.auto_resize_exec()
		print("Sprawdzenie operacji zmiany jasności")
		self.imgProcessor.auto_brightness_exec()
		print("Sprawdzenie działania filtrów automatycznych")
		self.imgProcessor.auto_filter(ImageFilter.BLUR)
		print("Sprawdzenie działania filtru Gaussa")
		self.imgProcessor.auto_gaussianblur_exec()
		print("Sprawdzenie działania maski wyostrzającej")
		self.imgProcessor.auto_unsharpmask_exec(True)
		print("Sprawdzenie działania filtru rankingowego")
		self.imgProcessor.auto_rankfilter_exec()
		print("Sprawdzenie działania filtru medianowego")
		self.imgProcessor.auto_medianfilter_exec()
		print("Sprawdzenie działania filtru minimalnego")
		self.imgProcessor.auto_minfilter_exec()
		print("Sprawdzenie działania filtru maksymalnego")
		self.imgProcessor.auto_maxfilter_exec()
		print("Sprawdzenie działania filtru modalnego")
		self.imgProcessor.auto_modefilter_exec()
		print("Sprawdzenie działania kadrowania")
		self.imgProcessor.auto_clipping((100, 100, 100, 100))
		print("Sprawdzenie operacji tworzenia nowego pliku")
		self.imgProcessor.auto_new_exec()
		print("Sprawdzenie zamknięcia zdjęcia")
		self.imgProcessor.image_close()
		print("Sprawdzenie ładowania zdjęcia do widgetu")
		self.imgProcessor.loadImageFromPIX("myfile.jpg")
		print("Sprawdzenie poprawności tworzenia okna modala na podstawie parametru")
		self.imgProcessor.image_adjustment("gamma",7)

		print("Sprawdzenie operacji zwykłego zapisu")
		self.imgProcessor.loadImage("./gui/image.jpg")
		self.imgProcessor.save_photo_normal()
		self.imgProcessor.image = None
		self.imgProcessor.save_photo_normal()

		print("Sprawdzenie operacji zapisz jako")
		self.imgProcessor.loadImage("./gui/image.jpg")
		self.imgProcessor.save_as("myfile.jpg")
		self.imgProcessor.image = None
		self.imgProcessor.save_as("myfile.jpg")

if __name__ == '__main__':
	unittest.main()
