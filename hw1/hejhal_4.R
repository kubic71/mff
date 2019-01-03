# Exact computation can be found here:
# Without returning the balls to the urn:
#       https://www.desmos.com/calculator/e81vxlygw7

# With returning the balls to the urn
#       https://www.desmos.com/calculator/3gwbxkfaru

# Default values
c = 6
b = 8
m = 6
n = 10

user.input = TRUE
returning = FALSE

if (user.input) {
    c <- as.integer(readline(prompt="Enter c:"))
    b <- as.integer(readline(prompt="Enter b:"))
    m <- as.integer(readline(prompt="Enter m:"))
    n <- as.integer(readline(prompt="Enter n:"))
    returning <- readline(prompt="Do you want the balls to be returned to urn?[y/n]:")
    if (startsWith(returning, "y")) { 
        returning = TRUE
    } else {
        returning = FALSE
    }
}

freq = c()

for( i in seq(1, 100000))  {
v = as.vector(sample(c(rep(0, c), rep(1, b + m)), size=n, replace=returning))
occurences = sum(v == 0)
freq = c(freq, occurences)
if (i %% 10 == 0) {
    barplot(table(freq)/i, main=paste("c:", c, ", b:", b, ", m:", m, ", n:", n, ", returning:", returning))
  }
}