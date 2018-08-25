# iFilter Image Editor
This Project is for submission as Image Editor GUI Assignment for EE610 Image Processing at IT Bombay.

# Contents
|**File**|**Description**|
|---|---|
|[*iFilter.py*](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/iImage.py)|Contains class iImage designed to contain image in HSV format, with transformation as class methods. Also handles `object.load()` and `object.save()` and some other internal properties like `object.RGB` and `object.QImage` that make it easy to handle the images in Qt application built with *pyQt5*|
|---|---|
|[*Final_GUI.py*](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/Final_GUI.py)|Contains GUI created with *Qt Creator*, converted to *Python* and then added all the required signal handling. A lot of New Buttons and other elements were added manually later.|
|---|---|


# iImage Class
`iImage` Class is takes a numpy array of either **RGB** or **Grayscale** as input and converts it into **HSV**
The **HSV** image is split into 3 different channels, and only VChannel saved as `self.ImageV` is manipulated.

## Common Methods
Class Method: `load()` is used to load the image using `PIL.Image` and then call the `iIMage` class constructor

`checkSave(transformedImage, save,...)` is called at the end of all transformations, to decide either to save the transformed VChannel image into same object or return a new object with transformed image. This new object is generally used to avoid saving the transformed image while trying diffferent values in gui

`logTransform(save=False)` method return logTransformed image, in either a new object or inplace, depending on `save` argument

`gammaTransform(gamma, save=False)` returns gamma corrected image by calling `checkSave()` to decide on the returned object

Similarly, `histEqualization()`, `blur()` and `sharpen()` also do their intened transform and call `checkSave` to decide on type of return(i.e., inplace or new object)

Some other `@property` Methods like `.RGB` return an **RGB** image after concatnating all the channels and converting the **HSV** image to **RGB**

# GUI
**Qt creator** was used to design the ui, and convert it into *python* file. The Generated *python* file was then editted to add all the button signals and a few more elements like Matplotlib's `FeatureCanvas` and `Qpixmap` for displaying the image, with an option to switch between the two with `use_matplotlib_backend` flag at the start.

`MplCanvas` Class sets up the Matplotlib Canvas for Qt
`Ui_MainWindow` Class sets up the main UI Window, with `setupUi()` method adding all the elements to it including Qwidgets, Qlayouts inside the Qwidgets and adding QButtons and other smaller elements inside the Layouts as designed in **Qt Creator** and things that were added later manually like `MlpCanvas`

`retranslateUi()` method adds all the texts like text on QButtons and QLabels to the Ui

`imshow_()` method displays the passed image in Ui using the appropriate backend
`update_history()` method clears the QTable and updates it with latest `history_text` from its `self.image` iImage object.

`checkout()` method lets the user checkout any saved image from `iImage.history` and is inspired by Git
`set_buttons_bindings()` method sets up all the button and slider binding methods that are to be called when buttons are clicked or sliders are released.

# Results

### Gui Home
![Home](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/home.png)

### Filtering in Frequency Domain with Jupyter Notebook
#### Highpass Filtering
![Highpass 1](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/HighPass_House.png)
#### Lowpass Filtering
![Lowpass Blur][https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/LowPass_Lena_GS.png]

### Home on Loading Image
![Lena_Color_OG](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/Lena_Color.png)

#### Navigating between saved Images with Text Column
![Navigating](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/Navigating.png)

#### Gamma Correction
![Lena_gamma_correction](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/Lena_GS_Gamma.png)

#### Histogram Equalization
![Lena Hist](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/Lena_GS_Hist.png)

#### Applying Blur in Gui
![Lena_Blur](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/Lena_Color_Blur.png)

#### Applying Log Transform to the above blurred Image in Gui
![LogT](https://github.com/dumbPy/iFilter_Image_Editor/blob/master/outpus_images/Lena_Color_Blur_LogT.png)


# Bugs
* FFt and IFFT works after a very long struggle, but the sharpened images in using Frequency Filtering don't look any much different even though edges are clearly getting extracted in HighPass Filtered Notebook Above.

* QPixmap backend for displaying images is buggy. Hence had to shift back to Matplotlib FeatureCanvas Backend, even though it has some white spaces around the images, unline Qpixmap that fits perfectly.
