# Retention scenarios R(L) = exp(-q3 L) from the converged rate chains kept by asr_diagnostics.R: four chains at
# Hooper et al.'s settings for eo and zyg, and four longer chains for ext, whose chain at those settings did not
# converge (README, "Diagnostics"). Run from this directory after both diagnostic runs:
#   Rscript retention_chains.R
source("common.R")
src <- c(ext = "out/diagnostics_maps_ext_b10000_s100.csv", eo = "out/diagnostics_maps.csv", zyg = "out/diagnostics_maps.csv")
rows <- list()
for (tn in names(src)) {
  d <- subset(read.csv(src[[tn]]), tree == tn)
  for (T0 in origins) {
    R <- exp(-d$q3_per_myr * (T0 - tau))
    rows[[length(rows) + 1]] <- data.frame(tree = tn, source = src[[tn]], chains = length(unique(d$chain)), maps = nrow(d),
      origin_ma = T0, tau_ma = tau, L_myr = T0 - tau, R_median = median(R), R_lo = unname(quantile(R, 0.025)),
      R_hi = unname(quantile(R, 0.975)), q3_median_per_myr = median(d$q3_per_myr))
  }
}
out <- do.call(rbind, rows)
write.csv(out, "out/retention_chains.csv", row.names = FALSE)
print(out[, c("tree", "origin_ma", "R_median", "R_lo", "R_hi")], digits = 3)
