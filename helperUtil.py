import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def readImagesFromFolder(folderName):
    imagesArr = []
    for fileName in os.listdir(folderName):
        curImg = cv2.imread(os.path.join(folderName, fileName))
        if (curImg is not None):
            imagesArr.append(curImg)
    return imagesArr

def readGrayImagesFromFolder(folderName):
    imagesArr = []
    for fileName in os.listdir(folderName):
        curImg = cv2.imread(os.path.join(folderName, fileName), 0)
        if (curImg is not None):
            imagesArr.append(curImg)
    return imagesArr

def fixImageIntensity(intensity):
    if (intensity < 0):
        intensity = 0
    elif (intensity > 255):
        intensity = 255
    return intensity

def addImages(img1, img2):
    tempImg = img1.copy()
    for i in range(0, len(img1[0])):
        for j in range(0, len(img1[1])):
            addedIntensityVal = img1[i][j] + img2[i][j]
            fixedIntesityVal = fixImageIntensity(addedIntensityVal)
            tempImg[i][j] = fixedIntesityVal
    return tempImg

def regExclusion(img, channel):
    copiedImg = img.copy()
    if(channel == 'B'):
        copiedImg[:,:,0] = 0
    if(channel == 'G'):
        copiedImg[:,:,1] = 0
    if(channel == 'R'):
        copiedImg[:,:,2] = 0
    return copiedImg

def convolve(img,filter):
    #flipped filter b/c in convolution filter is flipped. if i donot flip filter it would become correlation
    copiedImg = img.copy()
    filter = np.flip(filter)
    curImgRowCount = len(copiedImg[0])
    curImgColCount = len(copiedImg[1])
    filterRowCount = len(filter[0])
    filterColCount = len(filter[1])
    startImgRowIndex = filterRowCount//2
    startImgColIndex = filterColCount//2
    endImgRowIndex = curImgRowCount - startImgRowIndex
    endImgColIndex = curImgColCount - startImgColIndex
    filterNormalizationFactor = np.sum(filter)
    if (filterNormalizationFactor <= 0):
        filterNormalizationFactor = 1
    for curImgRowIndex in range (startImgRowIndex, endImgRowIndex):
         for curImgColIndex in range (startImgColIndex, endImgColIndex):
             sumOfProduct = 0
             orgRowIndex = -(filterRowCount//2)
             orgColIndex = -(filterColCount//2)
             for filterRowIndex in range (orgRowIndex, (filterRowCount//2)+1):
                 for filterColIndex in range (orgColIndex, (filterColCount//2)+1):
                     operandImgRowIndex = curImgRowIndex+filterRowIndex
                     operandImgColIndex = curImgColIndex+filterColIndex
                     operandFilterRowIndex = filterRowIndex+ filterRowCount//2
                     operandFilterColIndex = filterColIndex+filterColCount//2
                     imgPixelVal = img[operandImgRowIndex][operandImgColIndex]
                     filterPixelVal = filter[operandFilterRowIndex][operandFilterColIndex]
                     sumOfProduct +=  imgPixelVal * filterPixelVal
             normalizedValue = sumOfProduct // filterNormalizationFactor
             normalizedValue = fixImageIntensity(normalizedValue)
             copiedImg[curImgRowIndex][curImgColIndex] = normalizedValue
    return copiedImg
