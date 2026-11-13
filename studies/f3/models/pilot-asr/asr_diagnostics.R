# Monte Carlo precision of the X21 persistence read from the stochastic maps (Codex review, 2026-10-31).
# Four independent chains per tree under the reproduction's settings; every map's sampled rate and path
# indicators are kept; summarise_chains.R summarises them. Design and acceptance: README.md, "Diagnostics".
# Run from this directory:
#   Rscript asr_diagnostics.R                       # every tree at Hooper's settings
#   Rscript asr_diagnostics.R ext 10000 100         # one tree with a longer chain (burn-in, thinning)
source("common.R")
suppressPackageStartupMessages(library(parallel))

args <- commandArgs(trailingOnly = TRUE)
only <- if (length(args)) args[1] else names(trees)
burnin <- if (length(args)) as.integer(args[2]) else 1000L
samplefreq <- if (length(args)) as.integer(args[3]) else 10L
tag <- if (length(args)) sprintf("_%s_b%d_s%d", only, burnin, samplefreq) else ""
chains <- 4L
s0 <- keep$X21
jobs <- expand.grid(chain = seq_len(chains), tree = only, stringsAsFactors = FALSE)
jobs$seed <- 20261031L + 100L * match(jobs$tree, names(trees)) + jobs$chain + if (length(args)) 10L else 0L

one_chain <- function(i) {
  tree <- trees[[jobs$tree[i]]]
  edges <- path_edges(tree, getMRCA(tree, land), getMRCA(tree, groups$Tracheophyta))
  set.seed(jobs$seed[i])
  maps <- hooper_simmap(tree, tip_states(tree, "X21"), burnin, samplefreq)
  runs <- t(vapply(maps, function(m) path_runs(path_history(m, edges), s0), numeric(5)))
  data.frame(tree = jobs$tree[i], chain = jobs$chain[i], seed = jobs$seed[i], map = seq_along(maps),
             q3_per_myr = vapply(maps, function(m) q_out(m$Q, s0), 0) / myr_per_unit, runs)
}
maps <- do.call(rbind, mclapply(seq_len(nrow(jobs)), one_chain, mc.cores = min(nrow(jobs), 6L)))

dir.create("out", showWarnings = FALSE)
files <- sprintf("out/diagnostics_maps%s.csv", tag)
write.csv(maps, files, row.names = FALSE)
write_json(list(zip_sha256 = zip_sha, seeds = setNames(as.list(jobs$seed), paste(jobs$tree, jobs$chain)),
                chains = chains, nsim = 1000, burnin = burnin, samplefreq = samplefreq, r = R.version.string, phytools = as.character(packageVersion("phytools")),
                coda = as.character(packageVersion("coda")), outputs = as.list(tools::sha256sum(files))),
           sprintf("out/diagnostics_receipt%s.json", tag), auto_unbox = TRUE, pretty = TRUE)
