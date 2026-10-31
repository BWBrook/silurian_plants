# Summaries of the kept chains from asr_diagnostics.R: per-chain and pooled persistence with its Monte Carlo
# error, rate-chain convergence, and retention scenarios. eo and zyg use four chains at Hooper et al.'s settings;
# ext uses both its failed run at those settings and its four longer chains (README, "Diagnostics").
#   Rscript summarise_chains.R
source("common.R")
suppressPackageStartupMessages(library(coda))

runs <- c("", "_ext_b10000_s100")
ess <- function(v) if (var(v) == 0) NA_real_ else unname(effectiveSize(v))
# Conditional persistence p = sum(persist) / sum(start) is a ratio. Its Monte Carlo error comes from the linearised
# series z = (persist - p * start) / mean(start). Independent chains pool through the variances of their means,
# sqrt(sum(n_i^2 var(z_i) / ESS_i)) / sum(n_i) (Codex review, 2026-10-31); a constant chain contributes zero.
ratio_mcse <- function(d, p) {
  z <- split((d$persist - p * d$start) / mean(d$start), d$chain)
  v <- vapply(z, function(x) { e <- ess(x); if (is.na(e)) 0 else length(x)^2 * var(x) / e }, 0)
  sqrt(sum(v)) / nrow(d)
}

retention <- list(); receipt <- list()
for (tag in runs) {
  maps <- read.csv(sprintf("out/diagnostics_maps%s.csv", tag))
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
    pc <- per_chain$p_persist_given_start[per_chain$tree == d$tree[1]]
    data.frame(tree = d$tree[1], chains = length(unique(d$chain)), maps = nrow(d), starts = sum(d$start),
               departures_from_start = sum(d$start & !d$persist), p_start = mean(d$start), p_persist = mean(d$persist),
               p_persist_given_start = p, mcse_given_start = ratio_mcse(d, p), chain_range_given_start = max(pc) - min(pc),
               # With no departure seen, the rule of three on the effective number of trilete starts bounds the
               # departure probability; the effective number scales the starts by the rate chain's ESS share.
               rule_of_three_departure_upper = if (all(d$persist == d$start)) 3 / (sum(d$start) * ess_q3 / nrow(d)) else NA_real_,
               mean_entries = mean(d$entries), mean_reentries = mean(d$reentries), q3_median = median(d$q3_per_myr),
               ess_q3 = ess_q3, rhat_q3 = unname(gelman.diag(q, autoburnin = FALSE)$psrf[1, "Point est."]))
  }))
  out <- sprintf("out/diagnostics_%s%s.csv", c("chains", "summary"), tag)
  write.csv(per_chain, out[1], row.names = FALSE)
  write.csv(summary_rows, out[2], row.names = FALSE)
  print(summary_rows[, c("tree", "p_persist_given_start", "mcse_given_start", "ess_q3", "rhat_q3")], digits = 4)
  # Retention from the converged chains only: the longer chains for ext, Hooper's settings for eo and zyg.
  keep_trees <- if (tag == "") c("eo", "zyg") else "ext"
  for (tn in keep_trees) {
    d <- maps[maps$tree == tn, ]
    for (T0 in origins) {
      R <- exp(-d$q3_per_myr * (T0 - tau))
      retention[[length(retention) + 1]] <- data.frame(tree = tn, source = sprintf("out/diagnostics_maps%s.csv", tag),
        chains = length(unique(d$chain)), maps = nrow(d), origin_ma = T0, tau_ma = tau, L_myr = T0 - tau,
        R_median = median(R), R_lo = unname(quantile(R, 0.025)), R_hi = unname(quantile(R, 0.975)),
        q3_median_per_myr = median(d$q3_per_myr))
    }
  }
  receipt[[sprintf("out/diagnostics_maps%s.csv", tag)]] <- unname(tools::sha256sum(sprintf("out/diagnostics_maps%s.csv", tag)))
}
retention <- do.call(rbind, retention)
retention <- retention[order(match(retention$tree, c("ext", "eo", "zyg")), retention$origin_ma), ]
write.csv(retention, "out/retention_chains.csv", row.names = FALSE)
outputs <- c(sprintf("out/diagnostics_%s%s.csv", rep(c("chains", "summary"), length(runs)), rep(runs, each = 2)), "out/retention_chains.csv")
write_json(list(inputs = receipt, coda = as.character(packageVersion("coda")), outputs = as.list(tools::sha256sum(outputs))),
           "out/summary_receipt.json", auto_unbox = TRUE, pretty = TRUE)
