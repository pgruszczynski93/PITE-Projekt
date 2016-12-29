from PyQt4 import QtCore, QtGui
from ImageWidget import *
from ImagePreProcessor import *
from PIL import ImageQt
import sys
from PIL import ImageFilter

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QWidget):

	def __init__(self):
		super(Ui_MainWindow, self).__init__()
		self.imgPreProc = ImagePreProcessor()
		self.selected_filter = 0
		self.pred_filters = [
		ImageFilter.BLUR,ImageFilter.CONTOUR,ImageFilter.DETAIL,
		ImageFilter.EDGE_ENHANCE,ImageFilter.EDGE_ENHANCE_MORE,ImageFilter.EMBOSS,
		ImageFilter.FIND_EDGES,ImageFilter.SMOOTH,ImageFilter.SMOOTH_MORE, ImageFilter.SHARPEN]

	def setupUi(self, MainWindow):

		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(1024, 645)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

		# gridLayout_4
		self.gridLayout = QtGui.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		# zdjecie w ramce
		self.frame = QtGui.QFrame(self.centralwidget)
		self.frame.setGeometry(QtCore.QRect(50, 0, 800, 600))
		self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
		self.frame.setFrameShadow(QtGui.QFrame.Raised)
		self.frame.setObjectName(_fromUtf8("frame"))

		 #gridLayout_2
		self.gridLayout_2 = QtGui.QGridLayout(self.frame)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))

		self.scrollArea = QtGui.QScrollArea(self.frame)
		self.scrollArea.setGeometry(QtCore.QRect(0, 0, 800, 600))
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName(_fromUtf8("scrollArea"))

		self.scrollAreaWidgetContents = QtGui.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 800, 600))
		self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))

		#gridLayout_5
		self.gridLayout_3 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
		self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))

		self.org_image = ImageWidget(self.scrollAreaWidgetContents)
		# self.org_image = QtGui.QWidget(self.scrollAreaWidgetContents)
		# self.org_image.setGeometry(QtCore.QRect(0, 0, 800, 600))
		self.org_image.setObjectName(_fromUtf8("org_image"))
		# self.addWidget(self.original_image, 0, 0, 1, 1)
		self.gridLayout_3.addWidget(self.org_image,0,0,1,1)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)

		self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		# self.frame_2 = QtGui.QFrame(self.centralwidget)
		# self.frame_2.setGeometry(QtCore.QRect(510, 0, 450, 600))
		# self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
		# self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
		# self.frame_2.setObjectName(_fromUtf8("frame_2"))
		# self.scrollArea_2 = QtGui.QScrollArea(self.frame_2)
		# self.scrollArea_2.setGeometry(QtCore.QRect(0, 0, 450, 600))
		# self.scrollArea_2.setWidgetResizable(True)
		# self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
		# self.scrollAreaWidgetContents_2 = QtGui.QWidget()
		# self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 448, 598))
		# self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
		# self.copy_image = QtGui.QWidget(self.scrollAreaWidgetContents_2)
		# self.copy_image.setGeometry(QtCore.QRect(0, 0, 450, 600))
		# self.copy_image.setObjectName(_fromUtf8("copy_image"))
		# self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuPlik = QtGui.QMenu(self.menubar)
		self.menuPlik.setObjectName(_fromUtf8("menuPlik"))
		self.menuFilters = QtGui.QMenu(self.menubar)
		self.menuFilters.setObjectName(_fromUtf8("menuFilters"))
		self.menuSzum = QtGui.QMenu(self.menuFilters)
		self.menuSzum.setObjectName(_fromUtf8("menuSzum"))
		self.menuBluring = QtGui.QMenu(self.menuFilters)
		self.menuSharpening = QtGui.QMenu(self.menuFilters)
		self.menuSharpening.setObjectName(_fromUtf8("menuSharpening"))
		self.menuBluring.setObjectName(_fromUtf8("menuBluring"))
		self.menuSmoothing = QtGui.QMenu(self.menuFilters)
		self.menuSmoothing.setObjectName(_fromUtf8("menuSmoothing"))
		self.menuEdgeDetection = QtGui.QMenu(self.menuFilters)
		self.menuEdgeDetection.setObjectName(_fromUtf8("menuEdgeDetection"))
		self.menuInne = QtGui.QMenu(self.menuFilters)
		self.menuInne.setObjectName(_fromUtf8("menuInne"))
		self.menuTransformacja = QtGui.QMenu(self.menubar)
		self.menuTransformacja.setObjectName(_fromUtf8("menuTransformacja"))
		self.menuDopasowania = QtGui.QMenu(self.menubar)
		self.menuDopasowania.setObjectName(_fromUtf8("menuDopasowania"))
		self.menuHistogram = QtGui.QMenu(self.menuDopasowania)
		self.menuHistogram.setObjectName(_fromUtf8("menuHistogram"))
		self.menuWstawianie = QtGui.QMenu(self.menubar)
		self.menuWstawianie.setObjectName(_fromUtf8("menuWstawianie"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		self.actionOpen = QtGui.QAction(MainWindow)
		self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
		self.actionOpen.setShortcut('Ctrl+O');
		self.actionOpen.triggered.connect(self.show_open_dialog)


		self.actionQuit = QtGui.QAction(MainWindow)
		self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
		self.actionQuit.setShortcut('Ctrl+Q')
		self.actionQuit.triggered.connect(self.close_application)


		self.actionNew = QtGui.QAction(MainWindow)
		self.actionNew.setObjectName(_fromUtf8("actionNew"))
		self.actionNew.setShortcut('Ctrl+N')
		self.actionNew.triggered.connect(self.auto_new)

		self.actionG_rnoprzepustowy = QtGui.QAction(MainWindow)
		self.actionG_rnoprzepustowy.setObjectName(_fromUtf8("actionG_rnoprzepustowy"))
		self.actionDolnoprzepustowy = QtGui.QAction(MainWindow)
		self.actionDolnoprzepustowy.setObjectName(_fromUtf8("actionDolnoprzepustowy"))

######################################
######################################
######################################
		self.actionSharpen = QtGui.QAction(MainWindow)
		self.actionSharpen.setObjectName(_fromUtf8("actionSharpen"))
		self.actionSharpen.triggered.connect(lambda: self.auto_filter(9))

		self.actionBluring = QtGui.QAction(MainWindow)
		self.actionBluring.setObjectName(_fromUtf8("actionBluring"))
		self.actionBluring.triggered.connect(lambda: self.auto_filter(0))

		self.actionContour = QtGui.QAction(MainWindow)
		self.actionContour.setObjectName(_fromUtf8("actionContour"))
		self.actionContour.triggered.connect(lambda: self.auto_filter(1))

		self.actionDetail = QtGui.QAction(MainWindow)
		self.actionDetail.setObjectName(_fromUtf8("actionContour"))
		self.actionDetail.triggered.connect(lambda: self.auto_filter(2))

		self.actionEdgeEnhance = QtGui.QAction(MainWindow)
		self.actionEdgeEnhance.setObjectName(_fromUtf8("actionEdgeEnhance"))
		self.actionEdgeEnhance.triggered.connect(lambda: self.auto_filter(3))

		self.actionEdgeEnhanceMore = QtGui.QAction(MainWindow)
		self.actionEdgeEnhanceMore.setObjectName(_fromUtf8("actionEdgeEnhanceMore"))
		self.actionEdgeEnhanceMore.triggered.connect(lambda: self.auto_filter(4))

		self.actionFindEdges = QtGui.QAction(MainWindow)
		self.actionFindEdges.setObjectName(_fromUtf8("actionEdgeEnhanceMore"))
		self.actionFindEdges.triggered.connect(lambda: self.auto_filter(6))

		self.actionEmboss = QtGui.QAction(MainWindow)
		self.actionEmboss.setObjectName(_fromUtf8("actionEmboss"))
		self.actionEmboss.triggered.connect(lambda: self.auto_filter(5))

		self.actionSmooth = QtGui.QAction(MainWindow)
		self.actionSmooth.setObjectName(_fromUtf8("actionSmooth"))
		self.actionSmooth.triggered.connect(lambda: self.auto_filter(7))

		self.actionSmoothMore = QtGui.QAction(MainWindow)
		self.actionSmoothMore.setObjectName(_fromUtf8("actionSmoothMore"))
		self.actionSmoothMore.triggered.connect(lambda: self.auto_filter(8))

		self.actionGaussianBlur = QtGui.QAction(MainWindow)
		self.actionGaussianBlur.setObjectName(_fromUtf8("actionGaussianBlur"))
		self.actionGaussianBlur.triggered.connect(self.auto_gaussianblur)

		self.actionUnsharpMask = QtGui.QAction(MainWindow)
		self.actionUnsharpMask.setObjectName(_fromUtf8("actionUnsharpMask"))
		self.actionUnsharpMask.triggered.connect(self.auto_unsharpmask)
		
		self.actionKernel = QtGui.QAction(MainWindow)
		self.actionKernel.setObjectName(_fromUtf8("actionKernel"))
		self.actionKernel.triggered.connect(self.auto_kernel)

		self.actionRankFilter = QtGui.QAction(MainWindow)
		self.actionRankFilter.setObjectName(_fromUtf8("actionRankFilter"))
		self.actionRankFilter.triggered.connect(self.auto_rankfilter)
		
		self.actionMedianFilter = QtGui.QAction(MainWindow)
		self.actionMedianFilter.setObjectName(_fromUtf8("actionMedianFilter"))
		self.actionMedianFilter.triggered.connect(self.auto_medianfilter)
		
		self.actionMinFilter = QtGui.QAction(MainWindow)
		self.actionMinFilter.setObjectName(_fromUtf8("actionMinFilter"))
		self.actionMinFilter.triggered.connect(self.auto_minfilter)
		
		self.actionMaxFilter = QtGui.QAction(MainWindow)
		self.actionMaxFilter.setObjectName(_fromUtf8("actionMaxFilter"))
		self.actionMaxFilter.triggered.connect(self.auto_maxfilter)
		
		self.actionModeFilter = QtGui.QAction(MainWindow)
		self.actionModeFilter.setObjectName(_fromUtf8("actionModeFilter"))
		self.actionModeFilter.triggered.connect(self.auto_modefilter)


######################################
######################################
######################################
		self.actionUsuwanie_szumu_i_ziarna = QtGui.QAction(MainWindow)
		self.actionUsuwanie_szumu_i_ziarna.setObjectName(_fromUtf8("actionUsuwanie_szumu_i_ziarna"))
		self.actionZaszumianie = QtGui.QAction(MainWindow)
		self.actionZaszumianie.setObjectName(_fromUtf8("actionZaszumianie"))
		self.actionG_rnoprzepustowy_2 = QtGui.QAction(MainWindow)
		self.actionG_rnoprzepustowy_2.setObjectName(_fromUtf8("actionG_rnoprzepustowy_2"))
		self.actionDolnoprzepustowy_2 = QtGui.QAction(MainWindow)
		self.actionDolnoprzepustowy_2.setObjectName(_fromUtf8("actionDolnoprzepustowy_2"))

		self.actionEdgeDetection = QtGui.QAction(MainWindow)
		self.actionEdgeDetection.setObjectName(_fromUtf8("actionEdgeDetection"))

		self.actionZaznaczanie = QtGui.QAction(MainWindow)
		self.actionZaznaczanie.setObjectName(_fromUtf8("actionZaznaczanie"))

		self.actionRotate = QtGui.QAction(MainWindow)
		self.actionRotate.setObjectName(_fromUtf8("actionRotate"))
		self.actionRotate.setShortcut('Alt+R')
		self.actionRotate.triggered.connect(self.auto_rotate)

		self.actionSkalowanie = QtGui.QAction(MainWindow)
		self.actionSkalowanie.setObjectName(_fromUtf8("actionSkalowanie"))

		self.actionFitScale= QtGui.QAction(MainWindow)
		self.actionFitScale.setObjectName(_fromUtf8("actionFitScale"))
		self.actionFitScale.setShortcut('Ctrl+Alt+F')
		self.actionFitScale.triggered.connect(self.auto_fitscale)

		self.actionResize= QtGui.QAction(MainWindow)
		self.actionResize.setObjectName(_fromUtf8("actionFitScale"))
		self.actionResize.setShortcut('Ctrl+Alt+I')
		self.actionResize.triggered.connect(self.auto_resize)

		self.actionKadrowanie = QtGui.QAction(MainWindow)
		self.actionKadrowanie.setObjectName(_fromUtf8("actionKadrowanie"))

		self.actionBrightness = QtGui.QAction(MainWindow)
		self.actionBrightness.setObjectName(_fromUtf8("actionBrightness"))
		self.actionBrightness.setShortcut('Alt+B')
		self.actionBrightness.triggered.connect(self.auto_brightness)

		self.actionColorBalance = QtGui.QAction(MainWindow)
		self.actionColorBalance.setObjectName(_fromUtf8("actionColorBalance"))
		self.actionColorBalance.setShortcut('Alt+C')
		self.actionColorBalance.triggered.connect(self.auto_colorbalance)

		self.actionKontrast = QtGui.QAction(MainWindow)
		self.actionKontrast.setObjectName(_fromUtf8("actionKontrast"))

		self.actionAutoContrast = QtGui.QAction(MainWindow)
		self.actionAutoContrast.setObjectName(_fromUtf8("actionAutoContrast"))
		self.actionAutoContrast.setShortcut('Shift+Ctrl+Alt+L')
		self.actionAutoContrast.triggered.connect(self.auto_contrast)

		self.actionNasycenie = QtGui.QAction(MainWindow)
		self.actionNasycenie.setObjectName(_fromUtf8("actionNasycenie"))
		self.actionGamma = QtGui.QAction(MainWindow)
		self.actionGamma.setObjectName(_fromUtf8("actionGamma"))

		self.actionGrayScale = QtGui.QAction(MainWindow)
		self.actionGrayScale.setObjectName(_fromUtf8("actionGrayScale"))
		self.actionGrayScale.setShortcut("Ctrl+Alt+S")
		self.actionGrayScale.triggered.connect(self.auto_grayscale)

		self.actionColorize = QtGui.QAction(MainWindow)
		self.actionColorize.setObjectName(_fromUtf8("actionColorize"))
		self.actionColorize.setShortcut("Ctrl+Alt+K")
		self.actionColorize.triggered.connect(self.auto_colorize)

		self.actionInverseColors = QtGui.QAction(MainWindow)
		self.actionInverseColors.setObjectName(_fromUtf8("actionInverseColors"))
		self.actionInverseColors.setShortcut('Alt+I')
		self.actionInverseColors.triggered.connect(self.auto_negative)

		self.actionMirrorEffect = QtGui.QAction(MainWindow)
		self.actionMirrorEffect.setObjectName(_fromUtf8("actionMirrorEffect"))
		self.actionMirrorEffect.setShortcut('Alt+L')
		self.actionMirrorEffect.triggered.connect(self.auto_mirror)

		self.actionFlip = QtGui.QAction(MainWindow)
		self.actionFlip.setObjectName(_fromUtf8("actionFlip"))
		self.actionFlip.setShortcut('Alt+F')
		self.actionFlip.triggered.connect(self.auto_flip)

		self.actionPosterize = QtGui.QAction(MainWindow)
		self.actionPosterize.setObjectName(_fromUtf8("actionPosterize"))
		self.actionPosterize.setShortcut('Alt+P')
		self.actionPosterize.triggered.connect(self.auto_posterize)

		self.actionSolarize = QtGui.QAction(MainWindow)
		self.actionSolarize.setObjectName(_fromUtf8("actionSolarize"))
		self.actionSolarize.setShortcut('Alt+S')
		self.actionSolarize.triggered.connect(self.auto_solarize)

		self.actionDeleteBorder = QtGui.QAction(MainWindow)
		self.actionDeleteBorder.setObjectName(_fromUtf8("actionDeleteBorder"))
		self.actionDeleteBorder.setShortcut('Ctrl+Alt+B')
		self.actionDeleteBorder.triggered.connect(self.auto_delete_border)

		self.actionTreshold = QtGui.QAction(MainWindow)
		self.actionTreshold.setObjectName(_fromUtf8("actionTreshold"))
		self.actionTreshold.triggered.connect(self.treshold)
		self.actionPodgl_d = QtGui.QAction(MainWindow)
		self.actionPodgl_d.setObjectName(_fromUtf8("actionPodgl_d"))

		self.actionEqualizeHistogram = QtGui.QAction(MainWindow)
		self.actionEqualizeHistogram.setObjectName(_fromUtf8("actionEqualizeHistogram"))
		self.actionEqualizeHistogram.setShortcut('Ctrl+Alt+H')
		self.actionEqualizeHistogram.triggered.connect(self.auto_equalize_histogram)

		self.actionAddFrame = QtGui.QAction(MainWindow)
		self.actionAddFrame.setObjectName(_fromUtf8("actionAddFrame"))
		self.actionAddFrame.setShortcut('Alt+F')
		self.actionAddFrame.triggered.connect(self.auto_add_color_border)

		self.actionText = QtGui.QAction(MainWindow)
		self.actionText.setObjectName(_fromUtf8("actionText"))
		self.actionText.setShortcut('Alt+T')
		self.actionText.triggered.connect(self.auto_add_text)

		self.actionKolor = QtGui.QAction(MainWindow)
		self.actionKolor.setObjectName(_fromUtf8("actionKolor"))
		self.actionWype_nianie = QtGui.QAction(MainWindow)
		self.actionWype_nianie.setObjectName(_fromUtf8("actionWype_nianie"))

		self.actionSave = QtGui.QAction(MainWindow)
		self.actionSave.setObjectName("actionSave")
		self.actionSave.setShortcut('Ctrl+S')
		self.actionSave.triggered.connect(self.save_img)
		
		self.actionSaveAs = QtGui.QAction(MainWindow)
		self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
		self.actionSaveAs.setShortcut('Ctrl+Shift+S')
		self.actionSaveAs.triggered.connect(self.show_save_as_dialog)


		self.menuPlik.addAction(self.actionNew)
		self.menuPlik.addAction(self.actionOpen)
		self.menuPlik.addAction(self.actionSave)
		self.menuPlik.addAction(self.actionSaveAs)
		self.menuPlik.addAction(self.actionQuit)
		self.menuSzum.addAction(self.actionUsuwanie_szumu_i_ziarna)
		self.menuSzum.addAction(self.actionZaszumianie)
		self.menuInne.addAction(self.actionG_rnoprzepustowy_2)
		self.menuInne.addAction(self.actionDolnoprzepustowy_2)
		self.menuInne.addAction(self.actionTreshold)

#########################3
#########################3
#########################3
		self.menuSharpening.addAction(self.actionSharpen)
		self.menuFilters.addAction(self.menuSharpening.menuAction())
		# self.menuFilters.addAction(self.actionSharpen)
		self.menuFilters.addAction(self.menuBluring.menuAction())
		# self.menuFilters.addAction(self.actionBluring)
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
		# self.menuEdgeDetection.addAction(self.actionEdgeDetection)
		self.menuFilters.addAction(self.menuSzum.menuAction())
		self.menuFilters.addAction(self.menuInne.menuAction())
		self.menuFilters.addAction(self.actionKernel)
		
		# self.menuFilters.addAction(self.menuEdgeDetection.menuAction())

#########################3
#########################3
#########################3
		self.menuTransformacja.addAction(self.actionZaznaczanie)
		self.menuTransformacja.addAction(self.actionRotate)
		self.menuTransformacja.addAction(self.actionSkalowanie)
		self.menuTransformacja.addAction(self.actionFitScale)
		self.menuTransformacja.addAction(self.actionResize)
		self.menuTransformacja.addAction(self.actionKadrowanie)
		self.menuTransformacja.addAction(self.actionDeleteBorder)
		self.menuTransformacja.addAction(self.actionAddFrame)
		self.menuHistogram.addAction(self.actionPodgl_d)
		self.menuHistogram.addAction(self.actionEqualizeHistogram)
		self.menuDopasowania.addAction(self.actionBrightness)
		self.menuDopasowania.addAction(self.actionKontrast)
		self.menuDopasowania.addAction(self.actionAutoContrast)
		self.menuDopasowania.addAction(self.actionNasycenie)
		self.menuDopasowania.addAction(self.actionGamma)
		self.menuDopasowania.addAction(self.actionInverseColors)
		self.menuDopasowania.addAction(self.actionGrayScale)
		self.menuDopasowania.addAction(self.actionColorBalance)
		self.menuDopasowania.addAction(self.actionFlip)
		self.menuDopasowania.addAction(self.actionMirrorEffect)
		self.menuDopasowania.addAction(self.actionPosterize)
		self.menuDopasowania.addAction(self.actionSolarize)
		self.menuDopasowania.addAction(self.menuHistogram.menuAction())
		self.menuDopasowania.addAction(self.actionColorize)
		self.menuDopasowania.addAction(self.actionKolor)
		self.menuDopasowania.addAction(self.actionWype_nianie)
		self.menuWstawianie.addAction(self.actionText)
		self.menubar.addAction(self.menuPlik.menuAction())
		self.menubar.addAction(self.menuFilters.menuAction())
		self.menubar.addAction(self.menuTransformacja.menuAction())
		self.menubar.addAction(self.menuDopasowania.menuAction())
		self.menubar.addAction(self.menuWstawianie.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "PITE - Project", None))
		self.menuPlik.setTitle(_translate("MainWindow", "Plik", None))
		self.menuFilters.setTitle(_translate("MainWindow", "Filtr", None))
		self.menuSzum.setTitle(_translate("MainWindow", "Szum", None))
		self.menuInne.setTitle(_translate("MainWindow", "Inne", None))
		self.menuTransformacja.setTitle(_translate("MainWindow", "Transformacja", None))
		self.menuDopasowania.setTitle(_translate("MainWindow", "Dopasowania", None))
		self.menuHistogram.setTitle(_translate("MainWindow", "Histogram", None))
		self.menuWstawianie.setTitle(_translate("MainWindow", "Wstawianie", None))
		self.actionOpen.setText(_translate("MainWindow", "Otwórz...", None))
		self.actionQuit.setText(_translate("MainWindow", "Zakończ", None))
		self.actionNew.setText(_translate("MainWindow", "Nowy", None))
		self.actionG_rnoprzepustowy.setText(_translate("MainWindow", "Górnoprzepustowy", None))
		self.actionDolnoprzepustowy.setText(_translate("MainWindow", "Dolnoprzepustowy", None))
		self.actionSharpen.setText(_translate("MainWindow", "Wyostrzanie", None))
		self.actionBluring.setText(_translate("MainWindow", "Zwykłe rozmywanie", None))
		self.actionUsuwanie_szumu_i_ziarna.setText(_translate("MainWindow", "Usuwanie szumu i ziarna", None))
		self.actionZaszumianie.setText(_translate("MainWindow", "Zaszumianie", None))
		self.actionG_rnoprzepustowy_2.setText(_translate("MainWindow", "Górnoprzepustowy", None))
		self.actionDolnoprzepustowy_2.setText(_translate("MainWindow", "Dolnoprzepustowy", None))
		self.menuEdgeDetection.setTitle(_translate("MainWindow", "Filtry krawędziowe", None))
		self.menuSmoothing.setTitle(_translate("MainWindow", "Wygładzanie", None))
		self.menuBluring.setTitle(_translate("MainWindow", "Rozmycie", None))
		self.menuSharpening.setTitle(_translate("MainWindow", "Wyostrzanie", None))
		self.actionZaznaczanie.setText(_translate("MainWindow", "Zaznaczanie", None))
		self.actionRotate.setText(_translate("MainWindow", "Obrót", None))
		self.actionSkalowanie.setText(_translate("MainWindow", "Skalowanie", None))
		self.actionFitScale.setText(_translate("MainWindow", "Skaluj i dopasuj", None))
		self.actionResize.setText(_translate("MainWindow", "Zmiana rozmiaru", None))
		self.actionKadrowanie.setText(_translate("MainWindow", "Kadrowanie", None))
		self.actionBrightness.setText(_translate("MainWindow", "Jasność", None))
		self.actionKontrast.setText(_translate("MainWindow", "Kontrast", None))
		self.actionAutoContrast.setText(_translate("MainWindow","Auto Kontrast", None))
		self.actionNasycenie.setText(_translate("MainWindow", "Nasycenie", None))
		self.actionFlip.setText(_translate("MainWindow", "Przerzuć", None))
		self.actionColorBalance.setText(_translate("MainWindow","Balans kolorów", None))
		self.actionGamma.setText(_translate("MainWindow", "Gamma", None))
		self.actionInverseColors.setText(_translate("MainWindow", "Odwróć kolory", None))
		self.actionGrayScale.setText(_translate("MainWidndow","Skala Szarości", None))
		self.actionMirrorEffect.setText(_translate("MainWindow","Lustro",None))
		self.actionColorize.setText(_translate("MainWidndow","Koloryzacja", None))
		self.actionPosterize.setText(_translate("MainWidndow","Posteryzacja", None))
		self.actionDeleteBorder.setText(_translate("MainWidndow","Usuń brzeg zdjęcia", None))
		self.actionContour.setText(_translate("MainWidndow","Kontury", None))
		self.actionDetail.setText(_translate("MainWidndow","Ekstrakcja detali", None))
		self.actionEdgeEnhance.setText(_translate("MainWidndow","Wzmocnienie krawędzie", None))
		self.actionEdgeEnhanceMore.setText(_translate("MainWidndow","Mocniejsze wzmocnienie krawędzi", None))
		self.actionFindEdges.setText(_translate("MainWidndow","Wykrywanie krawędzi", None))
		self.actionEmboss.setText(_translate("MainWidndow","Płaskorzeźba", None))
		
		self.actionSmooth.setText(_translate("MainWidndow","Wygładzanie", None))
		self.actionSmoothMore.setText(_translate("MainWidndow","Mocniejsze wygładzanie", None))
		self.actionGaussianBlur.setText(_translate("MainWidndow","Rozmycie Gaussa", None))
		self.actionUnsharpMask.setText(_translate("MainWidndow","Maska wyostrzająca", None))
		self.actionKernel.setText(_translate("MainWidndow","Własny filtr splotowy", None))
		self.actionRankFilter.setText(_translate("MainWidndow","Filtr rankingowy", None))
		self.actionMedianFilter.setText(_translate("MainWidndow","Filtr medianowy", None))
		self.actionMinFilter.setText(_translate("MainWidndow","Filtr minimum", None))
		self.actionMaxFilter.setText(_translate("MainWidndow","Filtr maksimum", None))
		self.actionModeFilter.setText(_translate("MainWidndow","Filtr modalny", None))

		self.menuEdgeDetection.addAction(self.actionFindEdges)
		self.actionSolarize.setText(_translate("MainWidndow","Solaryzacja", None))
		self.actionTreshold.setText(_translate("MainWindow", "Progowanie", None))
		self.actionAddFrame.setText(_translate("MainWindow", "Dodaj kolorową ramkę", None))
		self.actionPodgl_d.setText(_translate("MainWindow", "Podgląd", None))
		self.actionEqualizeHistogram.setText(_translate("MainWindow", "Wyrównanie (Normalizacja)", None))
		self.actionText.setText(_translate("MainWindow", "Tekst", None))
		self.actionKolor.setText(_translate("MainWindow", "Kolor (Pipeta)", None))
		self.actionWype_nianie.setText(_translate("MainWindow", "Wypełnianie", None))
		self.actionSave.setText(_translate("MainWindow", "Zapisz", None))
		self.actionSaveAs.setText(_translate("MainWindow", "Zapisz jako...", None))

	def show_open_dialog(self):
		filepath = QtGui.QFileDialog.getOpenFileName(None, 'Otworz', '', 'Wszystkie pliki (*.*);;jpeg (*.jpeg);;jpg (*.jpg);;png (*.png)')

		if filepath:
			self.open_image(filepath)

	def open_image(self, filepath):
		# msg = QtGui.QMessageBox.question(None, 'Sciezka', str(filepath),QtGui.QMessageBox.Ok)
		self.imgPreProc.loadImage(str(filepath))
		self.org_image.Qimg = ImageQt.ImageQt(self.imgPreProc.image.convert("RGB") if self.imgPreProc.image.mode == "L" else self.imgPreProc.image)
		self.org_image.repaint()
		self.refresh_all()

	def repaint_image(self):
		self.org_image.Qimg = ImageQt.ImageQt(self.imgPreProc.image.convert("RGB") if self.imgPreProc.image.mode == "L" else self.imgPreProc.image) 
		self.org_image.repaint()
		#  albo dać tu zdjecie zmodyfikowane w panelu 0

	def auto_negative(self):
		self.imgPreProc.negative()
		self.org_image.repaint()
		self.refresh_all()

	def auto_contrast(self):
		self.imgPreProc.auto_contrast()
		self.org_image.repaint()
		self.refresh_all()

	def auto_grayscale(self):
		self.imgPreProc.auto_grayscale()
		self.org_image.repaint()
		self.refresh_all()

	def auto_colorize(self):
		self.imgPreProc.auto_colorize()
		self.org_image.repaint()
		self.refresh_all()

	def auto_mirror(self):
		self.imgPreProc.auto_mirror()
		self.org_image.repaint()
		self.refresh_all()

	def auto_flip(self):
		self.imgPreProc.auto_flip()
		self.org_image.repaint()
		self.refresh_all()

	def auto_posterize(self):
		self.imgPreProc.auto_posterize()
		self.org_image.repaint()
		self.refresh_all()

	def auto_solarize(self):
		self.imgPreProc.auto_solarize()
		self.org_image.repaint()
		self.refresh_all()

	def auto_delete_border(self):
		self.imgPreProc.auto_delete_border()
		self.org_image.repaint()
		self.refresh_all()

	def auto_equalize_histogram(self):
		self.imgPreProc.auto_equalize_histogram()
		self.org_image.repaint()
		self.refresh_all()

	def auto_add_color_border(self):
		self.imgPreProc.auto_add_color_border()
		self.org_image.repaint()
		self.refresh_all()

	def auto_fitscale(self):
		self.imgPreProc.auto_fitscale()
		self.org_image.repaint()
		self.refresh_all()

	def auto_rotate(self):
		self.imgPreProc.auto_rotate()
		self.org_image.repaint()
		self.refresh_all()

	def auto_resize(self):
		self.imgPreProc.auto_resize()
		self.org_image.repaint()
		self.refresh_all()

	def auto_brightness(self):
		self.imgPreProc.auto_brightness()
		self.org_image.repaint()
		self.refresh_all()

	def auto_colorbalance(self):
		self.imgPreProc.auto_colorbalance()
		self.org_image.repaint()
		self.refresh_all()

	def auto_new(self):
		self.imgPreProc.auto_new()
		self.org_image.repaint()
		self.refresh_all()

	def auto_add_text(self):
		self.imgPreProc.auto_add_text()
		self.org_image.repaint()
		self.refresh_all()

	def auto_unsharpmask(self):
		self.imgPreProc.auto_unsharpmask()
		self.org_image.repaint()
		self.refresh_all()

	def auto_kernel(self):
		self.imgPreProc.auto_kernel()
		self.org_image.repaint()
		self.refresh_all()

	def auto_rankfilter(self):
		self.imgPreProc.auto_rankfilter()
		self.org_image.repaint()
		self.refresh_all()

	def auto_medianfilter(self):
		self.imgPreProc.auto_medianfilter()
		self.org_image.repaint()
		self.refresh_all()
		
	def auto_minfilter(self):
		self.imgPreProc.auto_minfilter()
		self.org_image.repaint()
		self.refresh_all()

	def auto_maxfilter(self):
		self.imgPreProc.auto_maxfilter()
		self.org_image.repaint()
		self.refresh_all()

	def auto_modefilter(self):
		self.imgPreProc.auto_modefilter()
		self.org_image.repaint()
		self.refresh_all()

	# def set_filter_mode(self, selected_filter):
	# 	self.selected_filter = selected_filter

	# def get_filter_mode(self):
	# 	return self.selected_filter

	def auto_filter(self, selected_filter):
		self.imgPreProc.auto_filter(self.pred_filters[selected_filter])
		self.org_image.repaint()
		self.refresh_all()

	def auto_gaussianblur(self):
		self.imgPreProc.auto_gaussianblur()
		self.org_image.repaint()
		self.refresh_all()

	def treshold(self):
		self.imgPreProc.pre_treshold()
		self.org_image.repaint()
		self.refresh_all()

	def save_img(self):
		message_text = self.imgPreProc.save_photo_normal()
		self.show_save_message(message_text)

	def save_img_as(self):
		# naprawić save as- sciezki ok ale nie zapisuje
		savepath = self.show_save_as_dialog()
		self.imgPreProc.save_as(savepath)

	def refresh_all(self):
		self.repaint_image()

	def close_application(self):
		app.quit()

	def show_save_message(self, message_text):
		save_msg = QtGui.QMessageBox.question(None, 'Stan zapisu', message_text ,QtGui.QMessageBox.Ok)

	def show_save_as_dialog(self):
		savepath = QtGui.QFileDialog.getSaveFileName(None, 'Zapisz', '', 'Wszystkie pliki (*.*);;jpeg (*.jpeg);;jpg (*.jpg);;png (*.png)')
		if savepath:
			msg = QtGui.QMessageBox.question(None, 'Ścieżka zapisu',savepath,QtGui.QMessageBox.Ok)
			return savepath
		else:
			# self.open(filename) - ma zapisac
			msg = QtGui.QMessageBox.question(None, 'Ścieżka zapisu', "Nie wskazano miejsca zapisu",QtGui.QMessageBox.Ok)

	def mouse_get_but_pos_stop(self,event):
		if event.buttons() == QtCore.Qt.LeftButton:
				pos = event.pos()
				self.imgPreProc.set_mouse_pos((pos.x(), pos.y()))
				print('x: %d, y: %d' % (self.imgPreProc.get_mouse_pos()[0], self.imgPreProc.get_mouse_pos()[1]))

		elif event.buttons() == QtCore.Qt.RightButton:
				pos = event.pos()
				# zrobić coś po rightclicku 
				# self.imgPreProc.set_mouse_pos((pos.x(), pos.y()))
				# print('x: %d, y: %d' % (self.imgPreProc.get_mouse_pos()[0], self.imgPreProc.get_mouse_pos()[1]))

	def eventFilter(self, source, event):
		# dorobić coś na ruch muszy
		if event.type() == QtCore.QEvent.MouseMove:
			if event.buttons() == QtCore.Qt.LeftButton:
				pos = event.pos()
				# print('rx: %d, ry: %d' % (pos.x(), pos.y()))
			elif event.buttons() == QtCore.Qt.RightButton:
				pos = event.pos()
				# print('rx: %d, ry: %d' % (pos.x(), pos.y()))
		if event.type() == QEvent.MouseButtonPress:
			self.mouse_get_but_pos_stop(event)
		return QtGui.QMainWindow.eventFilter(self, source, event)

	
	
if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	app.installEventFilter(ui)
	MainWindow.show()
	sys.exit(app.exec_())
