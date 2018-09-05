from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.fftpack as fp
from PIL import ImageQt


def conv2D(image, filt, padding='reflect', **kwargs): #1 Channel Conv2D
        pad=int((filt.shape[0]-1)/2)
        m,n=filt.shape
        i,j=image.shape
        weight=1/filt.sum()
        image=image.astype(np.float32) #for multithreading
        filt=filt.astype(np.float32)   #for multithreading. Works only with float32
        if padding is None:
            padded=image #don't pad. used for sharpenning where  padding messes things up
            c=np.asarray([[(weight*np.multiply(padded[x:x+m,y:y+n],filt)).sum()
                      for y in range(j-n+1)] for x in range(i-m+1)])
            return c.reshape((i-m+1, j-n+1))
        else:
            padded=np.pad(image, pad_width=pad, mode=padding, **kwargs) 
            c=np.asarray([[(weight*np.multiply(padded[x:x+m,y:y+n],filt)).sum()
                      for y in range(j)] for x in range(i)])
            return c.reshape(image.shape)

from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
class iImage(object):
    def __init__(self, image):
        """Custom Image Class with inbuilt Transforms
        Parameters
        ------------
        image: Numpy nD array for RGB Color Image, or Grayscale Image
        
        Returns
        ------------
        iImage Object
        """
        if len(image.shape)==2:
            image=np.dstack((image,image,image)) #Convert 1 channel image to 3 channel grayscale
        if image.shape[2]==3:                         # 3 Channel Image
            if not self.is3CGrayScale(image):              #Is 3 Channel RGB Image
                self.isRGB=True
                self.OGImage=rgb_to_hsv(image)        
                self.ImageV=self.OGImage[:,:,2]       #Current HSV Image V Channel (Inatialised to Original)
            else:                                    #Is 3 Channel GrayScale
                self.isRGB=False
                self.OGImage=np.dstack((np.zeros(image.shape[:2]),
                                       np.zeros(image.shape[:2]),
                                       image[:,:,0]))            #Use First Channel as Grayscale's VChannel, H and S channel are zeros
                self.ImageV=image[:,:,0]       
        else:
            self.OGImage=image
            self.ImageV=self.OGImage.copy()              #Current GrayScale image
            self.isRGB=False
        
        self.history=[]          #Saves different version of the image transformed over time
        self.text_history=[]

        self.history.append(self.ImageV)
        self.text_history.append('Original Image')

    @classmethod
    def load(cls, path):
        rawImage=Image.open(path).convert('RGB')
        rawImage=np.asarray(rawImage)
        return cls(rawImage)
    
    def save(self, filename):  Image.fromarray(self.RGB).save(filename)
    
    @property
    def RGB(self): image=self.getRGB(); return ((255/image.max())*image).astype('uint8')   #Used to return RGB Image After Transforms 
        

    @property
    def QImage(self): #Retruns QImage wrapper over current image, to be used by Qt's Qpixmap
        return ImageQt.ImageQt(Image.fromarray(self.RGB))

    @property
    def HChannel(self): return self.OGImage[:,:,0] #Return H Channel of the main iIMage object
    @property
    def SChannel(self): return self.OGImage[:,:,1] #Return's S Channel. Both used for assembling HSV image before converting to RGB
    @property
    def VChannel(self): return self.ImageV  #Used to checkout any state in History. Returns VChannel

    @property
    def V(self): return self.ImageV
        
    def getRGB(self, VChannel=None):       #Used to return RGB from custom HSV VChannel
        if VChannel is None: VChannel=self.ImageV
        if self.isRGB: return hsv_to_rgb(np.dstack(
                             (self.HChannel, self.SChannel, VChannel)))
        else: return np.dstack((VChannel, VChannel, VChannel))
        
    def checkout(self,index): #Checkout some image from history. Like Git
        self.ImageV=self.history[index]
        return self
    
    def is3CGrayScale(self, image): #Checks if 3Channnel Image is Greyscale
        return not(False in ((image[:,:,0]==image[:,:,1]) == (image[:,:,1]==image[:,:,2])))
    
    def checkSave(self, transformedImage, save, save_text): 
                                                            
            if save: 
                self.history.append(transformedImage) #If Save=True is passed, save the transformed VChannel in main iIMage object
                self.text_history.append(save_text)
                self.ImageV=transformedImage
                return self
            else:
                return iImage(self.getRGB(VChannel=transformedImage)) #Else return a new temporary iImage object
    
    def fft(self): #Get fft of the main iImage's VChannel, returned a a new temporary iImage object that can be manupulated without touching the mail iImage
        image=self.ImageV.astype(float) 
        image=fp.fftshift(fp.fft2(image) ) #Calc fft and center the zero frequency
        return iImage(image) #return a new object of main iImage's VChannel's fft. only VChannel of this new object will again be extracted by its .ifft() method

    def ifft(self): #Get ifft of the image as a new iImage object
        image=self.ImageV  #Take the current image's v channel (expected to be an frequency domain image), hence should be used after self.fft() only
        image= (fp.ifft2(fp.ifftshift(image))).real #Shift the zero freq to edges and calc inverse fft
        return iImage(image) #return a new temporary iImage object of this ifft image. Only .VChannel will be extracted from it by the mail iImage object.

    def apply_freq_filter(self, parameter_ratio=0.2, mode='highpass', shape="radial"): #radius_ratio is ratio of radius of filter to smallest side of image
            """Applies a mask of passed shape with parameter of shape(side of square or radius of circle)
            """
            
            image=self.VChannel
            parameter=parameter_ratio*min(self.ImageV.shape[:2])/2 #parameter ratio times min of shape of 2d V Channel
            x0,y0= np.asarray(image.shape)/2
            radius=parameter; side=parameter #used in two types of filter masks
            def is_inside(i,j): #Check if i,j is inside the filter radius
                if shape=='square':
                    
                    #return true if pixel (i,j) are inside the square mask of side `side`
                    if ((i>x0-side and i<x0+side) and(j>y0-side and j<y0+side)): return True
                    else: return False
                elif shape=='radial':
                    
                    if ((x0-i)**2+(y0-j)**2)**0.5 < radius: return True #return true if point i,j is inside the radial makk
                    else: return False
            
            if mode=='highpass':
                def inner(i,j): return 0
                def outer(i,j): return image[i,j]
            elif mode=='lowpass':
                def inner(i,j): return image[i,j]
                def outer(i,j): return 0
            else: raise NotImplementedError #other modes of filters are not implemented

            filtered_image= np.asarray([[inner(i,j) if is_inside(i,j) else outer(i,j) for j in range(image.shape[1])] 
                                                                                      for i in range(image.shape[0])])
            return iImage(filtered_image)

    def logTransform_(self, base=None): return self.logTransform(base,save=True) #Inplace (PyTorch Like)
    def logTransform(self, base=None, save=False): #Log  Transforms
        """
        Parameters
        base: base value for Log Transform. default Loge
        save: Save the Transformed Image to History
        """
        import math
        if base:  base = int(base)    #If base is provided, use it, else Natural Log e
        c=255/math.log(1+self.ImageV.max())   #Scaling Constant for Gamma Transform
        if base: func = np.vectorize(lambda x: int(c*math.log(1+x, base))) #element wise log transform
        else:    func = np.vectorize(lambda x: int(c*math.log(1+x)))
        transformedV= func(self.ImageV)
        return self.checkSave(transformedV, save, f'LogT: Base {base}')
    
    def show(self, isFFT=False, axis=None, *args, **kwargs): #Can be used for debugging. shows the RGB image be default. can be used to see frequency spectrum
            import matplotlib.pyplot as plt
            if axis is None: f, axis=plt.subplots(1,1, *args, **kwargs)
            if isFFT:       mapable=axis.imshow(20*np.log10(0.1+self.VChannel).astype(float), cmap=plt.cm.gray, *args, **kwargs)
            elif self.isRGB:mapable=axis.imshow(self.RGB) #Show RGB Image
                #Show Grayscale Image (avoids calling self.getRGB that calls hsv_to_rgb on the image that was caussing image to look really bad)
            else:           mapable=axis.imshow(self.VChannel, cmap=plt.cm.gray, *args, **kwargs) 
            return mapable

    def gammaTransform_(self, gamma=None): return self.gammaTransform(gamma, save=True) #Inplace (PyTorch Like)
    def gammaTransform(self,gamma=None, save=False):
        if gamma is None: self.gamma=1
        else: self.gamma=gamma
        from math import pow
        
        func = np.vectorize(lambda x: pow(x, self.gamma))
        transformedG=func(self.ImageV/self.ImageV.max()) #Gamma of Normalized Image
        transformedG = transformedG*(255/transformedG.max()) #Denormalizing to 8bit
        return self.checkSave(transformedG, save, f'Gamma: {gamma}')
    
    def histEqualization_(self, iterations=1): return self.histEqualization(iterations, save=True) #Inplace (PyTorch Like)
    def histEqualization(self, iterations=1, save=False):
        import numpy as np
        transformedH=np.zeros(shape=self.ImageV.shape)
        for _ in range(iterations):
            pdf,bins=np.histogram(self.ImageV, bins=256, density=True) #Returns PDF at intensity(bin)
            cdf=pdf.cumsum() #calc cdf at each intensity bin
            #normalize histogram,scale by 255  and 8 bit
            transformedH=(np.interp(self.ImageV, bins[:-1], cdf)*255).astype('uint8')
        return self.checkSave(transformedH, save, f'HistogramEQ: {iterations}')
    
    def blur_(self,*args, **kwargs): return self.blur(*args, **kwargs, save=True) #Inplace (PyTorch Like)
    def blur(self, *args, **kwargs): return self.blur_2(*args, **kwargs)
    def blur_1(self, kernelSize=3, save=False):
        """Blur using average filter."""
        if kernelSize<1: kernelSize=1 #Handle all possible human error in kernel size
        elif kernelSize%2!=1:
            if int(kernelSize)%2==1: kernelSize=int(kernelSize)
            else: kernelSize=int(kernelSize)-1
        transformedB=conv2D(self.ImageV, np.ones(shape=(kernelSize,kernelSize)))
        #print(transformedB.shape)
        return self.checkSave(transformedB, save, f'Blur: {kernelSize}')
    
    def blur_2(self, param=5, save=False):
        """Blur using Frequenct Transforms
        passed param is inverse of frequency mask ratio"""
        freq_ratio=5/param #as low ratio gives more blured. Inverse was used to make it more-value = more-blur
        #Apply fft, apply a lowpass radial filter to the fft image and get inverse fft of the modified freq image and grab VChannel of that new object
        # self.fft().apply_freq_filter(freq_ratio, mode='lowpass').ifft().show()
        blured_image=self.fft().apply_freq_filter(freq_ratio, mode='lowpass').ifft().VChannel
        blured_image*=(255/blured_image.max())
        return self.checkSave(blured_image, save, f'Blured: {freq_ratio}')


    def sharpen_(self, weight=0.5): return self.sharpen(weight=weight, save=True)
    def sharpen(self,*args, **kwargs): return self.sharpen_3(*args,**kwargs)
    def sharpen_1(self, weight=0.5, save=False): #Sharpen with unmask sharpening
        if weight<0:  weight = 0
        if weight >1: weight = weight
        # #print(f"Initial Dimension: {self.ImageV.shape}")
        blured=self.blur().V
        blured=blured/blured.max()  #Normalized to max 0-1
        orignal=self.ImageV/self.ImageV.max()
        transformedS = np.add(orignal*(1-weight), np.subtract(orignal, blured)*weight) #Unsharp Masking Wikipedia
        transformedS = np.add(self.ImageV, np.subtract(blured, orignal)*weight)
        # #print((np.subtract(orignal, blured)*weight).max())
        transformedS=np.clip(transformedS, 0, 255)
#         transformedS= transformedS*(255/transformedS.max())
        # #print(f"Final Dimention: {self.ImageV.shape}")

        return self.checkSave(transformedS, save, f'Sharpen: {weight}')

    def sharpen_2(self, weight=0.5, save=False): #Sharpen with convolving  a filter
        """Sharpen using Convolution: Used in V1. Unused Now
        """
        weight/=5 #Scaling as QSlider has only integers
        #kernel from https://nptel.ac.in/courses/117104069/chapter_8/8_32.html
        kernel=0.34*np.asarray([[8 if x==y else -1 for y in range(3)] for x in range(3)])
        image=self.ImageV/self.ImageV.max()
        filtered=conv2D(image, kernel, padding=None, constant_values=0)
        #Avoiding Padding makes image smaller, so adding 0 pad after extracting edges
        filtered=np.pad(filtered, pad_width=int((kernel.shape[0]-1)/2), mode='constant', constant_values=0)
        edges= np.subtract(filtered, image)
        edges=edges*255/edges.max()
        transformedS=np.add(self.ImageV, edges*weight)
        transformedS=np.clip(transformedS, 0, 255)
        return self.checkSave(transformedS, save, f'Sharpen: {weight}')

    def sharpen_3(self, freq_ratio=0.1, freq_mask_shape='radial', save=False, *args, **kwargs):
        """Sharpening Filter using FFT
        Parameters
        -------------
        freq_ratio: ratio of shape parameter(side of square or radius of circle) to smallest side of photo
        freq_mask_shape: ('radial', 'square', 'custom') Shape of zero mask to be used in frequency domain
        Returns
        -------
        New iImage object with Sharpened iImage if save=False, or Same Object with Sharpened image"""
        if   freq_mask_shape=='radial': low=0.005; high=0.05 #By trial and Error. Written in parameters.txt
        elif freq_mask_shape=='square': low=0.01;  high=0.1
        else: raise NotImplementedError
        freq_ratio= low + freq_ratio*(high-low)/20 #Scaling Slider returned value between high and low. slider max=20
    
        image=self.ImageV
        #Apply fft on current VChannel, apply a zero mask on it, take ifft of the modified image, and grab the VChannel of the returned object 
        edge_mask=self.fft().apply_freq_filter(freq_ratio, mode='highpass', shape=freq_mask_shape, *args, **kwargs).ifft().VChannel
        image=image+edge_mask #Combine edge mask and orignal image
        image*(255/image.max()) #Normalize for 8  bit
        return self.checkSave(image, save, f'Sharpened: {freq_ratio}')

if __name__=="__main__":
    image=iImage.load("/home/sufiyan/Pictures/Screenshot from 2018-08-24 14-11-32.png")
    import matplotlib.pyplot as plt
    plt.imshow(image.sharpen(5).show())
