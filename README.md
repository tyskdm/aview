# aview

Convert the `AUTOSAR C++14 Coding Rules` pdf files to formatted text files.

- **It's not yet viewer.**

## 1. Version and Stability

| Version | Stability |
| ------- | --------- |
| 0.5.0   | [Stability: 1 - Experimental](https://nodejs.org/api/documentation.html#documentation_stability_index)

## 2. Motivation

```sh
$ aview rule A10-2-1@17-10
#### Rule A10-2-1 (required, implementation, automated)<br>Non-virtual member functions shall not be redefined in derived classes.
```

```sh
$ aview diff A10-2-1
< #### Rule A10-2-1 (required, implementation, automated)<br>Non-virtual member functions shall not be redefined in derived classes.
---
> #### Rule A10-2-1 (required, implementation, automated)<br>Non-virtual public or protected member functions shall not be redefined in derived classes.
```

## 3. Requirements

1. pdftotext

   If you don't have it:

   ```sh
   $ sudo apt-get install poppler-utils
   ```

   pdftotext is a part of poppler-utils.

2. python3

## 4. Installation

### 4.1. aview command

1. download or clone aview anywhere you want.
2. add execution path to './bin'.

```sh
$ aview -v
```

### 4.2. database

1. ```sh
   $ make db-install
   ```

   Downloads `AUTOSAR_RS_CPP14Guidelines.pdf` from AUTOSAR official web site.
   - ver. 17-10 from Release package 17-10
   - ver. 19-03 from Release package 21-11

2. ```sh
   $ make db
   ```

   Converts pdf to text using `pdftotext`, and formats it by aview.

## 5. Usage

You can see `./database/19-03/[19-03]_C++14_Coding_Rules.txt` and `./database/17-10/[17-10]_C++14_Coding_Rules.txt`.

diff them by your hands.
