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
        self.allSupportedLangDict = {"mr":"Marathi",
                                    "bs":"Bosnian",
                                    "ee-TG":"Ewe (Togo)",
                                    "ms":"Malay",
                                    "kam-KE":"Kamba (Kenya)",
                                    "mt":"Maltese",
                                    "ha":"Hausa",
                                    "es-HN":"Spanish (Honduras)",
                                    "ml-IN":"Malayalam (India)",
                                    "ro-MD":"Romanian (Moldova)",
                                    "kab-DZ":"Kabyle (Algeria)",
                                    "he":"Hebrew",
                                    "es-CO":"Spanish (Colombia)",
                                    "my":"Burmese",
                                    "es-PA":"Spanish (Panama)",
                                    "az-Latn":"Azerbaijani (Latin)",
                                    "mer":"Meru",
                                    "en-NZ":"English (New Zealand)",
                                    "xog-UG":"Soga (Uganda)",
                                    "sg":"Sango",
                                    "fr-GP":"French (Guadeloupe)",
                                    "sr-Cyrl-BA":"Serbian (Cyrillic  Bosnia and Herzegovina)",
                                    "hi":"Hindi",
                                    "fil-PH":"Filipino (Philippines)",
                                    "lt-LT":"Lithuanian (Lithuania)",
                                    "si":"Sinhala",
                                    "en-MT":"English (Malta)",
                                    "si-LK":"Sinhala (Sri Lanka)",
                                    "luo-KE":"Luo (Kenya)",
                                    "it-CH":"Italian (Switzerland)",
                                    "teo":"Teso",
                                    "mfe":"Morisyen",
                                    "sk":"Slovak",
                                    "uz-Cyrl-UZ":"Uzbek (Cyrillic  Uzbekistan)",
                                    "sl":"Slovenian",
                                    "rm-CH":"Romansh (Switzerland)",
                                    "az-Cyrl-AZ":"Azerbaijani (Cyrillic  Azerbaijan)",
                                    "fr-GQ":"French (Equatorial Guinea)",
                                    "kde":"Makonde",
                                    "sn":"Shona",
                                    "cgg-UG":"Chiga (Uganda)",
                                    "so":"Somali",
                                    "fr-RW":"French (Rwanda)",
                                    "es-SV":"Spanish (El Salvador)",
                                    "mas-TZ":"Masai (Tanzania)",
                                    "en-MU":"English (Mauritius)",
                                    "sq":"Albanian",
                                    "hr":"Croatian",
                                    "sr":"Serbian",
                                    "en-PH":"English (Philippines)",
                                    "ca":"Catalan",
                                    "hu":"Hungarian",
                                    "mk-MK":"Macedonian (Macedonia)",
                                    "fr-TD":"French (Chad)",
                                    "nb":"Norwegian Bokmål",
                                    "sv":"Swedish",
                                    "kln-KE":"Kalenjin (Kenya)",
                                    "sw":"Swahili",
                                    "nd":"North Ndebele",
                                    "sr-Latn":"Serbian (Latin)",
                                    "el-GR":"Greek (Greece)",
                                    "hy":"Armenian",
                                    "ne":"Nepali",
                                    "el-CY":"Greek (Cyprus)",
                                    "es-CR":"Spanish (Costa Rica)",
                                    "fo-FO":"Faroese (Faroe Islands)",
                                    "pa-Arab-PK":"Punjabi (Arabic  Pakistan)",
                                    "seh":"Sena",
                                    "ar-YE":"Arabic (Yemen)",
                                    "ja-JP":"Japanese (Japan)",
                                    "ur-PK":"Urdu (Pakistan)",
                                    "pa-Guru":"Punjabi (Gurmukhi)",
                                    "gl-ES":"Galician (Spain)",
                                    "zh-Hant-HK":"Chinese (Traditional Han  Hong Kong SAR China)",
                                    "ar-EG":"Arabic (Egypt)",
                                    "nl":"Dutch",
                                    "th-TH":"Thai (Thailand)",
                                    "es-PE":"Spanish (Peru)",
                                    "fr-KM":"French (Comoros)",
                                    "nn":"Norwegian Nynorsk",
                                    "kk-Cyrl-KZ":"Kazakh (Cyrillic  Kazakhstan)",
                                    "kea":"Kabuverdianu",
                                    "lv-LV":"Latvian (Latvia)",
                                    "kln":"Kalenjin",
                                    "tzm-Latn":"Central Morocco Tamazight (Latin)",
                                    "yo":"Yoruba",
                                    "gsw-CH":"Swiss German (Switzerland)",
                                    "ha-Latn-GH":"Hausa (Latin  Ghana)",
                                    "is-IS":"Icelandic (Iceland)",
                                    "pt-BR":"Portuguese (Brazil)",
                                    "cs":"Czech",
                                    "en-PK":"English (Pakistan)",
                                    "fa-IR":"Persian (Iran)",
                                    "zh-Hans-SG":"Chinese (Simplified Han  Singapore)",
                                    "luo":"Luo",
                                    "ta":"Tamil",
                                    "fr-TG":"French (Togo)",
                                    "kde-TZ":"Makonde (Tanzania)",
                                    "mr-IN":"Marathi (India)",
                                    "ar-SA":"Arabic (Saudi Arabia)",
                                    "ka-GE":"Georgian (Georgia)",
                                    "mfe-MU":"Morisyen (Mauritius)",
                                    "id":"Indonesian",
                                    "fr-LU":"French (Luxembourg)",
                                    "de-LU":"German (Luxembourg)",
                                    "ru-MD":"Russian (Moldova)",
                                    "cy":"Welsh",
                                    "zh-Hans-HK":"Chinese (Simplified Han  Hong Kong SAR China)",
                                    "te":"Telugu",
                                    "bg-BG":"Bulgarian (Bulgaria)",
                                    "shi-Latn":"Tachelhit (Latin)",
                                    "ig":"Igbo",
                                    "ses":"Koyraboro Senni",
                                    "ii":"Sichuan Yi",
                                    "es-BO":"Spanish (Bolivia)",
                                    "th":"Thai",
                                    "ko-KR":"Korean (South Korea)",
                                    "ti":"Tigrinya",
                                    "it-IT":"Italian (Italy)",
                                    "shi-Latn-MA":"Tachelhit (Latin  Morocco)",
                                    "pt-MZ":"Portuguese (Mozambique)",
                                    "ff-SN":"Fulah (Senegal)",
                                    "haw":"Hawaiian",
                                    "zh-Hans":"Chinese (Simplified)",
                                    "so-KE":"Somali (Kenya)",
                                    "bn-IN":"Bengali (India)",
                                    "en-UM":"English (U.S. Minor Outlying Islands)",
                                    "to":"Tonga",
                                    "id-ID":"Indonesian (Indonesia)",
                                    "uz-Cyrl":"Uzbek (Cyrillic)",
                                    "en-GU":"English (Guam)",
                                    "es-EC":"Spanish (Ecuador)",
                                    "en-US-POSIX":"English (United States  Computer)",
                                    "sr-Latn-BA":"Serbian (Latin  Bosnia and Herzegovina)",
                                    "is":"Icelandic",
                                    "luy":"Luyia",
                                    "tr":"Turkish",
                                    "en-NA":"English (Namibia)",
                                    "it":"Italian",
                                    "da":"Danish",
                                    "bo-IN":"Tibetan (India)",
                                    "vun-TZ":"Vunjo (Tanzania)",
                                    "ar-SD":"Arabic (Sudan)",
                                    "uz-Latn-UZ":"Uzbek (Latin  Uzbekistan)",
                                    "az-Latn-AZ":"Azerbaijani (Latin   Azerbaijan)",
                                    "de":"German",
                                    "es-GQ":"Spanish (Equatorial Guinea)",
                                    "ta-IN":"Tamil (India)",
                                    "de-DE":"German (Germany)",
                                    "fr-FR":"French (France)",
                                    "rof-TZ":"Rombo (Tanzania)",
                                    "ar-LY":"Arabic (Libya)",
                                    "en-BW":"English (Botswana)",
                                    "asa":"Asu",
                                    "zh":"Chinese",
                                    "ha-Latn":"Hausa (Latin)",
                                    "fr-NE":"French (Niger)",
                                    "es-MX":"Spanish (Mexico)",
                                    "bem-ZM":"Bemba (Zambia)",
                                    "zh-Hans-CN":"Chinese (Simplified Han  China)",
                                    "bn-BD":"Bengali (Bangladesh)",
                                    "pt-GW":"Portuguese (Guinea-Bissau)",
                                    "om":"Oromo",
                                    "jmc":"Machame",
                                    "de-AT":"German (Austria)",
                                    "kk-Cyrl":"Kazakh (Cyrillic)",
                                    "sw-TZ":"Swahili (Tanzania)",
                                    "ar-OM":"Arabic (Oman)",
                                    "et-EE":"Estonian (Estonia)",
                                    "or":"Oriya",
                                    "da-DK":"Danish (Denmark)",
                                    "ro-RO":"Romanian (Romania)",
                                    "zh-Hant":"Chinese (Traditional)",
                                    "bm-ML":"Bambara (Mali)",
                                    "ja":"Japanese",
                                    "fr-CA":"French (Canada)",
                                    "naq":"Nama",
                                    "zu":"Zulu",
                                    "en-IE":"English (Ireland)",
                                    "ar-MA":"Arabic (Morocco)",
                                    "es-GT":"Spanish (Guatemala)",
                                    "uz-Arab-AF":"Uzbek (Arabic  Afghanistan)",
                                    "en-AS":"English (American Samoa)",
                                    "bs-BA":"Bosnian (Bosnia and Herzegovina)",
                                    "am-ET":"Amharic (Ethiopia)",
                                    "ar-TN":"Arabic (Tunisia)",
                                    "haw-US":"Hawaiian (United States)",
                                    "ar-JO":"Arabic (Jordan)",
                                    "fa-AF":"Persian (Afghanistan)",
                                    "uz-Latn":"Uzbek (Latin)",
                                    "en-BZ":"English (Belize)",
                                    "nyn-UG":"Nyankole (Uganda)",
                                    "ebu-KE":"Embu (Kenya)",
                                    "te-IN":"Telugu (India)",
                                    "cy-GB":"Welsh (United Kingdom)",
                                    "uk":"Ukrainian",
                                    "nyn":"Nyankole",
                                    "en-JM":"English (Jamaica)",
                                    "en-US":"English (United States)",
                                    "fil":"Filipino",
                                    "ar-KW":"Arabic (Kuwait)",
                                    "af-ZA":"Afrikaans (South Africa)",
                                    "en-CA":"English (Canada)",
                                    "fr-DJ":"French (Djibouti)",
                                    "ti-ER":"Tigrinya (Eritrea)",
                                    "ig-NG":"Igbo (Nigeria)",
                                    "en-AU":"English (Australia)",
                                    "ur":"Urdu",
                                    "fr-MC":"French (Monaco)",
                                    "pt-PT":"Portuguese (Portugal)",
                                    "pa":"Punjabi",
                                    "es-419":"Spanish (Latin America)",
                                    "fr-CD":"French (Congo - Kinshasa)",
                                    "en-SG":"English (Singapore)",
                                    "bo-CN":"Tibetan (China)",
                                    "kn-IN":"Kannada (India)",
                                    "sr-Cyrl-RS":"Serbian (Cyrillic  Serbia)",
                                    "lg-UG":"Ganda (Uganda)",
                                    "gu-IN":"Gujarati (India)",
                                    "ee":"Ewe",
                                    "nd-ZW":"North Ndebele (Zimbabwe)",
                                    "bem":"Bemba",
                                    "uz":"Uzbek",
                                    "sw-KE":"Swahili (Kenya)",
                                    "sq-AL":"Albanian (Albania)",
                                    "hr-HR":"Croatian (Croatia)",
                                    "mas-KE":"Masai (Kenya)",
                                    "el":"Greek",
                                    "ti-ET":"Tigrinya (Ethiopia)",
                                    "es-AR":"Spanish (Argentina)",
                                    "pl":"Polish",
                                    "en":"English",
                                    "eo":"Esperanto",
                                    "shi":"Tachelhit",
                                    "kok":"Konkani",
                                    "fr-CF":"French (Central African Republic)",
                                    "fr-RE":"French (RÃ©union)",
                                    "mas":"Masai",
                                    "rof":"Rombo",
                                    "ru-UA":"Russian (Ukraine)",
                                    "yo-NG":"Yoruba (Nigeria)",
                                    "dav-KE":"Taita (Kenya)",
                                    "gv-GB":"Manx (United Kingdom)",
                                    "pa-Arab":"Punjabi (Arabic)",
                                    "es":"Spanish",
                                    "teo-UG":"Teso (Uganda)",
                                    "ps":"Pashto",
                                    "es-PR":"Spanish (Puerto Rico)",
                                    "fr-MF":"French (Saint Martin)",
                                    "et":"Estonian",
                                    "pt":"Portuguese",
                                    "eu":"Basque",
                                    "ka":"Georgian",
                                    "rwk-TZ":"Rwa (Tanzania)",
                                    "nb-NO":"Norwegian BokmÃ¥l (Norway)",
                                    "fr-CG":"French (Congo - Brazzaville)",
                                    "cgg":"Chiga",
                                    "zh-Hant-TW":"Chinese (Traditional Han  Taiwan)",
                                    "sr-Cyrl-ME":"Serbian (Cyrillic  Montenegro)",
                                    "lag":"Langi",
                                    "ses-ML":"Koyraboro Senni (Mali)",
                                    "en-ZW":"English (Zimbabwe)",
                                    "ak-GH":"Akan (Ghana)",
                                    "vi-VN":"Vietnamese (Vietnam)",
                                    "sv-FI":"Swedish (Finland)",
                                    "to-TO":"Tonga (Tonga)",
                                    "fr-MG":"French (Madagascar)",
                                    "fr-GA":"French (Gabon)",
                                    "fr-CH":"French (Switzerland)",
                                    "de-CH":"German (Switzerland)",
                                    "es-US":"Spanish (United States)",
                                    "ki":"Kikuyu",
                                    "my-MM":"Burmese (Myanmar [Burma])",
                                    "vi":"Vietnamese",
                                    "ar-QA":"Arabic (Qatar)",
                                    "ga-IE":"Irish (Ireland)",
                                    "rwk":"Rwa",
                                    "bez":"Bena",
                                    "ee-GH":"Ewe (Ghana)",
                                    "kk":"Kazakh",
                                    "as-IN":"Assamese (India)",
                                    "ca-ES":"Catalan (Spain)",
                                    "kl":"Kalaallisut",
                                    "fr-SN":"French (Senegal)",
                                    "ne-IN":"Nepali (India)",
                                    "km":"Khmer",
                                    "ms-BN":"Malay (Brunei)",
                                    "ar-LB":"Arabic (Lebanon)",
                                    "ta-LK":"Tamil (Sri Lanka)",
                                    "kn":"Kannada",
                                    "ur-IN":"Urdu (India)",
                                    "fr-CI":"",
                                    "ko":"Korean",
                                    "ha-Latn-NG":"Hausa (Latin  Nigeria)",
                                    "sg-CF":"Sango (Central African Republic)",
                                    "om-ET":"Oromo (Ethiopia)",
                                    "zh-Hant-MO":"Chinese (Traditional Han  Macau SAR China)",
                                    "uk-UA":"Ukrainian (Ukraine)",
                                    "fa":"Persian",
                                    "mt-MT":"Maltese (Malta)",
                                    "ki-KE":"Kikuyu (Kenya)",
                                    "luy-KE":"Luyia (Kenya)",
                                    "kw":"Cornish",
                                    "pa-Guru-IN":"Punjabi (Gurmukhi  India)",
                                    "en-IN":"English (India)",
                                    "kab":"Kabyle",
                                    "ar-IQ":"Arabic (Iraq)",
                                    "ff":"Fulah",
                                    "en-TT":"English (Trinidad and Tobago)",
                                    "bez-TZ":"Bena (Tanzania)",
                                    "es-NI":"Spanish (Nicaragua)",
                                    "uz-Arab":"Uzbek (Arabic)",
                                    "ne-NP":"Nepali (Nepal)",
                                    "fi":"Finnish",
                                    "khq":"Koyra Chiini",
                                    "gsw":"Swiss German",
                                    "zh-Hans-MO":"Chinese (Simplified Han  Macau SAR China)",
                                    "en-MH":"English (Marshall Islands)",
                                    "hu-HU":"Hungarian (Hungary)",
                                    "en-GB":"English (United Kingdom)",
                                    "fr-BE":"French (Belgium)",
                                    "de-BE":"German (Belgium)",
                                    "saq":"Samburu",
                                    "be-BY":"Belarusian (Belarus)",
                                    "sl-SI":"Slovenian (Slovenia)",
                                    "sr-Latn-RS":"Serbian (Latin  Serbia)",
                                    "fo":"Faroese",
                                    "fr":"French",
                                    "xog":"Soga",
                                    "fr-BF":"French (Burkina Faso)",
                                    "tzm":"Central Morocco Tamazight",
                                    "sk-SK":"Slovak (Slovakia)",
                                    "fr-ML":"French (Mali)",
                                    "he-IL":"Hebrew (Israel)",
                                    "ha-Latn-NE":"Hausa (Latin  Niger)",
                                    "ru-RU":"Russian (Russia)",
                                    "fr-CM":"French (Cameroon)",
                                    "teo-KE":"Teso (Kenya)",
                                    "seh-MZ":"Sena (Mozambique)",
                                    "kl-GL":"Kalaallisut (Greenland)",
                                    "fi-FI":"Finnish (Finland)",
                                    "kam":"Kamba",
                                    "es-ES":"Spanish (Spain)",
                                    "af":"Afrikaans",
                                    "asa-TZ":"Asu (Tanzania)",
                                    "cs-CZ":"Czech (Czech Republic)",
                                    "tr-TR":"Turkish (Turkey)",
                                    "es-PY":"Spanish (Paraguay)",
                                    "tzm-Latn-MA":"Central Morocco Tamazight (Latin  Morocco)",
                                    "lg":"Ganda",
                                    "ebu":"Embu",
                                    "en-HK":"English (Hong Kong SAR China)",
                                    "nl-NL":"Dutch (Netherlands)",
                                    "en-BE":"English (Belgium)",
                                    "ms-MY":"Malay (Malaysia)",
                                    "es-UY":"Spanish (Uruguay)",
                                    "ar-BH":"Arabic (Bahrain)",
                                    "kw-GB":"Cornish (United Kingdom)",
                                    "ak":"Akan",
                                    "chr":"Cherokee",
                                    "dav":"Taita",
                                    "lag-TZ":"Langi (Tanzania)",
                                    "am":"Amharic",
                                    "so-DJ":"Somali (Djibouti)",
                                    "shi-Tfng-MA":"Tachelhit (Tifinagh  Morocco)",
                                    "sr-Latn-ME":"Serbian (Latin  Montenegro)",
                                    "sn-ZW":"Shona (Zimbabwe)",
                                    "or-IN":"Oriya (India)",
                                    "ar":"Arabic",
                                    "as":"Assamese",
                                    "fr-BI":"French (Burundi)",
                                    "jmc-TZ":"Machame (Tanzania)",
                                    "chr-US":"Cherokee (United States)",
                                    "eu-ES":"Basque (Spain)",
                                    "saq-KE":"Samburu (Kenya)",
                                    "vun":"Vunjo",
                                    "lt":"Lithuanian",
                                    "naq-NA":"Nama (Namibia)",
                                    "ga":"Irish",
                                    "af-NA":"Afrikaans (Namibia)",
                                    "kea-CV":"Kabuverdianu (Cape Verde)",
                                    "es-DO":"Spanish (Dominican Republic)",
                                    "lv":"Latvian",
                                    "kok-IN":"Konkani (India)",
                                    "de-LI":"German (Liechtenstein)",
                                    "fr-BJ":"French (Benin)",
                                    "az":"Azerbaijani",
                                    "guz-KE":"Gusii (Kenya)",
                                    "rw-RW":"Kinyarwanda (Rwanda)",
                                    "mg-MG":"Malagasy (Madagascar)",
                                    "km-KH":"Khmer (Cambodia)",
                                    "gl":"Galician",
                                    "shi-Tfng":"Tachelhit (Tifinagh)",
                                    "ar-AE":"Arabic (United Arab Emirates)",
                                    "fr-MQ":"French (Martinique)",
                                    "rm":"Romansh",
                                    "sv-SE":"Swedish (Sweden)",
                                    "az-Cyrl":"Azerbaijani (Cyrillic)",
                                    "ro":"Romanian",
                                    "so-ET":"Somali (Ethiopia)",
                                    "en-ZA":"English (South Africa)",
                                    "ii-CN":"Sichuan Yi (China)",
                                    "fr-BL":"French (Saint BarthÃ©lemy)",
                                    "hi-IN":"Hindi (India)",
                                    "gu":"Gujarati",
                                    "mer-KE":"Meru (Kenya)",
                                    "nn-NO":"Norwegian Nynorsk (Norway)",
                                    "gv":"Manx",
                                    "ru":"Russian",
                                    "ar-DZ":"Arabic (Algeria)",
                                    "ar-SY":"Arabic (Syria)",
                                    "en-MP":"English (Northern Mariana Islands)",
                                    "nl-BE":"Dutch (Belgium)",
                                    "rw":"Kinyarwanda",
                                    "be":"Belarusian",
                                    "en-VI":"English (U.S. Virgin Islands)",
                                    "es-CL":"Spanish (Chile)",
                                    "bg":"Bulgarian",
                                    "mg":"Malagasy",
                                    "hy-AM":"Armenian (Armenia)",
                                    "zu-ZA":"Zulu (South Africa)",
                                    "guz":"Gusii",
                                    "mk":"Macedonian",
                                    "es-VE":"Spanish (Venezuela)",
                                    "ml":"Malayalam",
                                    "bm":"Bambara",
                                    "khq-ML":"Koyra Chiini (Mali)",
                                    "bn":"Bengali",
                                    "ps-AF":"Pashto (Afghanistan)",
                                    "so-SO":"Somali (Somalia)",
                                    "sr-Cyrl":"Serbian (Cyrillic)",
                                    "pl-PL":"Polish (Poland)",
                                    "fr-GN":"French (Guinea)",
                                    "bo":"Tibetan",
                                    "om-KE":"Oromo (Kenya)"
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
        print("============================================================================")
        print("File: "+ filePath)
        print("============================================================================")


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
        print('XCLocale Version: '+ ver)
    

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
                fo.write(str(sn) + "," + key)
                for key in allSupportedLangkeys:
                   
                    if key in langObj.keys():
                        fo.write("," + langObj[key])
                    else :
                        fo.write("," + " ")
                fo.write("\n ")
            
            fo.close()
            print("[INFO: ] Missing localization report is generated at "+'"'+ os.getcwd()+'/'+filename+'"')
        else:
            print("[INFO: ] There is no missing key in all supported localization string files.")

    
    def validateLocalizedFile(self, src, checkBOM):
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
                    
                    # Check BOM
                    if checkBOM and lineNo == 0:
                        arr = bytes(filterLine, 'utf-8')
                        if arr[:3] == b'\xef\xbb\xbf':
                            filterLine = arr[3:].decode('utf-8')
                        else:
                            foundError = True
                            print("[ERROR: ] BOM is missing!")
                            break
                    
                    lineNo = lineNo + 1
                    if not self.isIgnoredCaseLine(filterLine):
                        patternMatched = re.search(validPattern,filterLine)
                        if not patternMatched:
                            if canPrintFileName:
                                self.printFileHeader(filePath)
                                canPrintFileName = False
                            foundError = True
                            print("[ERROR: ] Line :" + str(lineNo) + " " + filterLine)
            f.close()
        if not foundError :  
            print("[INFO: ] There is no error in localization string files.")


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
                print("[WARNING: ]  Duplicate localization keys")
                print("------------------------------------------")
                c = 0
                for key in duplicateKeys :
                    c = c + 1
                    print(str(c) +". "+key)
                print('\n')
                print("[WARNING: ]  Duplicate translations")
                print("---------------------------------------")
                c = 0
                for value in duplicateValues :
                    c = c + 1
                    print(str(c) +". "+value)
            else :
                print("[INFO: ] There is no duplicate key or value in localization string files.")


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
                    
    parser.add_option('-b', '--check_bom',
                        action='store_true',
                        dest='checkBOM',
                        help='This will check for BOM UTF8 bytes in the beginning of the file')
                    
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
            ltoolObject.validateLocalizedFile(options.filename, options.checkBOM)

    if options.checkDuplicate:
        if not filePathError(options,parser):
            ltoolObject.checheckDuplicatekeysValues(options.filename)



if __name__ == '__main__':
    main(sys.argv[1:])

