# preprocess CAFA files
# 1. learn the distribution of GO term frequencies
# 2. select protein sequences related to a particular term
# 3. work with GO.db to get the ontology structure

library(Biostrings)
library(GO.db)
library(GOfuncR)

## read the protein annotation file
annotGO <- read.csv("CAFA3_training_data/uniprot_sprot_exp.txt", sep="\t", header=F)
names(annotGO) <- c("protein","go","ont")

## get the most frequent annotations
# GO:0005634 -- nucleus
# GO:0005829 -- cytosol
# ... they fall to cellular component ontology
tail(sort(table(annotGO$go)),20)

## focus on BP only
# GO:0045944 -- 1707, positive regulation of transcription by RNA polymerase II
# GO:0000122 -- 1172, negative regulation of transcription by RNA polymerase II
# we could join to GO:0006357 -- 564, regulation of transcription by RNA polymerase II
# ...
# GO:0007165 -- 866, signal transduction
# GO:0006468 -- 799, protein phosphorylation
tail(sort(table(annotGO$go[annotGO$ont=="P"])),20)
length(annotGO$protein[annotGO$go=="GO:0006357"])

gosearch <- tail(sort(table(annotGO$go[annotGO$ont=="P"])),20)
get_names(rownames(gosearch))

#' Get child terms in BP ontology
#'
#' use GO.db package
#' 
#' @param go A go term to study
#'
#' @return A list of child terms
#' @export
getBPChildren <- function(go){
  BPchild <- as.list(GOBPCHILDREN)
  return(BPchild[[which(names(BPchild)==go)]])
}

## child terms for GO:0006468 -- protein phosphorylation
childrenGO6468 <- getBPChildren("GO:0006468")
length(annotGO$protein[annotGO$go %in% childrenGO6468])

## conclusion:
# focus on regulation of transcription by RNA polymerase II with its two frequent child terms
# focus on protein phosphorylation with its child terms (one term that is a child term of regulation of transcription by RNA polymerase II was excluded from the list)
#   GO:0070816 -- phosphorylation of RNA polymerase II C-terminal domain

#' Get sequences for given GO term
#'
#' use annotation file to get protein names first, then get their sequences
#' 
#' @param go A go term to get
#'
#' @return A list of sequences
#' @export
getSequences <- function(go){
  p<-annotGO$protein[annotGO$go==go]
  seqDatabase[names(seqDatabase) %in% p,]
}

## read the sequential CAFA data
seqDatabase <- readAAStringSet("CAFA3_training_data/uniprot_sprot_exp.fasta")
# focus on protein phosphorylation
writeXStringSet(getSequences("GO:0006468"),"CAFA3_training_data/phosphorylation.fasta")
# and regulation of transcription by RNA polymerase II
writeXStringSet(getSequences("GO:0006357"),"CAFA3_training_data/regulation.fasta")

regulation <- readAAStringSet("CAFA3_training_data/regulation.fasta")

