# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    # Material
    global material, line_material

    material = THREE.MeshBasicMaterial.new()
    material.color = THREE.Color.new(255,255,255)
    material.transparent = True
    material.opacity = 0.5

    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new(100,100,100)

    # All Objects
    global all_Dodecahedrons, all_Dodecahedron_edges
    all_Dodecahedrons = []
    all_Dodecahedron_edges = []

    # Control Parameters
    global geom1_params
    geom1_params = {"distance": 50, "iterations":2}
    geom1_params = Object.fromEntries(to_js(geom1_params))


    # First Dodecahedron 
    global geometries
    geometries = []
    geometry = THREE.DodecahedronGeometry.new(10)
    geometry.rotateX(math.radians(31.717))
    
    geometries.append(geometry)

    move_geometry(0, geom1_params.iterations, geometries)

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'distance', 25,100)
    param_folder.add(geom1_params, 'iterations', 1,4,1)
    param_folder.open()
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()

#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Update Secne
def update():
    global all_Dodecahedrons, all_Dodecahedron_edges, t, iteration
    if geom1_params.distance != t or geom1_params.iterations != iteration:
        for Dodecahedron in all_Dodecahedrons:  
            scene.remove(Dodecahedron)
        for Dodecahedron_edges in all_Dodecahedron_edges:
            scene.remove(Dodecahedron_edges)
        all_Dodecahedrons = []
        all_Dodecahedron_edges = []
        move_geometry(0, geom1_params.iterations, geometries)
    else:
        pass

# Move Dodecahedrons
def move_geometry(current_iteration, max_iterations, geometries):
    current_iteration += 1
    mesh_geometry(geometries)
    new_geometries = []
    for geometry in geometries:
        get_vectors(geometry)
        
        new_geometry1 = geometry.clone()
        new_geometry1.translate(vector1.x, vector1.y, vector1.z)
        new_geometries.append(new_geometry1)

        new_geometry2 = geometry.clone()
        new_geometry2.translate(vector2.x, vector2.y, vector2.z)
        new_geometries.append(new_geometry2)

        new_geometry3 = geometry.clone()
        new_geometry3.translate(vector3.x, vector3.y, vector3.z)
        new_geometries.append(new_geometry3)
    
        new_geometry4 = geometry.clone()
        new_geometry4.translate(vector4.x, vector4.y, vector4.z)
        new_geometries.append(new_geometry4)    

        new_geometry5 = geometry.clone()
        new_geometry5.translate(vector5.x, vector5.y, vector5.z)
        new_geometries.append(new_geometry5)
    
        new_geometry6 = geometry.clone()
        new_geometry6.translate(vector6.x, vector6.y, vector6.z)
        new_geometries.append(new_geometry6)
    
        new_geometry7 = geometry.clone()
        new_geometry7.translate(vector7.x, vector7.y, vector7.z)
        new_geometries.append(new_geometry7)

        new_geometry8 = geometry.clone()
        new_geometry8.translate(vector8.x, vector8.y, vector8.z)
        new_geometries.append(new_geometry8)

        new_geometry9 = geometry.clone()
        new_geometry9.translate(vector9.x, vector9.y, vector9.z)
        new_geometries.append(new_geometry9)    

        new_geometry10 = geometry.clone()
        new_geometry10.translate(vector10.x, vector10.y, vector10.z)
        new_geometries.append(new_geometry10)

        new_geometry11 = geometry.clone()
        new_geometry11.translate(vector11.x, vector11.y, vector11.z)
        new_geometries.append(new_geometry11)        

        new_geometry12 = geometry.clone()
        new_geometry12.translate(vector12.x, vector12.y, vector12.z)
        new_geometries.append(new_geometry12)

    if current_iteration >= max_iterations:
        new_geometries = []

        global iteration
        iteration = geom1_params.iterations

        pass
        
    else:
        return move_geometry(current_iteration, max_iterations, new_geometries) 

# Get Vectors
def get_vectors(geometry):
    # Get Geometry Center:
    geometry.computeBoundingBox()
    center = THREE.Vector3.new()
    geometry.boundingBox.getCenter(center)

    global t
    t = geom1_params.distance

    global vector1, vector2, vector3, vector4, vector5, vector6, vector7, vector8, vector9, vector10, vector11, vector12

    vector1 = THREE.Vector3.new((0*t) + center.x, (1*t) + center.y, (0*t) + center.z)
    vector2 = THREE.Vector3.new((0*t) + center.x, (-1*t) + center.y, (0*t) + center.z)
    vector3 = THREE.Vector3.new((-0.723604*t) + center.x, (-0.447221*t) + center.y, (0.525728*t) + center.z)
    vector4 = THREE.Vector3.new((0.723604*t) + center.x, +(0.447221*t) + center.y, (-0.525728*t) + center.z)
    vector5 = THREE.Vector3.new((0.276394*t) + center.x, (-0.447221*t) + center.y, (0.850647*t) + center.z)
    vector6 = THREE.Vector3.new((-0.276394*t) + center.x, (0.447221*t) + center.y, (-0.850647*t) + center.z)
    vector7 = THREE.Vector3.new((0.894423*t) + center.x, (-0.447221*t) + center.y, (9.7106*(10**(-6))*t) + center.z) 
    vector8 = THREE.Vector3.new((-0.894423*t) + center.x, (0.447221*t)  + center.y, (-9.7106*(10**(-6))*t) + center.z)
    vector9 = THREE.Vector3.new((0.276412*t) + center.x, (-0.447221*t) + center.y, (-0.850641*t) + center.z)
    vector10 = THREE.Vector3.new((-0.276412*t) + center.x, (0.447221*t) + center.y, (0.850641*t) + center.z)
    vector11 = THREE.Vector3.new((-0.723594*t) + center.x, (-0.447221*t) + center.y, (-0.525742*t) + center.z)
    vector12 = THREE.Vector3.new((0.723594*t) + center.x, (0.447221*t) + center.y, (0.525742*t) + center.z)

# Mesh the Geometries
def mesh_geometry(geometries):
    for geometry in geometries:
        Dodecahedron = THREE.Mesh.new(geometry, material)

        geometry_edges = THREE.EdgesGeometry.new(Dodecahedron.geometry)
        Dodecahedron_edges = THREE.LineSegments.new(geometry_edges, line_material)

        scene.add(Dodecahedron)
        scene.add(Dodecahedron_edges)

        all_Dodecahedrons.append(Dodecahedron)
        all_Dodecahedron_edges.append(Dodecahedron_edges)

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update()
    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()

