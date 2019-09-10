*annonex2embl*
==============

Converts an annotated DNA multi-sequence alignment (in [NEXUS](http://wiki.christophchamp.com/index.php?title=NEXUS_file_format) format) to an EMBL flatfile for submission to [ENA](http://www.ebi.ac.uk/ena) via the [Webin-CLI submission tool](https://ena-docs.readthedocs.io/en/latest/cli_05.html).


## INSTALLATION
```
python2 setup.py install  # Installation
python2 setup.py test     # Testing
```

## FILE PREPARATION
The annotations of a NEXUS file are specified via [SETS-block](http://hydrodictyon.eeb.uconn.edu/eebedia/index.php/Phylogenetics:_NEXUS_Format), which is located beneath a DATA-block and defines sets of characters in the DNA alignment. In such a SETS-block, every gene and every exon charset must be accompanied by one CDS charset. Other charsets can be defined unaccompanied.

#### Example of a complete SETS-BLOCK
```
BEGIN SETS;
CHARSET trnK_intron_forward = 0-928 2531-2813 2849-3152;
CHARSET matK_gene_forward = 929-2530;
CHARSET matK_CDS_forward = 929-2530;    # Accompanying the charset matK_gene
CHARSET trnK_exon_reverse = 2814-2848;
CHARSET trnK_CDS_reverse = 2814-2848;   # Accompanying the charset trnK_exon
CHARSET psbA_gene_forward = 3153-3200;
CHARSET psbA_CDS_forward = 3153-3200;   # Accompanying the charset psbA_gene
END;
```

#### Examples of DESCR variable
```
# ITS of nuclear ribosomal DNA
DESCR="18S rRNA gene (partial), ITS1, 5.8S rRNA gene, ITS2 and 28S rRNA gene (partial)"

# trnL-trnF intergenic spacer of plastid genome
DESCR="tRNA-Leu (trnL) gene, partial sequence; trnL-trnF intergenix spacer, complete sequence; and tRNA-Phe (trnF) gene"

# trnK-matK region of plastid genome
DESCR="tRNA-Lys (trnK) gene and intron, partial sequence; maturase K (matK) gene, complete cds; psbA gene, partial sequence"

# rpl16 intron of plastid genome
DESCR="rpl16 intron, partial sequence"
```

## USAGE
#### On Linux / MacOS
```
SCRPT=$PWD/scripts/annonex2embl_CMD.py
INPUT=examples/input/reverse.nex
METAD=examples/input/reverse.csv
DESCR="description of alignment"
EMAIL=your_email_here@yourmailserver.com
AUTHR="your name here"
MNFTS=PRJEB00000

python2 $SCRPT -n $INPUT -c $METAD -o ${INPUT%.nex*}.embl -d $DESCR -e $EMAIL -a $AUTHR -ms $MNFTS -mn ${DESCR//[^[:alnum:]]/_}
```

#### On Windows
```
SET SCRPT=$PWD/scripts/annonex2embl_CMD.py
SET INPUT=examples/input/reverse.nex
SET METAD=examples/input/reverse.csv
SET DESCR="description of alignment"
SET EMAIL=your_email_here@yourmailserver.com
SET AUTHR="your name here"
SET MNFTS=PRJEB00000

SET OTPUT=output.embl
SET MNFTN=a_unique_description_here

python %SCRPT% -n %INPUT% -c %METAD% -o %OTPUT% -d %DESCR% -e %EMAIL% -a %AUTHR% -ms %MNFTS% -mn %MNFTN%
```


## TO DO
* Section "POST-PROCESSING OF FILES": Please write equivalent code for post-processing the output file in the Windows cmd shell as already exists for post-processing the output file in the Bash shell.
* Currently, --taxcheck requires "True" of "False" as parameters; how can I use it such that only the presence of --taxcheck indicates "True", whereas its abscence indicates "False"?


<!---
NOT NECESSARY AT THIS POINT
* Implement improvements of argparser (scripts/annonex2embl_CMD.py): Currently, the "required" and "optional" parameters are not displayed when calling scripts/annonex2embl_CMD.py. It incorrectly says "optional parameters" for all.
* Add a function that (a) reads and parses a bibtex file, extracts the citation info as well as the submitter references as from that file, and write the correctly formatted string-lines into the EMBL output file during post-processing.
--->


## DEVELOPMENT
#### Testing for development
To run the unittests outside of 'python setup.py test':
```
python -m unittest discover -s tests -p "*_test.py"
```

## CHANGELOG
See [`CHANGELOG.md`](CHANGELOG.md) for a list of recent changes to the software.
