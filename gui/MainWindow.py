from PyQt4 import QtCore, QtGui
from ImageWidget import *
from ImagePreProcessor import *
from PIL import ImageQt
import sys
from PIL import ImageFilter

class Ui_MainWindow(QtGui.QWidget):

	def __init__(self):
		super(Ui_MainWindow, self).__init__()
		self.imgPreProc = ImagePreProcessor()
		self.selected_filter = 0
		self.pred_filters = [
		ImageFilter.BLUR,ImageFilter.CONTOUR,ImageFilter.DETAIL,
		ImageFilter.EDGE_ENHANCE,ImageFilter.EDGE_ENHANCE_MORE,ImageFilter.EMBOSS,
		ImageFilter.FIND_EDGES,ImageFilter.SMOOTH,ImageFilter.SMOOTH_MORE, ImageFilter.SHARPEN]

		self.in_clipping_mode = False
		self.clipping_not_done = True
		self.border_rect = None
		self.clip_rect = None
		self.dragging = None
		self.drag_offset = QPoint()
		self.handle_offsets = (QPoint(8, 8), QPoint(-1, 8), QPoint(8, -1), QPoint(-1, -1))
		self.clipping_pos = None
		self.last_clipping_pos = [0,0,0,0]

	def setupUi(self, MainWindow):

		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1024, 645)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.centralwidget.setObjectName("centralwidget")

		self.gridLayout = QtGui.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName("gridLayout")
		# zdjecie w ramce
		self.frame = QtGui.QFrame(self.centralwidget)
		self.frame.setGeometry(QtCore.QRect(50, 0, 800, 600))
		self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtGui.QFrame.Raised)
		self.frame.setObjectName("frame")

		self.gridLayout_2 = QtGui.QGridLayout(self.frame)
		self.gridLayout_2.setObjectName("gridLayout_2")

		self.scrollArea = QtGui.QScrollArea(self.frame)
		self.scrollArea.setGeometry(QtCore.QRect(0, 0, 800, 600))
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName("scrollArea")

		self.scrollAreaWidgetContents = QtGui.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 800, 600))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

		self.gridLayout_3 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
		self.gridLayout_3.setObjectName("gridLayout_3")

		self.org_image = ImageWidget(self.scrollAreaWidgetContents)
		self.org_image.setObjectName("org_image")
		self.gridLayout_3.addWidget(self.org_image,0,0,1,1)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)

		self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

		self.scrollArea.setWidget(self.scrollAreaWidgetContents)

		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
		self.menubar.setObjectName("menubar")
		self.menuPlik = QtGui.QMenu(self.menubar)
		self.menuPlik.setObjectName("menuPlik")
		self.menuFilters = QtGui.QMenu(self.menubar)
		self.menuFilters.setObjectName("menuFilters")
		self.menuSzum = QtGui.QMenu(self.menuFilters)
		self.menuSzum.setObjectName("menuSzum")
		self.menuKernel = QtGui.QMenu(self.menuFilters)
		self.menuKernel.setObjectName("menuKernel")
		self.menuBluring = QtGui.QMenu(self.menuFilters)
		self.menuSharpening = QtGui.QMenu(self.menuFilters)
		self.menuSharpening.setObjectName("menuSharpening")
		self.menuBluring.setObjectName("menuBluring")
		self.menuSmoothing = QtGui.QMenu(self.menuFilters)
		self.menuSmoothing.setObjectName("menuSmoothing")
		self.menuEdgeDetection = QtGui.QMenu(self.menuFilters)
		self.menuEdgeDetection.setObjectName("menuEdgeDetection")
		self.menuInne = QtGui.QMenu(self.menuFilters)
		self.menuInne.setObjectName("menuInne")
		self.menuTransformacja = QtGui.QMenu(self.menubar)
		self.menuTransformacja.setObjectName("menuTransformacja")
		self.menuDopasowania = QtGui.QMenu(self.menubar)
		self.menuDopasowania.setObjectName("menuDopasowania")
		self.menuHistogram = QtGui.QMenu(self.menuDopasowania)
		self.menuHistogram.setObjectName("menuHistogram")
		self.menuWstawianie = QtGui.QMenu(self.menubar)
		self.menuWstawianie.setObjectName("menuWstawianie")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.actionOpen = QtGui.QAction(MainWindow)
		self.actionOpen.setObjectName("actionOpen")
		self.actionOpen.setShortcut('Ctrl+O');
		self.actionOpen.triggered.connect(self.show_open_dialog)

		self.actionQuit = QtGui.QAction(MainWindow)
		self.actionQuit.setObjectName("actionQuit")
		self.actionQuit.setShortcut('Ctrl+Q')
		self.actionQuit.triggered.connect(self.close_application)

		self.actionNew = QtGui.QAction(MainWindow)
		self.actionNew.setObjectName("actionNew")
		self.actionNew.setShortcut('Ctrl+N')
		self.actionNew.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "newfile", 2, "Wymiary nowego pliku", None, None, None))

		self.actionSharpen = QtGui.QAction(MainWindow)
		self.actionSharpen.setObjectName("actionSharpen")
		self.actionSharpen.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[9]))

		self.actionBluring = QtGui.QAction(MainWindow)
		self.actionBluring.setObjectName("actionBluring")
		self.actionBluring.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[0]))

		self.actionContour = QtGui.QAction(MainWindow)
		self.actionContour.setObjectName("actionContour")
		self.actionContour.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[1]))

		self.actionDetail = QtGui.QAction(MainWindow)
		self.actionDetail.setObjectName("actionContour")
		self.actionDetail.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[2]))

		self.actionEdgeEnhance = QtGui.QAction(MainWindow)
		self.actionEdgeEnhance.setObjectName("actionEdgeEnhance")
		self.actionEdgeEnhance.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[3]))

		self.actionEdgeEnhanceMore = QtGui.QAction(MainWindow)
		self.actionEdgeEnhanceMore.setObjectName("actionEdgeEnhanceMore")
		self.actionEdgeEnhanceMore.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[4]))

		self.actionFindEdges = QtGui.QAction(MainWindow)
		self.actionFindEdges.setObjectName("actionEdgeEnhanceMore")
		self.actionFindEdges.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[6]))

		self.actionEmboss = QtGui.QAction(MainWindow)
		self.actionEmboss.setObjectName("actionEmboss")
		self.actionEmboss.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[5]))

		self.actionSmooth = QtGui.QAction(MainWindow)
		self.actionSmooth.setObjectName("actionSmooth")
		self.actionSmooth.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[7]))

		self.actionSmoothMore = QtGui.QAction(MainWindow)
		self.actionSmoothMore.setObjectName("actionSmoothMore")
		self.actionSmoothMore.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_filter, self.pred_filters[8]))

		self.actionGaussianBlur = QtGui.QAction(MainWindow)
		self.actionGaussianBlur.setObjectName("actionGaussianBlur")
		self.actionGaussianBlur.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "gauss", 1, "Rozmycie Gaussa", "Promień rozmycia: ", [0,10],[0,10,1]))

		self.actionUnsharpMask = QtGui.QAction(MainWindow)
		self.actionUnsharpMask.setObjectName("actionUnsharpMask")
		self.actionUnsharpMask.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "unsharp", 5, "Maska wyostrzająca", None, None, None))

		self.actionMask3 = QtGui.QAction(MainWindow)
		self.actionMask3.setObjectName("actionMask3")
		self.actionMask3.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_kernel,3 ))

		self.actionMask5 = QtGui.QAction(MainWindow)
		self.actionMask5.setObjectName("actionMask5")
		self.actionMask5.triggered.connect(lambda: self.process_image(self.imgPreProc.auto_kernel, 5))

		self.actionRankFilter = QtGui.QAction(MainWindow)
		self.actionRankFilter.setObjectName("actionRankFilter")
		self.actionRankFilter.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "rankfilter", 1, "Filtr rankingowy","Rozmiar rozmycia: ", [1,15],[1,15,2]))

		self.actionMedianFilter = QtGui.QAction(MainWindow)
		self.actionMedianFilter.setObjectName("actionMedianFilter")
		self.actionMedianFilter.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "medianfilter", 1, "Filtr medianowy","Rozmiar rozmycia: ", [1,15],[1,15,2]))

		self.actionMinFilter = QtGui.QAction(MainWindow)
		self.actionMinFilter.setObjectName("actionMinFilter")
		self.actionMinFilter.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "minfilter", 1, "Filtr minimalny","Rozmiar rozmycia: ", [1,15],[1,15,2]))

		self.actionMaxFilter = QtGui.QAction(MainWindow)
		self.actionMaxFilter.setObjectName("actionMaxFilter")
		self.actionMaxFilter.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "maxfilter", 1, "Filtr maksymalny","Rozmiar rozmycia: ", [1,15],[1,15,2]))
		
		self.actionModeFilter = QtGui.QAction(MainWindow)
		self.actionModeFilter.setObjectName("actionModeFilter")
		self.actionModeFilter.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "modefilter", 1, "Filtr modalny","Rozmiar rozmycia: ", [0,10],[0,10,1]))

		self.actionDeleteNoise = QtGui.QAction(MainWindow)
		self.actionDeleteNoise.setObjectName("actionDeleteNoise")
		self.actionDeleteNoise.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "medianfilter", 1, "Filtr medianowy","Rozmiar rozmycia: ", [1,15],[1,15,2]))

		self.actionNoise = QtGui.QAction(MainWindow)
		self.actionNoise.setObjectName("actionNoise")
		self.actionNoise.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "noisegen", 1, "Pieprz i sol", "Zaszumienie (%): ", [0,100],[0,100,1]))
		
		self.actionEdgeDetection = QtGui.QAction(MainWindow)
		self.actionEdgeDetection.setObjectName("actionEdgeDetection")

		self.actionRotate = QtGui.QAction(MainWindow)
		self.actionRotate.setObjectName("actionRotate")
		self.actionRotate.setShortcut('Alt+R')
		self.actionRotate.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "rotate", 1, "Rotacja", "Kąt obrotu: ", [0,360],[0,360,1]))

		self.actionFitScale= QtGui.QAction(MainWindow)
		self.actionFitScale.setObjectName("actionFitScale")
		self.actionFitScale.setShortcut('Ctrl+Alt+F')
		self.actionFitScale.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "fitscale", 2, "Skalowanie i dopasowanie", None, None, None))

		self.actionResize= QtGui.QAction(MainWindow)
		self.actionResize.setObjectName("actionFitScale")
		self.actionResize.setShortcut('Ctrl+Alt+I')
		self.actionResize.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "resize", 2, "Zmiana rozmiaru", None, None, None))

		self.actionClipping = QtGui.QAction(MainWindow)
		self.actionClipping.setObjectName("actionClipping")
		self.actionClipping.setShortcut('C')
		self.actionClipping.triggered.connect(self.clipping_mode)

		self.actionBrightness = QtGui.QAction(MainWindow)
		self.actionBrightness.setObjectName("actionBrightness")
		self.actionBrightness.setShortcut('Alt+B')
		self.actionBrightness.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "brightness", 1, "Zmiana jasności", "Jasność (%): ", [0,200],[0,200,1]))

		self.actionColorWheel = QtGui.QAction(MainWindow) 
		self.actionColorWheel.setObjectName("actionColorWheel")
		self.actionColorWheel.setShortcut('Shift+Alt+C')
		self.actionColorWheel.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "colorwheel", 1, "Koło barw", "Zmiana koloru (%): ", [0,360],[0,360,1]))

		self.actionAutoContrast = QtGui.QAction(MainWindow)
		self.actionAutoContrast.setObjectName("actionAutoContrast")
		self.actionAutoContrast.setShortcut('Shift+Ctrl+Alt+L')
		self.actionAutoContrast.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "contrast", 1, "Zmiana kontrastu", "Kontrast: ", [0,50],[0,50,1]))

		self.actionSaturation = QtGui.QAction(MainWindow)
		self.actionSaturation.setObjectName("actionSaturation")
		self.actionSaturation.setShortcut('Ctrl+Alt+S')
		self.actionSaturation.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "saturation", 1, "Nasycenie","Stopień nasycenia (%): ", [0,200],[0,200,1]))

		self.actionGamma = QtGui.QAction(MainWindow)
		self.actionGamma.setObjectName("actionGamma")
		self.actionGamma.setShortcut('Alt+G')
		self.actionGamma.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "gamma", 1, "Korekcja Gamma", "Wartość wspołczynnika: ", [1,799],[1,799,1]))

		self.actionGrayScale = QtGui.QAction(MainWindow)
		self.actionGrayScale.setObjectName("actionGrayScale")
		self.actionGrayScale.setShortcut("Ctrl+Alt+S")
		self.actionGrayScale.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "grayscale", 0, None, None, None,None))

		self.actionColorize = QtGui.QAction(MainWindow)
		self.actionColorize.setObjectName("actionColorize")
		self.actionColorize.setShortcut("Ctrl+Alt+K")
		self.actionColorize.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "colorize", 3, None, None, None,None))

		self.actionInverseColors = QtGui.QAction(MainWindow)
		self.actionInverseColors.setObjectName("actionInverseColors")
		self.actionInverseColors.setShortcut('Alt+I')
		self.actionInverseColors.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "negative", 0, None, None, None,None))

		self.actionMirrorEffect = QtGui.QAction(MainWindow)
		self.actionMirrorEffect.setObjectName("actionMirrorEffect")
		self.actionMirrorEffect.setShortcut('Alt+L')
		self.actionMirrorEffect.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "mirror", 0, None, None, None,None))

		self.actionFlip = QtGui.QAction(MainWindow)
		self.actionFlip.setObjectName("actionFlip")
		self.actionFlip.setShortcut('Alt+F')
		self.actionFlip.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "flip", 0, None, None, None,None))

		self.actionPosterize = QtGui.QAction(MainWindow)
		self.actionPosterize.setObjectName("actionPosterize")
		self.actionPosterize.setShortcut('Alt+P')
		self.actionPosterize.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "posterize", 1, "Posteryzacja", "Bity kanałów: ", [1,8],[1,8,1]))

		self.actionSolarize = QtGui.QAction(MainWindow)
		self.actionSolarize.setObjectName("actionSolarize")
		self.actionSolarize.setShortcut('Alt+S')
		self.actionSolarize.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "solarization", 1, "Solaryzacja", "Próg solaryzacji: ", [0,128],[0,128,1]))

		self.actionDeleteBorder = QtGui.QAction(MainWindow)
		self.actionDeleteBorder.setObjectName("actionDeleteBorder")
		self.actionDeleteBorder.setShortcut('Ctrl+Alt+B')
		self.actionDeleteBorder.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "cropborder", 1, "Usuwanie ramki zdjęcia", "Piksele do usunięcia: ", [0,200],[0,200,1]))

		self.actionTreshold = QtGui.QAction(MainWindow)
		self.actionTreshold.setObjectName("actionTreshold")
		self.actionTreshold.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "treshold", 1, "Progowanie", "Próg: ", [0,255],[0,255,1]))

		self.actionShowHistogram = QtGui.QAction(MainWindow)
		self.actionShowHistogram.setObjectName("actionShowHistogram")
		self.actionShowHistogram.setShortcut('Shift+H')
		self.actionShowHistogram.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "histogram", 4, "Histogram ", None, None, None))

		self.actionEqualizeHistogram = QtGui.QAction(MainWindow)
		self.actionEqualizeHistogram.setObjectName("actionEqualizeHistogram")
		self.actionEqualizeHistogram.setShortcut('Ctrl+Alt+H')
		self.actionEqualizeHistogram.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "equalize_hist", 0, None, None, None,None))

		self.actionAddFrame = QtGui.QAction(MainWindow)
		self.actionAddFrame.setObjectName("actionAddFrame")
		self.actionAddFrame.setShortcut('Alt+F')
		self.actionAddFrame.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "colorborder", 1, "Kolorowa ramka zdjęcia", "Grubość ramki: ",[0,200],[0,200,1]))

		self.actionMarker = QtGui.QAction(MainWindow)
		self.actionMarker.setObjectName("actionMarker")
		self.actionMarker.setShortcut('Alt+M')
		self.actionMarker.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "marker", 6, "Wstawianie markera", None, None, None))

		self.actionSampleColor = QtGui.QAction(MainWindow)
		self.actionSampleColor.setObjectName("actionSampleColor")
		self.actionSampleColor.setShortcut('Alt+Q')
		self.actionSampleColor.triggered.connect(lambda: self.process_image(self.imgPreProc.image_adjustment, "samplecolor", 4, "Wartość koloru w RGB ", None, None, None))

		self.actionSave = QtGui.QAction(MainWindow)
		self.actionSave.setObjectName("actionSave")
		self.actionSave.setShortcut('Ctrl+S')
		self.actionSave.triggered.connect(self.save_img)
		
		self.actionSaveAs = QtGui.QAction(MainWindow)
		self.actionSaveAs.setObjectName("actionSaveAs")
		self.actionSaveAs.setShortcut('Ctrl+Shift+S')
		self.actionSaveAs.triggered.connect(self.show_save_as_dialog)

		self.menuPlik.addAction(self.actionNew)
		self.menuPlik.addAction(self.actionOpen)
		self.menuPlik.addAction(self.actionSave)
		self.menuPlik.addAction(self.actionSaveAs)
		self.menuPlik.addAction(self.actionQuit)
		self.menuSzum.addAction(self.actionDeleteNoise)
		self.menuSzum.addAction(self.actionNoise)
		self.menuInne.addAction(self.actionTreshold)
		self.menuSharpening.addAction(self.actionSharpen)
		self.menuFilters.addAction(self.menuSharpening.menuAction())
		self.menuFilters.addAction(self.menuBluring.menuAction())
		self.menuFilters.addAction(self.menuEdgeDetection.menuAction())
		self.menuFilters.addAction(self.menuSmoothing.menuAction())
		self.menuEdgeDetection.addAction(self.actionContour)
		self.menuEdgeDetection.addAction(self.actionDetail)
		self.menuEdgeDetection.addAction(self.actionEdgeEnhance)
		self.menuEdgeDetection.addAction(self.actionEdgeEnhanceMore)
		self.menuEdgeDetection.addAction(self.actionFindEdges)
		self.menuEdgeDetection.addAction(self.actionEmboss)
		self.menuSmoothing.addAction(self.actionSmooth)
		self.menuSmoothing.addAction(self.actionSmoothMore)
		self.menuBluring.addAction(self.actionBluring)
		self.menuBluring.addAction(self.actionGaussianBlur)
		self.menuSharpening.addAction(self.actionUnsharpMask)
		self.menuBluring.addAction(self.actionRankFilter)
		self.menuBluring.addAction(self.actionMedianFilter)
		self.menuBluring.addAction(self.actionMinFilter)
		self.menuBluring.addAction(self.actionMaxFilter)
		self.menuBluring.addAction(self.actionModeFilter)
		self.menuFilters.addAction(self.menuSzum.menuAction())
		self.menuFilters.addAction(self.menuInne.menuAction())
		self.menuFilters.addAction(self.menuKernel.menuAction())
		self.menuKernel.addAction(self.actionMask3)
		self.menuKernel.addAction(self.actionMask5)
		self.menuTransformacja.addAction(self.actionRotate)
		self.menuTransformacja.addAction(self.actionFitScale)
		self.menuTransformacja.addAction(self.actionResize)
		self.menuTransformacja.addAction(self.actionClipping)
		self.menuTransformacja.addAction(self.actionDeleteBorder)
		self.menuTransformacja.addAction(self.actionAddFrame)
		self.menuHistogram.addAction(self.actionShowHistogram)
		self.menuHistogram.addAction(self.actionEqualizeHistogram)
		self.menuDopasowania.addAction(self.actionBrightness)
		self.menuDopasowania.addAction(self.actionColorWheel)
		self.menuDopasowania.addAction(self.actionAutoContrast)
		self.menuDopasowania.addAction(self.actionSaturation)
		self.menuDopasowania.addAction(self.actionGamma)
		self.menuDopasowania.addAction(self.actionInverseColors)
		self.menuDopasowania.addAction(self.actionGrayScale)
		self.menuDopasowania.addAction(self.actionFlip)
		self.menuDopasowania.addAction(self.actionMirrorEffect)
		self.menuDopasowania.addAction(self.actionPosterize)
		self.menuDopasowania.addAction(self.actionSolarize)
		self.menuDopasowania.addAction(self.menuHistogram.menuAction())
		self.menuDopasowania.addAction(self.actionColorize)
		self.menuDopasowania.addAction(self.actionSampleColor)
		self.menuWstawianie.addAction(self.actionMarker)
		self.menubar.addAction(self.menuPlik.menuAction())
		self.menubar.addAction(self.menuFilters.menuAction())
		self.menubar.addAction(self.menuTransformacja.menuAction())
		self.menubar.addAction(self.menuDopasowania.menuAction())
		self.menubar.addAction(self.menuWstawianie.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle("PITE - Project")
		self.menuPlik.setTitle("Plik")
		self.menuFilters.setTitle("Filtr")
		self.menuSzum.setTitle("Szum")
		self.menuKernel.setTitle("Własny filtr splotowy")
		self.menuInne.setTitle("Inne")
		self.menuTransformacja.setTitle("Transformacja")
		self.menuDopasowania.setTitle("Dopasowania")
		self.menuHistogram.setTitle("Histogram")
		self.menuWstawianie.setTitle("Wstawianie")
		self.actionOpen.setText("Otwórz...")
		self.actionQuit.setText("Zakończ")
		self.actionNew.setText("Nowy")
		self.actionSharpen.setText("Wyostrzanie")
		self.actionBluring.setText("Zwykłe rozmywanie")
		self.actionDeleteNoise.setText("Usuwanie szumu i ziarna")
		self.actionNoise.setText("Zaszumianie")
		self.menuEdgeDetection.setTitle("Filtry krawędziowe")
		self.menuSmoothing.setTitle("Wygładzanie")
		self.menuBluring.setTitle("Rozmycie")
		self.menuSharpening.setTitle("Wyostrzanie")
		self.actionRotate.setText("Obrót")
		self.actionFitScale.setText("Skaluj i dopasuj")
		self.actionResize.setText("Zmiana rozmiaru")
		self.actionClipping.setText("Kadrowanie")
		self.actionBrightness.setText("Jasność")
		self.actionColorWheel.setText("Zmiana koloru (HSV)")
		self.actionAutoContrast.setText("Kontrast")
		self.actionSaturation.setText("Nasycenie")
		self.actionFlip.setText("Przerzuć")
		self.actionGamma.setText("Gamma")
		self.actionInverseColors.setText("Odwróć kolory")
		self.actionGrayScale.setText("Skala Szarości")
		self.actionMirrorEffect.setText("Lustro")
		self.actionColorize.setText("Koloryzacja")
		self.actionPosterize.setText("Posteryzacja")
		self.actionDeleteBorder.setText("Usuń brzeg zdjęcia")
		self.actionContour.setText("Kontury")
		self.actionDetail.setText("Ekstrakcja detali")
		self.actionEdgeEnhance.setText("Wzmocnienie krawędzie")
		self.actionEdgeEnhanceMore.setText("Mocniejsze wzmocnienie krawędzi")
		self.actionFindEdges.setText("Wykrywanie krawędzi")
		self.actionEmboss.setText("Płaskorzeźba")
		self.actionMarker.setText("Wstaw marker")
		self.actionSmooth.setText("Wygładzanie")
		self.actionSmoothMore .setText("Mocniejsze wygładzanie")
		self.actionGaussianBlur.setText("Rozmycie Gaussa")
		self.actionUnsharpMask.setText("Maska wyostrzająca")
		self.actionRankFilter.setText("Filtr rankingowy")
		self.actionMedianFilter.setText("Filtr medianowy")
		self.actionMinFilter.setText("Filtr minimum")
		self.actionMaxFilter.setText("Filtr maksimum")
		self.actionModeFilter.setText("Filtr modalny")
		self.menuEdgeDetection.addAction(self.actionFindEdges)
		self.actionSolarize.setText("Solaryzacja")
		self.actionTreshold.setText("Progowanie")
		self.actionAddFrame.setText("Dodaj kolorową ramkę")
		self.actionShowHistogram.setText("Wyświetl histogram")
		self.actionEqualizeHistogram.setText("Wyrównanie (Normalizacja)")
		self.actionMask3.setText("Maska 3x3")
		self.actionMask5.setText("Maska 5x5")
		self.actionSampleColor.setText("Kolor (Pipeta)")
		self.actionSave.setText("Zapisz")
		self.actionSaveAs.setText("Zapisz jako...")
# 	nowa wersja obsługi klikniec
		self.scrollAreaWidgetContents.mouseReleaseEvent=self.mouse_get_but_pos_stop
		self.scrollAreaWidgetContents.mousePressEvent=self.mouse_press_clipping
		self.scrollAreaWidgetContents.mouseMoveEvent=self.resize_clipping_frame
		self.scrollAreaWidgetContents.paintEvent=self.paint_clipping_frame

# własne metody
	def show_open_dialog(self):
		filepath = QtGui.QFileDialog.getOpenFileName(None, 'Otworz', '', 'Wszystkie pliki (*.*);;jpeg (*.jpeg);;jpg (*.jpg);;png (*.png);;\
			bmp (*.bmp);;eps (*.eps);;ppm (*.ppm);;')

		if filepath:
			self.open_image(filepath)

	def open_image(self, filepath):
		self.imgPreProc.loadImage(str(filepath))
		self.org_image.Qimg = ImageQt.ImageQt(self.imgPreProc.image.convert("RGB") if self.imgPreProc.image.mode == "L" else self.imgPreProc.image)
		self.org_image.repaint()
		self.refresh_all()
		self.clipping_pos = [0,0, self.imgPreProc.width, self.imgPreProc.height]
		self.in_clipping_mode = False
		self.clipping_not_done = True
		self.clipping_mode()

	def repaint_image(self):
		self.org_image.Qimg = ImageQt.ImageQt(self.imgPreProc.image.convert("RGB") if self.imgPreProc.image.mode == "L" else self.imgPreProc.image) 
		self.org_image.repaint()

	# metoda ogolna do przetwarzania obrazow
	def process_image(self, operation, *args):
		if len(args) == 1:
			operation(args[0])
		elif len(args) > 0 and len(args) < 7:
			operation(args[0],args[1],args[2],args[3],args[4],args[5] )
			if(args[0] in ["rotate", "colorborder", "cropborder" ,"fitscale","resize","newfile"] and self.in_clipping_mode == True):
				self.in_clipping_mode = False
				# self.clipping_not_done = True
				print(args[0])
		else:
			operation()
		self.org_image.repaint()
		self.refresh_all()

	def save_img(self):
		self.imgPreProc.save_photo_normal()
		self.show_save_message()

	def refresh_all(self):
		self.repaint_image()

	def close_application(self):
		QApplication.quit()

	def show_save_message(self):
		save_msg = QtGui.QMessageBox.question(None, 'Stan zapisu', self.imgPreProc.save_message ,QtGui.QMessageBox.Ok)

	def show_save_as_dialog(self):
		savepath = QtGui.QFileDialog.getSaveFileName(None, 'Zapisz', '', 'Wszystkie pliki (*.*);;jpeg (*.jpeg);;jpg (*.jpg);;png (*.png);;\
			bmp (*.bmp);;eps (*.eps);;ppm (*.ppm);;')
		if savepath and any(extension in savepath for extension in [".jpeg",".jpg",".png",".bmp",".eps",".ppm"]):
			msg = QtGui.QMessageBox.question(None, 'Stan zapisu', "Zapisano pomyślnie", QtGui.QMessageBox.Ok)
			self.imgPreProc.save_as(savepath)
		else:
			msg = QtGui.QMessageBox.question(None, 'Ścieżka zapisu', "Nie wskazano miejsca zapisu bądź formatu pliku",QtGui.QMessageBox.Ok)

# jesli zdjecie jest pionowe to zamienia wspolrzedne x y 
	def mouse_get_but_pos_stop(self,event):
		pos = event.pos()
		if pos.x() <= self.imgPreProc.width and pos.y() <= self.imgPreProc.height:
			self.imgPreProc.mouse_pos = (pos.x(), pos.y())
			print('x: %d, y: %d' % (self.imgPreProc.mouse_pos[0], self.imgPreProc.mouse_pos[1]))

	def paint_clipping_frame(self,event):
		if self.in_clipping_mode:
			painter = QPainter(self.scrollAreaWidgetContents)
			painter.setRenderHint(QPainter.Antialiasing)
			painter.setPen(QPen(QBrush(Qt.red), 1, Qt.DashLine))
			painter.drawRect(self.border_rect)
			painter.setPen(QPen(Qt.black))
			painter.drawRect(self.clip_rect)
			for i in range(4):
				painter.drawRect(self.corner(i))
			
			painter.setClipRect(self.clip_rect)
			painter.setBrush(QBrush(Qt.blue))

	def resize_clipping_frame(self, event):
		if self.dragging is None:
			self.clipping_pos = [0,0,self.imgPreProc.width,self.imgPreProc.height]
			return
		  
		left = self.border_rect.left()
		right = self.border_rect.right()
		top = self.border_rect.top()
		bottom = self.border_rect.bottom()
		point = event.pos() + self.drag_offset + self.handle_offsets[self.dragging]
		point.setX(max(left, min(point.x(), right)))
		point.setY(max(top, min(point.y(), bottom)))

		print("Mysza %d %d %d"%(self.dragging, event.pos().x(), event.pos().y()))
		print(self.clipping_pos)
	  
		if self.dragging == 0:
			self.clip_rect.setTopLeft(point)
			self.clipping_pos[0] = event.pos().x() 
			self.clipping_pos[1] = event.pos().y()

		elif self.dragging == 1:
			self.clip_rect.setTopRight(point)
			self.clipping_pos[2] = event.pos().x() 
			self.clipping_pos[1] = event.pos().y()

		elif self.dragging == 2:
			self.clip_rect.setBottomLeft(point)
			self.clipping_pos[0] = event.pos().x() 
			self.clipping_pos[3] = event.pos().y()

		elif self.dragging == 3:
			self.clip_rect.setBottomRight(point)
			self.clipping_pos[2] = event.pos().x() 
			self.clipping_pos[3] = event.pos().y()

		self.scrollAreaWidgetContents.update()

	def mouse_press_clipping(self, event):
		print(event)
		for i in range(4):
			rect = self.corner(i)
			if rect.contains(event.pos()):
				self.dragging = i
				self.drag_offset = rect.topLeft() - event.pos()
				
				break
			else:
				self.dragging = None

	def corner(self, number):
		if number == 0:
			return QRect(self.clip_rect.topLeft() - self.handle_offsets[0], QSize(8, 8))
		elif number == 1:
			return QRect(self.clip_rect.topRight() - self.handle_offsets[1], QSize(8, 8))
		elif number == 2:
			return QRect(self.clip_rect.bottomLeft() - self.handle_offsets[2], QSize(8, 8))
		elif number == 3:
			return QRect(self.clip_rect.bottomRight() - self.handle_offsets[3], QSize(8, 8))

	def clipping_mode(self):
		width = self.imgPreProc.get_sizes()[0] 
		height = self.imgPreProc.get_sizes()[1] 
		if (width > 0 and height > 0):
			self.in_clipping_mode = not self.in_clipping_mode
			self.border_rect = QRect(8,8,width+2,height+2)
			self.clip_rect = QRect(8,8,width+2,height+2)
			self.scrollAreaWidgetContents.update()

			if self.clipping_not_done == False:

				reply = QtGui.QMessageBox.question(self, "Kadrowanie", 
								"Wykonać kadrowanie?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

				if reply == QtGui.QMessageBox.Yes:
					self.imgPreProc.auto_clipping(self.clipping_pos)
					self.org_image.repaint()
					self.refresh_all()
					self.in_clipping_mode = False
					self.clipping_pos = [0,0,self.imgPreProc.width,self.imgPreProc.height]
				else:
					self.in_clipping_mode = False

			self.clipping_not_done = not self.clipping_not_done
		else:
			msg = QtGui.QMessageBox.question(None, 'Kadrowanie', 'Błąd kadrowania - najpierw wczytaj zdjęcie.' ,QtGui.QMessageBox.Ok)
	

def main():
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
