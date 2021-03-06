# aview

`AUTOSAR C++14` ans `MISRA C++:2008` Guidelines viewer / diff viewer

<br>

- [1. Version and Stability](#1-version-and-stability)
- [2. Motivation](#2-motivation)
- [3. Requirements](#3-requirements)
- [4. Installation](#4-installation)
- [5. Preparing data](#5-preparing-data)
- [6. Usage](#6-usage)
  - [6.1. `diff`](#61-diff)
  - [6.2. Write your own subcommands](#62-write-your-own-subcommands)
- [7. Limitation](#7-limitation)

<br>

## 1. Version and Stability

| Version | Stability | Changes |
| :-----: | :-------: | ------- |
| 0.7.1   | [Stability: 1 - Experimental](https://nodejs.org/api/documentation.html#documentation_stability_index) | Added MISRA C++:2008 to the list of supported documents.
| 0.7.0   | [Stability: 1 - Experimental](https://nodejs.org/api/documentation.html#documentation_stability_index)

## 2. Motivation

I needed to get diff between AUTOSAR C++14 Coding Rules 17-10 and 19-03. \
And it was difficult to prevent mistakes when checking by eye balls, so I wrote this code.

Using aview, you can see them like this:

```text
$ aview diff A18-1-3 -HTR
## A18-1-3

diff: - A17-10 / + A19-03
-------------------------
Compare : header, text, rationale
Ignore  : classifier, note, exception, example, seealso

Section:
  6 AUTOSAR C++14 coding rules
  6.18 Language support library - partial
  6.18.1 Types

Rule:
- The std::auto_ptr shall not be used.
+ The std::auto_ptr type shall not be used.
?                   +++++

Rationale:
- The std::auto_ptr smart pointer is deprecated since C++11 Language Standard and it is planned to be withdrawn in C++17 Language Standard.
- The std::auto_ptr provides unusual copy semantics and it can not be placed in STL containers. It is recommended to use std::unique_ptr instead.
+ The std::auto_ptr type has been deprecated since the C++11 Language Standard and is removed from the C++17 Language Standard. Due to the lack of move semantics in pre C++11 standards, it provides unusual copy semantics and cannot be placed in STL containers.
+ The correct alternative is std::unique_ptr, which shall be used instead.
```

## 3. Requirements

1. pdftotext

   If you don't have the command:

   ```sh
   $ sudo apt-get install poppler-utils
   $ pdftotext -v
   pdftotext version 20.09.0
   Copyright 2005-2020 The Poppler Developers - http://poppler.freedesktop.org
   Copyright 1996-2011 Glyph & Cog, LLC
   ```

   pdftotext is a part of poppler-utils.

2. python3

## 4. Installation

1. download or clone aview anywhere you want.
2. add execution path to './bin'.

```sh
$ aview -v
```

## 5. Preparing data

1. ```sh
   /path/to/aview$ make pdf-install
   ```

   Downloads `AUTOSAR_RS_CPP14Guidelines.pdf` from AUTOSAR official web site.
   - ver. 17-10 from Release package 17-10
   - ver. 19-03 from Release package 21-11

2. **Be sure to read and agree to the license terms.**

   - The PDFs are stored in `database/pdf/`.

3. ```sh
   /path/to/aview$ make db
   ```

   Converts pdf to text using `pdftotext`, and converts them to json files as caches.

- #### NOTE: <!-- omit in toc -->

  In accordance with the restrictions of the license terms, aview does not store or cache any MISRA C++:2008 data.

  MISRA data will be retrieved from the PDF file specified in the command line option each time aview is executed.

## 6. Usage

### 6.1. `diff`

#### 6.1.1. Differences in individual rules

#### Compare 17-10 and 19-03 <!-- omit in toc -->

```sh
$ aview diff A18-1-3
```

```sh
$ aview diff A18-1-3 -HTR
```

- Using opts, specify which part of the rule data to compare. \
  more > `aview diff -h`

#### Compare specified rules/versions <!-- omit in toc -->

```sh
$ aview diff 0-1-7@2008 A0-1-2@1903 -m path/to/your/misra.pdf
```

- @ opts are:

  - 1710 = AUTOSAR C++:17-10
  - 1903 = AUTOSAR C++:19-03
  - 2008 = MISRA C++:2008


#### 6.1.2. Differences in all rules

```sh
$ aview diff all -A
```

If all is specified as the ID:

- Compare A17-10 and A19-03.
- Only the differences will be displayed, not the parts with the same content.

### 6.2. Write your own subcommands

It's easy to add your own subcommands. Just add the features you want.

1. Duplicate a subcommand

   Duplicate `./aview/app/diff` folder with any name your choice. \
   and you see:

   ```text
   $ aview -h
   usage: aview [-h] [-v] {diff,conv} ...

   optional arguments:
   -h, --help     show this help message and exit
   -v, --version  show version

   commands:
   {diff,conv}
      diff         Display rules with the difference information.
      conv         Converts AUTOSAR text file to json data file
      My_Command   Display rules with the difference information.  <<< new
   ```

2. Read `command.py` and rewrite.

   - The `setup()` function sets up the argparse object for command line options,
   - And the `run()` function is the body of the subcommand.

## 7. Limitation

Current known limitations are:

1. Aview yet does not correctly fix all the formatting collapses when converting pdf files to text data.

   It can cause the same text in two versions to be perceived differently.

2. In 19-03, there are rules whose IDs have been changed from 17-10

   When `aview diff all`, aview cannot consider them as same rules.
