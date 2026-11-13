# Checks the local fix of the arrival branch of Rextinct::griwm and Rextinct::criwm (README.md).
# Run from the repository root:  Rscript models/griwm_r/test_arrival_fix.R [path/to/upstream/griwm.R]
# Needs data.table. Dates have zero error, so resampling is deterministic.

here <- "models/griwm_r"
args <- commandArgs(trailingOnly = TRUE)

run <- function(file, fun, ages, signor_lipps, alpha = exp(-1)) {
  env <- new.env()
  sys.source(file, envir = env)
  path <- tempfile(fileext = ".txt")
  write.table(data.frame(ages, 0), path, row.names = FALSE, col.names = FALSE)
  invisible(capture.output(out <- suppressMessages(env[[fun]](path, signor_lipps = signor_lipps, alpha = alpha,
                                                               resample = 5, radiocarbon = 0, calibra = FALSE))))
  as.numeric(out[[3]][2, "median"])  # years BP
}

# Bradshaw et al. (2012) estimator by hand, for the arrival end: each series of the m oldest dates
# extends beyond the oldest by (span + 1) * -log(alpha) / m; series are weighted by 1 / span.
by_hand <- function(ages, alpha = exp(-1)) {
  a <- sort(ages, decreasing = TRUE)
  m <- 2:length(a)
  span <- a[1] - a[m]
  est <- a[1] + (span + 1) * -log(alpha) / m
  sum(est / span) / sum(1 / span)
}

ok <- TRUE
check <- function(label, got, want, tol = 0.51) {
  pass <- abs(got - want) <= tol
  cat(sprintf("%-46s got %9.2f  want %9.2f  %s\n", label, got, want, if (pass) "ok" else "FAIL"))
  if (!pass) ok <<- FALSE
}

toy <- c(100, 90, 60)
set.seed(1)  # the functions call set.seed internally, so draw every test series first
cases <- lapply(1:5, function(r) round(runif(sample(4:12, 1), 1000, 9000)))
for (fun in c("griwm", "criwm")) {
  file <- file.path(here, paste0(fun, ".R"))
  check(paste(fun, "arrival, toy series"), run(file, fun, toy, "arr"), 107.13)
  check(paste(fun, "extinction, toy series (unchanged)"), run(file, fun, toy, "ext"), 45.29)
  for (r in seq_along(cases)) {
    ages <- cases[[r]]
    est <- run(file, fun, ages, "arr")
    check(paste(fun, "arrival vs by-hand estimator, case", r), est, by_hand(ages))
    check(paste(fun, "arrival older than oldest record, case", r), max(est, max(ages) + 1), est, tol = 0)
  }
}

if (length(args) == 1) {
  check("upstream griwm arrival, toy series (the fault)", run(args[1], "griwm", toy, "arr"), 100)
}

if (!ok) quit(status = 1)
cat("all checks passed\n")
