#straight outta optimization homework i had
function exFunc(vec::AbstractArray)
    a = 500
    b = 0.1
    c = pi/2
    x1(x) = 25*x
    x2(y) = 25*y
    F10(x) = -a * exp(-b * sqrt( (x1(x[1])^2 + x2(x[2])^2) /2) ) - exp((cos(c*x1(x[1])) + cos(c*x2(x[2]))) /2) + exp(1)
    zsh(x) = 0.5 - (( sin( sqrt(x[1]^2 + x[2]^2) )^2 ) -0.5)/ ((1 + 0.1* (x[1]^2 + x[2]^2) )^2)
    Fobj(x) = F10(x)*zsh(x)
    r(x) = 100*(x[2] - x[1]*x[1])^2 + (1 - x[1])^2
    rd(x) = 1 + (x[2] - x[1]^2)^2 + (1-x[1])^2
    z(x) = x[1]*sin(sqrt(abs(x[1]))) - x[2]*sin(sqrt(abs(x[2])))
    w4(x) = sqrt(r(x)^2 + z(x)^2)+Fobj(x)
    w23(x) = z(x)/rd(x)
    w27(x) = w4(x) + w23(x)
    return w27(vec)
end