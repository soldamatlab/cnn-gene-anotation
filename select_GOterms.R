library(Biostrings)
library(GO.db)
library(GOfuncR)

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

getSequencesMultipleTerms <- function(terms){
  p <- c()
  for (go in terms) {
    p <- c(p, annotGO$protein[annotGO$go==go])
  }
  seqDatabase[names(seqDatabase) %in% p,]
}

annotGO <- read.csv("CAFA3_training_data/uniprot_sprot_exp.txt", sep="\t", header=F)
names(annotGO) <- c("protein","go","ont")

seqDatabase <- readAAStringSet("CAFA3_training_data/uniprot_sprot_exp.fasta")

# GO:0042127 regulation of cell population proliferation
# GO:0042981 regulation of apoptotic process
# GO:0006974 DNA damage response
GO_id = "GO:0006974"

terms <- c(GO_id, getBPChildren(GO_id))
sequences <- getSequencesMultipleTerms(terms)

writeXStringSet(sequences, "CAFA3_training_data/damage.fasta")
