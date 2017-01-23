#!/usr/bin/env python
'''
Classes to degap sequences but maintain annotations
'''

#####################
# IMPORT OPERATIONS #
#####################

###############
# AUTHOR INFO #
###############

__author__ = 'Michael Gruenstaeudl <m.gruenstaeudl@fu-berlin.de>'
__copyright__ = 'Copyright (C) 2016-2017 Michael Gruenstaeudl'
__info__ = 'nex2embl'
__version__ = '2017.01.22.2300'

#############
# DEBUGGING #
#############

import pdb
#pdb.set_trace()

####################
# GLOBAL VARIABLES #
####################

###########
# CLASSES #
###########

class DegapButMaintainAnno:
    ''' This class contains functions to degap DNA sequences while maintaining 
    annotations. 
    
    Specifically, the functions remove dashes from strings while 
    maintaining annotations on these strings. Only some of the implementations 
    work if the charsets are overlapping.
    
    Args:
        seq (str):      a string that represents an aligned DNA sequence;
                        example: "ATG-C"
        charsets (dict):a dictionary with gene names (str) as keys and lists 
                        of nucleotide positions (list) as values; example: 
                        {"gene_1":[0,1],"gene_2":[2,3,4]}
    Returns:
        tupl.   The return consists of the degapped sequence and the 
                corresponding degapped charsets; example: 
                (degapped_seq, degapped_charsets)
    Raises:
        currently nothing
    '''
    
    def __init__(self, seq, rmchar, charsets):
        self.seq = seq
        self.rmchar = rmchar
        self.charsets = charsets
    
    def degap(self):
        ''' This function works on overlapping charsets and is preferable over 
        "degap_legacy".
        Source: http://stackoverflow.com/questions/35233714/
        maintaining-overlapping-annotations-while-removing-dashes-from-string
        '''
        from copy import copy
        
        seq = self.seq
        rmchar = self.rmchar
        charsets = self.charsets
        
        annotations = copy(charsets)
        index = seq.find(rmchar)
        while index > -1: # if any occurrence is found
            for gene_name, indices in annotations.items():
                if index in indices:
                    indices.remove(index)
                annotations[gene_name] = [e-1 if e > index else e \
                    for e in indices]
            seq = seq[:index] + seq[index+1:]
            index = seq.find(rmchar)
        return seq, annotations
    
    """
    @staticmethod
    def _intersection_exists(ranges_list):
        init_range = set(ranges_list[0])
        for r in ranges_list[1:]:
            if init_range.intersection(r):
                return True # Exits the entire function with 'True' (i.e., stops all of the loops)
        return False
    
    def degap_legacy(self):
        '''
        In its current implementation, this function only works if none of the 
        charsets are overlapping; hence, the initial check.
    
        Examples:
                   
            Example 4: # Overlapping genes with internal gaps
                >>> seq = "A--AT--T"
                >>> charsets = {"gene1":[0,1,2,3,4], "gene2":[4,5,6,7]}
                >>> DegapButMaintainAnno(seq, annot).degap_legacy()
                Out: ('AATTT', {'gene1': [0, 1, 2], 'gene2': [2, 3]})
                    
            Example 5: # Overlapping genes with start and end gaps
                >>> seq = "AA----TT"
                >>> charsets = {"gene1":[0,1,2,3,4], "gene2":[4,5,6,7]}
                >>> DegapButMaintainAnno(seq, annot).degap_legacy()
                Out: ('AATT', {'gene1': [0, 1], 'gene2': [1, 2]})
            
        TODO:
            (i)   Error in example 4: Out: AATT[sic!]T
            (ii)  Error in example 5: Out: {'gene1': [0, 1], 'gene2': [1[sic!], 2]})
        
        Notes:
            (i) In its current implementation, this function only works if 
            none of the charsets are overlapping; hence, the initial check.
            (ii) Order of charset in charsets seems to be irrelevant.
            
        '''
        seq = self.seq
        charsets = self.charsets
        
        if _intersection_exists(charsets.values()):
            raise ME.MyException('nex2embl ERROR: Character sets are overlapping.')
    
        degapped_seq = ''
        degapped_charsets = {}
        gaps_cumulative = 0
        for gene_name, index_list in charsets.items():
            gaps_within_gene = 0
            for pos, nucl in enumerate(seq):
                if pos in index_list and nucl == '-':
                    index_list.remove(pos)
                    gaps_within_gene += 1
                if pos in index_list and nucl != '-':
                    degapped_seq += nucl
                    index_list[index_list.index(pos)] = pos - gaps_within_gene
            index_list = [i-gaps_cumulative for i in index_list]
            degapped_charsets[gene_name] = index_list
            gaps_cumulative += gaps_within_gene
        return (degapped_seq, degapped_charsets)
    """

class RmAmbigsButMaintainAnno:
    ''' This class removes ambiguous nucleotides from a DNA sequence
    while maintaining the annotations.
    
    Args:
        seq (str):      a string that represents an aligned DNA sequence;
                        example: "NNATGCNNN"
        charsets (dict):a dictionary with gene names (str) as keys and lists 
                        of nucleotide positions (list) as values; example: 
                        {"gene_1":[0,1,2,3],"gene_2":[4,5,6,7,8]}
    Returns:
        tupl.   The return consists of the shortened DNA sequence and 
                the corresponding shortened charsets; example: 
                (shortened_seq, shortened_charsets)
    Raises:
        currently nothing
    '''
    
    def __init__(self):
        pass
    
    @staticmethod
    def rm_leadambig(seq, rmchar, charsets):
        ''' This class removes leading ambiguous nucleotides from a DNA
        sequence while maintaining the annotations.
        '''
        
        if seq[0] == rmchar:
            lead_stripoff = len(seq)-len(seq.lstrip(rmchar))
            for gene_name, indices in charsets.items():
                indices_shifted = [i-lead_stripoff for i in indices]
                charsets[gene_name] = [i for i in indices_shifted if i >= 0]
            seq = seq[lead_stripoff:]
        
        return seq, charsets
    
    @staticmethod
    def rm_trailambig(seq, rmchar, charsets):
        ''' This class removes trailing ambiguous nucleotides from a DNA
        sequence while maintaining the annotations.
        '''
        from copy import copy
        
        if seq[-1] == rmchar:
            trail_stripoff = len(seq.rstrip(rmchar))
            range_stripoff = range(trail_stripoff, len(seq))
            #range_stripoff = range(trail_stripoff, len(seq)+1)
            #print 'range_stripoff:', range_stripoff
            for gene_name, indices in charsets.items():
                indices_new = copy(indices)
                for index in range_stripoff:
                    if index in indices_new:
                        indices_new.remove(index)
                #    else:
                #        print "Warning: Index %s out of range." %(index)
                charsets[gene_name] = indices_new

            ## counting must be reversed, as we remove from tail
            #for index in reversed(range(trail_stripoff, len(seq)+1)):
                #for gene_name, indices in annotations.items():
                    #if index in indices:
                        #indices.remove(index)
                    #annotations[gene_name] = indices

            seq = seq[:trail_stripoff]

        return seq, charsets


#############
# FUNCTIONS #
#############

########
# MAIN #
########
