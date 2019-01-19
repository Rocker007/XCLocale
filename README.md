# XCLocale.py
XCLocale.py is tool to check syntax error for Localization string in iOS Project which is not discovered by Xcode and also tells if any localization string is missed in any localization String file.

## Getting Started
Copy this file in you local directory and give execute permission to this.

```
$ sudo chmod 777  XCLocale.py 
```

### Tool usage
    Usage: XCLocale.py [options] --file filename

    Options:

        -h, --help                  show this help message and exit
  
        -v, --version               Show the XCLocale version
  
        -m, --missig_localization   Generate a .CVS report for all missing localized string in current directory
                        
        -c, --check_syntax          This will check for errors if exist in localized string file
                        
        -d, --check_duplicate       This will check for duplicate localization keys and values
                        
        -f FILENAME, --file=FILENAME [Required] to pass Xcode project path
  
### Example
```
1. ./XCLocale.py -mf <iOS project path>
```
This will generate .CVS report where row is localization keys and column is language of missing localization string.

![report](https://github.com/Rocker007/XCLocale/blob/master/Image%20/Report.png)


```
2. ./XCLocale.py -cf <iOS project path>
```
This will check all localization string file in project for any syntax error.


**Output:**<br/>

      =============================================================
       File: Localization/en.lproj/Localizable.strings
      =============================================================
      [ERROR: ] Line:1 #"HomeController.screenTitle" =  "Screen1";

      =============================================================
      File: Localization/de.lproj/Localizable.strings
      =============================================================
      [ERROR: ] Line:6 "button.title" = "hinzufügen"

<br/>
<br/>


```
3. ./XCLocale.py -df <iOS project path>
```
This will check for all duplicate key and localized string in project file

**Output:**<br/>

      =============================================================
      File: Localization/zh-Hant.lproj/Localizable.strings
      =============================================================
      [WARNING: ]  Duplicate localization keys
      ------------------------------------------
        1. home.deleteBtn

      [WARNING: ]  Duplicate translations
      ---------------------------------------
        1. 添加
