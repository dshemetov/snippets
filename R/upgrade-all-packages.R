# Update all packages (you're probably better off using renv and renv::update())

# Install pre-built pak binary from their repo
install.packages(
  "pak",
  repos = sprintf(
    "https://r-lib.github.io/p/pak/stable/%s/%s/%s",
    .Platform$pkgType,
    R.Version()$os,
    R.Version()$arch
  )
)
pak::pkg_install("purrr")

failed <- c()
purrr::pwalk(
  pak::pkg_list(),
  function(...) {
    x <- list(...)
    print(c(x$package, x$remotepkgref))
    tryCatch(
      if (!is.na(x$remotepkgref)) {
        pak::pkg_install(x$remotepkgref, upgrade = TRUE, ask = FALSE)
      } else {
        pak::pkg_install(x$package, upgrade = TRUE, ask = FALSE)
      },
      error = function(e) {
        failed <<- c(failed, x$package)
      }
    )
  },
  .progress = TRUE
)
print("Failed to update:")
print(failed)
