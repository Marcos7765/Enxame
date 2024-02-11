using Distributed

#setup section of the application
@everywhere begin

    #struct and function definitions
    include("Enxame.jl")
    #test function
    include("exampleFunction.jl")
    #values abstracted off to config.jl to both serve as a settings file
    #and declutter this file
    include("config.jl")
    
    params = PSO.PSOParams(nParticles, length(area), inertia,
    cognFactor, socialFactor, area, vLim, exFunc, isMax)
    pop = PSO.populate(params)
    
    println("$(pop.bestVal)")
    
    function getBest()
        return (pop.bestVal, pop.gBest)
    end
    
    function setBest(val::Tuple{S, Vector{S}}) where S
        pop.bestVal = val[1]
        pop.gBest .= val[2]
        return true
    end
    
    and(a,b) = a && b
end

#execution loop
while (gens > 0)
    @everywhere begin 
        PSO.update(params, pop)
        PSO.avaliate(params, pop)
        #here could be a local save
    end

    #synchronizing to get the better value and pass it around,
    #ideal place for a global save
    global res = reduce(min, [remotecall_fetch(getBest ,i) for i in procs()])
    test = reduce(and, [remotecall_fetch(setBest, i, res) for i in procs()])
    #here could be a global save
    global gens = gens -1
    println("$(pop.bestVal)")
end

#finalization
@everywhere println(pop.bestVal)
println("Result: $(res)")