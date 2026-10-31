# Shared inputs and path readers for asr_persistence.R and asr_diagnostics.R. Run from this directory.
suppressPackageStartupMessages({
  library(ape)
  library(phytools)
  library(jsonlite)
})

root <- normalizePath(file.path("..", ".."))
zip <- file.path(root, "data/external/deposits/hooper2026-spore-evolution/02. Ancestral State Estimation.zip")
inventory <- read.csv(file.path(root, "data/pilot/hooper2026-asr/source_inventory.csv"), stringsAsFactors = FALSE)
zip_sha <- unname(tools::sha256sum(zip))
stopifnot(zip_sha %in% unlist(inventory))

work <- file.path(tempdir(), "hooper-asr")
unzip(zip, exdir = work)
src <- file.path(work, "02. Ancestral State Estimation")
traits <- read.csv(file.path(src, "asr_matrix.csv"), row.names = 1, fileEncoding = "UTF-8-BOM")
trees <- list(ext = read.tree(file.path(src, "extant.tre")),
              eo = read.tree(file.path(src, "eophyte sister.tre")),
              zyg = read.tree(file.path(src, "zygnema sister.tre")))

land <- c("Anthoceros", "Leiosporoceros", "Phaeomegaceros", "Apotreubia", "Blasia", "Haplomitrium", "Riccardia",
          "Andreaea", "Oedipodium", "Sphagnum", "Takakia", "Huperzia", "Isoetes", "Lycopodium", "Selaginella",
          "Equisetum", "Marattia", "Ophioglossum", "Psilotum", "Alsophila", "Anemia", "Thelypteris", "Osmunda", "Cycas")
groups <- list(Tracheophyta = c("Huperzia", "Isoetes", "Lycopodium", "Selaginella", "Equisetum", "Marattia", "Ophioglossum",
                                "Psilotum", "Alsophila", "Anemia", "Thelypteris", "Osmunda", "Cycas"),
               mosses = c("Andreaea", "Oedipodium", "Sphagnum", "Takakia"),
               hornworts = c("Anthoceros", "Leiosporoceros", "Phaeomegaceros"),
               liverworts = c("Apotreubia", "Blasia", "Haplomitrium", "Riccardia"))
keep <- list(X21 = "3", X26 = "4")  # proximal trilete aperture; trilete or inaperturate monad
myr_per_unit <- 100
tau <- 452.8  # base of the Katian: a chosen stage-boundary scenario for the first appearance
origins <- c(459.1, 470, 480, 500, 515.5)

tip_states <- function(tree, ch) {
  x <- as.factor(traits[match(tree$tip.label, rownames(traits)), ch]); names(x) <- tree$tip.label
  x
}
# Hooper et al.'s settings; burnin 1000 is make.simmap's default. Longer chains change only burnin and samplefreq.
hooper_simmap <- function(tree, x, burnin = 1000, samplefreq = 10)
  make.simmap(tree, x, model = "ER", nsim = 1000, Q = "mcmc", vQ = 0.01, prior = list(use.empirical = TRUE),
              burnin = burnin, samplefreq = samplefreq, message = FALSE)
path_edges <- function(tree, from, to) {
  nodes <- nodepath(tree, from, to)
  vapply(seq_len(length(nodes) - 1), function(i) which(tree$edge[, 1] == nodes[i] & tree$edge[, 2] == nodes[i + 1]), 1L)
}
path_history <- function(map, edges) unlist(lapply(edges, function(e) names(map$maps[[e]])), use.names = FALSE)
q_out <- function(Q, s) -Q[s, s]

# One mapped path: held in s0 throughout; departures from s0; entries into s0 (first acquisition included);
# re-entries (entries after the path has already been in s0); whether it starts in s0.
path_runs <- function(h, s0) {
  r <- rle(h)$values
  into <- which(head(r, -1) != s0 & tail(r, -1) == s0) + 1
  c(persist = all(h == s0), departures = sum(head(r, -1) == s0 & tail(r, -1) != s0), entries = length(into),
    reentries = sum(vapply(into, function(j) any(r[seq_len(j - 1)] == s0), NA)), start = h[1] == s0)
}
