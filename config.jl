#imagine here that the function to be optimized is really expensive

const size = nprocs()

const area::Vector{Tuple{Float64, Float64}} = [(-500., 500.),(-500.,500.)]
const vLim = area

const totalParticles = 20
const nParticles = div(totalParticles,size) + (myid() <= rem(totalParticles, size) ? 1 : 0)

gens::Int = 20

const inertia = 0.5

const cognFactor = socialFactor = 2.

const isMax = false