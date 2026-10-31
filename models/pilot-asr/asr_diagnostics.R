# Monte Carlo precision of the X21 persistence read from the stochastic maps (Codex review, 2026-10-31).
# Four independent chains per tree under the reproduction's settings; every map's sampled rate and path
# indicators are kept. Design and acceptance: README.md, "Diagnostics". Run from this directory:
#   Rscript asr_diagnostics.R                       # every tree at Hooper's settings
#   Rscript asr_diagnostics.R ext 10000 100         # one tree with a longer chain (burn-in, thinning)
source("common.R")
suppressPackageStartupMessages({
  library(coda)
  library(parallel)
})

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

ess <- function(v) if (var(v) == 0) NA_real_ else unname(effectiveSize(v))
# Conditional persistence p = sum(persist) / sum(start) is a ratio; its Monte Carlo error comes from the
# linearised series z = (persist - p * start) / mean(start), with each chain's autocorrelation counted.
ratio_mcse <- function(d, p) {
  z <- split((d$persist - p * d$start) / mean(d$start), d$chain)
  e <- sum(vapply(z, ess, 0), na.rm = TRUE)
  if (e == 0) NA_real_ else sd(unlist(z)) / sqrt(e)
}

per_chain <- do.call(rbind, lapply(split(maps, list(maps$tree, maps$chain), drop = TRUE), function(d) data.frame(
  tree = d$tree[1], chain = d$chain[1], seed = d$seed[1], maps = nrow(d), starts = sum(d$start),
  departures_from_start = sum(d$start & !d$persist), p_start = mean(d$start), p_persist = mean(d$persist),
  p_persist_given_start = sum(d$persist) / sum(d$start), mean_departures = mean(d$departures),
  mean_entries = mean(d$entries), mean_reentries = mean(d$reentries), q3_median = median(d$q3_per_myr),
  ess_q3 = ess(d$q3_per_myr), ess_start = ess(d$start))))

summary_rows <- do.call(rbind, lapply(split(maps, maps$tree), function(d) {
  p <- sum(d$persist) / sum(d$start)
  q <- mcmc.list(lapply(split(d$q3_per_myr, d$chain), mcmc))
  ess_q3 <- unname(effectiveSize(q))
  starts_eff <- sum(d$start) * ess_q3 / nrow(d)
  pc <- per_chain$p_persist_given_start[per_chain$tree == d$tree[1]]
  data.frame(tree = d$tree[1], chains = length(unique(d$chain)), maps = nrow(d), starts = sum(d$start),
             departures_from_start = sum(d$start & !d$persist), p_start = mean(d$start), p_persist = mean(d$persist),
             p_persist_given_start = p, mcse_given_start = ratio_mcse(d, p),
             chain_range_given_start = max(pc) - min(pc),
             # With no departure seen, the rule of three on the effective number of trilete starts bounds the
             # departure probability; the effective number scales the starts by the rate chain's ESS share.
             rule_of_three_departure_upper = if (all(d$persist == d$start)) 3 / starts_eff else NA_real_,
             mean_entries = mean(d$entries), mean_reentries = mean(d$reentries),
             q3_median = median(d$q3_per_myr), ess_q3 = ess_q3,
             rhat_q3 = unname(gelman.diag(q, autoburnin = FALSE)$psrf[1, "Point est."]))
}))

dir.create("out", showWarnings = FALSE)
files <- sprintf("out/diagnostics_%s%s.csv", c("maps", "chains", "summary"), tag)
write.csv(maps, files[1], row.names = FALSE)
write.csv(per_chain, files[2], row.names = FALSE)
write.csv(summary_rows, files[3], row.names = FALSE)
write_json(list(zip_sha256 = zip_sha, seeds = setNames(as.list(jobs$seed), paste(jobs$tree, jobs$chain)),
                chains = chains, nsim = 1000, burnin = burnin, samplefreq = samplefreq, r = R.version.string, phytools = as.character(packageVersion("phytools")),
                coda = as.character(packageVersion("coda")), outputs = as.list(tools::sha256sum(files))),
           sprintf("out/diagnostics_receipt%s.json", tag), auto_unbox = TRUE, pretty = TRUE)
print(summary_rows, digits = 4)
