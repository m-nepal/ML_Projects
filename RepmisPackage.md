# Repmis Examples
Following document shows examples of functions that are available in repmis package.

# Install repmis package. 


## Git_stamp example
For this function to work, make sure you have git installed. You should have git and R studio linked by now. If not, please go through the video lectures again. Installation for git: <https://git-scm.com/>


```r
git_stamp(repo = 'D:/ML_Projects/')
```

```
##                                     commit 
## "58c13500442750c5732bc5dbb4662d20000011a5" 
##                                     branch 
##                                   "master" 
##                                    message 
##                           "Add Iris Excel"
```
The repo should be a local repository (which is not hosted on github but is stored on your local machine). The function will return the latest git commit and the corresponding message and the cmmit id. 

## Install Old Packages
This function installs older versions of packages you require. Use this function with care, since this replaces the latest version of the package if you already have it installed. Please revert back to the latest version of the package by using *install.packages()*.


```r
InstallOldPackages(pkgs = 'gtools', versions = "2.6.1")
```

```
## Installing package into 'C:/Users/Raunak Mundada/Documents/R/win-library/3.4'
## (as 'lib' is unspecified)
```

```
## Warning: running command '"C:/PROGRA~1/R/R-34~1.0/bin/x64/R" CMD
## INSTALL -l "C:\Users\Raunak Mundada\Documents\R\win-library\3.4"
## "gtools_2.6.1.tar.gz"' had status 1
```

```
## Warning in install.packages(TempFile, repos = NULL, type = "source", lib
## = lib): installation of package 'gtools_2.6.1.tar.gz' had non-zero exit
## status
```

```
##     pkgs V1
## 1 gtools  0
```
<!-- This does not work anymore. I was unable to figure out the reason.  -->
<!-- Alternatively, -->
<!-- ```{r devtools} -->
<!-- require(devtools) -->
<!-- install_version("ggplot2", version = "0.9.1", repos = "http://cran.us.r-project.org") -->
<!-- ``` -->
<!-- devtools (<https://cran.r-project.org/web/packages/devtools/devtools.pdf>) is a package that lets you work with development versions of different packages available on cran. -->

## Load and Cite
This function will install packages and automaticall create a bibTex file citing the packages. Easy way to publish!


```r
LoadandCite(pkgs = 'ggplot2', file='D:/MSDS6306/Jan2017/citations.bib')
```
The citation file is created at the file location.

## Scan HTTPS
Read a character text file from a secure site into R.


```r
data1 <- scan_https(url='https://fivethirtyeight.com/')
```

```
## SHA-1 hash of file is 39faede2703deb328ac8abe5b868010fd3d58b3f
```

## Set valid working directory
Set a valid working directory from a list of directories. 


```r
set_valid_wd(c('D:/MSDS6306/Jan2017/','D:/MSDS6306/Jan2017/DoesNotExist'))
```

```
## No valid directory found.
```

```r
print(getwd())
```

```
## [1] "D:/MSDS6306/Summer2017"
```

## Source Data
Load plain-text data and RData from a URL (either http or https)


```r
iris <- source_data(url='http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data')
```

```
## Downloading data from: http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
```

```
## SHA-1 hash of the downloaded data file is:
## d11777fac6574637a4ec5f0effeab8542ae88b65
```

```r
iris <- data.frame(iris)
head(iris)
```

```
##    V1  V2  V3  V4          V5
## 1 5.1 3.5 1.4 0.2 Iris-setosa
## 2 4.9 3.0 1.4 0.2 Iris-setosa
## 3 4.7 3.2 1.3 0.2 Iris-setosa
## 4 4.6 3.1 1.5 0.2 Iris-setosa
## 5 5.0 3.6 1.4 0.2 Iris-setosa
## 6 5.4 3.9 1.7 0.4 Iris-setosa
```

## source xlsx data

```r
library(xlsx)
```

```
## Loading required package: rJava
```

```
## Loading required package: xlsxjars
```

```r
data2 <- source_XlsxData(url='https://github.com/raunakm90/ML_Projects/blob/master/Iris_Data.xlsx?raw=true',sheet = 1)
```

```
## Downloading data from: https://github.com/raunakm90/ML_Projects/blob/master/Iris_Data.xlsx?raw=true
```

```
## SHA-1 hash of the downloaded data file is:
## eeae66d55d26e585d61e2d67023e4e693fe1c606
```

```r
head(data2)
```

```
##   sepal_length sepal_width petal_length petal_width       class
## 1          5.1         3.5          1.4         0.2 Iris-setosa
## 2          4.9         3.0          1.4         0.2 Iris-setosa
## 3          4.7         3.2          1.3         0.2 Iris-setosa
## 4          4.6         3.1          1.5         0.2 Iris-setosa
## 5          5.0         3.6          1.4         0.2 Iris-setosa
## 6          5.4         3.9          1.7         0.4 Iris-setosa
```
This will download an excel file hosted on the web.

Note - You may have issues with your xlsx package, rJava and Java. Please follow these steps to resolve the issue - 

1. Install/Update Java. ([Dowload Java]https://www.java.com/en/download/). For windows machine, install it at "C:/Program Files" which will be default for most.
2. Set your JAVA_HOME variable in RStudio. Use the command - *Sys.setenv("JAVA_HOME"="C:/Program Files/Java/jdk1.8.0_73/jre/")*
3. Install rJava package - *install.packages("rJava")*.
4. Install xlsx package. *install.packages("xlsx")*

After you finish all these steps, *source_XlsxData()* should work.

Hope this is helpful!
