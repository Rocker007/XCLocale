#!/usr/bin/python
#coding:utf-8

# ==================================================================================
# The MIT License (MIT)

# Copyright (c) 2018 Deepak Pandey

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =================================================================================


# XCLocale.py
# Author: Deepak Pandey
# Email: deepak.pandey07@gmail.com
# Version: 1.0


import os, sys, re, shutil, getopt, fnmatch,optparse,codecs,collections
from optparse import OptionParser

ver = '1.0'

class localizationData (object):
     def __init__(self, lConst, key, comment=None):
        self.lConst = lConst
        self.key = key
        self.comment = comment

class LTool (object):
    
    def __init__(self):
        self.LocalizedStringList = []
        self.localizationFilePathDict = {}
        self.missinglocatization = {}
        """
            iOS Localization id for all supported lanagauge is copied from https://gist.github.com/jacobbubu/1836273#file-ioslocaleidentifiers-csv with some modification.
        """
        self.allSupportedLangDict = {
            "af":"Afrikaans",
            "af-NA":"Afrikaans (Namibia)",
            "af-ZA":"Afrikaans (South Africa)",
            "ak":"Akan",
            "ak-GH":"Akan (Ghana)",
            "am":"Amharic",
            "am-ET":"Amharic (Ethiopia)",
            "ar":"Arabic",
            "ar-AE":"Arabic (United Arab Emirates)",
            "ar-BH":"Arabic (Bahrain)",
            "ar-DZ":"Arabic (Algeria)",
            "ar-EG":"Arabic (Egypt)",
            "ar-IQ":"Arabic (Iraq)",
            "ar-JO":"Arabic (Jordan)",
            "ar-KW":"Arabic (Kuwait)",
            "ar-LB":"Arabic (Lebanon)",
            "ar-LY":"Arabic (Libya)",
            "ar-MA":"Arabic (Morocco)",
            "ar-OM":"Arabic (Oman)",
            "ar-QA":"Arabic (Qatar)",
            "ar-SA":"Arabic (Saudi Arabia)",
            "ar-SD":"Arabic (Sudan)",
            "ar-SY":"Arabic (Syria)",
            "ar-TN":"Arabic (Tunisia)",
            "ar-YE":"Arabic (Yemen)",
            "as":"Assamese",
            "as-IN":"Assamese (India)",
            "asa":"Asu",
            "asa-TZ":"Asu (Tanzania)",
            "az":"Azerbaijani",
            "az-Cyrl":"Azerbaijani (Cyrillic)",
            "az-Cyrl-AZ":"Azerbaijani (Cyrillic  Azerbaijan)",
            "az-Latn":"Azerbaijani (Latin)",
            "az-Latn-AZ":"Azerbaijani (Latin   Azerbaijan)",
            "be":"Belarusian",
            "be-BY":"Belarusian (Belarus)",
            "bem":"Bemba",
            "bem-ZM":"Bemba (Zambia)",
            "bez":"Bena",
            "bez-TZ":"Bena (Tanzania)",
            "bg":"Bulgarian",
            "bg-BG":"Bulgarian (Bulgaria)",
            "bm":"Bambara",
            "bm-ML":"Bambara (Mali)",
            "bn":"Bengali",
            "bn-BD":"Bengali (Bangladesh)",
            "bn-IN":"Bengali (India)",
            "bo":"Tibetan",
            "bo-CN":"Tibetan (China)",
            "bo-IN":"Tibetan (India)",
            "bs":"Bosnian",
            "bs-BA":"Bosnian (Bosnia and Herzegovina)",
            "ca":"Catalan",
            "ca-ES":"Catalan (Spain)",
            "cgg":"Chiga",
            "cgg-UG":"Chiga (Uganda)",
            "chr":"Cherokee",
            "chr-US":"Cherokee (United States)",
            "cs":"Czech",
            "cs-CZ":"Czech (Czech Republic)",
            "cy":"Welsh",
            "cy-GB":"Welsh (United Kingdom)",
            "da":"Danish",
            "da-DK":"Danish (Denmark)",
            "dav":"Taita",
            "dav-KE":"Taita (Kenya)",
            "de":"German",
            "de-AT":"German (Austria)",
            "de-BE":"German (Belgium)",
            "de-CH":"German (Switzerland)",
            "de-DE":"German (Germany)",
            "de-LI":"German (Liechtenstein)",
            "de-LU":"German (Luxembourg)",
            "ebu":"Embu",
            "ebu-KE":"Embu (Kenya)",
            "ee":"Ewe",
            "ee-GH":"Ewe (Ghana)",
            "ee-TG":"Ewe (Togo)",
            "el":"Greek",
            "el-CY":"Greek (Cyprus)",
            "el-GR":"Greek (Greece)",
            "en":"English",
            "en-AS":"English (American Samoa)",
            "en-AU":"English (Australia)",
            "en-BE":"English (Belgium)",
            "en-BW":"English (Botswana)",
            "en-BZ":"English (Belize)",
            "en-CA":"English (Canada)",
            "en-GB":"English (United Kingdom)",
            "en-GU":"English (Guam)",
            "en-HK":"English (Hong Kong SAR China)",
            "en-IE":"English (Ireland)",
            "en-IN":"English (India)",
            "en-JM":"English (Jamaica)",
            "en-MH":"English (Marshall Islands)",
            "en-MP":"English (Northern Mariana Islands)",
            "en-MT":"English (Malta)",
            "en-MU":"English (Mauritius)",
            "en-NA":"English (Namibia)",
            "en-NZ":"English (New Zealand)",
            "en-PH":"English (Philippines)",
            "en-PK":"English (Pakistan)",
            "en-SG":"English (Singapore)",
            "en-TT":"English (Trinidad and Tobago)",
            "en-UM":"English (U.S. Minor Outlying Islands)",
            "en-US":"English (United States)",
            "en-US-POSIX":"English (United States  Computer)",
            "en-VI":"English (U.S. Virgin Islands)",
            "en-ZA":"English (South Africa)",
            "en-ZW":"English (Zimbabwe)",
            "eo":"Esperanto",
            "es":"Spanish",
            "es-419":"Spanish (Latin America)",
            "es-AR":"Spanish (Argentina)",
            "es-BO":"Spanish (Bolivia)",
            "es-CL":"Spanish (Chile)",
            "es-CO":"Spanish (Colombia)",
            "es-CR":"Spanish (Costa Rica)",
            "es-DO":"Spanish (Dominican Republic)",
            "es-EC":"Spanish (Ecuador)",
            "es-ES":"Spanish (Spain)",
            "es-GQ":"Spanish (Equatorial Guinea)",
            "es-GT":"Spanish (Guatemala)",
            "es-HN":"Spanish (Honduras)",
            "es-MX":"Spanish (Mexico)",
            "es-NI":"Spanish (Nicaragua)",
            "es-PA":"Spanish (Panama)",
            "es-PE":"Spanish (Peru)",
            "es-PR":"Spanish (Puerto Rico)",
            "es-PY":"Spanish (Paraguay)",
            "es-SV":"Spanish (El Salvador)",
            "es-US":"Spanish (United States)",
            "es-UY":"Spanish (Uruguay)",
            "es-VE":"Spanish (Venezuela)",
            "et":"Estonian",
            "et-EE":"Estonian (Estonia)",
            "eu":"Basque",
            "eu-ES":"Basque (Spain)",
            "fa":"Persian",
            "fa-AF":"Persian (Afghanistan)",
            "fa-IR":"Persian (Iran)",
            "ff":"Fulah",
            "ff-SN":"Fulah (Senegal)",
            "fi":"Finnish",
            "fi-FI":"Finnish (Finland)",
            "fil":"Filipino",
            "fil-PH":"Filipino (Philippines)",
            "fo":"Faroese",
            "fo-FO":"Faroese (Faroe Islands)",
            "fr":"French",
            "fr-BE":"French (Belgium)",
            "fr-BF":"French (Burkina Faso)",
            "fr-BI":"French (Burundi)",
            "fr-BJ":"French (Benin)",
            "fr-BL":"French (Saint BarthÃ©lemy)",
            "fr-CA":"French (Canada)",
            "fr-CD":"French (Congo - Kinshasa)",
            "fr-CF":"French (Central African Republic)",
            "fr-CG":"French (Congo - Brazzaville)",
            "fr-CH":"French (Switzerland)",
            "fr-CI":"",
            "fr-CM":"French (Cameroon)",
            "fr-DJ":"French (Djibouti)",
            "fr-FR":"French (France)",
            "fr-GA":"French (Gabon)",
            "fr-GN":"French (Guinea)",
            "fr-GP":"French (Guadeloupe)",
            "fr-GQ":"French (Equatorial Guinea)",
            "fr-KM":"French (Comoros)",
            "fr-LU":"French (Luxembourg)",
            "fr-MC":"French (Monaco)",
            "fr-MF":"French (Saint Martin)",
            "fr-MG":"French (Madagascar)",
            "fr-ML":"French (Mali)",
            "fr-MQ":"French (Martinique)",
            "fr-NE":"French (Niger)",
            "fr-RE":"French (RÃ©union)",
            "fr-RW":"French (Rwanda)",
            "fr-SN":"French (Senegal)",
            "fr-TD":"French (Chad)",
            "fr-TG":"French (Togo)",
            "ga":"Irish",
            "ga-IE":"Irish (Ireland)",
            "gl":"Galician",
            "gl-ES":"Galician (Spain)",
            "gsw":"Swiss German",
            "gsw-CH":"Swiss German (Switzerland)",
            "gu":"Gujarati",
            "gu-IN":"Gujarati (India)",
            "guz":"Gusii",
            "guz-KE":"Gusii (Kenya)",
            "gv":"Manx",
            "gv-GB":"Manx (United Kingdom)",
            "ha":"Hausa",
            "ha-Latn":"Hausa (Latin)",
            "ha-Latn-GH":"Hausa (Latin  Ghana)",
            "ha-Latn-NE":"Hausa (Latin  Niger)",
            "ha-Latn-NG":"Hausa (Latin  Nigeria)",
            "haw":"Hawaiian",
            "haw-US":"Hawaiian (United States)",
            "he":"Hebrew",
            "he-IL":"Hebrew (Israel)",
            "hi":"Hindi",
            "hi-IN":"Hindi (India)",
            "hr":"Croatian",
            "hr-HR":"Croatian (Croatia)",
            "hu":"Hungarian",
            "hu-HU":"Hungarian (Hungary)",
            "hy":"Armenian",
            "hy-AM":"Armenian (Armenia)",
            "id":"Indonesian",
            "id-ID":"Indonesian (Indonesia)",
            "ig":"Igbo",
            "ig-NG":"Igbo (Nigeria)",
            "ii":"Sichuan Yi",
            "ii-CN":"Sichuan Yi (China)",
            "is":"Icelandic",
            "is-IS":"Icelandic (Iceland)",
            "it":"Italian",
            "it-CH":"Italian (Switzerland)",
            "it-IT":"Italian (Italy)",
            "ja":"Japanese",
            "ja-JP":"Japanese (Japan)",
            "jmc":"Machame",
            "jmc-TZ":"Machame (Tanzania)",
            "ka":"Georgian",
            "ka-GE":"Georgian (Georgia)",
            "kab":"Kabyle",
            "kab-DZ":"Kabyle (Algeria)",
            "kam":"Kamba",
            "kam-KE":"Kamba (Kenya)",
            "kde":"Makonde",
            "kde-TZ":"Makonde (Tanzania)",
            "kea":"Kabuverdianu",
            "kea-CV":"Kabuverdianu (Cape Verde)",
            "khq":"Koyra Chiini",
            "khq-ML":"Koyra Chiini (Mali)",
            "ki":"Kikuyu",
            "ki-KE":"Kikuyu (Kenya)",
            "kk":"Kazakh",
            "kk-Cyrl":"Kazakh (Cyrillic)",
            "kk-Cyrl-KZ":"Kazakh (Cyrillic  Kazakhstan)",
            "kl":"Kalaallisut",
            "kl-GL":"Kalaallisut (Greenland)",
            "kln":"Kalenjin",
            "kln-KE":"Kalenjin (Kenya)",
            "km":"Khmer",
            "km-KH":"Khmer (Cambodia)",
            "kn":"Kannada",
            "kn-IN":"Kannada (India)",
            "ko":"Korean",
            "ko-KR":"Korean (South Korea)",
            "kok":"Konkani",
            "kok-IN":"Konkani (India)",
            "kw":"Cornish",
            "kw-GB":"Cornish (United Kingdom)",
            "lag":"Langi",
            "lag-TZ":"Langi (Tanzania)",
            "lg":"Ganda",
            "lg-UG":"Ganda (Uganda)",
            "lt":"Lithuanian",
            "lt-LT":"Lithuanian (Lithuania)",
            "luo":"Luo",
            "luo-KE":"Luo (Kenya)",
            "luy":"Luyia",
            "luy-KE":"Luyia (Kenya)",
            "lv":"Latvian",
            "lv-LV":"Latvian (Latvia)",
            "mas":"Masai",
            "mas-KE":"Masai (Kenya)",
            "mas-TZ":"Masai (Tanzania)",
            "mer":"Meru",
            "mer-KE":"Meru (Kenya)",
            "mfe":"Morisyen",
            "mfe-MU":"Morisyen (Mauritius)",
            "mg":"Malagasy",
            "mg-MG":"Malagasy (Madagascar)",
            "mk":"Macedonian",
            "mk-MK":"Macedonian (Macedonia)",
            "ml":"Malayalam",
            "ml-IN":"Malayalam (India)",
            "mr":"Marathi",
            "mr-IN":"Marathi (India)",
            "ms":"Malay",
            "ms-BN":"Malay (Brunei)",
            "ms-MY":"Malay (Malaysia)",
            "mt":"Maltese",
            "mt-MT":"Maltese (Malta)",
            "my":"Burmese",
            "my-MM":"Burmese (Myanmar [Burma])",
            "naq":"Nama",
            "naq-NA":"Nama (Namibia)",
            "nb":"Norwegian Bokmål",
            "nb-NO":"Norwegian BokmÃ¥l (Norway)",
            "nd":"North Ndebele",
            "nd-ZW":"North Ndebele (Zimbabwe)",
            "ne":"Nepali",
            "ne-IN":"Nepali (India)",
            "ne-NP":"Nepali (Nepal)",
            "nl":"Dutch",
            "nl-BE":"Dutch (Belgium)",
            "nl-NL":"Dutch (Netherlands)",
            "nn":"Norwegian Nynorsk",
            "nn-NO":"Norwegian Nynorsk (Norway)",
            "nyn":"Nyankole",
            "nyn-UG":"Nyankole (Uganda)",
            "om":"Oromo",
            "om-ET":"Oromo (Ethiopia)",
            "om-KE":"Oromo (Kenya)",
            "or":"Oriya",
            "or-IN":"Oriya (India)",
            "pa":"Punjabi",
            "pa-Arab":"Punjabi (Arabic)",
            "pa-Arab-PK":"Punjabi (Arabic  Pakistan)",
            "pa-Guru":"Punjabi (Gurmukhi)",
            "pa-Guru-IN":"Punjabi (Gurmukhi  India)",
            "pl":"Polish",
            "pl-PL":"Polish (Poland)",
            "ps":"Pashto",
            "ps-AF":"Pashto (Afghanistan)",
            "pt":"Portuguese",
            "pt-BR":"Portuguese (Brazil)",
            "pt-GW":"Portuguese (Guinea-Bissau)",
            "pt-MZ":"Portuguese (Mozambique)",
            "pt-PT":"Portuguese (Portugal)",
            "rm":"Romansh",
            "rm-CH":"Romansh (Switzerland)",
            "ro":"Romanian",
            "ro-MD":"Romanian (Moldova)",
            "ro-RO":"Romanian (Romania)",
            "rof":"Rombo",
            "rof-TZ":"Rombo (Tanzania)",
            "ru":"Russian",
            "ru-MD":"Russian (Moldova)",
            "ru-RU":"Russian (Russia)",
            "ru-UA":"Russian (Ukraine)",
            "rw":"Kinyarwanda",
            "rw-RW":"Kinyarwanda (Rwanda)",
            "rwk":"Rwa",
            "rwk-TZ":"Rwa (Tanzania)",
            "saq":"Samburu",
            "saq-KE":"Samburu (Kenya)",
            "seh":"Sena",
            "seh-MZ":"Sena (Mozambique)",
            "ses":"Koyraboro Senni",
            "ses-ML":"Koyraboro Senni (Mali)",
            "sg":"Sango",
            "sg-CF":"Sango (Central African Republic)",
            "shi":"Tachelhit",
            "shi-Latn":"Tachelhit (Latin)",
            "shi-Latn-MA":"Tachelhit (Latin  Morocco)",
            "shi-Tfng":"Tachelhit (Tifinagh)",
            "shi-Tfng-MA":"Tachelhit (Tifinagh  Morocco)",
            "si":"Sinhala",
            "si-LK":"Sinhala (Sri Lanka)",
            "sk":"Slovak",
            "sk-SK":"Slovak (Slovakia)",
            "sl":"Slovenian",
            "sl-SI":"Slovenian (Slovenia)",
            "sn":"Shona",
            "sn-ZW":"Shona (Zimbabwe)",
            "so":"Somali",
            "so-DJ":"Somali (Djibouti)",
            "so-ET":"Somali (Ethiopia)",
            "so-KE":"Somali (Kenya)",
            "so-SO":"Somali (Somalia)",
            "sq":"Albanian",
            "sq-AL":"Albanian (Albania)",
            "sr":"Serbian",
            "sr-Cyrl":"Serbian (Cyrillic)",
            "sr-Cyrl-BA":"Serbian (Cyrillic  Bosnia and Herzegovina)",
            "sr-Cyrl-ME":"Serbian (Cyrillic  Montenegro)",
            "sr-Cyrl-RS":"Serbian (Cyrillic  Serbia)",
            "sr-Latn":"Serbian (Latin)",
            "sr-Latn-BA":"Serbian (Latin  Bosnia and Herzegovina)",
            "sr-Latn-ME":"Serbian (Latin  Montenegro)",
            "sr-Latn-RS":"Serbian (Latin  Serbia)",
            "sv":"Swedish",
            "sv-FI":"Swedish (Finland)",
            "sv-SE":"Swedish (Sweden)",
            "sw":"Swahili",
            "sw-KE":"Swahili (Kenya)",
            "sw-TZ":"Swahili (Tanzania)",
            "ta":"Tamil",
            "ta-IN":"Tamil (India)",
            "ta-LK":"Tamil (Sri Lanka)",
            "te":"Telugu",
            "te-IN":"Telugu (India)",
            "teo":"Teso",
            "teo-KE":"Teso (Kenya)",
            "teo-UG":"Teso (Uganda)",
            "th":"Thai",
            "th-TH":"Thai (Thailand)",
            "ti":"Tigrinya",
            "ti-ER":"Tigrinya (Eritrea)",
            "ti-ET":"Tigrinya (Ethiopia)",
            "to":"Tonga",
            "to-TO":"Tonga (Tonga)",
            "tr":"Turkish",
            "tr-TR":"Turkish (Turkey)",
            "tzm":"Central Morocco Tamazight",
            "tzm-Latn":"Central Morocco Tamazight (Latin)",
            "tzm-Latn-MA":"Central Morocco Tamazight (Latin  Morocco)",
            "uk":"Ukrainian",
            "uk-UA":"Ukrainian (Ukraine)",
            "ur":"Urdu",
            "ur-IN":"Urdu (India)",
            "ur-PK":"Urdu (Pakistan)",
            "uz":"Uzbek",
            "uz-Arab":"Uzbek (Arabic)",
            "uz-Arab-AF":"Uzbek (Arabic  Afghanistan)",
            "uz-Cyrl":"Uzbek (Cyrillic)",
            "uz-Cyrl-UZ":"Uzbek (Cyrillic  Uzbekistan)",
            "uz-Latn":"Uzbek (Latin)",
            "uz-Latn-UZ":"Uzbek (Latin  Uzbekistan)",
            "vi":"Vietnamese",
            "vi-VN":"Vietnamese (Vietnam)",
            "vun":"Vunjo",
            "vun-TZ":"Vunjo (Tanzania)",
            "xog":"Soga",
            "xog-UG":"Soga (Uganda)",
            "yo":"Yoruba",
            "yo-NG":"Yoruba (Nigeria)",
            "zh":"Chinese",
            "zh-Hans":"Chinese (Simplified)",
            "zh-Hans-CN":"Chinese (Simplified Han  China)",
            "zh-Hans-HK":"Chinese (Simplified Han  Hong Kong SAR China)",
            "zh-Hans-MO":"Chinese (Simplified Han  Macau SAR China)",
            "zh-Hans-SG":"Chinese (Simplified Han  Singapore)",
            "zh-Hant":"Chinese (Traditional)",
            "zh-Hant-HK":"Chinese (Traditional Han  Hong Kong SAR China)",
            "zh-Hant-MO":"Chinese (Traditional Han  Macau SAR China)",
            "zh-Hant-TW":"Chinese (Traditional Han  Taiwan)",
            "zu":"Zulu",
            "zu-ZA":"Zulu (South Africa)",
        }

    def isIgnoreFolder(str,src) :
        ignoreFolder = False
        if src == '.git' or src.endswith('.xcassets') or src.endswith( '.xcodeproj') or src == '.svn' or src.endswith('.framework') or src.endswith( '.app'):
            ignoreFolder = True
        return ignoreFolder
                
    def isIgnoredCaseLine(self,line) :
        ignoreCase = False
        ignoreCaseRegx = re.compile('^[/\*|//]+',re.MULTILINE)
        filterLine = line.rstrip("u'\\n'")
        result = re.search(ignoreCaseRegx,line)
        if result or (len(filterLine) == 0):
            ignoreCase = True
        return ignoreCase

    def getLocalizeKeyValue(self, filePath):
        fileLocalizationKeyValue = []
        validPattern = re.compile('^\s*\"(.*?)\"\s*=\s*\"(.*?)\"\s*\;',re.DOTALL)
        with codecs.open(filePath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                patternMatched = re.search(validPattern,line)
                if patternMatched :
                    dict = {}
                    dict[patternMatched.group(1)] = patternMatched.group(2)
                    fileLocalizationKeyValue.append(dict)
        f.close()
        return fileLocalizationKeyValue

    def printFileHeader(self, filePath):
        print('\n')
        print "============================================================================"
        print "File: "+ filePath
        print "============================================================================"


    def getAlllocalizedkeys(self,src):
        for item in os.listdir(src):
            path = os.path.join(src, item)
            if os.path.isdir(path):
                self.getAlllocalizedkeys(path)
            else:
                self.searchlocalizedkeys(path)

    def searchlocalizedkeys(self, file):
        if file.endswith('.m') or file.endswith('.swift') or file.endswith('.h'):
            localizeStringPattern = re.compile('^(\s*#define|\s*let|\s*static\s*let)\s*(.*?)\s*=?\s*NSLocalizedString\s*\(@?\s*\"(.*?)\"\s*,\s*(nil|@|comment:)\s*@?(\"(.*?)\")?', re.DOTALL)
            with open(file) as f:
                lines = f.readlines()
                for line in lines:
                    searchResult = re.search(localizeStringPattern,line)
                    if searchResult:
                        self.addlocalizedString(searchResult.group(2),searchResult.group(3),searchResult.group(6))
            f.close()

    def addlocalizedString(self, lConst, key, comment):
        lObject = localizationData(lConst, key, comment)
        self.LocalizedStringList.append(lObject)

    def getAllLocalizationFilePathsMapping(self,src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            if self.isIgnoreFolder(item):
                continue
            if s.endswith('.lproj'):
                localizedStringfilePath = os.path.join(s,'Localizable.strings')
                if os.path.exists(localizedStringfilePath):
                    langCode = (os.path.splitext(item)[0])
                    self.localizationFilePathDict[langCode] = localizedStringfilePath
            else : 
                if os.path.isdir(s):
                    self.getAllLocalizationFilePathsMapping(s)


    def getToolVersion(self):
        print 'XCLocale Version: '+ ver
    

    def showAllMissingLocalization(self, src):
        self.getAllLocalizationFilePathsMapping(src)
        for lObject in self.LocalizedStringList :
            for langCode, filePath in self.localizationFilePathDict.items() :
                langDictList = self.getLocalizeKeyValue(filePath)
                if not next((i for i,dict in enumerate(langDictList) if lObject.key in dict), None):
                    if lObject.key in self.missinglocatization.keys():
                        dict = self.missinglocatization[lObject.key]
                    else :
                        dict = {}
                    dict[langCode] = "Missing"
                    self.missinglocatization[lObject.key] = dict
        self.generateMissingLocalizationReport()
        

    def generateMissingLocalizationReport(self):
        allSupportedLangkeys = self.localizationFilePathDict.keys()
        filename = "MissingLocalizationReport.csv"
        if self.missinglocatization :
            fo = open(filename,'w+')
            fo.write("\n")
            fo.write("\n")
            fo.write("Missing Localization Report"+"\n")
            fo.write("\n")
            fo.write("\n")
            fo.write("S.No, Key |Langauage code")
            sn = 0
            for key in allSupportedLangkeys:
                fo.write(","+self.allSupportedLangDict[key]+" ("+ key +" )")
            fo.write("\n")
            for key,langObj in self.missinglocatization.items():
                sn = sn + 1
                fo.write(`sn`+","+key)
                for key in allSupportedLangkeys:
                   
                    if key in langObj.keys():
                        fo.write("," + langObj[key])
                    else :
                        fo.write("," + " ")
                fo.write("\n ")
            
            fo.close()
            print "[INFO: ] Missing localization report is generated at "+'"'+ os.getcwd()+'/'+filename+'"'
        else:
            print "[INFO: ] There is no missing key in all supported localization string files."

    
    def validateLocalizedFile(self,src):
        self.getAllLocalizationFilePathsMapping(src)
        validPattern = re.compile('^\s*\"(.*?)\"\s*=\s*\"(.*?)\"\s*\;',re.DOTALL)
        foundError = False
        for langCode, filePath in self.localizationFilePathDict.items() :
            with codecs.open(filePath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                lineNo = 0
                canPrintFileName = True
                for line in lines:
                    filterLine = line.lstrip().rstrip()
                    lineNo = lineNo + 1
                    if not self.isIgnoredCaseLine(filterLine):
                        patternMatched = re.search(validPattern,filterLine)
                        if not patternMatched :
                            if canPrintFileName:
                                self.printFileHeader(filePath)
                                canPrintFileName = False
                            foundError = True    
                            print "[ERROR: ] Line:" + str(lineNo) + " " + line.rstrip('\n')
            f.close()
        if not foundError :  
            print "[INFO: ] There is no error in localization string files."                     


    def  checheckDuplicatekeysValues(self,src) :
        self.getAllLocalizationFilePathsMapping(src)
        for langCode, filePath in self.localizationFilePathDict.items() :
            langDictList = self.getLocalizeKeyValue(filePath)
            allKeys = [i for s in [dLang.keys() for dLang in langDictList] for i in s]
            duplicateKeys = [item for item, count in collections.Counter(allKeys).items() if count > 1]
            allValues = [i for s in [dLang.values() for dLang in langDictList] for i in s]
            duplicateValues = [item for item, count in collections.Counter(allValues).items() if count > 1]
            canPrintFileName = True
            if duplicateKeys or duplicateValues :
                if canPrintFileName:
                    self.printFileHeader(filePath)
                    canPrintFileName = False
                print "[WARNING: ]  Duplicate localization keys"
                print "------------------------------------------"
                c = 0
                for key in duplicateKeys :
                    c = c + 1
                    print str(c) +". "+key
                print('\n')
                print "[WARNING: ]  Duplicate translations"
                print "---------------------------------------"
                c = 0
                for value in duplicateValues :
                    c = c + 1
                    print str(c) +". "+value
            else :
                print "[INFO: ] There is no duplicate key or value in localization string files."


def filePathError (options,parser):
    filePathErr = False
    if not options.filename :
        parser.error('Xcode project path is a mandatory field')
        filePathErr = True
    return filePathErr    


def main(argv):
    ltoolObject = LTool()
    parser = OptionParser(usage='usage: %prog [options] --file filename')
    parser.add_option('-v', '--version',
                        action='store_true',
                        dest='version',
                        help='Show the XCLocale version',
                        default=False)
        
    parser.add_option('-m', '--missig_localization',
                        action='store_true',
                        dest='checkMissinglocalization',
                        help='Generate a .CVS report for all missing localized string in current directory',
                        default=False)
                      
    parser.add_option('-c', '--check_syntax',
                        action='store_true',
                        dest='checkSyntax',
                        help='This will check for errors if exist in localized string file',
                        default=False)
                    
    parser.add_option('-d', '--check_duplicate',
                        action='store_true',
                        dest='checkDuplicate',
                        help='This will check for duplicate localization keys and values')
                    
    parser.add_option('-f', '--file',
                        action='store',
                        dest='filename',
                        help='[Required] to pass Xcode project path',
                        type='string')
                    
                      
    (options, _) = parser.parse_args()
   
    if options.version :
        ltoolObject.getToolVersion()

    if options.checkMissinglocalization :
        if not filePathError(options,parser):
            ltoolObject.getAlllocalizedkeys(options.filename)
            ltoolObject.showAllMissingLocalization(options.filename)
    
    if options.checkSyntax:
        if not filePathError(options,parser):
            ltoolObject.validateLocalizedFile(options.filename)

    if options.checkDuplicate:
        if not filePathError(options,parser):
            ltoolObject.checheckDuplicatekeysValues(options.filename)



if __name__ == '__main__':
    main(sys.argv[1:])

