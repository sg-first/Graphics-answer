import numpy as np

# material parameters
albedo = np.ones((3,))
metallic = 1.0
roughness = 1.0
ao = 1.0

# lights
lightPositions = np.ones((4,3))
lightColors = np.ones((4,3))

camPos = np.ones((3,))

PI = 3.14159265359

def normalize(arr, t_min=0, t_max=1):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return np.array(norm_arr)



def DistributionGGX(N, H, roughness):
    a = roughness*roughness
    a2 = a*a
    NdotH = max(np.dot(N, H), 0.0)
    NdotH2 = NdotH*NdotH
    nom = a2
    denom = (NdotH2*(a2-1.0)+1.0)
    denom = PI*denom*denom

    return nom/denom



def GeometrySchlickGGX(NdotV, roughness):
    r = roughness+1.0
    k = (r*r)/8.0

    nom = NdotV
    denom = NdotV*(1.0-k)+k

    return nom/denom



def GeometrySmith(N, V, L, roughness):
    NdotV = max(np.dot(N,V),0.0)
    NdotL = max(np.dot(N,L),0.0)
    ggx2 = GeometrySchlickGGX(NdotV,roughness)
    ggx1 = GeometrySchlickGGX(NdotL,roughness)

    return ggx1*ggx2



def fresnelSchlick(cosTheta, F0):
    return F0+(1.0-F0)*pow(1.0-cosTheta,5.0)



def PBRmain(TexCoords,WorldPos,Normal):
    N = normalize(Normal)
    V = normalize(camPos - WorldPos)

    F0 = np.array([0.04]*3)
    F0 = mix(F0,albedo,metallic)  # 函数没写

    Lo = np.array([0.0]*3)

    for i in range(4):
        # calculate per-light radiance
        L = normalize(lightPositions[i]-WorldPos)
        H = normalize(V+L)
        distance = np.linalg.norm(lightPositions[i] - WorldPos)
        attenuation = 1.0 /(distance*distance)
        radiance = lightColors[i]*attenuation

        # cook-torrance brdf
        NDF = DistributionGGX(N, H, roughness)
        G = GeometrySmith(N,V,L,roughness)
        F = fresnelSchlick(max(np.dot(H,V),0.0),F0)

        kS = F
        kD = np.array([1.0]*3)-kS
        kD *= 1.0-metallic

        nominator = NDF*G*F
        denominator = 4.0*max(np.dot(N,V),0.0)*max(np.dot(N, L), 0.0) + 0.001
        specular = nominator / denominator

        # add to outgoing radiance Lo
        NdotL = max(np.dot(N, L), 0.0)
        Lo += (kD * albedo / PI + specular) * radiance * NdotL

    ambient = np.array([0.03]*3)*albedo*ao
    color = ambient + Lo

    color = color / (color + np.array([1.0]*3))
    color = np.power(color,  np.array([1.0/2.2]*3))

    FragColor = np.array(color.tolist()+[1])

    return FragColor