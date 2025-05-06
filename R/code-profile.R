# Profile some R code
library(profvis)

# Required to keep source when running from a script
options(keep.source = TRUE)
p <- profvis({
  # Your code goes here
})
htmlwidgets::saveWidget(p, "prof-exploration.html")
