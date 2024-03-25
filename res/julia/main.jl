using DataStructures
using JSON

lens = Dict{Tuple{Int64, Int64}, Real}()

# for i in 1:4
#     for j in 1:4
#         ind = (i, j)
#         if i == j
#             lens[ind] = 0
#         else
#             lens[ind] = 1
#         end
#     end
# end
digits = 8
eps = 1e-6

function cross_prod(v::AbstractVector{<:Real}, w::AbstractVector{<:Real})
    return v[1] * w[2] - v[2] * w[1]
end

function quadratic_equation_solve(a::Real, b::Real, c::Real)
    D = b * b - 4 * a * c
    return [(-b - sqrt(D)) / (2 * a), (-b + sqrt(D)) / (2 * a)]
end

function dist(v::AbstractVector{<:Real}, w::AbstractVector{<:Real})
    return sqrt((v[1] - w[1]) * (v[1] - w[1]) + (v[2] - w[2]) * (v[2] - w[2]))
end

function dist3(v::AbstractVector{<:Real}, w::AbstractVector{<:Real})
    return sqrt((v[1] - w[1]) * (v[1] - w[1]) + (v[2] - w[2]) * (v[2] - w[2]) + (v[3] - w[3]) * (v[3] - w[3]))
end

function intersection(w1::Tuple{AbstractVector{<:Real}, <:Real}, w2::Tuple{AbstractVector{<:Real}, <:Real})
    x1 = w1[1][1]
    x2 = w2[1][1]
    y1 = w1[1][2]
    y2 = w2[1][2]
    r1 = w1[2]
    r2 = w2[2]

    a = 2 * (x2 - x1)
    b = 2 * (y2 - y1)
    c = (x1 * x1 - x2 * x2 + y1 * y1 - y2 * y2 - r1 * r1 + r2 * r2)
    if abs(b) < eps
        x = -c / a
        ys = quadratic_equation_solve(1, -2 * y1, y1 * y1 - r1 * r1 + (x - x1) * (x - x1))
        xs = [x, x]
    else
        xs = quadratic_equation_solve(((a * a) / (b * b)) + 1, -2 * x1 + 2 * (a / b) * (y1 + c / b), x1 * x1 - r1 * r1 + (y1 + c / b) * (y1 + c / b))
        ys = [(-c - a * xs[1]) / b, (-c - a * xs[2]) / b]
    end
    # println((xs[1] - x1) * (xs[1] - x1) + (ys[1] - y1) * (ys[1] - y1) - r1 * r1, ' ', (xs[1] - x2) * (xs[1] - x2) + (ys[1] - y2) * (ys[1] - y2) - r2 * r2)
    return [[xs[1], ys[1]], [xs[2], ys[2]]]
end


function make_next(A::Tuple{AbstractVector{<:Real}, Int64}, B::Tuple{AbstractVector{<:Real}, Int64}, C::Tuple{AbstractVector{<:Real}, Int64}, edge::Tuple{Int64, Int64})
    left = edge[1]
    right = edge[2]
    vertexes = [A, B, C]
    ver_nums = [A[2], B[2], C[2]]
    V1 = vertexes[(findfirst(x -> x == left, ver_nums))]
    V2 = vertexes[(findfirst(x -> x == right, ver_nums))]
    V3 = vertexes[(findfirst(x -> !(x == left || x == right), ver_nums))]
    num_D = 10 - A[2] - B[2] - C[2]
    V1D = lens[(V1[2], num_D)]
    V2D = lens[(V2[2], num_D)] 
    Ds = intersection((V1[1], V1D), (V2[1], V2D))
    D1 = Ds[1]
    D2 = Ds[2]
    V1V2 = [V2[1][1] - V1[1][1], V2[1][2] - V1[1][2]]
    V1D1 = [D1[1] - V1[1][1], D1[2] - V1[1][2]]
    V1V3 = [V3[1][1] - V1[1][1], V3[1][2] - V1[1][2]]
    D = (D1, num_D)
    if cross_prod(V1V2, V1D1) * cross_prod(V1V2, V1V3) > 0
        D = (D2, num_D)
    end
    return [V1, V2, D]
end

function add_point(P::Tuple{AbstractVector{<:Real}, Int64}, points::Set{Tuple{AbstractVector{Real}, Int64}}, t::Real)
    P[1][1] = round(P[1][1], digits=digits)
    P[1][2] = round(P[1][2], digits=digits)
    if (dist(P[1], [0, 0])) > t
        return false
    end
    if !(P in points)
        push!(points, P)
        return true
    end
    return false
end


function save_points(points)
    io = open("points_irreg2.json", "w");
    JSON.print(io, points, 2)
    close(io);
    return;
end


function get_all_points(A::AbstractVector{<:Real}, B::AbstractVector{<:Real}, C::AbstractVector{<:Real}, D::AbstractVector{<:Real}, t::Real)
    vertexes = [A, B, C, D]
    for i in 1:4
        for j in 1:4
            ind = (i, j)
            if i == j
                lens[ind] = 0
            else
                lens[ind] = dist3(vertexes[i], vertexes[j])
            end
        end
    end

    Ap = (A[1:2], 1)
    Bp = (B[1:2], 2)
    Cp = (C[1:2], 3)
    start = [Ap, Bp, Cp]
    points = Base.Set{Tuple{AbstractVector{Real}, Int64}}()
    push!(points, Ap)
    push!(points, Bp)
    push!(points, Cp)
    q = Queue{Tuple{AbstractVector{Tuple{AbstractVector{Real}, Int64}}, Tuple{Int64, Int64}}}()
    enqueue!(q, (start, (0, 0)))
    start_time = time_ns()
    while length(q) != 0
        if (time_ns() - start_time) >= 1e10
            save_points(points)
            println(length(points))
            # println(log(get_geodesics(points, digits)))
            start_time = time_ns()
        end
        info = dequeue!(q)
        face = info[1]
        last_edge = info[2]
        edges = [(face[1][2], face[2][2]), (face[1][2], face[3][2]), (face[2][2], face[3][2])]
        edges = filter(x -> x != last_edge, edges)
        faces = Base.Vector{Tuple{AbstractVector{Tuple{AbstractVector{<:Real}, Int64}}, Tuple{Int64, Int64}}}()
        for edge in edges
            push!(faces, (make_next(face[1], face[2], face[3], edge), edge))
        end
        for info_it in faces
            face_it = info_it[1]
            if add_point(face_it[3], points, t)
                enqueue!(q, info_it)
            end
        end
    end
    return points
end

function get_geodesics(points::Set{Tuple{AbstractVector{Real}, Int64}}, precision::Int64)
    result = Set{Real}()
    for A in points
        for B in points
            if A[2] == B[2]
                continue
            end
            geodesic_len = round(dist(A[1], B[1]), digits=precision)
            push!(result, geodesic_len)
        end
    end
    return length(result)
end


A = [0, 0, 0]
B = [1, 0, 0]
C = [1 / 2, 1 / 2, 1 / 2]

# a = tan(80 * (π / 180))/2
# b = sqrt(3) / 6
# h = sqrt(a * a - b * b)
# h = sqrt(6) / 2
# D = [1 / 2, b, h]
D = [1 / 2, 1 / 2, -1 / 2]
count_lens = Dict{Real, Int64}()
r = 10

info = Vector{AbstractVector{<:Real}}()
push!(info, A)
push!(info, B)
push!(info, C)
push!(info, D)
io = open("info_irreg2.json", "w");
JSON.print(io, info, 2)
close(io);

for double_t in 3:1000
    t = double_t / 2
    points = get_all_points(A, B, C, D, t)
    count_lens[t] = get_geodesics(points, digits)
    println("done ", t)
    println(count_lens[t])

    if double_t % 10 == 0
        io = open("data_$(t).json", "w");
        JSON.print(io, count_lens, 2)
        close(io);
    end
end

io = open("data.json", "w");
JSON.print(io, count_lens, 2)
close(io);

println(1)