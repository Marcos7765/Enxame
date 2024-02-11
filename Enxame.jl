module PSO

    struct PSOParams{T<:Number, S<:AbstractFloat}
        numPart::T
        nDim::T
        inertia::S
        cogn::S
        soc::S
        posLim::Vector{Tuple{S, S}}
        vLim::Vector{Tuple{S, S}}
        targetFunc::Function
        max::Bool
    end

    mutable struct Particles{T<:Real}
        pos::Matrix{T}
        vel::Matrix{T}
        lBest::Matrix{T}
        gBest::Vector{T}
        bestVal::T
    end

    function populate(param::PSOParams)
        T = typeof(param.posLim[1][1])
        pos = rand(T, (param.nDim, param.numPart))
        scale = [x[2]-x[1] for x in param.posLim]
        pos = pos .* scale .+ [x[1] for x in param.posLim]
        lBest = Matrix(pos)
        #initializing gBest and bestVal with the first particle instead of
        #the worst value possible for the type. Shouldnt make a difference but
        #could prevent an all worst values case
        gBest = Vector(pos[:,1])
        bestVal = param.targetFunc(gBest)
        op = param.max ? (>) : (<)
        for col in eachcol(pos)
            testVal = param.targetFunc(col)
            if op(testVal, bestVal)
                gBest .= col
                bestVal = testVal
            end
        end
        vel = zeros(T, size(pos))
        return Particles(pos, vel, lBest, gBest, bestVal)
    end

    function update(param::PSOParams, pop::Particles)
        T = typeof(param.posLim[1][1])
        rf1 = rand(T, param.nDim)
        rf2 = rand(T, param.nDim)
        pop.vel .= pop.vel .* param.inertia + param.cogn*rf1 .* (pop.lBest .- pop.pos) + param.soc*rf2 .*(pop.gBest .- pop.pos)
        for col in eachcol(pop.vel)
            for (i, ele) in enumerate(col)
                if param.vLim[i][2] < ele
                    col[i] = param.vLim[i][2]
                    continue
                end
                if param.vLim[i][1] > ele
                    col[i] = param.vLim[i][1]
                end
            end
        end
        pop.pos .= pop.vel .+ pop.pos
        for col in eachcol(pop.pos)
            for (i, ele) in enumerate(col)
                if param.posLim[i][2] < ele
                    col[i] = param.posLim[i][2]
                    continue
                end
                if param.posLim[i][1] > ele
                    col[i] = param.posLim[i][1]
                end
            end
        end
    end

    function avaliate(param::PSOParams, pop::Particles)
        op = param.max ? (>) : (<)
        for (i, col) in enumerate(eachcol(pop.pos))
            testVal = param.targetFunc(col)
            if op(testVal, param.targetFunc(pop.lBest[:, i]))
                pop.lBest[:, i] .= col
                if op(testVal, pop.bestVal)
                    pop.gBest .= col
                    pop.bestVal = testVal
                end
            end
        end
    end

end