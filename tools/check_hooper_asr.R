args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args)) args[[1]] else "."
if (!requireNamespace("ape", quietly = TRUE)) stop("The independent check requires R package ape")
out <- file.path(root, "data/pilot/hooper2026-asr")
archive <- file.path(root, "data/external/deposits/hooper2026-spore-evolution/02. Ancestral State Estimation.zip")
nodes <- read.csv(file.path(out, "nodes.csv"), check.names = FALSE)
states <- read.csv(file.path(out, "crown_states.csv"), check.names = FALSE, colClasses = "character")
trees <- list()
for (member in unique(nodes$tree_member)) {
  con <- unz(archive, member)
  trees[[member]] <- ape::read.tree(text = readLines(con, warn = FALSE))
  close(con)
}
for (i in seq_len(nrow(nodes))) {
  row <- nodes[i, ]
  tr <- trees[[row$tree_member]]
  id <- ape::getMRCA(tr, strsplit(row$mrca_extant_tips, ";", fixed = TRUE)[[1]])
  stopifnot(id == row$node_id, ape::Ntip(tr) == row$n_tips)
  stopifnot(setequal(ape::extract.clade(tr, id)$tip.label,
                    strsplit(row$descendant_tips, ";", fixed = TRUE)[[1]]))
}
reported <- 0L
absent <- 0L
for (member in unique(states$source_member)) {
  con <- unz(archive, member)
  tab <- read.csv(text = readLines(con, warn = FALSE), row.names = 1, check.names = FALSE)
  close(con)
  subset <- states[states$source_member == member, ]
  for (i in seq_len(nrow(subset))) {
    row <- subset[i, ]
    if (row$state %in% colnames(tab)) {
      stopifnot(row$status == "reported", is.finite(as.numeric(row$value)))
      stopifnot(abs(tab[row$node_id, row$state] - as.numeric(row$value)) < 1e-14)
      reported <- reported + 1L
    } else {
      stopifnot(row$status == "column_absent", row$value == "")
      absent <- absent + 1L
    }
  }
}
cat("Independent ape", as.character(utils::packageVersion("ape")), "check:", nrow(nodes),
    "MRCA nodes and descendant sets;", reported, "reported values;", absent,
    "absent state columns retained without imputation.\n")
